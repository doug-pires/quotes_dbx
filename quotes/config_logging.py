import logging

# Create the Formatter
formatter = logging.Formatter(
    "%(asctime)s :-: %(levelname)s :-: %(name)s :-: %(message)s"
)


# Create Handlers and set the ACCORDING LEVEL
def get_stream_handler():
    """
    Create and configure a logging StreamHandler with a specific formatter and log level.

    Returns:
        logging.StreamHandler: A StreamHandler instance configured with the specified formatter and log level.

    Example:
        handler = get_stream_handler()
        logger = logging.getLogger(__name__)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    """
    stream_handler = logging.StreamHandler()
    # Add Formatter to Handlers
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    return stream_handler


# Create Logger and set its level
def get_stream_logger(logger_name: str):
    """
    Create and configure a logging logger with a specific name, log level, and a StreamHandler.

    Args:
        logger_name (str): The name of the logger.

    Returns:
        logging.Logger: A Logger instance configured with the specified name, log level, and a StreamHandler.

    Example:
        logger = get_logger('my_logger')
        logger.info('This is an informational message')
        logger.error('This is an error message')
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # Add the Handlers to Logger
    logger.addHandler(get_stream_handler())
    return logger


if __name__ == "__main__":  # pragma: no cover
    # Testing
    logger = get_stream_logger("app_logger")
    logger.info("Hi from Logging!")
