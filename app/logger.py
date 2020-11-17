import logging
import argparse
import sys
import coloredlogs

# Check The Command Line For Log Level
parser = argparse.ArgumentParser()
parser.add_argument(
    "-log", 
    "--log", 
    default="debug",
    help=(
        "Provide logging level. "
        "Example --log debug', default='warning'"),
    )
options = parser.parse_args()
levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
level = levels.get(options.log.lower())
if level is None:
    raise ValueError(
        f"log level given: {options.log}"
        f" -- must be one of: {' | '.join(levels.keys())}")

# Initialize Logger
_LOGGER = logging.getLogger(__name__)

# Set Output And Level
logging.basicConfig(stream=sys.stdout, level=level)
coloredlogs.install(level=level)
