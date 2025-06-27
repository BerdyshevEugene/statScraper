from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger.logger import setup_logger

logger = setup_logger(module_name=__name__)


def setup_filters(driver: WebDriver) -> None:
    """
    функция ставит необходимые параметры:
    -> вчерашняя дата
    -> все очереди
    -> не учитывать звонки менее 5 сек.
    -> показать
    """
    wait = WebDriverWait(driver, 10)

    yesterday = (datetime.today() - timedelta(days=1)).strftime("%d.%m.%Y")
    logger.info(f"setting date input to yesterday: {yesterday}")
    date_input = wait.until(EC.presence_of_element_located((By.NAME, "fromdate")))
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        date_input,
        yesterday,
    )

    logger.info("selecting 'all queues'")
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ddcl-1")))
    dropdown.click()

    all_queues_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "ddcl-1-i0")))
    if not all_queues_checkbox.is_selected():
        logger.info("checking 'all queues' checkbox")
        all_queues_checkbox.click()
    else:
        logger.info("'all queues' checkbox already selected")

    close_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(@class, "ui-dropdownchecklist-close")]')
        )
    )
    close_btn.click()
    logger.info("closed queues dropdown")

    checkbox = driver.find_element(By.NAME, "five_sec_less")
    if not checkbox.is_selected():
        logger.info("checking 'exclude calls less than 5 seconds'")
        checkbox.click()
    else:
        logger.info("'exclude calls less than 5 seconds' checkbox already selected")

    show_button = wait.until(EC.element_to_be_clickable((By.ID, "button-search")))
    logger.info("clicking show button")
    show_button.click()

    logger.info("filters set successfully")
