#!/usr/bin/env python

import pygame.mixer
from time import sleep

pygame.mixer.init(48000, -16, 1, 1024)
sound = pygame.mixer.Sound("music.wav")
channelA = pygame.mixer.Channel(1)
channelA.play(sound)
sleep(2.0)