ansible-role-wireguard
======================

This Ansible role is used in my blog series [Kubernetes the not so hard way with Ansible](https://www.tauceti.blog/post/kubernetes-the-not-so-hard-way-with-ansible-wireguard/) but can be used standalone of course. I use WireGuard and this Ansible role to setup a fully meshed VPN between all nodes of my little Kubernetes cluster. This VPN also includes two clients so that I can communicate securely with the Kubernetes API server. Also my Postfix mailserver running as K8s DaemonSet forwards mails to my internal Postfix through WireGuard VPN.

I used [PeerVPN](https://peervpn.net/) before but that wasn't updated for a while. As I moved my cloud hosts from Scaleway to Hetzner cloud it was a good time to switch the VPN solution ;-) In general PeerVPN still works perfectly fine esp. if you need a easy to setup fully meshed network (where every node is able to talk to all other nodes and even if node `A` should be able to talk to Node `C` via node `B` ;-) ). But PeerVPN needs also lot of CPU resources and throughput could be better. That's solved with [WireGuard](https://www.wireguard.io/).

In general WireGuard is a network tunnel (VPN) for IPv4 and IPv6 that uses UDP. If you need more information about [WireGuard](https://www.wireguard.io/) you can find a good introduction here: [Installing WireGuard, the Modern VPN](https://research.kudelskisecurity.com/2017/06/07/installing-wireguard-the-modern-vpn/).

This role is tested with Ubuntu 18.04 (Bionic Beaver), Ubuntu 20.04 (Focal Fossa) and Archlinux. Ubuntu 16.04 (Xenial Xerus), Debian 10 (Buster), Fedora 31 (or later), CentOS 7 and partially MacOS (see below) might also work or other distributions but haven't tested it (code for this operating systems was submitted by other contributors). If someone tested it let me please know if it works or send a pull request to make it work ;-)

### Running the VPN on MacOS

While this playbook configures, enables and starts a `systemd` service on Linux in a such a way that no additional action is needed, on MacOS it installs the required packages and it just generates the correct `wg0.conf` file that is then placed in the specified `wireguard_remote_directory` (`/opt/local/etc/wireguard` by default). In order to run the VPN, then, you need to: 

```
sudo wg-quick up wg0
```

and to deactivate it

```
sudo wg-quick down wg0
```

or you can install the [official app](https://apps.apple.com/it/app/wireguard/id1451685025?l=en&mt=12) and import the `wg0.conf` file. 


Versions
--------

I tag every release and try to stay with [semantic versioning](http://semver.org). If you want to use the role I recommend to checkout the latest tag. The master branch is basically development while the tags mark stable releases. But in general I try to keep master in good shape too.

Requirements
------------

By default port `51820` (protocol UDP) should be accessible from the outside. But you can adjust the port by changing the variable `wireguard_port`. Also IP forwarding needs to be enabled e.g. via `echo 1 > /proc/sys/net/ipv4/ip_forward `. I decided not to implement this task in this Ansible role. IMHO that should be handled elsewhere. You can use my [ansible-role-harden-linux](https://github.com/githubixx/ansible-role-harden-linux) e.g. Besides changing sysctl entries (which you need to enable IP forwarding) it also manages firewall settings among other things. Nevertheless the `PreUp`, `PreDown`, `PostUp` and `PostDown` hooks may be a good place to do some network related stuff before a WireGuard interface comes up or goes down.

Changelog
---------

see [CHANGELOG.md](https://github.com/githubixx/ansible-role-wireguard/blob/master/CHANGELOG.md)

Role Variables
--------------

These variables can be changed in `group_vars/` e.g.:

```yaml
# Directory to store WireGuard configuration on the remote hosts
wireguard_remote_directory: "/etc/wireguard"              # On Linux
# wireguard_remote_directory: "/opt/local/etc/wireguard"  # On MacOS

# The default port WireGuard will listen if not specified otherwise.
wireguard_port: "51820"

# The default interface name that WireGuard should use if not specified otherwise.
wireguard_interface: "wg0"

# The default owner of the wg.conf file
wireguard_conf_owner: root

# The default group of the wg.conf file
wireguard_conf_group: "{{ 'root' if not ansible_os_family == 'Darwin' else 'wheel' }}"

# The default mode of the wg.conf file
wireguard_conf_mode: 0600
```

The following variable is mandatory and needs to be configured for every host in `host_vars/` e.g.:

```yaml
wireguard_address: "10.8.0.101/24"
```

Of course all IP's should be in the same subnet like `/24` we see in the example above. If `wireguard_allowed_ips` is not set then the default value is the value from `wireguard_address` without the CIDR but instead with `/32` which is basically a host route (have a look `templates/wg.conf.j2`). Let's see this example and let's assume you don't set `wireguard_allowed_ips` explicitly:

```ini
[Interface]
Address = 10.8.0.2/24
PrivateKey = ....
ListenPort = 51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.101/32
Endpoint = controller01.p.domain.tld:51820
```

This is part of the WireGuard config from my workstation. It has the VPN IP `10.8.0.2` and we've a `/24` subnet in which all my WireGuard hosts are located. Also you can see we've a peer here that has the endpoint `controller01.p.domain.tld:51820`. When `wireguard_allowed_ips` is not explicitly set the Ansible template will add an `AllowedIPs` entry with the IP of that host plus `/32`. In WireGuard this basically specifies the routing. The config above says: On my workstation with the IP `10.8.0.2` I want send all traffic to `10.8.0.101/32` to the endpoint `controller01.p.domain.tld:51820`. Now let's assume we set `wireguard_allowed_ips: "0.0.0.0/0"`. Then the resulting config looks like this.

```ini
[Interface]
Address = 10.8.0.2/24
PrivateKey = ....
ListenPort = 51820

[Peer]
PrivateKey = ....
AllowedIPs = 0.0.0.0/0
Endpoint = controller01.p.domain.tld:51820
```

Now this is basically the same as above BUT now the config says: I want to route EVERY traffic originating from my workstation to the endpoint `controller01.p.domain.tld:51820`. If that endpoint can handle the traffic is of course another thing and it's up to you how you configure the endpoint routing ;-)

You can specify further optional settings (they don't have a default and won't be set if not specified besides `wireguard_allowed_ips` as already mentioned) also per host in `host_vars/` (or in your Ansible hosts file if you like). The values for the following variables are just examples and no defaults (for more information and examples see [wg-quick.8](https://git.zx2c4.com/WireGuard/about/src/tools/man/wg-quick.8)):

```yaml
wireguard_allowed_ips: ""
wireguard_endpoint: "host1.domain.tld"
wireguard_persistent_keepalive: "30"
wireguard_dns: "1.1.1.1"
wireguard_fwmark: "1234"
wireguard_mtu: "1492"
wireguard_table: "5000"
wireguard_preup:
  - ...
wireguard_predown:
  - ...
wireguard_postup:
  - ...
wireguard_postdown:
  - ...
wireguard_save_config: "true"
wireguard_unmanaged_peers:
  client.example.com:
    public_key: 5zsSBeZZ8P9pQaaJvY9RbELQulcwC5VBXaZ93egzOlI=
    # preshared_key: ... e.g. from ansible-vault?
    allowed_ips: 10.0.0.3/32
    endpoint: client.example.com:51820
    persistent_keepalive: 0
```

`wireguard_(preup|predown|postup|postdown)` are specified as lists. Here are two examples:

```yaml
wireguard_postup:
  - iptables -t nat -A POSTROUTING -o ens12 -j MASQUERADE
  - iptables -A FORWARD -i %i -j ACCEPT
  - iptables -A FORWARD -o %i -j ACCEPT
```

```yaml
wireguard_preup:
  - echo 1 > /proc/sys/net/ipv4/ip_forward
  - ufw allow 51820/udp
```

The commands are executed in order as described in [wg-quick.8](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8).

`wireguard_address` is required as already mentioned. It's the IP of the interface name defined with `wireguard_interface` variable (`wg0` by default). Every host needs a unique VPN IP of course. If you don't set `wireguard_endpoint` the playbook will use the hostname defined in the `vpn` hosts group (the Ansible inventory hostname). If you set `wireguard_endpoint` to `""` (empty string) that peer won't have a endpoint. That means that this host can only access hosts that have a `wireguard_endpoint`. That's useful for clients that don't expose any services to the VPN and only want to access services on other hosts. So if you only define one host with `wireguard_endpoint` set and all other hosts have `wireguard_endpoint` set to `""` (empty string) that basically means you've only clients besides one which in that case is the WireGuard server. The third possibility is to set `wireguard_endpoint` to some hostname. E.g. if you have different hostnames for the private and public DNS of that host and need different DNS entries for that case setting `wireguard_endpoint` becomes handy. Take for example the IP above: `wireguard_address: "10.8.0.101"`. That's a private IP and I've created a DNS entry for that private IP like `host01.i.domain.tld` (`i` for internal in that case). For the public IP I've created a DNS entry like `host01.p.domain.tld` (`p` for public). The `wireguard_endpoint` needs to be a interface that the other members in the `vpn` group can connect to. So in that case I would set `wireguard_endpoint` to `host01.p.domain.tld` because WireGuard normally needs to be able to connect to the public IP of the other host(s).

Here is a litte example for what I use the playbook: I use WireGuard to setup a fully meshed VPN (every host can directly connect to every other host) and run my Kubernetes (K8s) cluster at Hetzner Cloud (but you should be able to use any hoster you want). So the important components like the K8s controller and worker nodes (which includes the pods) only communicate via encrypted WireGuard VPN. Also (as already mentioned) I've two clients. Both have `kubectl` installed and are able to talk to the internal Kubernetes API server by using WireGuard VPN. One of the two clients also exposes a WireGuard endpoint because the Postfix mailserver in the cloud and my internal Postfix needs to be able to talk to each other. I guess that's maybe a not so common use case for WireGuard :D But it shows what's possible. So let me explain the setup which might help you to use this Ansible role.

First, here is a part of my Ansible `hosts` file:

```
[vpn]
controller0[1:3].i.domain.tld
worker0[1:2].i.domain.tld
server.at.home.i.domain.tld
workstation.i.domain.tld

[k8s_controller]
controller0[1:3].i.domain.tld

[k8s_worker]
worker0[1:2].i.domain.tld
```

As you can see I've three gropus here: `vpn` (all hosts on that will get WireGuard installed), `k8s_controller` (the Kubernetes controller nodes) and `k8s_worker` (the Kubernetes worker nodes). The `i` in the domainname is for `internal`. All the `i.domain.tld` DNS entries have a `A` record that points to the WireGuard IP that we define shortly for every host e.g.: ` controller01.i.domain.tld. IN A 10.8.0.101`. The reason for that is that all Kubernetes components only binds and listen on the WireGuard interface in my setup. And since I need this internal IPs for all my Kubernetes components I specify the internal DNS entries in my Ansible `hosts` file. That way I can use the Ansible inventory hostnames and variables very easy in the playbooks and templates.

For the Kubernetes controller nodes I've defined the following host variables:

Ansible host file: `host_vars/controller01.i.domain.tld`
```yaml
---
wireguard_address: "10.8.0.101/24"
wireguard_endpoint: "controller01.p.domain.tld"
ansible_host: "controller01.p.domain.tld"
ansible_python_interpreter: /usr/bin/python3
```

Ansible host file: `host_vars/controller02.i.domain.tld`:
```yaml
---
wireguard_address: "10.8.0.102/24"
wireguard_endpoint: "controller02.p.domain.tld"
ansible_host: "controller02.p.domain.tld"
ansible_python_interpreter: /usr/bin/python3
```

Ansible host file: `host_vars/controller03.i.domain.tld`:
```yaml
---
wireguard_address: "10.8.0.103/24"
wireguard_endpoint: "controller03.p.domain.tld"
ansible_host: "controller03.p.domain.tld"
ansible_python_interpreter: /usr/bin/python3
```

I've specified `ansible_python_interpreter` here for every node as the controller nodes use Ubuntu 18.04 which has Python 3 installed by default. `ansible_host` is set to the public DNS of that host. Ansible will use this hostname to connect to the host via SSH. I use the same value also for `wireguard_endpoint` because of the same reason. The WireGuard peers needs to connect to the other peers via a public IP (well at least via a IP that the WireGuard hosts can connect to - that could be of course also a internal IP if it works for you). The `wireguard_address` needs to be unique of course for every host.

For the Kubernetes worker I've defined the following variables:

Ansible host file: `host_vars/worker01.i.domain.tld`
```yaml
---
wireguard_address: "10.8.0.111/24"
wireguard_endpoint: "worker01.p.domain.tld"
wireguard_persistent_keepalive: "30"
ansible_host: "worker01.p.domain.tld"
ansible_python_interpreter: /usr/bin/python3
```

Ansible host file: `host_vars/worker02.i.domain.tld`:
```yaml
---
wireguard_address: "10.8.0.112/24"
wireguard_endpoint: "worker02.p.domain.tld"
wireguard_persistent_keepalive: "30"
ansible_host: "worker02.p.domain.tld"
ansible_python_interpreter: /usr/bin/python3
```

As you can see the variables are basically the same as the controller nodes have with one exception: `wireguard_persistent_keepalive: "30"`. My worker nodes (at Hetzner Cloud) and my internal server (my server at home) are connected because I've running Postfix at my cloud nodes and the external Postfix server forwards the received mails to my internal server (and vice versa). I needed the keepalive setting because from time to time the cloud instances and the internal server lost connection and this setting solved the problem. The reason for this is of course because my internal server is behind NAT and the firewall/router must keep the NAT/firewall mapping valid (NAT and Firewall Traversal Persistence).

For my internal server at home (connected via DSL router to the internet) we've this configuration:

```yaml
---
wireguard_address: "10.8.0.1/24"
wireguard_endpoint: "server.at.home.p.domain.tld"
wireguard_persistent_keepalive: "30"
ansible_host: 192.168.2.254
ansible_port: 22
```

By default the SSH daemon is listening on a different port than 22 on all of my public nodes but internally I use `22` and that's the reason to set `ansible_port: 22` here. Also `ansible_host` is of course a internal IP for that host. The `wireguard_endpoint` value is a dynamic DNS entry. Since my IP at home isn't static I need to run a script every minute at my home server that checks if the IP has changed and if so adjusts my DNS record. I use OVH's DynHost feature to accomplish this but you can use and DynDNS provider you want of course. Also I forward incoming traffic on port `51820/UDP` to my internal server to allow incoming WireGuard traffic. The `wireguard_address` needs to be of course part of our WireGuard subnet.

And finally for my workstation (on which I run all `ansible-playbook` commands):

```yaml
wireguard_address: "10.8.0.2/24"
wireguard_endpoint: ""
ansible_connection: local
ansible_become: false
```

As you can see `wireguard_endpoint: ""` is a empty string here. That means the Ansible role won't set an endpoint for my workstation. Since there is no need for the other hosts to connect to my workstation it doesn't makes sense to have a endpoint defined. So in this case I can access all hosts defined in the Ansible group `vpn` from my workstation but not the other way round. So the resulting WireGuard config for my workstation looks like this:

```ini
[Interface]
Address = 10.8.0.2/24
PrivateKey = ....
ListenPort = 51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.101/32
Endpoint = controller01.p.domain.tld:51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.102/32
Endpoint = controller02.p.domain.tld:51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.103/32
Endpoint = controller03.p.domain.tld:51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.111/32
PersistentKeepalive = 30
Endpoint = worker01.p.domain.tld:51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.112/32
PersistentKeepalive = 30
Endpoint = worker02.p.domain.tld:51820

[Peer]
PrivateKey = ....
AllowedIPs = 10.8.0.1/32
PersistentKeepalive = 30
Endpoint = server.at.home.p.domain.tld:51820
```

The other WireGuard config files (`wg0.conf` by default) looks similar but of course `[Interface]` includes the config of that specific host and the `[Peer]` entries lists the config of the other hosts.

Example Playbook
----------------

```yaml
- hosts: vpn
  roles:
    - wireguard
```

Example Inventory using two different WireGuard interfaces on host "multi"
--------------------------------------------------------------------------

This is a complex example using yaml inventory format:

```yaml
vpn1:
  hosts:
    multi:
      wireguard_address: 10.9.0.1/32
      wireguard_allowed_ips: "10.9.0.1/32, 192.168.2.0/24"
      wireguard_endpoint: multi.exemple.com
    nated:
      wireguard_address: 10.9.0.2/32
      wireguard_allowed_ips: "10.9.0.2/32, 192.168.3.0/24"
      wireguard_persistent_keepalive: 15
      wireguard_endpoint: nated.exemple.com
      wireguard_postup:
        - iptables -t nat -A POSTROUTING -o ens12 -j MASQUERADE
        - iptables -A FORWARD -i %i -j ACCEPT
        - iptables -A FORWARD -o %i -j ACCEPT
      wireguard_postdown:
        - iptables -t nat -D POSTROUTING -o ens12 -j MASQUERADE
        - iptables -D FORWARD -i %i -j ACCEPT
        - iptables -D FORWARD -o %i -j ACCEPT

vpn2:
  hosts:
    # Use a different name, and define ansible_host, to avoid mixing of vars without
    # needing to prefix vars with interface name.
    multi-wg1:
      ansible_host: multi
      wireguard_interface: wg1
      # when using several interface on one host, we must use different ports
      wireguard_port: 51821
      wireguard_address: 10.9.1.1/32
      wireguard_endpoint: multi.exemple.com
    another:
      wireguard_address: 10.9.1.2/32
      wireguard_endpoint: another.exemple.com
```

Playbooks
---------

```yaml
- hosts: vpn1
  roles:
    - wireguard
```

```yaml
- hosts: vpn2
  roles:
    - wireguard
```

License
-------

GNU GENERAL PUBLIC LICENSE Version 3

Author Information
------------------

[http://www.tauceti.blog](http://www.tauceti.blog)
