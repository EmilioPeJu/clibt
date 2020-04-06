#!/usr/bin/env python
import pygame as pg
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
FONT_SIZE = 24
FONT_COLOR = (0, 255, 100)
FPS = 20


class GuiManager(object):
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self.key_callbacks = []
        self.draw_callbacks = []
        self._img_cache = {}
        self._sound_cache = {}
        self.font = pg.font.SysFont(None, FONT_SIZE)
        self.clock = pg.time.Clock()

    def add_key_callback(self, callback):
        self.key_callbacks.append(callback)

    def add_draw_callback(self, callback):
        self.draw_callbacks.append(callback)

    def draw_image(self, img_path, adjust_window=True):
        surf = self._img_cache.get(img_path)
        if not surf:
            surf = pg.image.load(img_path)
            surf.convert()
            self._img_cache[img_path] = surf

        rect = surf.get_rect()
        if adjust_window:
            self.screen = pg.display.set_mode(rect.size, pg.RESIZABLE)
        self.screen.blit(surf, rect)
        pg.display.update()

    def play_sound(self, sound_path):
        sound = self._sound_cache.get(sound_path)
        if not sound:
            sound = pg.mixer.Sound(sound_path)
            self._sound_cache[sound_path] = sound
        sound.play()

    def draw_text(self, text):
        surf = self.font.render(text, True, FONT_COLOR)
        rect = surf.get_rect()
        self.screen.blit(surf, rect)
        pg.display.update()

    def notify_key(self, key):
        for callback in self.key_callbacks:
            callback(key)

    def notify_draw(self):
        for callback in self.draw_callbacks:
            callback()

    def fill_background(self):
        self.screen.fill(BACKGROUND_COLOR)

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.notify_key(chr(event.key))

    def tick(self):
        self.clock.tick(FPS)

    def quit(self):
        pg.quit()
