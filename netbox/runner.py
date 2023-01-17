import logging

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.debug("This is debug msg")
    logger.info("This is info msg")
    logger.warning("This is warning msg")
    logger.error("This is error msg")
    logger.critical("This is critical msg")

    a = 5
    b = 0
    try:
        c = a / b
    except Exception as e:
        logger.exception("Exception occurred", exc_info=True)

    print("Done.")
