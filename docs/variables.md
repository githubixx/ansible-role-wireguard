---
title: Справочник переменных
description: Все переменные роли — новые в форке и основные из upstream.
---

Значения по умолчанию лежат в `defaults/main.yml`.

## Новые в форке

| Переменная | По умолчанию | Описание |
|---|---|---|
| `wireguard_backend` | `wireguard` | `wireguard` или `amneziawg` |
| `wireguard_amneziawg_params` | генерируется | параметры обфускации (`jc`, `jmin`, `jmax`, `s1`–`s4`, `h1`–`h4`, `i1`–`i5`), см. [AmneziaWG](../amneziawg/) |
| `wireguard_amneziawg_ppa_suite` | авто | сьют `ppa:amnezia/ppa` |
| `wireguard_amneziawg_install_kernel_headers` | `true` | ставить `linux-headers-$(uname -r)` для DKMS |
| `wireguard_local_directory` | `{{ playbook_dir }}/wireguard-artifacts` | каталог на контроллере для конфигов и секретов |
| `wireguard_preshared_keys` | `false` | PSK для всех туннелей, см. [Pre-shared keys](../preshared-keys/) |
| `wireguard_clients` | `{}` | клиенты без SSH, см. [Клиенты без SSH](../clients/) |
| `wireguard_clients_defaults` | `{}` | значения по умолчанию для каждого клиента |
| `wireguard_clients_qrcode` | `false` | писать PNG с QR-кодом (нужен `qrencode` на контроллере) |
| `wireguard_ip_forward` | `false` | включить IPv4/IPv6 forwarding через sysctl |

## Адресация и пиры (upstream)

| Переменная | Описание |
|---|---|
| `wireguard_address` | адрес хоста в туннеле, например `10.8.0.1/24` |
| `wireguard_addresses` | список адресов (IPv4 + IPv6) вместо `wireguard_address` |
| `wireguard_endpoint` | публичный адрес хоста. Пустая строка `""` значит, что хост за NAT и входящих не принимает |
| `wireguard_port` | порт (`51820`) |
| `wireguard_allowed_ips` | сети, доступные через этот хост, см. [Маршрутизация](../routing/) |
| `wireguard_persistent_keepalive` | keepalive в секундах |
| `wireguard_as_spoke` | `true`: соединяться только с хабами |
| `wireguard_dc` | `name`, `endpoint`, `port`: другой endpoint для хостов из других ДЦ |
| `wireguard_unmanaged_peers` | пиры с известными ключами (без генерации конфигов) |

## Интерфейс (upstream)

| Переменная | По умолчанию | Описание |
|---|---|---|
| `wireguard_interface` | `wg0` / `awg0` | имя интерфейса |
| `wireguard_remote_directory` | `/etc/wireguard` / `/etc/amnezia/amneziawg` | каталог конфига на хосте |
| `wireguard_conf_filename` | `<interface>.conf` | имя файла конфига |
| `wireguard_private_key` | из существующего конфига или новый | приватный ключ (шифруйте через Vault) |
| `wireguard_dns`, `wireguard_mtu`, `wireguard_fwmark`, `wireguard_table` | — | поля `[Interface]` |
| `wireguard_preup`, `wireguard_postup`, `wireguard_predown`, `wireguard_postdown` | — | списки команд |
| `wireguard_save_config` | — | `SaveConfig` |

## Сервис и применение изменений (upstream)

| Переменная | По умолчанию | Описание |
|---|---|---|
| `wireguard_service_enabled` | `yes` | автозапуск `wg-quick@`/`awg-quick@` |
| `wireguard_service_state` | `started` | состояние сервиса |
| `wireguard_interface_restart` | `false` | `true`: применять изменения перезапуском интерфейса вместо `syncconf` |
| `wireguard_flush_handlers` | `false` | применять изменения в конце роли, а не в конце плея |
| `wireguard_install_kernel_module` | `true` | ставить и загружать модуль ядра |
| `wireguard_update_cache` | `true` | обновлять кэш пакетов |
| `wireguard_ubuntu_use_netplan` | `false` | конфиг через netplan (только WireGuard) |

## Теги

| Тег | Что выполняется |
|---|---|
| `wg-install` | установка пакетов и модуля |
| `wg-generate-keys` | генерация ключей и секретов |
| `wg-config` | генерация конфигов (включая клиентов) |
| `wg-service` | запуск и включение сервиса |

Пример: перегенерировать конфиги (серверные и клиентские) без установки пакетов:

```bash
ansible-playbook site.yml --tags wg-config
```
