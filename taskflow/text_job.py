#!/usr/bin/env python 

import sys
sys.path.append("../")

from taskflow.config import text_queue_config

from taskflow.tasks.text_task import TextTaskOne,TextTaskTwo,TextTaskThree,TextTaskThreeOld,TextTaskThreeEven
from taskflow.tasks.basetask import TaskPool

from taskflow.channels.queue_channel import QueueChannel

from taskflow.jobs.Job import Job

from config_logger import logger

# queue definations
queue_one = QueueChannel("queue_one", text_queue_config)
queue_two = QueueChannel("queue_two", text_queue_config)
queue_three_old = QueueChannel("queue_three_old", text_queue_config)
queue_three_even = QueueChannel("queue_three_even", text_queue_config)

# taskflow definations
#tasks_one = [TextTaskOne("task_one_%s" % t) for t in range(10)] 
#for t in tasks_one:
#    t.outputs = [queue_one]

task_pool_one = TaskPool(TextTaskOne, name="text_task_pool", num=10, outputs=[queue_one], logger=logger)
#task_one.outputs = [queue_one]

task_two = TextTaskTwo("task_two", logger=logger)
task_two.input = queue_one
task_two.outputs = [queue_two]

task_three = TaskPool(TextTaskThree, name="task_three", num=3, input=queue_two, outputs=[queue_three_old, queue_three_even], logger=logger)

#task_three = TextTaskThree("task_three", logger=logger)
#task_three.input = queue_two
#task_three.outputs = [queue_three_old, queue_three_even]

task_three_old = TextTaskThreeOld("task_three_old", logger=logger)
task_three_old.input = queue_three_old

task_three_even = TextTaskThreeEven("task_three_even", logger=logger)
task_three_even.input = queue_three_even

# job
#job = Job("text_job", [tasks_one, task_two, task_three, task_three_old, task_three_even])
job = Job("text_job", [task_pool_one, task_two, task_three, task_three_old, task_three_even])
job.start()
job.wait_to_exit()

