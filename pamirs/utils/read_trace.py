# !/usr/bin/python3
# -*- coding: utf-8 -*-
import mmap
import timeit


def display_time(func):
    def wrapper(file_path):
        start = timeit.default_timer()
        func(file_path)
        stop = timeit.default_timer()
        print('Time: ', stop - start)
    return wrapper


@display_time
def read_trace_using_read(file_path):
    """Read trace using direct IO."""
    with open(file_path, mode="r", encoding="utf8") as f:
        for line in f:
            print(line.rstrip())


@display_time
def read_trace_using_mmap(file_path):
    """Read trace using mmap."""
    with open(file_path, mode="r", encoding="utf8") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_f:
            for line in iter(mmap_f.readline, b""):
                print(line.decode("utf-8").rstrip())
