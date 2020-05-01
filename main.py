import logging.config
from utils import elastic_logs, configurable

logger = logging.getLogger("lol")


@elastic_logs
def start_loggable_application():
    logger.debug("This is usual debug from start_loggable_application")
    logger.info("This is info from start_loggable_application")
    logger.warning("This is warning from start_loggable_application")
    logger.error("This is handled error from start_loggable_application")

    try:
        1 / 0
    except ArithmeticError:
        logger.exception('Handled exception from start_loggable_application', exc_info=True)


@elastic_logs
@configurable(filename="config/application_prod.json")
def start_loggable_and_configurable(config):
    logger.info(config['name'])

    logger.debug("This is usual debug from start_loggable_and_configurable")
    logger.info("This is info from start_loggable_and_configurable")
    logger.warning("This is warning from start_loggable_and_configurable")
    logger.error("This is handled error from start_loggable_and_configurable")

    try:
        1 / 0
    except ArithmeticError:
        logger.exception('Handled exception from start_loggable_and_configurable', exc_info=True)

    1 / 0

    print("I won't be executed after unhandled exception")


if __name__ == '__main__':
    start_loggable_application()
    start_loggable_and_configurable()
