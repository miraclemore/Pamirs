# !/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict

from pamirs.trace_processor.common.slice import Slice
from pamirs.trace_processor.cpu.sched_slice import SchedSlice
from pamirs.trace_processor.cpu.sched_state import SchedState
from pamirs.trace_processor.cpu.thread_info import ThreadInfo
from pamirs.trace_processor.cpu.thread_state import ThreadState


class CPU:
    def __init__(self, tp):
        self._tp = tp
        self._events_list = tp.events_list

        self._sched_events = list()
        self._sched_slices = defaultdict(list)
        self._thread_slices = defaultdict(list)

        self._filter_sched_events()
        self._parse_sched_events()

    def __repr__(self):
        pass

    def _filter_sched_events(self):
        for event in self._events_list:
            if event.tracepoint == "sched_switch" \
                    or event.tracepoint == "sched_waking":
                    self._sched_events.append(event)

    def _parse_sched_events(self):
        last_seen_state = defaultdict(ThreadInfo)
        last_seen_timestamp = defaultdict(defaultdict(ThreadInfo))

        for event in self._events_list:
            if event == "sched_wakeup":
                data = event.data
                target_cpu = data.target_cpu
                waker_pid = self.find_thread_pid(data.comm, data.tid)
                waker_thread = ThreadInfo(data.comm, data.tid, waker_pid, data.prio)

                waker_thread_state = ThreadState(
                    SchedState.TASK_RUNNABLE, 0, None,
                    event.name, event.tid, event.cpu)

                last_seen_state[waker_thread] = waker_thread_state
                last_seen_timestamp[target_cpu][waker_thread] = event.ts_int

            elif event == "sched_switch":
                data = event.data
                cpu = event.cpu
                prev_pid = self.find_thread_pid(data.prev_comm, data.prev_tid)
                prev_thread = ThreadInfo(data.prev_comm, data.prev_tid, prev_pid, data.prev_prio)
                if prev_thread in last_seen_state:
                    # For running and runnable, both set wakeup state.
                    busy_sched_slice = SchedSlice(prev_thread, last_seen_state[prev_thread],
                               Slice(last_seen_timestamp[cpu][prev_thread], event.ts))
                else:
                    # Consider prev_thread as a new thread.
                    busy_sched_slice = SchedSlice(prev_thread, None, Slice(0, event.ts_int))

                self._sched_slices[cpu].append(busy_sched_slice)
                self._thread_slice[prev_thread].append(busy_sched_slice)

                if data.prev_state == 'R':
                    prev_thread_state = ThreadState(
                        SchedState.TASK_RUNNABLE, 0, None,data.next_comm,
                        data.next_tid, event.cpu)
                    last_seen_state[prev_thread] = prev_thread_state
                elif data.prev_state == 'R+':
                    prev_thread_state = ThreadState(
                        SchedState.TASK_PREEMPTED, 0, None, data.next_comm,
                        data.next_tid, event.cpu)
                    last_seen_state[prev_thread] = prev_thread_state
                elif data.prev_state == 'I':
                    # TBD
                    pass

                next_pid = self.find_thread_pid(data.next_comm, data.next_tid)
                next_thread = ThreadInfo(data.next_comm, data.next_tid, next_pid, data.next_prio)

                # Find the earliest seen timestamp for next thread.
                # The magic number need to remove later.
                earliest_seen_timestamp = 0
                for _cpu in range(6):
                    if next_thread in last_seen_timestamp[_cpu]:
                        if earliest_seen_timestamp == 0:
                            earliest_seen_timestamp = last_seen_timestamp[_cpu]

                        if earliest_seen_timestamp > last_seen_timestamp[_cpu]:
                            earliest_seen_timestamp = last_seen_timestamp[_cpu]

                # last_seen_state should be updated due to waker.
                wait_sched_slice = SchedSlice(
                    next_thread, last_seen_state[next_thread],
                    Slice(earliest_seen_timestamp, event.ts_int))

                # RUNNABLE / PREEMPTED => RUNNING
                self._thread_slices[next_thread].append(wait_sched_slice)