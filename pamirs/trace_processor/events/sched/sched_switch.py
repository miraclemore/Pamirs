# !/usr/bin/python3
# -*- coding: utf-8 -*-
import re

sched_switch_pattern = re.compile(
    r"""
    prev_comm=(?P<prev_comm>.*)\s+
    prev_pid=(?P<prev_pid>\d+)\s+
    prev_prio=(?P<prev_prio>\d+)\s+
    prev_state=(?P<prev_state>.+)\s+ # todo: handled corner cases e.g. D|W
    ==>\s+
    next_comm=(?P<next_comm>.*)\s+
    next_pid=(?P<next_pid>\d+)\s+
    next_prio=(?P<next_prio>\d+)
    """,
    re.X | re.M
)


class SchedSwitch:

    def __init__(self, prev_comm, prev_pid, prev_prio,
                 prev_state, next_comm, next_pid, next_prio):
        self.prev_comm = prev_comm.strip()
        self.prev_tid = int(prev_pid)
        self.prev_prio = int(prev_prio)
        self.prev_state = prev_state
        self.next_comm = next_comm.strip()
        self.next_tid = int(next_pid)
        self.next_prio = int(next_prio)

    def __repr__(self):
        return "SchedSwitch(prev_pid={} prev_prio={} ===> next_pid={} next_prio={})".format(
            self.prev_tid, self.prev_prio, self.next_tid, self.next_prio
        )


def sched_switch(payload):
    """Parser for `sched_switch` tracepoint"""
    match = re.match(sched_switch_pattern, payload)
    if match:
        match_group_dict = match.groupdict()
        return SchedSwitch(**match_group_dict)
    else:
        return None
