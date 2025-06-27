import datetime
import json
import math
import sys

from pathlib import Path
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from logger.logger import setup_logger

logger = setup_logger(module_name=__name__)


def value_in_cell(cell):
    try:
        text = cell.text.strip()
        value = float(text.replace(",", ".").split()[0])
        return value > 0
    except (ValueError, IndexError, StaleElementReferenceException) as e:
        logger.debug(f"value_in_cell exception: {e}")
        return False


def parse_data(driver) -> dict:
    """
    функция парсит полученные данные по статистике
    """
    logger.info("start waiting for table data presence")
    WebDriverWait(driver, 10).until(
        lambda d: any(
            value_in_cell(cell)
            for cell in d.find_elements(By.XPATH, '//table[@class="grid"]//tr/td[2]')
        )
    )
    logger.info("table data is present, starting parsing")

    rows = driver.find_elements(By.XPATH, '//table[@class="grid"]//tr')
    data = {}

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) != 2:
            continue

        label = cells[0].text.strip()
        value = cells[1].text.strip()

        if "В среднем клиенты ждут" in label or "В среднем разговор длится" in label:
            try:
                number = float(value.split()[0].replace(",", "."))
                data[label] = math.ceil(number)
            except (ValueError, IndexError) as e:
                logger.warning(
                    f"failed to parse number from value '{value}' in label '{label}': {e}"
                )
                data[label] = 0
        else:
            data[label] = value
    logger.info(f"parsing finished, extracted {len(data)} items")
    return data


def save_result(data: dict) -> None:
    """
    сохраняет результат в result/result_год_месяц_день.json
    """
    today_str = datetime.date.today().strftime("%Y_%m_%d")

    if getattr(sys, "frozen", False):
        BASE_DIR = Path(sys.executable).parent
    else:
        BASE_DIR = Path(__file__).resolve().parent

    result_dir = BASE_DIR / "result"
    result_dir.mkdir(exist_ok=True)

    result_path = result_dir / f"result_{today_str}.json"

    try:
        with result_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"result saved successfully to {result_path}")
    except Exception as e:
        logger.error(f"failed to save result to {result_path}: {e}")
