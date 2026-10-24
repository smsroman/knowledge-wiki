# База знаний

Нейтральная открытая вики на [Zensical](https://zensical.org/).

**Сайт:** https://wiki.00340034.xyz/

## Участие

На любой статье нажмите карандаш: он открывает соответствующий Markdown-файл на GitHub. Предложите изменение через Pull Request. Проверка собирает сайт и проверяет внутренние ссылки и адреса редактирования. После Merge в `main` GitHub Actions публикует новую версию на GitHub Pages.

Инструкция: [docs/contributing.md](docs/contributing.md).

## Локальная работа

Требуется Python 3.12.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/zensical serve
```

Сборка и проверка:

```sh
.venv/bin/zensical build --clean
.venv/bin/python scripts/check_site.py
```

## Структура

- `docs/` — статьи и изображения.
- `zensical.toml` — название, оформление, навигация и ссылки на GitHub.
- `.github/workflows/docs.yml` — проверка Pull Request и публикация основной ветки.
- `docs/CNAME` — адрес сайта. При смене домена обновите также `site_url` и настройку Pages.

## Публикация и восстановление

В Settings → Pages выберите источник **GitHub Actions** и custom domain `wiki.00340034.xyz`. DNS: CNAME `wiki` → `smsroman.github.io`, без Cloudflare proxy.

Каждый Pull Request проверяется без публикации и без секретов. Принятый коммит публикуется автоматически; ход сборки виден во вкладке Actions. Чтобы вернуть предыдущий текст, создайте revert-коммит и дождитесь успешной публикации. Файлы в репозитории и их история — источник для восстановления сайта.

Отдельная база данных и постоянный сервер приложения не требуются.
