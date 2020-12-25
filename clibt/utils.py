#!/usr/bin/env python
import argparse
import heapq
import inspect
import random
import time

_last_times = [0]*100
_next_events = []


def parse_args_from_func(func):
    parser = argparse.ArgumentParser()
    sig = inspect.signature(func)
    for name, parameter in sig.parameters.items():
        if name == 'self':
            continue
        default = parameter.default if parameter.default != inspect._empty \
            else None
        _type = parameter.annotation \
            if parameter.annotation != inspect._empty else None
        parser.add_argument(f'--{name}', type=_type, default=default,
                            required=default is None)
    return vars(parser.parse_args())


def chunk_string(string, width):
    for i in range(0, len(string), width):
        yield string[i:i+width]


def get_random_digits(n=2, base=10):
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C",
              "D", "E", "F"]
    res = (digits[random.randint(0, base-1)] for _ in range(n))
    return "".join(res)


def _time_ms():
    return int(time.monotonic() * 1000)


def wait_period(ms, key=1):
    current_time = _time_ms()
    target_time = _last_times[key] + ms
    diff_ms = target_time - current_time
    if diff_ms > 0:
        time.sleep(diff_ms / 1000.0)
    _last_times[key] = current_time


def tick(key=0):
    _last_times[key] = _time_ms()


def tock(key=0):
    return _time_ms() - _last_times[key]


def add_periodic_task(period, callback):
    next_time = _time_ms() + period
    heapq.heappush(_next_events, (next_time, callback, period))


def process_periodic_tasks(force=False):
    current_time = _time_ms()
    try:
        task_time, task_cb, task_period = \
            heapq.heappop(_next_events)
        if task_time <= current_time or force:
            task_cb()
            task_time = current_time + task_period
        heapq.heappush(_next_events, (task_time, task_cb, task_period))
    except IndexError:
        pass


def clear_periodic_tasks():
    global _next_events
    _next_events = []
