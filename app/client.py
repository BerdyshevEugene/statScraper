from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config import settings
from app.parser import parse_data
from app.filters.filters import setup_filters
from logger.logger import setup_logger

logger = setup_logger(module_name=__name__)


def login_and_get_data(driver: WebDriver) -> str:
    logger.info("opening login page")
    driver.get(str(settings.login_url))

    logger.info("filling login and password")
    driver.find_element(By.NAME, "slogin").send_keys(settings.username)
    password_input = driver.find_element(By.NAME, "spass")
    password_input.send_keys(settings.password.get_secret_value())
    password_input.send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submenu-title"))
        )
        logger.info("login success: submenu-title found")
    except TimeoutException:
        logger.warning("login failed: trying alternative login button")
        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Войти"]]'))
        )
        login_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submenu-title"))
        )
        logger.info("login success after alternative method")

    # переход в "очереди"
    try:
        logger.info("finding link to queue.php")
        queue_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "queue.php")]'))
        )
        queue_link.click()
        logger.info("clicked queue link")
    except TimeoutException:
        logger.error("queue link not found or not clickable")
        raise

    try:
        logger.info("waiting for queue section to load")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "fl_l")]'))
        )
    except TimeoutException:
        logger.error("queue section did not load")
        raise

    # переход на вкладку "суточный"
    try:
        logger.info("finding day_tab")
        day_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[contains(@href, "section=day")]')
            )
        )
        day_tab.click()
        logger.info("clicked day_tab")
    except TimeoutException:
        logger.error("day tab not clickable")
        raise

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//li[@class="current"]/a[contains(@href, "section=day")]')
            )
        )
        logger.info("day tab successfully opened")
    except TimeoutException:
        logger.error("day tab did not open properly")
        raise

    setup_filters(driver)

    return parse_data(driver)
