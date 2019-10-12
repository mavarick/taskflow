#encoding:utf8

""" 从mongo中获取数据的task

external vars: mongo configuration
"""
import time
from taskflow.utils.utils import get_datetime_now

###############################################################################
import random
from taskflow.tasks.basetask import BaseTask


class TextTaskOne(BaseTask):
    def __init__(self, name, **kwargs):
        super(TextTaskOne, self).__init__(name, **kwargs)

    def process(self, fetch_num=50):
        output_queue = self.outputs[0]

        cnt = 1
        while 1:
            cnt = random.randint(1, 10000)
            d = {"_id": cnt, "data": cnt}
            self.logger.info("[%s]PUSH:%s" % (self.name, d))
            output_queue.push(d)
            time.sleep(0.3)
            cnt += 1

#
class TextTaskTwo(BaseTask):
    def __init__(self, name, **kwargs):
        super(TextTaskTwo, self).__init__(name, **kwargs)
        # data_api, should be implemented by mongodb_api

    def process(self, fetch_num=50):
        output_queue = self.outputs[0]

        while 1:
            item = self.input.get()
            if not item:
                time.sleep(1)
                continue
            output_queue.push(item)
            self.logger.info("[%s][PUSH]output_queue_old: %s" % (self.name, item))

#
class TextTaskThree(BaseTask):
    def __init__(self, name, **kwargs):
        super(TextTaskThree, self).__init__(name, **kwargs)
        # data_api, should be implemented by mongodb_api

    def process(self, fetch_num=50):
        output_queue_old = self.outputs[0]
        output_queue_even = self.outputs[1]

        while 1:
            item = self.input.get()
            if not item:
                time.sleep(1)
                continue
            _id = item["_id"]
            data = item["data"]
            if data % 2 == 1:
                output_queue_old.push(item)
                self.logger.info("[%s][PUSH]output_queue_old: %s" % (self.name, item))
            else:
                output_queue_even.push(item)
                self.logger.info("[%s][PUSH]output_queue_even: %s" % (self.name, item))


#
class TextTaskThreeOld(BaseTask):
    def __init__(self, name, **kwargs):
        super(TextTaskThreeOld, self).__init__(name, **kwargs)
        # data_api, should be implemented by mongodb_api

    def process(self, fetch_num=50):
        while 1:
            item = self.input.get()
            if not item:
                time.sleep(1)
                continue
            self.logger.info("[%s][GET]:%s" % (self.name, item))

#
class TextTaskThreeEven(BaseTask):
    def __init__(self, name, **kwargs):
        super(TextTaskThreeEven, self).__init__(name, **kwargs)
        # data_api, should be implemented by mongodb_api

    def process(self, fetch_num=50):
        while 1:
            item = self.input.get()
            if not item:
                time.sleep(1)
                continue
            self.logger.info("[%s][GET]:%s" % (self.name, item))

