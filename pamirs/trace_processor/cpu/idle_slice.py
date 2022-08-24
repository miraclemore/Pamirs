# !/usr/bin/python3
# -*- coding: utf-8 -*-

class IdleSlice:
    def __init__(self, cpu_id, state, slice):
        self.cpu_id = cpu_id
        self.state = state
        self.slice = slice

    def __repr__(self):
        return "IdleSlice(cpu{} freq={} {})".format(
            self.cpu_id, self.state, self.slice
        )
