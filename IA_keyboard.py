import numpy as np
from pygame.locals import *
import pygame
import random as rd

from snake_env import Render, Map
import time

class IA():

    def __init__(self):
        self.name = "IA_keyboard"
        self.step = 0

    def __str__(self):
        return self.name

    def act(self, state, reward, dead):
        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_RIGHT]):
                return 0
            if (keys[K_UP]):
                return 1
            if (keys[K_LEFT]):
                return 2
            if (keys[K_DOWN]):
                return 3
