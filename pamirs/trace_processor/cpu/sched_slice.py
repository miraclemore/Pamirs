# !/usr/bin/python3
# -*- coding: utf-8 -*-

class SchedSlice:
    def __init__(self, thread_info, thread_state, slice):
        self.thread_info = thread_info
        self.thread_state = thread_state
        self.slice = slice
