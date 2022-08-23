# !/usr/bin/python3
# -*- coding: utf-8 -*-
from enum import IntEnum


class SchedState(IntEnum):
    TASK_RUNNING = 0x0
    TASK_INTERRUPT = 0x1
    TASK_UNINTERRUPT = 0x2
    TASK_RUNNABLE = 0x4
    TASK_PREEMPTED = 0x8
    TASK_WAKEUP = 0x10
