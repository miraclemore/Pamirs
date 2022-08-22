# !/usr/bin/python3
# -*- coding: utf-8 -*-

class Event:
    def __init__(self, name, tid, pid, cpu, timestamp, tracepoint, data, **kwargs):
        self.name = name
        self.tid = tid
        self.pid = pid
        self.cpu = cpu
        self.tracepoint = tracepoint
        self.ts_int = int(float(timestamp) * 1000000)
        self.data = data

    def __repr__(self):
        return "Event(name={} tid={} pid={} cpu={} ts={} tp={})".format(
            self.name, self.tid, self.pid, self.cpu, self.ts_int, self.tracepoint
        )
