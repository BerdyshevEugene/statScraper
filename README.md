
[![Ruff](https://github.com/BerdyshevEugene/statScraper/actions/workflows/ruff.yml/badge.svg?cache=buster)](https://github.com/BerdyshevEugene/statScraper/actions/workflows/ruff.yml)

# statScraper

скрипт для сбора статистики с телефонии

## Структура проекта:

<details>

```python

statScraper/
│
├── app/
│   ├── __init__.py
│   ├── filters/filters.py   # параметры для снятия статистики
│   ├── rabbitmq/
│   │   └── publish_results.py  # отправка данных в rabbit
│   ├── browser.py           # инициализация WebDriver
│   ├── client.py            # авторизация и переход к получению данных
│   ├── config.py            # настройки (URL, логин, пароль, пути) из .env
│   └── parser.py            # обработка полученных данных
│
├── main.py                  # точка входа
│
├── requirements.txt         # зависимости
├── .env                     # логины, пароли, URL
├── logger/                  # конфиг логгера
│   └── logger.log
├── logs/                    # логи
│   └── debug/errors.log
├── resources/               
│   └── app_icon.ico         # медиа
└── chromedriver             # драйвер для selenium
```

</details>

---

## Установка и использование UV

<details>
<summary>📦 Способы установки UV</summary>

### 1. Установка через автономные установщики (рекомендуется)

**Для macOS и Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Для Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Установка через PyPI (альтернативный способ)
```bash
pip install uv
```

### Обновление UV
После установки вы можете обновить UV до последней версии:
```bash
uv self update
```

🔗 Подробнее об установке: [Официальная документация](https://docs.astral.sh/uv/getting-started/installation/)
</details>

---

<summary>🚀 Основные команды UV</summary>

<details>

### Управление Python-окружением

**Установка конкретной версии Python:**
```bash
uv python install 3.13  # Установит Python 3.13
```

### Управление зависимостями

**Синхронизация зависимостей проекта:**
```bash
uv sync  # Аналог pip install + pip-compile
```

**Запуск команд в окружении проекта:**
```bash
uv run <COMMAND>  # Например: uv run pytest
```

**Запуск Django-сервера:**
```bash
uv run manage.py runserver  # Альтернатива python manage.py runserver
```
</details>

---


<summary>🔍 Интеграция с Ruff</summary>

<details>

[Ruff](https://github.com/astral-sh/ruff) - это молниеносный линтер для Python, также разработанный Astral.

**Установка Ruff через UV:**
```bash
uvx ruff  # Установит последнюю версию Ruff
```

**Проверка кода с помощью Ruff:**
```bash
uvx ruff check .  # Проверит все файлы в текущей директории
```
</details>

---

## Инструкция по запуску проекта

<details>

### Установка и запуск окружения:
```bash
uv venv .venv  # создаём виртуальное окружение на python 3.11
uv pip install -r requirements.txt  # ставим зависимости
```

### Запуск программы:
```bash
py main.py
```
### Компиляция в скрипт:
```bash
pyinstaller --onefile --icon=resources/app_icon.ico main.py
```

### Компиляция в скрипт (использовать данное решение):
```
pyinstaller main.py --onefile --icon=resources/app_icon.ico --copy-metadata aio-pika --copy-metadata pamqp --copy-metadata yarl
```

</details>

---


## Остальная информация

<details>

```
CompanyName: GMG
FileDescription: statScraper
InternalName: statScraper
ProductName: statScraper
Author: Berdyshev E.A.
Development and support: Berdyshev E.A.
LegalCopyright: © GMG. All rights reserved.
```

Media:
[иконки от Freepik - Flaticon](https://www.flaticon.com/ru/free-icon/bird_276097?related_id=276097&origin=pack)


</details>
