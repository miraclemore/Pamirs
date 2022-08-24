# !/usr/bin/python3
# -*- coding: utf-8 -*-


class WakerInfo:
    def __init__(self, waker_name, waker_tid, waker_cpu):
        self.waker_name = waker_name
        self.waker_tid = waker_tid
        self.waker_cpu = waker_cpu

    def __repr__(self):
        return "Waker({}-{} on cpu{})".format(
            self.waker_name, self.waker_tid, self.waker_cpu
        )


class SleepInfo:
    def __init__(self, iowait, blocked_func):
        self.iowait = iowait
        self.blocked_func = blocked_func


class SchedSlice:
    def __init__(self, thread_info, cpu, slice, state, wakee_info=None, sleep_info=None):
        self.thread_info = thread_info
        self.cpu = cpu
        self.slice = slice
        self.state = state

        if sleep_info:
            self.iowait = sleep_info.iowait
            self.blocked_func = sleep_info.blocked_func

        if wakee_info:
            self.waker_name = wakee_info.waker_name
            self.waker_tid = wakee_info.waker_tid
            self.waker_cpu = wakee_info.waker_cpu

    def __repr__(self):
        return "SchedSclice({} {} state={} slice={})".format(
            self.thread_info.name, self.thread_info.tid, self.state,
            self.slice
        )