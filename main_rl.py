import numpy as np
from pygame.locals import *
import pygame
import random as rd

from snake_env import Render, Map
import time

import IA_keyboard, IA_random, IA_rl

nagents = 1
M = Map(nagents=nagents, ncandies=3, gridsize=40)
e = Render(M, spacing=20)

IA = [IA_random.IA(i) for i in range(nagents)]
#IA[1] = IA_keyboard.IA(1)
IA[0] = IA_rl.IA(0)

step = 0

while True:
    index = 0
    print(step)
    e.render()

    for i in range(nagents):
        agent = IA[i]
        M.agents[i].nextAction(agent.act(M, 0))

    step+=1
    r, done = M.step()
    time.sleep(0.05)
