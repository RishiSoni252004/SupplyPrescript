import logging

def setup_logging():
    """
    Configure standard logging for the FastAPI application.
    Sets up the format and log level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully.")
