#encoding:utf8
#author: mavarick

from blinker import signal
import time


class Job(object):
    def __init__(self, name, tasks):
        s = signal("signal")
        s.connect(self.update_signal)

        self.name = name
        self.tasks = tasks

    def start(self):
        for task in self.tasks:
            task_name = task.name
            task.start()
            task.start_status()
            print("start [{}]".format(task_name))

    def update_signal(self, signal):
        self.signal = signal

    def wait_to_exit(self):
        try:
            while 1:
                time.sleep(0.3)
        except:
            time.sleep(1)
        print("::EXIT::")
