# !/usr/bin/python3
# -*- coding: utf-8 -*-
import mmap
import timeit


def display_time(func):
    def wrapper(file_path):
        start = timeit.default_timer()
        events = func(file_path)
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        return events
    return wrapper


@display_time
def read_trace_using_read(file_path, events_list):
    """Read trace using direct IO."""
    with open(file_path, mode="r", encoding="utf8") as f:
        for line in f:
            events_list.append(line)

    return events_list


@display_time
def read_trace_using_mmap(file_path):
    """Read trace using mmap."""
    events = []
    with open(file_path, mode="r", encoding="utf8") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_f:
            for line in iter(mmap_f.readline, b""):
                events.append(line.decode('utf-8').rstrip())
    return events
