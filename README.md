ansible-role-wireguard
======================

This Ansible role is used in my blog series [Kubernetes the not so hard way with Ansible](https://www.tauceti.blog/post/kubernetes-the-not-so-hard-way-with-ansible-at-scaleway-part-1/) but can be used standalone of course.

Versions
--------

I tag every release and try to stay with [semantic versioning](http://semver.org). If you want to use the role I recommend to checkout the latest tag. The master branch is basically development while the tags mark stable releases. But in general I try to keep master in good shape too.

Requirements
------------

By default port `51820` (protocol UDP) should be accessable from the outside. But you can adjust the port with by changing the variable `wireguard_port`.

Changelog
---------

**v1.0.0**

- initial implementation


Role Variables
--------------

This variables can be changed in `group_vars/`:

```
# The LOCAL directory where the Wireguard certificates are stored after they
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

# Directory to store Wireguard configuration on the remote hosts
wireguard_remote_directory: "/etc/wireguard"

# The port Wireguard will listen on.
wireguard_port: "51820"

# The interface name that wireguard should use.
wireguard_interface: "wg0"
```

The following variables are variables that needs to be set per host in `host_vars/`:

```
wireguard_ip: "10.3.0.101"
wireguard_endpoint: "host1.domain.tld"
```

`wireguard_ip` is required. It's the IP of the interface name defined with `wireguard_interface` variable (`wg0` by default). Every hosts needs a unique IP of course. If you don't set `wireguard_endpoint` the playbook will use the hostname defined in the `vpn` hosts group. If you set `wireguard_endpoint` to `""` (empty string) that peer won't have a endpoint. That means that this host can only access hosts that have a `wireguard_endpoint`. That's useful for clients that don't expose any services to the VPN and only want to access services on other hosts. The third possibility is to set `wireguard_endpoint` to some hostname. E.g. if you have different IP's for the private and public IP of that host and have different DNS entries for that case setting `wireguard_endpoint` becomes handy. Take for example the IP above: `wireguard_ip: "10.3.0.101"`. That's a private IP and I've created a DNS entry for that private IP like `host01.i.domain.tld` (`i` for internal that case). For the public IP I've created a DNS entry like `host01.p.domain.tld` (`p` for public). The `wireguard_endpoint` needs to be a interface that the other members in the `vpn` group can connect to.

Make it the intention more clear for what I use the playbook let's have a small example: I use Wireguard to setup a fully meshed VPN and run my Kubernetesi (K8s) cluster on top of it at Scaleway or Hetzner Cloud. So the important components like the K8s controller and worker nodes (which includes the pods) only communicate via encrypted Wireguard VPN.


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
