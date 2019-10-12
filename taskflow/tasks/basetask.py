#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 信号和退出机制:
    1, 会从signal("signal")中获取外层全局信号，看是否退出
    2, 拿到signal之后，会更改run_status的状态，
        当后续处理完成，更改run_status,
        当run_status为0的时候，就会退出
"""


from blinker import signal
from datetime import datetime
from taskflow.utils.decorators import wrap_threading, run_period

class BaseTask(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.input = None
        self.outputs = []

        self.logger = kwargs['logger']

        # use signal to control the process
        s = signal("signal")
        s.connect(self.update_signal)
        self.run_status = 0

    @wrap_threading
    def start(self, *args, **kwargs):
        # after all is set, then shoule start this
        print("[START]:%s" % (self.name,))
        self.process()

    @wrap_threading
    @run_period(interval=3)
    def start_status(self):
        self.update_status()
    
    def update_signal(self, signal):
        self.signal = signal

    def process(self):
        if self.signal == 0:
            raise Exception("signal exit")
        raise NotImplementedError

    def update_status(self):
        pass
        #raise NotImplementedError


class TaskPool(object):
    def __init__(self, task_class, name, num=1, input=None, outputs=[], **class_kwargs):
        self.task_class = task_class
        self.name = name
        self.num = num
        self.input = input
        self.outputs = outputs
        
        self.tasks = []
        for i in range(self.num):
            task_name = "%s#%s" % (self.name, i+1)
            t = task_class(task_name, **class_kwargs)
            t.input = self.input
            t.outputs = self.outputs
            self.tasks.append(t)
            
    def start(self):
        for t in self.tasks:
            t.start()

    def start_status(self):
        for t in self.tasks:
            t.start_status()

