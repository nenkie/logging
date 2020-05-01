import logging
import json
from datetime import datetime
import traceback


class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(self, validate=False)

    def format(self, record: logging.LogRecord) -> str:
        record.message = record.getMessage()
        input_data = {'@timestamp': datetime.utcnow().isoformat()[:-3] + 'Z', 'level': record.levelname}

        if record.message:
            input_data['message'] = record.message

        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            exception = traceback.format_exception(exc_type, exc_value, exc_traceback)
            input_data['exception'] = exception

        input_data['module'] = record.module

        return json.dumps(input_data)
