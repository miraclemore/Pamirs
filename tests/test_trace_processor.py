# !/usr/bin/python3
# -*- coding: utf-8 -*-
from pamirs.trace_processor.trace_processor import TraceProcessor

tp = TraceProcessor("/work/logs/example_android_trace_15s.systrace")

print(tp)

tp.dump_pids_map()
