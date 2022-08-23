# !/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from pamirs.trace_processor.systrace.systrace_parser import SystraceParser
from pamirs.utils.read_trace import read_trace_using_mmap, read_trace_using_read


class TraceProcessor:
    def __init__(self, trace_file_path):
        """Inits TraceProcessor."""
        self.trace_file_path = trace_file_path
        self.trace_raw_data = list()
        self.events_list = list()

        self.ts_raw_start = 0
        self.ts_raw_end = 0
        self.ts_dur = 0
        self.pids_map = defaultdict(int)
        self.load_trace(1)

        self.systrace_parser = SystraceParser()
        self.parse_trace()

    def __repr__(self):
        return "TP(file={} start={} end={} dur={})".format(
            self.trace_file_path, self.ts_raw_start, self.ts_raw_end, self.ts_dur
        )

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
                if self.ts_raw_start == 0:
                    self.ts_raw_start

                # name, tid, pid maybe reuse due to linux implementation.
                unique_id = event.name + "-" + str(event.tid)
                self.pids_map[unique_id] = event.pid

                self.events_list.append(event)
        self.ts_raw_end = self.events_list[-1].ts
        self.ts_dur = self.ts_raw_end - self.ts_raw_start

    def dump_events(self):
        for event in self.events_list:
            print(event)

    def dump_pids_map(self):
        for unique_id in self.pids_map:
            print("id={} pid={}".format(unique_id, self.pids_map[unique_id]))