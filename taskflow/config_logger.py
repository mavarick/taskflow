#!/usr/bin/env python
# -*- coding: utf-8 -*-

# LOGGER
import logging
from taskflow.utils.Logger import init_logger

# console, rfile, rtfile
# LOGGER_NAME = "console"
# LOGGER_NAME = "rtfile"
LOG_PATH = 'run.log'
#logger_names = ["console", "rfile"]
logger_names = ["console", "rtfile"]
#logger_names = ["console"]
# for formatter
formater = "detail"  # empty, simple, detail
# for detail information of configuration
logger_info = {
    "log_path": LOG_PATH,
    "backupCount": 30,
    "interval": 1,
    "when": "midnight",
    'level': logging.INFO, # DEBUG, INFO, WARNING, ERROR, CRITICAL
    #'level': logging.WARNING  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

logger = init_logger(logger_names, formatter=formater, **logger_info)


