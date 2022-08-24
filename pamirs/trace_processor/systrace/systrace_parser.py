# !/usr/bin/python3
# -*- coding: utf-8 -*-
import re

from pamirs.trace_processor.events.event import Event
from pamirs.trace_processor.events.power.cpu_frequency import cpu_frequency
from pamirs.trace_processor.events.power.cpuidle import cpu_idle
from pamirs.trace_processor.events.sched.sched_switch import sched_switch
from pamirs.trace_processor.events.sched.sched_wakeup import sched_wakeup

ftrace_handler_dict = {
    "sched_switch": sched_switch,
    "sched_wakeup": sched_wakeup,
    "cpu_idle": cpu_idle,
    "cpu_frequency": cpu_frequency
}


class SystraceParser:
    _TRACE_LINE_PATTERN = re.compile(
        r"""
        (?P<name>.+) # thread name
        \D
        (?P<tid>\d+) # tid
        \s+
        \D*(?P<pid>\d*)\D* # pid
        \s*
        \[(?P<cpu>\d+)\] # cpu#
        \s+
        (?P<irqs_off>[d|X|\.]) # irqs-off
        (?P<need_resched>[N|n|p|\.]) # need-resched
        (?P<irq_type>[H|h|s|.]) # hardirq/softirq
        (?P<preempt_depth>[0-9|.]) # preempt-depth
        \s+
        (?P<raw_timestamp>\d+\W{1}\d+)
        \W{1}\s+ 
        (?P<tracepoint>\w+) # tracepoint
        \W{1}\s+
        (?P<data>.+) # data
        """,
        re.X | re.M

    )

    def __init__(self):
        self.ts_raw_start = 0
        self.ts_raw_end = 0
        self.ts_dur = 0

    def systrace_parse_line(self, line):
        matched = re.match(self._TRACE_LINE_PATTERN, line)
        if matched:
            mgd = matched.groupdict()

            mgd['raw_timestamp'] = int(float(mgd['raw_timestamp']) * 1000000)
            if self.ts_raw_start == 0:
                self.ts_raw_start = mgd['raw_timestamp']
            mgd['timestamp'] = mgd['raw_timestamp'] - self.ts_raw_start

            if mgd['tracepoint'] == "tracing_mark_write":
                self.systrace_parse_print_event(mgd['data'])
            else:
                mgd['data'] = self.systrace_parse_ftrace_event(
                    mgd['tracepoint'], mgd['data'])

            return Event(**mgd)
        else:
            return None

    def systrace_parse_print_event(self, data):
        pass

    def systrace_parse_ftrace_event(self, tracepoint, data):
        if tracepoint in ftrace_handler_dict:
            return ftrace_handler_dict[tracepoint](data)
