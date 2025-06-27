import sys

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from logger.logger import setup_logger

logger = setup_logger(module_name=__name__)


def get_driver(headless: bool = True):
    logger.info("🔧 initializing the WebDriver")
    options = Options()
    if headless:
        options.add_argument("--start-maximized")
        logger.debug("🖥️ headless mode is set (without window)")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        # определение пути к chromedriver
        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).resolve().parent.parent

        driver_path = base_dir / "chromedriver.exe"
        logger.debug(f"🛠️ driver_path: {driver_path}")

        service = Service(executable_path=str(driver_path))
        driver = webdriver.Chrome(service=service, options=options)

        logger.success("✅ WebDriver successfully created")
        return driver

    except Exception as e:
        logger.exception(f"error when creating WebDriver: {e}")
        raise
