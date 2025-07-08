# statScraper

[![Ruff](https://github.com/BerdyshevEugene/statScraper/actions/workflows/ruff.yml/badge.svg?cache=buster)](https://github.com/BerdyshevEugene/statScraper/actions/workflows/ruff.yml)

---

## Описание

**statScraper** — инструмент для автоматизированного сбора статистики с телефонии и отправки данных в RabbitMQ. Подходит для интеграции с корпоративными системами и автоматизации отчетности.

---

## Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/BerdyshevEugene/statScraper.git
   cd statScraper
   ```
2. **Установите Python 3.11+** и [Chromedriver](https://chromedriver.chromium.org/downloads) (если используется Selenium).
3. **Создайте файл `.env` в корне проекта:**
   ```env
   URL=https://your-telephony-url
   LOGIN=your_login
   PASSWORD=your_password
   # Добавьте другие переменные по необходимости
   ```
4. **Установите зависимости:**
   ```bash
   uv venv .venv
   uv pip install -r requirements.txt
   ```
5. **Запустите проект:**
   ```bash
   py main.py
   ```

---


---

## Структура проекта

<details>
<summary>Показать структуру</summary>

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
├── resources/               # медиа
│   └── app_icon.ico
└── chromedriver             # драйвер для selenium
```
</details>

---

## Установка и запуск (подробно)

1. **Создайте виртуальное окружение:**
   ```bash
   uv venv .venv  # создаёт виртуальное окружение на python 3.11
   ```
2. **Установите зависимости:**
   ```bash
   uv pip install -r requirements.txt
   ```
3. **Запустите программу:**
   ```bash
   py main.py
   ```

---

## Компиляция в исполняемый файл

Для сборки standalone-скрипта используйте [PyInstaller](https://pyinstaller.org/):

```bash
pyinstaller main.py --onefile --icon=resources/app_icon.ico --copy-metadata aio-pika --copy-metadata pamqp --copy-metadata yarl
```

---

## Для разработчиков

### Использование UV

<details>
<summary>📦 Установка и команды UV</summary>

**Установка UV:**
- macOS/Linux:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- Windows (PowerShell):
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- Через PyPI:
  ```bash
  pip install uv
  ```

**Обновление UV:**
```bash
uv self update
```

**Установка Python:**
```bash
uv python install 3.13
```

**Синхронизация зависимостей:**
```bash
uv sync
```

**Запуск команд в окружении:**
```bash
uv run <COMMAND>
```
</details>

### Интеграция с Ruff

<details>
<summary>🔍 Проверка кода с помощью Ruff</summary>

[Ruff](https://github.com/astral-sh/ruff) — быстрый линтер для Python.

**Установка и запуск:**
```bash
uvx ruff
uvx ruff check .
```
</details>

---

## Лицензия и авторы

```
CompanyName: GMG
FileDescription: statScraper
InternalName: statScraper
ProductName: statScraper
Author: Berdyshev E.A.
Development and support: Berdyshev E.A.
LegalCopyright: © GMG. All rights reserved.
```

Media: [иконки от Freepik - Flaticon](https://www.flaticon.com/ru/free-icon/bird_276097?related_id=276097&origin=pack)
