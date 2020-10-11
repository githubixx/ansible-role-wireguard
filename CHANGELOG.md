<!--
Copyright (C) 2018-2020 Robert Wimmer
SPDX-License-Identifier: GPL-3.0-or-later
-->

Changelog
---------

**7.6.0**
- Add `wireguard_private_key` variable (contribution by @j8r)
- Fix check mode for Debian (contribution by @j8r)

**7.5.0**

- `wireguard` package is now available for Ubuntu 18.04 in universe repository. Before that `ppa:wireguard/wireguard` was used but that one isn't available anymore. The install procedure for Ubuntu 18.04 and 20.04 is now the same as both can use `wireguard` metapackage now. The role takes care to remove `wireguard-dkms` package in favour of `wireguard` metapackage but it leaves the configuration file for `ppa:wireguard/wireguard` repository untouched. So it's up to you to remove that PPA. Either use `apt-add-repository --remove ppa:wireguard/wireguard` or remove the file manually at `/etc/apt/sources.list.d/` directory (you man need to run `apt-get update` afterwards).

**7.4.0**

- Added initial molecule infrastructure
- Remove useless block for single task in `setup-debian-vanilla.yml` (contribution by @rubendibattista)

**7.3.1**

- Debian only: Ensure the headers for the currently running kernel are installed instead of the latest one which might not be running yet. This allows DKMS to build the module for the current kernel version and avoids the need for an reboot to load the module. (contribution by @ldelelis and @ypid)

**7.3.0**

- Fix spelling and typos in docs. (contribution by @ypid)
- Drop Debian Stretch from the list of tested distros. Actual support was dropped/broken in 6.0.4 without updating the docs. (contribution by @ypid)
- Remove obsolete `.reload-module-on-update` file. It does not serve any function anymore after support for module reloading has been removed from the postinst script in 0.0.20200215-2 on 2020-02-24. A module update is properly signaled via /run/reboot-required so that the admin can (automatically) schedule a reboot when convenient. This will also be more in line with future Debian releases because starting with Debian bullseye, the kernel ships the module. (contribution by @ypid)

- Add `ansible_managed` header to WireGuard configuration file (`wg0.conf` by default). This will most probably change the WireGuard configuration file but only the formatting. But since the Ansible registers this file as changed Ansible will sync/restart WireGuard service. For newer WireGuard versions (since Nov. 2019) this isn't a problem normally as `wg syncconf` command is used (also see `handlers/main.yml`). (contribution by @ypid)
- Behind the scenes coding style improvements and cleanup without user impact. (contribution by @ypid)

**7.2.0**

- Basic MacOS X support (contribution by @rubendibattista)
- Introduce variables `wireguard_conf_owner`, `wireguard_conf_group` and `wireguard_conf_mode` (contribution by @rubendibattista)
- Fixed a typo bug in `handlers/main.yml` (contribution by @gabriel-v). But it looks like this had no impact on the "sync/restart" functionality.
- Proper formatting of WireGuard configuration file (`wg0.conf` by default). This will most probably change the WireGuard configuration file but only the formatting. But since the Ansible registers this file as changed Ansible will sync/restart WireGuard service. For newer WireGuard versions (since Nov. 2019) this isn't a problem normally as `wg syncconf` command is used (also see `handlers/main.yml`).
- Introduce `wireguard_dc` variable. This is an alpha feature and subject to change and may be even removed in future releases again. Therefore no documentation for this variable yet.

**7.1.0**

- Add support for unmanaged peers with `wireguard_unmanaged_peers` (contribution by @joneskoo)

**7.0.0**

- Switched to install from ELRepo KMOD package for CentOS (see https://www.wireguard.com/install/). This change may break installation for systems with custom kernels. The role previously supported custom kernel implicitly because it was using DKMS package (contribution by @elcomtik)

  Role removes DKMS WireGuard package, however it doesn't remove jdoss-wireguard-epel-7 repository. If you don't need this repository, do cleanup by:
    * remove `/etc/yum.repos.d/wireguard.repo`


**6.3.1**

- Support Openstack Debian images (contribution by @pallinger)

**6.3.0**

- Support Raspbian (contribution by @penguineer)

**6.2.0**

- Support Ubuntu 20.04 (Focal Fossa)
- Introduce `wireguard_ubuntu_update_cache` and `wireguard_ubuntu_cache_valid_time` variables to specify individual Ubuntu package cache settings. Default values are the same as before.
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

- pass package list directly to some modules by using the new and preferred syntax instead `loop` or `with_items` (contribution by ahanselka)

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
