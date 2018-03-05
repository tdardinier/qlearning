import numpy as np
from pygame.locals import *
import pygame
import random as rd

from snake_env import Render, Map
import time

import IA_keyboard, IA_random, IA_rl

nagents = 1
IA = [IA_random.IA(i) for i in range(nagents)]
#IA[1] = IA_keyboard.IA(1)
IA[0] = IA_rl.IA(0)

n_candies = 5
gridsize = 20

step = 0

M = Map(nagents=nagents, ncandies=n_candies, gridsize=gridsize)
e = Render(M, spacing=20)

reward = 0
step_by_step = False

def press():
    pygame.event.pump()
    return pygame.key.get_pressed()

while True:

    while True:

        if step_by_step:
            while True:
                keys = press()
                if keys[K_RIGHT]:
                    time.sleep(0.1)
                    break
                if keys[K_UP]:
                    step_by_step = False
                    break
        index = 0
        print(step)
        e.render()

        if len(M.activeAgents) == 0:
            q = IA[0].dead()
            break

        for i in range(nagents):
            reward = 0

            if M.agents[i].has_eaten:
                reward = 1

            agent = IA[i]
            a = agent.act(M, reward)
            print("ACTION ", a)
            M.agents[i].nextAction(a)
        keys = press()
        if keys[K_DOWN]:
            step_by_step = True

        step += 1
        r, done = M.step()
        #time.sleep(0.001)

    M = Map(nagents=nagents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)
    IA[0] = IA_rl.IA(0, q)
