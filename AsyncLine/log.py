import sys
import logging

LOGGER = logging.getLogger(__file__)
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
FORMATTER = logging.Formatter("\r[%(asctime)s] [\x1b[31m%(levelname)s\x1b[39m] %(message)s", "%H:%M:%S")
LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)