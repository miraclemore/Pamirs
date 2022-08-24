# !/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import defaultdict

from pamirs.trace_processor.common.slice import Slice
from pamirs.trace_processor.cpu.freq_slice import FreqSlice
from pamirs.trace_processor.cpu.idle_slice import IdleSlice
from pamirs.trace_processor.cpu.sched_slice import SchedSlice, WakerInfo
from pamirs.trace_processor.cpu.sched_state import SchedState
from pamirs.trace_processor.cpu.thread_info import ThreadInfo


class CPU:
    def __init__(self, tp):
        self._tp = tp
        self._events = tp.events_list

        self._sched_events = list()
        self._sched_slices = defaultdict(list)
        self._thread_slices = defaultdict(list)

        self._freq_idle_events = defaultdict(list)
        # self._idle_events = list()
        self._idle_slices = defaultdict(list)
        # self._freq_events = list()
        self._freq_slices = defaultdict(list)

        self._filter_events()
        self._parse_sched_events()
        self._parse_freq_idle_events()

    def __repr__(self):
        pass

    def _filter_events(self):
        for event in self._events:
            if event.tracepoint == "sched_switch" \
                    or event.tracepoint == "sched_waking" \
                    or event.tracepoint == "sched_wakeup":
                self._sched_events.append(event)
            elif event.tracepoint == "cpu_idle":
                self._freq_idle_events[event.cpu].append(event)
            elif event.tracepoint == "cpu_frequency":
                # Due to freq updated by policy group, update the event cpu for each event list
                event.cpu = event.data.cpu_id
                self._freq_idle_events[event.cpu].append(event)

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
        last_seen_waker = defaultdict(lambda: None)
        last_seen_timestamp = defaultdict(lambda: defaultdict(int))

        for event in self._sched_events:
            if event.tracepoint == "sched_wakeup":
                data = event.data
                target_cpu = data.target_cpu
                wakee_pid = self.find_thread_pid(data.comm, data.tid)
                wakee_thread = ThreadInfo(data.comm, data.tid, wakee_pid, data.prio)

                last_seen_state[wakee_thread] = SchedState.TASK_WAKEUP
                last_seen_timestamp[target_cpu][wakee_thread] = event.ts

                waker = WakerInfo(event.name, event.tid, event.pid)
                last_seen_waker[wakee_thread] = waker

            elif event.tracepoint == "sched_switch":
                data = event.data
                cpu = event.cpu
                prev_pid = self.find_thread_pid(data.prev_comm, data.prev_tid)
                prev_thread = ThreadInfo(data.prev_comm, data.prev_tid, prev_pid, data.prev_prio)

                # For running and runnable, both set wakeup state.
                start = last_seen_timestamp[cpu][prev_thread]
                end = event.ts
                busy_sched_slice = SchedSlice(prev_thread, cpu, Slice(start, end), SchedState.TASK_RUNNING,
                                              last_seen_waker[prev_thread])

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
                    waker = WakerInfo(event.name, event.tid, event.pid)
                elif last_seen_state[next_thread] == SchedState.TASK_WAKEUP:
                    waker = last_seen_waker[next_thread]

                start = last_seen_timestamp[cpu][next_thread]
                end = event.ts

                wait_sched_slice = SchedSlice(next_thread, cpu, Slice(start, end),
                                              last_seen_state[next_thread], waker)

                # RUNNABLE / PREEMPTED => RUNNING
                self._thread_slices[next_thread].append(wait_sched_slice)

                last_seen_timestamp[cpu][next_thread] = event.ts
                last_seen_state[next_thread] = SchedState.TASK_RUNNING
                # last_seen_waker[next_thread] = waker

    def _parse_freq_idle_events(self):
        for cpu, events in self._freq_idle_events.items():
            last_idle_event = None
            last_freq_event = None

            for event in events:
                if event.tracepoint == "cpu_frequency":
                    if last_freq_event:
                        freq_slice = None
                        if idle == 0:
                            freq_slice = FreqSlice(cpu, last_freq_event.data.state,
                                                   Slice(max(last_freq_event.ts, last_idle_event.ts), event.ts))
                        else:
                            # idle --- freq --- idle
                            if last_freq_event.ts < last_idle_event.ts:
                                freq_slice = FreqSlice(cpu, last_freq_event.data.state,
                                                       Slice(last_freq_event.ts, last_idle_event.ts))

                        if freq_slice:
                            self._freq_slices[event.cpu].append(freq_slice)

                    last_freq_event = event

                elif event.tracepoint == "cpu_idle":
                    if event.data.state != 4294967295:
                        idle = 1
                        if last_idle_event and last_freq_event:
                            freq_slice = FreqSlice(cpu, last_freq_event.data.state,
                                                   Slice(last_freq_event.ts, event.ts))
                            self._freq_slices[event.cpu].append(freq_slice)

                    if last_idle_event and last_idle_event.data.state != 4294967295 \
                            and event.data.state == 4294967295:
                        idle_slice = IdleSlice(cpu, last_idle_event.data.state, Slice(last_idle_event.ts, event.ts))
                        self._idle_slices[cpu].append(idle_slice)

                    last_idle_event = event

                    if event.data.state == 4294967295:
                        idle = 0
                        if last_freq_event:
                            last_freq_event.ts = event.ts
