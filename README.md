# logging to JSON

This a small example of how to use decorators in order to log all application output to JSON (and possibly to elastic). sys.except_hook is used to catch all handled/unhandled exceptions and pass them via JSON formatter to output.

I used 2 decorators:
1) just logging in JSON (@elastic_logs)
2) logging in JSON + option to configure you application with some config (@elastic_logs + @configurable(...))

Feel free to use this code as reference, but mention this repo in your responses over the Internet.
