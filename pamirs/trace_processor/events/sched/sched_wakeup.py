# !/usr/bin/python3
# -*- coding: utf-8 -*-
import re

# NOTE: 'success' is optional for some android phones and linux kernels
# comm=tfm_b6bcf800 pid=1714 prio=35 success=1 target_cpu=000
sched_wakeup_pattern = re.compile(
    r"""
    comm=(?P<comm>.*)\s+
    pid=(?P<pid>\d+)\s+
    prio=(?P<prio>\d+)\s+
    target_cpu=(?P<target_cpu>\d+)
    """,
    re.X | re.M
)


class SchedWakeup:
    def __init__(self, comm, pid, prio, target_cpu):
        self.comm = comm.strip()
        self.tid = int(pid)
        self.prio = int(prio)
        self.target_cpu = int(target_cpu)

    def __repr__(self):
        return "SchedWakeup(comm={} tid={} prio={} target_cpu={})".format(
            self.comm, self.tid, self.prio, self.target_cpu
        )


def sched_wakeup(data):
    """Parser for `sched_wakeup` tracepoint"""
    match = re.match(sched_wakeup_pattern, data)
    if match:
        match_group_dict = match.groupdict()
        return SchedWakeup(**match_group_dict)
