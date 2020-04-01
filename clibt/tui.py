#!/usr/bin/env python

import curses
import locale
import time
from clibt.utils import chunk_string, wait_period
locale.setlocale(locale.LC_ALL, "")


class UiManager:
    def __init__(self):
        self.win = curses.initscr()
#        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.win.nodelay(1)
        self.line = 0
        self.win.clear()
        self.on_resize()
        self.key_callbacks = []
        self.draw_callbacks = []

    def on_resize(self):
        self.ymax, self.xmax = self.win.getmaxyx()

    def add_key_callback(self, callback):
        self.key_callbacks.append(callback)

    def add_draw_callback(self, callback):
        self.draw_callbacks.append(callback)

    def notify_key(self, key):
        for callback in self.key_callbacks:
            callback(key)

    def notify_draw(self):
        for callback in self.draw_callbacks:
            callback()

    def add_str(self, string, y=None, x=0):
        if y is None:
            y = self.line
        else:
            self.line = y

        if isinstance(string, list):
            for part in string:
                self.add_str(part, y=None, x=x)
            return

        for i, chunk in enumerate(chunk_string(string, self.xmax - x)):
            self.win.addstr(y + i, x, chunk.encode())
            self.line += 1

        self.win.refresh()

    def process_events(self):
        c = self.win.getch()
        if c != -1:
            self.notify_key(c)
        if c == curses.KEY_RESIZE:
            self.on_resize()
            self.notify_draw()

    def add_str_center(self, string, y=0, x=0):
        mod_y = y
        if isinstance(string, list):
            mod_y -= len(string) // 2
        self.add_str(string,
                     self.ymax // 2 + mod_y,
                     self.xmax // 2 - len(string) // 2 + x)

    def clear(self):
        self.win.clear()

    def get_str(self, y=None, x=0):
        if y is None:
            y = self.line
        else:
            self.line = y
        curses.echo()
        curses.nocbreak()
        self.win.nodelay(0)
        res = self.win.getstr(y, x)
        self.line += 1
        self.win.nodelay(1)
        curses.noecho()
        curses.cbreak()
        return res

    def quit(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
