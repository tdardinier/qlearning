import numpy as np
from pygame.locals import *
import pygame

from snake_env import Render, Map
import time

<<<<<<< HEAD

nagents = 3
M = Map(nagents=nagents, ncandies=3, gridsize=40)
e = Render(M, spacing=20)
=======
num_agents = 3
e = SnakeEnv(num_agents=num_agents, ncandies=3)
>>>>>>> 6757b2075352a545d00219c699941817ce899521
e.render()

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

#    if done:
#        e.reset()
time.sleep(0.05)
