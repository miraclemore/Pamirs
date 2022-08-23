# !/usr/bin/python3
# -*- coding: utf-8 -*-
from pamirs.trace_processor.cpu.cpu import CPU
from pamirs.trace_processor.trace_processor import TraceProcessor

tp = TraceProcessor("/work/logs/example_android_trace_15s.systrace")

cpu = CPU(tp)
