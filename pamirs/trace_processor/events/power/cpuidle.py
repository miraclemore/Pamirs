# !/usr/bin/python3
# -*- coding: utf-8 -*-
import re

cpu_idle_pattern = re.compile(
    r"""
    state=(?P<state>\d+)\s+
    cpu_id=(?P<cpu_id>\d+)
    """,
    re.X | re.M
)


class CpuIdle:
    def __init__(self, state, cpu_id):
        self.state = int(state)
        self.cpu_id = int(cpu_id)

    def __repr__(self):
        return "CpuIdle(state={} cpu{}".format(
            self.state, self.cpu_id
        )


def cpu_idle(data):
    """Parser for `cpu_idle` tracepoint"""
    matched = re.match(cpu_idle_pattern, data)
    if matched:
        match_group_dict = matched.groupdict()
        return CpuIdle(**match_group_dict)
