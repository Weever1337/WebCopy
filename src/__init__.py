from loguru import logger
import sys


def setup_logger():
    info = "<blue>{time:HH:mm:ss}</blue> => <green>{message}</green>"
    error = "<red>{time:HH:mm:ss}</red> => <red>{message}</red>"
    debug = "<yellow>{time:HH:mm:ss}</yellow> => <yellow>{message}</yellow>"

    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format=info,
        level="INFO",
        filter=lambda record: record["level"].name == "INFO",
    )
    logger.add(
        sys.stdout,
        colorize=True,
        format=error,
        level="ERROR",
        filter=lambda record: record["level"].name == "ERROR",
    )
    logger.add(
        sys.stdout,
        colorize=True,
        format=debug,
        level="DEBUG",
        filter=lambda record: record["level"].name == "DEBUG",
    )


setup_logger()
