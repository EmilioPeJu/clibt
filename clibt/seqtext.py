#!/usr/bin/env python

import random
import signal
import time

from itertools import batched

from clibt.tui import TuiManager
from clibt.utils import (get_random_digits, parse_args_from_func, tick, wait_period)


class SeqText(object):
    def __init__(self, bpm: int = 150, words_per_beat: int = 4,
                 text_path: str = '',):
        self.bpm = bpm
        self.words_per_beat = words_per_beat
        with open(text_path, 'r') as fhandle:
            self.text = fhandle.read()
        self.words = self.text.split()
        self.ui = TuiManager()
        self.line = ''
        self.ui.add_draw_callback(self.draw)
        self.key = None
        self.ui.add_key_callback(self.on_key)
        self.want_quit = False

    def on_key(self, c):
        if c == ord('q'):
            self.want_quit = True
        elif c == ord('+'):
            self.bpm += 5
        elif c == ord('-'):
            self.bpm = max(1, self.bpm - 5)

    def draw(self):
        self.ui.clear()
        self.ui.add_str_center(self.line)

    def run(self):
        wait_period(0)
        for words in batched(self.words, self.words_per_beat):
            self.line = ' '.join(words)
            self.ui.process_events()
            self.draw()
            if self.want_quit:
                break

            wait_period(60000.0 / self.bpm)

        self.ui.quit()


def main():
    parameters = parse_args_from_func(SeqText.__init__)
    ex = SeqText(**parameters)
    ex.run()


if __name__ == "__main__":
    main()
