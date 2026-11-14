#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Controller-side secret store for the WireGuard/AmneziaWG role.

Every sub-command creates a file only if it does not exist yet, so running
the role again never rotates keys. Prints "created" or "exists" per path so
that Ansible can report "changed" correctly.

Usage:
  wg_keystore.py key PATH...         # X25519 private keys (base64, clamped)
  wg_keystore.py psk PATH...         # 256 bit pre-shared keys (base64)
  wg_keystore.py awg-params PATH...  # random AmneziaWG obfuscation params (JSON)
"""

import base64
import json
import os
import secrets
import sys


def _write_new(path, content):
    os.makedirs(os.path.dirname(os.path.abspath(path)), mode=0o700, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w") as fh:
        fh.write(content)
    return True


def private_key():
    raw = bytearray(secrets.token_bytes(32))
    # Same clamping as "wg genkey"
    raw[0] &= 248
    raw[31] = (raw[31] & 127) | 64
    return base64.b64encode(bytes(raw)).decode() + "\n"


def preshared_key():
    return base64.b64encode(secrets.token_bytes(32)).decode() + "\n"


def awg_params():
    # Constraints from the AmneziaWG documentation (protocol 1.x, which is
    # understood by every AmneziaWG implementation):
    #   1 <= Jc <= 128, Jmin < Jmax <= 1280
    #   S1 <= 1132, S2 <= 1188, S1 + 56 != S2
    #   H1..H4 unique, outside 1..4 (the values used by plain WireGuard)
    rnd = secrets.SystemRandom()
    jmin = rnd.randint(40, 80)
    s1 = rnd.randint(15, 150)
    s2 = rnd.randint(15, 150)
    while s1 + 56 == s2:
        s2 = rnd.randint(15, 150)
    headers = set()
    while len(headers) < 4:
        headers.add(rnd.randint(5, 2147483647))
    h1, h2, h3, h4 = sorted(headers)
    params = {
        "jc": rnd.randint(4, 10),
        "jmin": jmin,
        "jmax": rnd.randint(jmin + 50, 1000),
        "s1": s1,
        "s2": s2,
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "h4": h4,
    }
    return json.dumps(params, indent=2) + "\n"


GENERATORS = {
    "key": private_key,
    "psk": preshared_key,
    "awg-params": awg_params,
}


def main(argv):
    if len(argv) < 3 or argv[1] not in GENERATORS:
        sys.stderr.write(__doc__)
        return 2
    for path in argv[2:]:
        created = _write_new(path, GENERATORS[argv[1]]())
        print("created" if created else "exists")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
