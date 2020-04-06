#!/usr/bin/env python

import random
import signal
import time
from clibt.tui import TuiManager
from clibt.utils import (get_random_digits, parse_args_from_func, tick, tock,
                         wait_period)


class SeqDig(object):
    def __init__(self, bpm: int = 150, duration: int = 30, base: int = 2,
                 rows: int = 2, cols: int = 4):
        self.__dict__.update(locals())
        self.ui = TuiManager()
        self.lines = []
        self.ui.add_draw_callback(self.draw)
        self.want_quit = False
        signal.signal(signal.SIGINT, self.signal_handle)

    def signal_handle(self, frame, sig):
        self.want_quit = True

    def draw(self):
        self.ui.clear()
        self.ui.add_str_center(self.lines)

    def run(self):
        period_ms = 60000.0 / self.bpm
        duration_ms = self.duration * 1000
        tick()

        while tock() < duration_ms and not self.want_quit:
            wait_period(period_ms)
            self.lines = [get_random_digits(self.cols, self.base)
                          for _ in range(self.rows)]
            self.ui.process_events()
            self.draw()

        self.ui.quit()


def main():
    parameters = parse_args_from_func(SeqDig.__init__)
    ex = SeqDig(**parameters)
    ex.run()


if __name__ == "__main__":
    main()
