import logging
import sys

from common.variables import LOGGING_LEVEL

console_logger = logging.getLogger("console")
formatter = logging.Formatter("%(asctime)s %(levelname)-10s %(module)s %(message)s")

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)

console_logger.addHandler(handler)
console_logger.setLevel(LOGGING_LEVEL)