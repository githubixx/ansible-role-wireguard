Changelog
---------

**6.2.0**

- Support Ubuntu 20.04 (Focal Fossa)
- Introduce `wireguard_ubuntu_update_cache` and `wireguard_ubuntu_cache_valid_time` variables to specifiy individual Ubuntu package cache settings. Default values are the same as before.
- As kernel >= 5.6 (and kernel 5.4 in Ubuntu 20.04) now have `wireguard` module included `wireguard-dkms` package is no longer needed in that case. That's why WireGuard package installation is now part of the includes for the specific OS to make it easier to handle various cases.

**6.1.0**

- Archlinux: Linux kernel >= 5.6 contains `wireguard` module now. No need to install `wireguard-dkms` anymore in this case. Installations with LTS kernel installs `wireguard-lts` package now instead of `wireguard-dkms`. Installations with kernel <= 5.6 will still install `wireguard-dkms` package.

**6.0.4**

- Use the buster-backports repository on Debian Buster (or older), use package standard repositories on sid/bullseye.
  standard repositories on sid/bullseye.

  The role no longer adds the unstable _repo_ nor the _apt preference_ for that repo. There is no need to clean the preference and unstable repository, since packages from your release have a higher priority.

  If you remove the apt preference (`/etc/apt/preferences.d/limit-unstable`) updates from `unstable` are accepted by apt. This likely is not what you want and may lead to an unstable state.

  If you want to clean up:
    * remove `/etc/apt/preferences.d/limit-unstable` and
    * remove `deb http://deb.debian.org/debian/ unstable main` from `/etc/apt/sources.list.d/deb_debian_org_debian.list`.

  The backports repository has a lower priority and does not need an apt preference.

**6.0.3**

- If `wg syncconf` command is not available do stop/start service instead of restart (contribution by @cristichiru)

**6.0.2**

- Debian: install `gnupg` package instead of `gpg`. (contribution by @zinefer)

**6.0.1**

- add shell options to syncconf handler to fail fast in case of error

**6.0.0**

- Newer versions of WireGuard (around November 2019) introduced `wg syncconf` subcommand. This has the advantage that changes to the WireGuard configuration can be applied without disturbing existing connections. With this change this role tries to use `wg syncconf` subcommand when available. This even works if you have hosts with older and newer WireGuard versions.

**5.0.0**

- `wireguard_(preup|postdown|preup|predown)` settings are now a list. If more `iptables` commands needs to be specified e.g. then this changes makes it more readable. The commands are executed in order as described in [wg-quick.8](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8). Also see README for more examples. (contribution by @Madic-)

**4.2.0**

- Add support for Fedora (contribution by @ties)


**4.1.1**

- Install GPG to be able to import WireGuard key (Debian)

**4.1.0**

- Allow to specifiy additional Wireguard interface options: `fwmark`, `mtu`, `table`, `preup` and `predown` (for more information and examples see [wg-quick.8](https://git.zx2c4.com/WireGuard/about/src/tools/man/wg-quick.8))
- Add host comments in Wireguard config file

**4.0.0**

- While the changes introduced are backwards compatible in general if you stay with your current settings some variables are no longer needed. So this is partly a breaking change and therefore justifies a new major version.
- Support multiple Wireguard interfaces. See README for examples (contribution by fbourqui)
- Make role stateless: In the previous versions the private and public keys of the Wireguard hosts were stored locally in the directory defined with the `wireguard_cert_directory` variable. This is no longer the case. The variables `wireguard_cert_directory`, `wireguard_cert_owner` and `wireguard_cert_group` are no longer needed and were removed. If you used this role before this release it's safe to remove them from your settings. The directory that was defined with the `wireguard_cert_directory` variable will be kept. While not tested it may enable you to go back to an older version of this role and it should still work (contribution by fbourqui)
- Reminder: `wireguard_cert_directory` default was `~/wireguard/certs`. Public and Private keys where stored on the host running ansible playbook. As a security best practice private keys of all your WireGuard endpoints should not be kept locally.

**3.2.2**

- remove unneeded `with_inventory_hostnames` loops (thanks to pierreozoux for initial PR)

**3.2.1**

- remove unecessary files (contribution by pierreozoux)

**3.2.0**

- add support for RHEL/CentOS (contribution by ahanselka)

**3.1.0**

- pass package list directly to some modules by using the new and prefered syntax instead `loop` or `with_items` (contribution by ahanselka)

**3.0.1**

- fix address in README

**3.0.0**

- support for Debian added (contribution by ties)

**2.0.1**

- make Ansible linter happy

**2.0.0**

- use correct semantic versioning as described in https://semver.org. Needed for Ansible Galaxy importer as it now insists on using semantic versioning.
- moved changelog entries to separate file
- make Ansible linter happy
- no major changes but decided to start a new major release as versioning scheme changed quite heavily

**v1.0.2**

- update README

**v1.0.1**

- update README

**v1.0.0**

- initial implementation
