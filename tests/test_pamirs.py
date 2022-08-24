# !/usr/bin/python3
# -*- coding: utf-8 -*-

from pamirs.trace_processor.cpu.cpu import CPU
from pamirs.trace_processor.trace_processor import TraceProcessor

tp = TraceProcessor("/work/logs/example_android_trace_15s.systrace")

# tp.dump_events()

for event in tp.events_list:
    if event.tracepoint == "cpu_frequency":
        print(event)

# cpu = CPU(tp)
