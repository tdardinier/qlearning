import numpy as np
from pygame.locals import *
import pygame

from snake_env import SnakeEnv
import time

num_agents = 3
e = SnakeEnv(num_agents=num_agents, ncandies=3)
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
            if index > num_agents:
                index = 0

        if (keys[K_RIGHT]):
            e.agents[index].nextAction(0)
            break

        if (keys[K_LEFT]):
            e.agents[index].nextAction(2)
            break

        if (keys[K_UP]):
            e.agents[index].nextAction(1)
            break

        if (keys[K_DOWN]):
            e.agents[index].nextAction(3)
            break
    step+=1

    obs, r, done, _ = e.step()
    time.sleep(0.05)

#    if done:
#        e.reset()
time.sleep(50.0 / 1000.0)
