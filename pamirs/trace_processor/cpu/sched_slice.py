# !/usr/bin/python3
# -*- coding: utf-8 -*-


class WakeeInfo:
    def __init__(self, wakee_name, wakee_tid, wakee_cpu):
        self.wakee_name = wakee_name
        self.wakee_tid = wakee_tid
        self.wakee_cpu = wakee_cpu


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
            self.wakee_name = wakee_info.wakee_name
            self.wakee_tid = wakee_info.wakee_tid
            self.wakee_cpu = wakee_info.wakee_cpu

    def __repr__(self):
        return "SchedSclice({} {} state={} slice={})".format(
            self.thread_info.name, self.thread_info.tid, self.state,
            self.slice
        )