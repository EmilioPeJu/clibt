#!/usr/bin/env python

import random
import signal
import time
from clibt.tui import TuiManager
from clibt.utils import (get_random_digits, parse_args_from_func, tick, tock,
                         wait_period)


class SeqWords(object):
    def __init__(self, path: str, wps: int = 350, width: int = 15,
            nlines: int = 1):
        self.path = path
        self.wps = wps
        self.width = width
        self.nlines = nlines
        self.ui = TuiManager()
        self.lines = []
        self.ui.add_draw_callback(self.draw)
        self.ui.add_key_callback(self.on_key)
        self.want_quit = False
        signal.signal(signal.SIGINT, self.signal_handle)

    def signal_handle(self, frame, sig):
        self.want_quit = True

    def draw(self):
        self.ui.clear()
        self.ui.add_str_center(self.lines)

    def on_key(self, c):
        pass

    def run(self):
        tick()
        while not self.want_quit:
            self.ui.process_events()
            self.draw()

        self.ui.quit()
        print(tock())


def main():
    parameters = parse_args_from_func(SeqWords.__init__)
    ex = SeqWords(**parameters)
    ex.run()


if __name__ == "__main__":
    main()
