#!/usr/bin/env python

import random
import signal
import time
from clibt.tui import TuiManager
from clibt.utils import (get_random_digits, parse_args_from_func, tick, tock,
                         wait_period)


class SeqList(object):
    def __init__(self, path: str, bpm: int = 150, duration: int = 30):
        self.__dict__.update(locals())
        self.entries = self.load_entries(self.path)
        self.current = None
        self.ui = TuiManager()
        self.lines = []
        self.ui.add_draw_callback(self.draw)
        self.ui.add_key_callback(self.on_key)
        self.key = None
        self.ui.set_half_delay(int(600.0 / self.bpm))
        self.want_quit = False
        signal.signal(signal.SIGINT, self.signal_handle)

    def load_entries(self, path):
        result = []
        for line in open(path, 'r'):
            if line.startswith("#") or not line.strip():
                continue
            result.append(line.split(' ', 1))
        return result

    def signal_handle(self, frame, sig):
        self.want_quit = True

    def draw(self):
        self.ui.clear()
        self.ui.add_str_center(self.lines)

    def on_key(self, c):
        self.key = c

    def next_item(self):
        self.current = random.sample(self.entries, 1)[0]
        self.lines = [self.current[0]]

    def show_full_item(self):
        if self.current:
            self.lines = self.current

    def run(self):
        duration_ms = self.duration * 1000
        tick()
        while tock() < duration_ms and not self.want_quit:
            self.ui.process_events()
            if self.key == ord(' '):
                self.show_full_item()
            else:
                self.next_item()
            self.draw()
        self.ui.quit()


def main():
    parameters = parse_args_from_func(SeqList.__init__)
    ex = SeqList(**parameters)
    ex.run()


if __name__ == "__main__":
    main()
