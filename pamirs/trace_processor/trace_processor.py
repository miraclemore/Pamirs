# !/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep

from pamirs.trace_processor.systrace.systrace_parser import SystraceParser
from pamirs.utils.read_trace import read_trace_using_mmap, read_trace_using_read


class TraceProcessor:
    def __init__(self, trace_file_path):
        """Inits TraceProcessor."""
        self.trace_file_path = trace_file_path
        self.trace_raw_data = list()
        self.events_list = list()

        self.load_trace(1)

        self.systrace_parser = SystraceParser()
        self.parse_trace()

    def load_trace(self, use_mmap):
        """load trace from trace file path."""
        if use_mmap:
            self.trace_raw_data = read_trace_using_mmap(self.trace_file_path)
        else:
            self.trace_raw_data = read_trace_using_read(self.trace_file_path,
                                                        self.trace_raw_data)

    def parse_trace(self):
        for line in self.trace_raw_data:
            event = self.systrace_parser.systrace_parse_line(line)
            if event:
                self.events_list.append(event)

    def dump_events(self):
        for event in self.events_list:
            print(event)
