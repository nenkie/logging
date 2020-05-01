import traceback
import functools
import sys
import logging
import json

logger = logging.getLogger("lol")

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
            "lol": {
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


def elastic_logs(func):
    @functools.wraps(func)
    def hook_wrapper(*args, **kwargs):
        sys.excepthook = except_jsonhook
        logging.config.dictConfig(json.loads(LOGGING))
        return func(*args, **kwargs)

    return hook_wrapper


def configurable(filename):
    def configure(func):
        @functools.wraps(func)
        def conf_wrapper(*args, **kwargs):
            return func(config=_load_application_config(filename), *args, **kwargs)

        return conf_wrapper

    return configure


def except_jsonhook(exc_type, exc_value, exc_traceback):
    # Do not print exception when user cancels the program
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    exception = traceback.format_exception(exc_type, exc_value, exc_traceback)

    logger.critical(f"Uncaught exception occurred, application will terminate: {exception}",
                    exc_info=(exc_type, exc_value, exc_traceback))


def _load_application_config(file_name):
    with open(file_name, "r") as f:
        return json.loads(f.read())
