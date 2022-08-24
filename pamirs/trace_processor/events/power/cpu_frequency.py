# !/usr/bin/python3
# -*- coding: utf-8 -*-
import re

cpu_frequency_pattern = re.compile(
        r"""
        state=(?P<state>\d+)\s+
        cpu_id=(?P<cpu_id>\d+)
        """,
        re.X|re.M
)

class CpuFrequency:
    def __init__(self, state, cpu_id):
        self.state = int(state)
        self.cpu_id = int(cpu_id)

    def __repr__(self):
        return "CpuFrequency(state={} cpu{})".format(
            self.state, self.cpu_id
        )


def cpu_frequency(data):
    """Parser for `cpu_frequency` tracepoint"""
    matched = re.match(cpu_frequency_pattern, data)
    if matched:
        match_group_dict = matched.groupdict()
        return CpuFrequency(**match_group_dict)
