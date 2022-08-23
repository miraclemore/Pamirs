# !/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict

from pamirs.trace_processor.common.slice import Slice
from pamirs.trace_processor.cpu.sched_slice import SchedSlice, WakeeInfo
from pamirs.trace_processor.cpu.sched_state import SchedState
from pamirs.trace_processor.cpu.thread_info import ThreadInfo
from pamirs.trace_processor.cpu.thread_state import ThreadState


class CPU:
    def __init__(self, tp):
        self._tp = tp
        self._events = tp.events_list

        self._sched_events = list()
        self._sched_slices = defaultdict(list)
        self._thread_slices = defaultdict(list)

        self._filter_sched_events()
        self._parse_sched_events()

    def __repr__(self):
        pass

    def _filter_sched_events(self):
        for event in self._events:
            if event.tracepoint == "sched_switch" \
                    or event.tracepoint == "sched_waking" \
                    or event.tracepoint == "sched_wakeup":
                self._sched_events.append(event)

    def find_thread_pid(self, name, tid):
        if name or tid is None:
            return None

        id = name + "-" + str(tid)
        if id in self._tp.pids_map:
            return self._tp.pids_map[id]
        else:
            return None

    def _parse_sched_events(self):
        last_seen_state = defaultdict(int)
        last_seen_wakee = defaultdict(lambda: None)
        last_seen_timestamp = defaultdict(lambda: defaultdict(int))

        for event in self._events:
            if event.tracepoint == "sched_wakeup":
                data = event.data
                target_cpu = data.target_cpu
                waker_pid = self.find_thread_pid(data.comm, data.tid)
                waker_thread = ThreadInfo(data.comm, data.tid, waker_pid, data.prio)

                last_seen_state[waker_thread] = SchedState.TASK_WAKEUP
                last_seen_timestamp[target_cpu][waker_thread] = event.ts

                wakee = WakeeInfo(event.name, event.tid, event.pid)
                last_seen_wakee[waker_thread] = wakee

            elif event.tracepoint == "sched_switch":
                data = event.data
                cpu = event.cpu
                prev_pid = self.find_thread_pid(data.prev_comm, data.prev_tid)
                prev_thread = ThreadInfo(data.prev_comm, data.prev_tid, prev_pid, data.prev_prio)

                # For running and runnable, both set wakeup state.
                start = last_seen_timestamp[cpu][prev_thread]
                end = event.ts
                busy_sched_slice = SchedSlice(prev_thread, cpu, Slice(start, end), SchedState.TASK_RUNNING,
                                              last_seen_wakee[prev_thread])

                self._sched_slices[cpu].append(busy_sched_slice)
                self._thread_slices[prev_thread].append(busy_sched_slice)

                last_seen_timestamp[cpu][prev_thread] = event.ts

                if data.prev_state == 'R':
                    last_seen_state[prev_thread] = SchedState.TASK_RUNNABLE
                elif data.prev_state == 'R+':
                    last_seen_state[prev_thread] = SchedState.TASK_PREEMPTED
                elif data.prev_state == 'I':
                    # TBD
                    pass

                next_pid = self.find_thread_pid(data.next_comm, data.next_tid)
                next_thread = ThreadInfo(data.next_comm, data.next_tid, next_pid, data.next_prio)

                if last_seen_state[next_thread] == SchedState.TASK_PREEMPTED \
                        or last_seen_state[next_thread] == SchedState.TASK_RUNNABLE:
                    wakee = WakeeInfo(event.name, event.tid, event.pid)
                elif last_seen_state[next_thread] == SchedState.TASK_WAKEUP:
                    wakee = last_seen_wakee[next_thread]

                start = last_seen_timestamp[cpu][next_thread]
                end = event.ts
                wait_sched_slice = SchedSlice(next_thread, cpu, Slice(start, end),
                                              SchedState.TASK_RUNNABLE, wakee)

                # RUNNABLE / PREEMPTED => RUNNING
                self._thread_slices[next_thread].append(wait_sched_slice)

                last_seen_timestamp[cpu][next_thread] = event.ts
                last_seen_state[next_thread] = SchedState.TASK_RUNNING
                last_seen_wakee[next_thread] = wakee
