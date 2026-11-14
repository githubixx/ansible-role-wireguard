---
title: Быстрый старт
description: VPN-сервер на AmneziaWG, доступ к внутренней сети и готовые конфиги для телефона и ноутбука.
---

Пример: сервер `vpn1` с публичным адресом `vpn.example.com`, за ним
внутренняя сеть `192.168.10.0/24`. Нужен доступ к этой сети с телефона и
ноутбука, на которых нет SSH.

## 1. Зависимости на контроллере

На машине, где запускается `ansible-playbook`:

```bash
pip install netaddr                 # нужен фильтрам ansible.utils.ipaddr
ansible-galaxy collection install community.general ansible.utils
# необязательно, для QR-кодов:
brew install qrencode               # или apt install qrencode
```

## 2. Подключение роли

`requirements.yml`:

```yaml
roles:
  - name: wireguard
    src: https://github.com/linuxfight/ansible-role-wireguard.git
    scm: git
    version: master
```

```bash
ansible-galaxy role install -r requirements.yml
```

## 3. Инвентарь

`inventory/hosts.yml`:

```yaml
all:
  children:
    vpn:
      hosts:
        vpn1:
          ansible_host: 203.0.113.10
```

`inventory/group_vars/vpn.yml`. Переменные из этого файла общие для всех
узлов группы:

```yaml
wireguard_backend: amneziawg
wireguard_preshared_keys: true
```

`inventory/host_vars/vpn1.yml`:

```yaml
wireguard_address: "10.8.0.1/24"
wireguard_endpoint: "vpn.example.com"
wireguard_port: 51820
wireguard_ip_forward: true
wireguard_postup:
  - "iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE"
wireguard_postdown:
  - "iptables -t nat -D POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE"

wireguard_clients_defaults:
  allowed_ips: ["10.8.0.0/24", "192.168.10.0/24"]
  dns: "192.168.10.1"
  persistent_keepalive: 25

wireguard_clients:
  phone:
    address: "10.8.0.10/32"
  laptop:
    address: "10.8.0.11/32"
```

## 4. Плейбук

`site.yml`:

```yaml
- hosts: vpn
  become: true
  roles:
    - wireguard
```

```bash
ansible-playbook -i inventory site.yml
```

## 5. Результат

На контроллере, рядом с плейбуком:

```text
wireguard-artifacts/
├── clients/vpn1/
│   ├── phone.conf      ← импортировать в AmneziaVPN / AmneziaWG
│   └── laptop.conf
└── state/              ← секреты, не удалять и не коммитить в открытом виде
    ├── amneziawg-params.json
    ├── clients/vpn1/{phone,laptop}.{key,psk}
    └── psk/
```

Импортируйте `phone.conf` в приложение **AmneziaVPN** или **AmneziaWG**
(Android, iOS, Windows, macOS, Linux). С `wireguard_clients_qrcode: true`
рядом появится `phone.png` для сканирования камерой.

## 6. Что дальше

- Добавьте клиента в `wireguard_clients` и запустите плейбук снова. Старые
  ключи не меняются, создаётся только новый.
- Чтобы удалить клиента, поставьте ему `state: absent`. Роль уберёт пир с
  сервера и удалит его локальные файлы.
- Если обфускацию начали распознавать, смените параметры (см. [AmneziaWG](../amneziawg/)).
