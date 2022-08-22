# !/usr/bin/python3
# -*- coding: utf-8 -*-
from enum import IntEnum


class SchedState(IntEnum):
    TASK_RUNNING = 0
    TASK_INTERRUPT = 1
    TASK_UNINTERRUPT = 2
    TASK_RUNNABLE = 4
    TASK_PREEMPTED = 8
