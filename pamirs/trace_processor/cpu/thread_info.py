# !/usr/bin/python3
# -*- coding: utf-8 -*-

class ThreadInfo:
    def __init__(self, name, tid, pid, prio=None):
        self.name = name
        self.tid = tid
        self.pid = pid
        self.prio = prio

    def __repr__(self):
        return "ThreadInfo(name={} tid={} pid={} prio={}".format(
            self.name, self.tid, self.pid, self.prio
        )

    def __eq__(self, other):
        if self.name == other.name \
                and self.tid == other.tid:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name + "-" + str(self.tid))
