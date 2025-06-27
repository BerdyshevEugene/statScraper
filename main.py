from app.browser import get_driver
from app.client import login_and_get_data
from app.parser import save_result
from logger.logger import setup_logger

logger = setup_logger(module_name=__name__)


def main():
    logger.info("🚀 START")
    driver = get_driver()
    try:
        data = login_and_get_data(driver)
        save_result(data)
        logger.success("💾 data was saved")
    except Exception as e:
        logger.exception(f"❌ error: {e}")
    finally:
        try:
            driver.quit()
            logger.success("app closed")
        except Exception:
            logger.warning("⚠️ app cannot closed")


if __name__ == "__main__":
    main()
