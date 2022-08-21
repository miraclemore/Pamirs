# !/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep

from pamirs.trace_processor.trace_processor import TraceProcessor

tp = TraceProcessor("/work/logs/example_android_trace_15s.systrace")
tp.load_trace(0)
sleep(5)
tp.load_trace(1)
