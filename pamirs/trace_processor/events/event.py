# !/usr/bin/python3
# -*- coding: utf-8 -*-

class Event:
    def __init__(self, name, tid, pid, cpu, raw_timestamp, timestamp, tracepoint, data, **kwargs):
        self.name = name.strip()
        self.tid = int(tid)
        if self.name == "<idle>":
            self.pid = None
        else:
            self.pid = int(pid)
        self.cpu = int(cpu)
        self.tracepoint = tracepoint
        self.raw_ts = raw_timestamp
        self.ts = timestamp
        self.data = data

    def __repr__(self):
        return "Event(name={} tid={} pid={} cpu={} ts={} tp={})".format(
            self.name, self.tid, self.pid, self.cpu, self.ts, self.tracepoint
        )
