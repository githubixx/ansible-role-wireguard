ansible-role-wireguard
======================

This Ansible role is used in my blog series [Kubernetes the not so hard way with Ansible](https://www.tauceti.blog/post/kubernetes-the-not-so-hard-way-with-ansible-at-scaleway-part-1/) but can be used standalone of course. I use WireGuard and this Ansible role to setup a fully meshed VPN between all nodes of my little Kubernetes cluster. This VPN also includes two clients so that I can communicate securly with the Kubernetes API server. Also my Postfix mailserver running as K8s DaemonSet forwards mails to my internal Postfix through WireGuard VPN.

I used [PeerVPN](https://peervpn.net/) before but that wasn't updated for a while. As I moved my cloud hosts from Scaleway to Hetzner cloud it was a good time to switch the VPN solution ;-) In general PeerVPN still works perfectly fine esp. if you need a fully meshed network (where every node is able to talk to all other nodes and even if node `A` should be able to talk to Node `C` via node `B` ;-) ). But PeerVPN needs also lot of CPU resources and throuhput could be better. That's solved with [WireGuard](https://www.wireguard.io/).

In general WireGuard is a network tunnel (VPN) for IPv4 and IPv6 that uses UDP. If need more information about [WireGuard](https://www.wireguard.io/) you can find a good introduction here: [Installing WireGuard, the Modern VPN](https://research.kudelskisecurity.com/2017/06/07/installing-wireguard-the-modern-vpn/).

This role was tested with Ubuntu 18.04 (Bionic Beaver) and Archlinux. It might also work with Ubuntu 16.04 (Xenial Xerus) but haven't tested it. If someone tested it let me please know if it works ;-)

Versions
--------

I tag every release and try to stay with [semantic versioning](http://semver.org). If you want to use the role I recommend to checkout the latest tag. The master branch is basically development while the tags mark stable releases. But in general I try to keep master in good shape too.

Requirements
------------

By default port `51820` (protocol UDP) should be accessable from the outside. But you can adjust the port with by changing the variable `wireguard_port`. Also IP forwarding needs to be enabled e.g. via `echo 1 > /proc/sys/net/ipv4/ip_forward `. I decided not to implement this task in this Ansible role. IMHO that should be handled elsewhere. You can use my [ansible-role-harden-linux](https://github.com/githubixx/ansible-role-harden-linux) e.g. Besides changing sysctl entries (which you need to enable IP forwarding) it also manages firewall settings among other things.

Changelog
---------

**v1.0.0**

- initial implementation


Role Variables
--------------

This variables can be changed in `group_vars/`:

```
# The LOCAL directory where the WireGuard certificates are stored after they
# were generated. By default this will expand to user's LOCAL ${HOME}
# (the user that run's "ansible-playbook" command) plus
# "/wireguard/certs". That means if the user's ${HOME} directory is e.g.
# "/home/da_user" then "wireguard_cert_directory" will have a value of
# "/home/da_user/wireguard/certs". If you change this make sure that
# the parent directory is writable by the user that runs "ansible-playbook"
# command.
wireguard_cert_directory: "{{ '~/wireguard/certs' | expanduser }}"
wireguard_cert_owner: "root"
wireguard_cert_group: "root"

# Directory to store WireGuard configuration on the remote hosts
wireguard_remote_directory: "/etc/wireguard"

# The port WireGuard will listen on.
wireguard_port: "51820"

# The interface name that wireguard should use.
wireguard_interface: "wg0"
```

The following variable is mandatory and needs to be configured for every host in `host_vars/`:

```
wireguard_ip: "10.3.0.101"
```

Additionally you can specify further optional settings also per host in `host_vars/`:

```
wireguard_endpoint: "host1.domain.tld"
wireguard_persistent_keepalive: "30"
wireguard_dns: "1.1.1.1"
wireguard_postup: "..."
wireguard_postdown: "..."
wireguard_save_config: "true"
```

`wireguard_ip` is required as already mentioned. It's the IP of the interface name defined with `wireguard_interface` variable (`wg0` by default). Every hosts needs a unique VPN IP of course. If you don't set `wireguard_endpoint` the playbook will use the hostname defined in the `vpn` hosts group. If you set `wireguard_endpoint` to `""` (empty string) that peer won't have a endpoint. That means that this host can only access hosts that have a `wireguard_endpoint`. That's useful for clients that don't expose any services to the VPN and only want to access services on other hosts. The third possibility is to set `wireguard_endpoint` to some hostname. E.g. if you have different IP's for the private and public IP of that host and have different DNS entries for that case setting `wireguard_endpoint` becomes handy. Take for example the IP above: `wireguard_ip: "10.3.0.101"`. That's a private IP and I've created a DNS entry for that private IP like `host01.i.domain.tld` (`i` for internal that case). For the public IP I've created a DNS entry like `host01.p.domain.tld` (`p` for public). The `wireguard_endpoint` needs to be a interface that the other members in the `vpn` group can connect to. So in that case I would set `wireguard_endpoint` to `host01.p.domain.tld` because WireGuard normally needs to be able to connect to the public IP of the other host(s).

Make it the intention more clear for what I use the playbook let's have a small example: I use WireGuard to setup a fully meshed VPN and run my Kubernetes (K8s) cluster at Hetzner Cloud (but you should be able to use and hoster you want). So the important components like the K8s controller and worker nodes (which includes the pods) only communicate via encrypted WireGuard VPN. Also (as already) mentioned I've two clients. Both have `kubectl` installed and are able to talk to the internal Kubernetes API server by using WireGuard VPN. One of the two clients also exposes a WireGuard endpoint because the Postfix in the cloud and my internal Postfix needs to be able to talk to each other. I guess that's maybe a not so common use case for WireGuard :D But it shows what's possible. So let me explain the setup which might help you to use this Ansible role.




Example Playbook
----------------

```
- hosts: vpn
  roles:
    - wireguard
```

License
-------

GNU GENERAL PUBLIC LICENSE Version 3

Author Information
------------------

[http://www.tauceti.blog](http://www.tauceti.blog)
