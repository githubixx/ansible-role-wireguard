Changelog
---------

**Unreleased**

- Allow to generate keys and configuration for non-ansible hosts like smartphones with `wireguard_unmanaged_hosts` (contribution by @juju4)

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
