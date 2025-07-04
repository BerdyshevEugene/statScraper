import datetime

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from logger.logger import setup_logger
from app.config import settings
from app.rabbitmq.publish_results import publish_results


logger = setup_logger(module_name=__name__)
CITY = settings.city


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

        phrases = [
            "В среднем клиенты ждут",
            "В среднем разговор длится",
            "Клиенты, не дождавшиеся ответа, ждали в среднем:",
        ]
        if any(phrase in label for phrase in phrases):
            try:
                number = float(value.split()[0].replace(",", "."))
                data[label] = round(number)
            except (ValueError, IndexError) as e:
                logger.warning(
                    f"failed to parse number from value '{value}' in label '{label}': {e}"
                )
                data[label] = 0
        else:
            data[label] = value
    logger.info(f"parsing finished, extracted {len(data)} items")
    return data


async def save_result(data: dict) -> None:
    """
    передаем результат в json
    """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    data["Date"] = yesterday.strftime("%Y-%m-%d")

    if not CITY:
        logger.warning("not CITY in .env")
    data["City"] = CITY

    try:
        await publish_results(data)
        logger.success(f"data was sent to rabbitmq {data}")
    except Exception as e:
        logger.error(f"error when sending data to the queue: {e}")
