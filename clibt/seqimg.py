#!/usr/bin/env python

import os
import random
import signal
import time
from clibt.gui import GuiManager
from clibt.utils import (get_random_digits, parse_args_from_func, tick, tock,
                         wait_period, add_periodic_task, clear_periodic_tasks,
                         process_periodic_tasks)


class Cards(object):
    def __init__(self, path):
        self.path = path
        self.words = {}
        self.texts = {}
        self.imgs = {}
        self.snds = {}
        self.keys = set()
        self.populate_data()

    @staticmethod
    def is_image(path):
        return path.endswith('.png') or path.endswith('.jpg')

    @staticmethod
    def is_sound(path):
        return path.endswith('.wav')

    @staticmethod
    def is_text(path):
        return path.endswith('.txt')

    @staticmethod
    def get_key(name):
        return name.split()[0]

    @staticmethod
    def get_subkey(name):
        try:
            return name.split()[1]
        except IndexError:
            return 0

    def populate_data(self):
        for name in os.listdir(self.path):
            short_name = os.path.basename(os.path.splitext(name)[0])
            key = self.get_key(short_name)
            face_key = self.get_subkey(short_name)
            full_path = os.path.join(self.path, name)
            if self.is_image(full_path):
                self.imgs.setdefault(key, {})[face_key] = full_path
            elif self.is_sound(full_path):
                self.snds.setdefault(key, {})[face_key] = full_path
            elif self.is_text(full_path):
                with open(full_path, 'r') as fhandle:
                    self.texts.setdefault(key, {})[face_key] = fhandle.read()
            else:
                continue
            self.words.setdefault(key, {})[face_key] = short_name
            self.keys.add(key)

    def get_random_card(self):
        key = random.choice(list(self.keys))
        face_keys = tuple(sorted(self.words[key].keys()))
        return (key, face_keys)

    def get_face(self, key, face_key):
        return (self.words.get(key, {}).get(face_key),
                self.texts.get(key, {}).get(face_key, ""),
                self.imgs.get(key, {}).get(face_key),
                self.snds.get(key, {}).get(face_key))


class SeqImg(object):
    def __init__(self, path: str, bpm: int = 30, duration: int = 10):
        self.__dict__.update(locals())
        self.cards = Cards(path)
        self.ui = GuiManager()
        self.ui.add_key_callback(self.on_key_press)
        self.want_quit = False
        signal.signal(signal.SIGINT, self.signal_handle)

    def on_key_press(self, c):
        if c == '\r':
            process_periodic_tasks(True)
        elif c == 'n':
            self.next_face()
            self.draw()
        elif c == '\x1b':
            self.want_quit = True

    def signal_handle(self, frame, sig):
        self.want_quit = True

    def draw(self):
        if self.img:
            self.ui.draw_image(self.img)
        else:
            self.ui.setup_default_screen_size()
        if self.snd:
            self.ui.play_sound(self.snd)
        self.ui.draw_text(self.name)
        if self.text:
            self.ui.draw_text(self.text, center=True)

    def next_card(self):
        self.card_face_index = 0
        self.card_key, self.card_face_keys = self.cards.get_random_card()
        self.card_face = self.card_face_keys[self.card_face_index]
        (self.name, self.text, self.img, self.snd) = self.cards.get_face(
            self.card_key, self.card_face)

    def next_face(self):
        # this assumes that next_card was called
        self.card_face_index = (self.card_face_index + 1) % \
            len(self.card_face_keys)
        self.card_face = self.card_face_keys[self.card_face_index]
        (self.name, self.text, self.img, self.snd) = self.cards.get_face(
            self.card_key, self.card_face)

    def run(self):
        period_ms = 60000.0 / self.bpm
        duration_ms = self.duration * 1000
        self.next_card()
        add_periodic_task(period_ms, self.next_card)
        tick()

        while tock() < duration_ms and not self.want_quit:
            self.ui.fill_background()
            process_periodic_tasks()
            self.ui.process_events()
            self.draw()
            self.ui.tick()

        clear_periodic_tasks()
        self.ui.quit()


def main():
    parameters = parse_args_from_func(SeqImg.__init__)
    ex = SeqImg(**parameters)
    ex.run()


if __name__ == "__main__":
    main()
