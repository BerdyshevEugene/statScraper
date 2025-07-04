import asyncio
import sys

from pathlib import Path
from dotenv import load_dotenv

from app.browser import get_driver
from app.client import login_and_get_data
from app.parser import save_result
from logger.logger import setup_logger


if getattr(sys, "frozen", False):
    env_path = Path(sys.executable).parent / ".env"
else:
    env_path = Path(__file__).parent / ".env"

load_dotenv(dotenv_path=env_path)

logger = setup_logger(module_name=__name__)


async def main():
    logger.info("start app")
    driver = get_driver()
    try:
        data = login_and_get_data(driver)
        await save_result(data)
    except Exception as e:
        logger.exception(f"❌ error: {e}")
    finally:
        try:
            driver.quit()
            logger.success("app closed")
        except Exception:
            logger.warning("⚠️ app cannot closed")


if __name__ == "__main__":
    asyncio.run(main())
