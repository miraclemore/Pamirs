# !/usr/bin/python3
# -*- coding: utf-8 -*-

class ThreadState:
    def __init__(self, state, io_wait=None, blocked_func=None,
                 wakee_name=None, wakee_tid=None, wakee_cpu=None):
        self.state = state
        self.io_wait = io_wait
        self.blocked_func = blocked_func
        self.wakee_name = wakee_name
        self.wakee_tid = wakee_tid
        self.wakee_cpu = wakee_cpu
