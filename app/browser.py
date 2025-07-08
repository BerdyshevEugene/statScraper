import sys

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from app.config import settings
from logger.logger import setup_logger

logger = setup_logger(module_name=__name__)


def str_to_bool(value: str) -> bool:
    return value.lower() in ("1", "true", "yes", "on")


def get_driver():
    logger.info("🔧 initializing the WebDriver")
    headless = settings.headless
    logger.debug(f"💡 HEADLESS mode from .env: {headless}")
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        logger.debug("🖥️ headless mode is set (without window)")
    else:
        options.add_argument("--start-maximized")

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
