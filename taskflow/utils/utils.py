#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

def get_datetime_now(pattern="%Y-%m-%d %H:%M:%S"):
    now = datetime.now()
    return now.strftime(pattern)

