import traceback
import functools
import sys
import logging
import json

logger = logging.getLogger()

LOGGING = """
        {
          "version": 1,
          "formatters": {
            "json": {
              "()": "json_formatter.JSONFormatter"
            }
          },
          "handlers": {
            "console": {
              "class": "logging.StreamHandler",
              "level": "INFO",
              "formatter": "json",
              "stream": "ext://sys.stdout"
            },
            "file": {
              "class": "logging.FileHandler",
              "level": "INFO",
              "filename": "log.log",
              "formatter": "json"
            }
          },
          "loggers": {
            "olaf": {
              "level": "INFO",
              "handlers": ["console","file"],
              "propagate": false
            }
          },
          "root": {
            "level": "INFO",
            "handlers": ["console"]
          }
        }
"""


def logging_hook(func):
    @functools.wraps(func)
    def hook_wrapper(*args, **kwargs):
        logger.info("Doing hook #1")
        sys.excepthook = except_jsonhook

        with open("application.json", "r") as f:
            application_config = json.loads(f.read())

        logging.config.dictConfig(json.loads(LOGGING))

        return func(*args, **kwargs, config=application_config)

    return hook_wrapper


def except_jsonhook(exc_type, exc_value, exc_traceback):
    # Do not print exception when user cancels the program
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    exception = traceback.format_exception(exc_type, exc_value, exc_traceback)

    logger.critical(f"Uncaught exception occurred, application will terminate: {exception}",
                    exc_info=(exc_type, exc_value, exc_traceback))
