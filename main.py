import numpy as np
from pygame.locals import *
import pygame
import random as rd

from snake_env import Render, Map
import time

import IA_keyboard
import IA_random

nagents = 3
M = Map(nagents=nagents, ncandies=3, gridsize=40)
e = Render(M, spacing=20)

IA = [IA_random.IA() for _ in range(nagents)]
IA[0] = IA_keyboard.IA()

step = 0

while True:
    index = 0
    print(step)
    e.render()

    for i in range(nagents):
        agent = IA[i]
        M.agents[i].nextAction(agent.act(0, 0, 0))

    step+=1
    r, done = M.step()
    time.sleep(0.05)
