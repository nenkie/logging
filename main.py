import logging.config
from utils import logging_hook

logger = logging.getLogger("olaf")


@logging_hook
def start_application2(config):

    print(config['name'])

    logger.debug("This is usual debug")
    logger.info("This is info")
    logger.warning("This is warning")
    logger.error("This is handled error")

    try:
        1 / 0
    except ArithmeticError:
        logger.exception('Handled exception', exc_info=True)

    # this is unhandled exception
    1 / 0

    print("I won't be executed after unhandled exception")


if __name__ == '__main__':
    start_application2()
