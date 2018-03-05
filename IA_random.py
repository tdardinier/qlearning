import numpy as np
from pygame.locals import *
import pygame
import random as rd

from snake_env import Render, Map
import time

class IA():

    def __init__(self):
        self.name = "IA random"
        self.step = 0

    def __str__(self):
        return self.name

    def act(self, state, reward, dead):
        return rd.randint(0, 3)
