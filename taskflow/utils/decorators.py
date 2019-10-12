#!/usr/bin/env python

import time
import threading


def wrap_threading(func):
    def wrap_func(*args, **kwargs):
        p = threading.Thread(target=func, args=args, kwargs=kwargs)
        p.setDaemon(True)
        p.start()
    return wrap_func


def try_run(max_try_cnt=3):
    def wrap_outer(func):
        def wrap_inner(*args, **kwargs):
            try_cnt = 0
            is_succ = True
            while 1:
                try:
                    content = func(*args, **kwargs)
                    if not content:
                        raise
                    return True, content
                except:
                    if try_cnt < max_try_cnt:
                        try_cnt += 1
                        continue
                    return False, None 
        return wrap_inner
    return wrap_outer


def run_period(interval=1, name=""):
    def wrap_inner(func):
        def wrap_outer(*args, **kwargs):
            while 1:
                flag = func(*args, **kwargs)
                if flag == -1:
                    print "run_period: break"
                    break
                if interval:
                    time.sleep(interval)
        return wrap_outer
    return wrap_inner



