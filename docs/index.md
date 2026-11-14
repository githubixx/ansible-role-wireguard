---
title: Обзор
description: Форк ansible-role-wireguard с поддержкой AmneziaWG, экспортом клиентских конфигов, PSK и маршрутизацией через переменные.
---

Это форк [githubixx/ansible-role-wireguard](https://github.com/githubixx/ansible-role-wireguard).
Он ставит и настраивает **WireGuard** или **AmneziaWG**. AmneziaWG — форк
WireGuard с обфускацией трафика: он проходит через DPI, который полностью
блокирует обычный WireGuard.

## Что добавлено в форке

| Возможность | Переменные | Страница |
|---|---|---|
| Бэкенд AmneziaWG (Debian/Ubuntu) | `wireguard_backend: amneziawg` | [AmneziaWG](./amneziawg/) |
| Конфиги для устройств без SSH сохраняются локально | `wireguard_clients` | [Клиенты без SSH](./clients/) |
| Повторный запуск не перегенерирует ключи | — | [Идемпотентность](./idempotency/) |
| Pre-shared keys (пост-квантовая защита) | `wireguard_preshared_keys` | [Pre-shared keys](./preshared-keys/) |
| Маршруты через host/group vars | `wireguard_allowed_ips`, `allowed_ips` клиента | [Маршрутизация](./routing/) |
| IP forwarding на сервере | `wireguard_ip_forward` | [Маршрутизация](./routing/) |

Всё новое выключено по умолчанию. Без новых переменных роль работает как
upstream.

## С чего начать

- [Быстрый старт](./getting-started/): VPN-сервер на AmneziaWG и конфиг для телефона.
- [Справочник переменных](./variables/)

## Структура документации

Документация лежит в `docs/` в виде Markdown-файлов с frontmatter
(`title`, `description`). Их можно подключить в Astro/Starlight: скопируйте
или подключите каталог `docs/` в `src/content/docs/`.
