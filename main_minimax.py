import numpy as np
from pygame.locals import *
import pygame
import random as rd
from tree_strategy import minimax 

from snake_env import Render, Map
import time

import IA_keyboard, IA_random, IA_rl

nagents = 2
IA = [IA_random.IA(i) for i in range(nagents)]
n_candies = 50

step = 0

M = Map(nagents=nagents, ncandies=n_candies, gridsize=40)
e = Render(M, spacing=20)

while True:
    e.render()
    r=minimax(0,0,M,2)
    M.agents[0].next_action=r[1]
    M.agents[1].next_action=IA[1].act(M,0)
    v=M.step()
    time.sleep(0.05)
    

