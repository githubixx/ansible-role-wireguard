---
title: AmneziaWG
description: Как роль ставит AmneziaWG, откуда берутся параметры обфускации и как их менять.
---

## Включение

```yaml
wireguard_backend: amneziawg
```

Задайте эту переменную в `group_vars` для всей сети. Узлы на WireGuard и
на AmneziaWG друг с другом не соединятся.

## Что меняется по сравнению с WireGuard

| | WireGuard | AmneziaWG |
|---|---|---|
| Пакеты | `wireguard` | `amneziawg-tools`, `amneziawg` (DKMS) из `ppa:amnezia/ppa` |
| Утилиты | `wg`, `wg-quick` | `awg`, `awg-quick` |
| Интерфейс по умолчанию | `wg0` | `awg0` |
| Каталог конфигов | `/etc/wireguard` | `/etc/amnezia/amneziawg` |
| systemd unit | `wg-quick@wg0` | `awg-quick@awg0` |
| Модуль ядра | `wireguard` | `amneziawg` |

## Поддерживаемые системы

Debian 11/12/13 и Ubuntu 22.04/24.04/26.04. Роль подключает PPA Amnezia,
ключ подписи `75C9DD72C799870E310542E24166F2C257290828` сохраняется в
`/etc/apt/keyrings/amnezia.asc`.

- Ubuntu берёт пакеты из сьюта своего релиза.
- Debian использует совместимый релиз Ubuntu: bullseye → focal,
  bookworm → jammy, trixie → noble. Сьют можно переопределить через
  `wireguard_amneziawg_ppa_suite`.

Модуль ядра собирается через DKMS, поэтому роль ставит
`linux-headers-$(uname -r)`. Если заголовки ставятся иначе, задайте
`wireguard_amneziawg_install_kernel_headers: false`.

Если хост не может загружать модули (непривилегированный LXC), задайте
`wireguard_install_kernel_module: false`. Тогда роль поставит только
`amneziawg-tools`, а модуль должен быть загружен на хосте-гипервизоре.

Netplan (`wireguard_ubuntu_use_netplan`) и macOS с AmneziaWG не
поддерживаются.

## Параметры обфускации

| Параметр | Смысл | Должен совпадать у обеих сторон |
|---|---|---|
| `jc` | количество мусорных пакетов перед handshake | нет |
| `jmin`, `jmax` | диапазон размера мусорных пакетов | нет |
| `s1`, `s2` | мусорные байты в init/response handshake | **да** |
| `h1`–`h4` | заголовки типов сообщений вместо 1–4 | **да** |
| `s3`, `s4`, `i1`–`i5` | параметры AmneziaWG 2.0 | `s3`, `s4` — да |

Если `wireguard_amneziawg_params` не задан, роль один раз генерирует
случайные значения AmneziaWG 1.x и сохраняет их в
`wireguard-artifacts/state/amneziawg-params.json`. Их используют все хосты
и клиенты. При следующих запусках значения читаются из этого файла.

Чтобы переопределить часть значений, задайте их в
`wireguard_amneziawg_params`. Они накладываются поверх сгенерированных:

```yaml
# group_vars/vpn.yml
wireguard_amneziawg_params:
  jc: 5
  jmin: 50
  jmax: 1000
```

У клиента свои `jc`/`jmin`/`jmax` задаются так:

```yaml
wireguard_clients:
  phone:
    address: "10.8.0.10/32"
    amneziawg_params:
      jc: 3
```

Параметры 2.0 (`s3`, `s4`, `i1`–`i5`) выводятся в конфиг, только если они
заданы. Их должна поддерживать версия `amneziawg-tools` на сервере и все
клиентские приложения.

## Смена параметров

1. Удалите `wireguard-artifacts/state/amneziawg-params.json` или поменяйте
   значения в `wireguard_amneziawg_params`.
2. Запустите плейбук. Конфиги серверов и клиентов перегенерируются.
3. Заново импортируйте клиентские конфиги на устройства. Ключи при этом не
   меняются.
