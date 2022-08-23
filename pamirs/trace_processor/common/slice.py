# !/usr/bin/python3
# -*- coding: utf-8 -*-

class Slice:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.dur = end - start

    def __repr__(self):
        return "Slice(start={} end={} dur={})".format(
            self.start, self.end, self.dur
        )

    def duration(self):
        return self.dur
