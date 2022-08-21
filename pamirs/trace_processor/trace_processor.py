# !/usr/bin/python3
# -*- coding: utf-8 -*-
from pamirs.utils.read_trace import read_trace_using_mmap, read_trace_using_read


class TraceProcessor:
    def __init__(self, trace_file_path):
        """Inits TraceProcessor."""
        self.trace_file_path = trace_file_path

    def load_trace(self, use_mmap):
        """load trace from trace file path."""
        if use_mmap:
            read_trace_using_mmap(self.trace_file_path)
        else:
            read_trace_using_read(self.trace_file_path)
