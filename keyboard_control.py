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

    while True:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        if np.any(keys[49:58]):
            index = keys[49:58].index(1)
            if index > nagents:
                index = 0
        


        if (keys[K_RIGHT]):
            M.agents[index].nextAction(0)
            break  

        if (keys[K_LEFT]):
            M.agents[index].nextAction(2)
            break  

        if (keys[K_UP]):
            M.agents[index].nextAction(1)
            break  

        if (keys[K_DOWN]):
            M.agents[index].nextAction(3)
            break  
    
   
    step+=1

    r, done = M.step()
    
    time.sleep(0.05)

#    if done:
#        e.reset()

