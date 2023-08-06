# -*- coding: utf-8 -*-

"""Pibooth plugin for sound effects"""

import os
import os.path as osp
import shutil
import pygame
import pibooth


__version__ = "0.0.1"


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('SOUNDS', 'sounds_path', "~/.config/pibooth/sounds",
                   "Path to the sounds")

@pibooth.hookimpl
def pibooth_reset(cfg, hard):
    """Populate sounds folder if it doesn't exists"""
    sound_path = cfg.getpath('SOUNDS', 'sounds_path')
    if not osp.isdir(sound_path) or hard:
        source_sound_path = osp.join(osp.dirname(osp.abspath(__file__)), 'sounds')
        shutil.copytree(source_sound_path, sound_path)

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    """Init the pygame mixer and load available sounds"""
    pygame.mixer.pre_init(channels=2, buffer=1024)
    pygame.mixer.init()
    app.sounds = {}
    notefile_list = os.listdir(cfg.getpath('SOUNDS', 'sounds_path'))
    for sound in notefile_list:
        if sound.endswith(".wav"):
            app.sounds[sound[:-4]] = pygame.mixer.Sound(os.path.join(cfg.getpath('SOUNDS', 'sounds_path'), sound))

@pibooth.hookimpl
def state_chosen_enter(app):
    """Start a new capture sequence."""
    app.sounds["button"].play()

@pibooth.hookimpl
def state_choose_enter(app):
    """Start a new capture sequence."""
    app.sounds["button"].play()

@pibooth.hookimpl
def state_capture_enter(app):
    """Capture state"""
    app.sounds['shutter'].play()

@pibooth.hookimpl
def state_preview_enter(app):
    """Preview state"""
    app.sounds['3beeps'].play()

@pibooth.hookimpl
def state_finish_enter(app):
    """finished state"""
    app.sounds['applause'].play()

@pibooth.hookimpl
def pibooth_cleanup():
    """Quit the mixer
    """
    pygame.mixer.quit()
