import numpy as np
from pygame.locals import *
import pygame
import random as rd

from snake_env import Render, Map
import time



nagents = 3
M = Map(nagents=nagents, ncandies=3, gridsize=40)
e = Render(M, spacing=20)


step = 0
while True:
    index = 0
    print(step)
    e.render()
    
    next_move=rd.randint(0,3)
    print(next_move)
    M.agents[index].nextAction(next_move)
   
    step+=1

    r, done = M.step()
    
    time.sleep(0.5)

#    if done:
#        e.reset()

