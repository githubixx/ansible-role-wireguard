Changelog
---------

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
