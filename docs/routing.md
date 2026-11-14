---
title: Маршрутизация
description: Как через host/group vars задать, какие сети доступны устройствам и через какой узел они идут.
---

В WireGuard маршрутизацию задаёт `AllowedIPs` у пира. Это одновременно
таблица маршрутов (куда слать пакеты) и фильтр (от кого их принимать).
Роль собирает `AllowedIPs` из переменных.

## Хосты под управлением Ansible

`wireguard_allowed_ips` на хосте означает «какие адреса доступны через
этот хост». Все остальные хосты пропишут эти сети в пир этого хоста.

```yaml
# host_vars/vpn1.yml: за vpn1 находится сеть офиса
wireguard_address: "10.8.0.1/24"
wireguard_allowed_ips: "10.8.0.1/32, 192.168.10.0/24"
```

Если `wireguard_allowed_ips` не задан, остальные хосты маршрутизируют к
этому хосту только его адрес в туннеле (`/32` или `/128`).

Переменная работает на любом уровне инвентаря: `host_vars`,
`group_vars/<группа>` или `group_vars/all`.

### Хаб и споки

```yaml
# group_vars/spokes.yml
wireguard_as_spoke: true      # споки соединяются только с хабами
```

У хаба в `wireguard_allowed_ips` перечисляются все сети, которые должны
быть доступны спокам через хаб.

## Клиенты без SSH

У клиента два разных набора адресов:

| Поле | Где оказывается | Смысл |
|---|---|---|
| `allowed_ips` | в конфиге **клиента**, `[Peer]` сервера | что клиент отправляет в туннель |
| `networks` | в конфиге **сервера**, `[Peer]` клиента | сети за клиентом (например, за роутером) |

Общие маршруты задаются в `wireguard_clients_defaults`, исключения — у
конкретного клиента:

```yaml
wireguard_clients_defaults:
  allowed_ips: ["10.8.0.0/24", "192.168.10.0/24"]   # split tunnel

wireguard_clients:
  phone:
    address: "10.8.0.10/32"
  laptop:
    address: "10.8.0.11/32"
    allowed_ips: ["0.0.0.0/0", "::/0"]             # full tunnel
```

Если `allowed_ips` не задан ни у клиента, ни в defaults, клиент получает
сети из `wireguard_address`/`wireguard_addresses` сервера. Например, для
`10.8.0.1/24` это `10.8.0.0/24`.

## Чтобы сервер пропускал трафик дальше

Чтобы клиенты попадали в сеть за сервером, сервер должен пересылать
пакеты:

```yaml
wireguard_ip_forward: true    # /etc/sysctl.d/90-wireguard-ip-forward.conf
```

Кроме того, нужно одно из двух:

- маршрут обратно в `10.8.0.0/24` через VPN-сервер на роутере внутренней
  сети;
- NAT (masquerade) на сервере:

```yaml
wireguard_postup:
  - "iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE"
wireguard_postdown:
  - "iptables -t nat -D POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE"
```

Для full tunnel (`0.0.0.0/0`) NAT на сервере обязателен.
