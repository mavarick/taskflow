#encoding:utf8

from datetime import datetime
import time
import Queue
import threading

from config_logger import logger

from taskflow.utils.utils import get_datetime_now

class QueueChannel(object):
    def __init__(self, name, queue_config):
        self.name = name
        self.queue_config = queue_config

        self.max_queue_size = self.queue_config.get("max_queue_size", 100)
        self.push_timeout = self.queue_config.get("push_timeout", 30)
        self.push_try_cnt = self.queue_config.get("push_try_cnt", 3)
        self.get_timeout = self.queue_config.get("get_timeout", 30)
        self.get_try_cnt = self.queue_config.get("get_try_cnt", 3)
        self.short_thresh = self.queue_config.get("short_thresh", 30)

        self.Q = Queue.Queue(maxsize=self.max_queue_size)

        # status
        self.push_cnt = 0
        self.push_succ_cnt = 0
        self.push_fail_cnt = 0
        self.last_push_time = None

        self.get_cnt = 0
        self.get_succ_cnt = 0
        self.get_fail_cnt = 0
        self.last_get_time = None

        self.init()

    def __del__(self):
        self.stop()

    def push(self, item):
        # push item to queue
        self.push_cnt += 1
        self.last_push_time = get_datetime_now()
        _push_cnt = 0
        while 1:
            try:
                self.Q.put(item, timeout=self.push_timeout)
                self.push_succ_cnt += 1
            except Queue.Full, ex:
                time.sleep(1)
                _push_cnt += 1
                logger.warn("[dumper][%s],Queue.Full")
                if self.push_try_cnt and _push_cnt > self.push_try_cnt:
                    self.push_fail_cnt += 1
                    return -1
                continue
            break
        return 0

    def get(self):
        self.get_cnt += 1
        self.last_get_time = get_datetime_now()
        _get_cnt = 0
        while 1:
            """
            if Controler._EXIT:
                if self.Q.qsize() == 0:
                    raise Controler.ExitException("Exit")
            """
            try:
                item = self.Q.get(block=True, timeout=self.get_timeout)
                self.get_succ_cnt += 1
                return item
            except Queue.Empty, ex:
                time.sleep(1)
                _get_cnt += 1
                if self.get_try_cnt and _get_cnt > self.get_try_cnt:
                    self.get_fail_cnt += 1
                    return None
                continue

    def size(self):
        return self.Q.qsize()

    def get_status(self):
        data = {
            "size": self.size()
        }
        return data

    # TODO
    def init(self):
        pass

    # TODO
    def stop(self):
        pass

