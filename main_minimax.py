import numpy as np
from pygame.locals import *
import pygame
import random as rd
from tree_strategy import minimax 

from snake_env import Render, Map
import time

import IA_keyboard, IA_random, IA_rl

nagents = 1
IA = [IA_random.IA(i) for i in range(nagents)]
#IA[1] = IA_keyboard.IA(1)
IA[0] = IA_rl.IA(0)
n_candies = 50

step = 0

M = Map(nagents=nagents, ncandies=n_candies, gridsize=40)
e = Render(M, spacing=20)

for i in range(10):
    e.render()
    print(minimax(0,0, M, 2))
    print(M.agents[0])
    time.sleep(1)
    e.render()

print(M.agents[0])
M.update(0, 0)
print(M.agents[0])
M.revertLastUpdate()
print(M.agents[0])
