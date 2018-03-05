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
n_candies = 50

step = 0

M = Map(nagents=nagents, ncandies=n_candies, gridsize=40)
e = Render(M, spacing=20)

reward = 0

while True:

    while True:
        index = 0
        print(step)
        e.render()

        for i in range(nagents):
            reward = 0

            if M.agents[i].has_eaten:
                reward = 2
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")
                print("WOAOFRJFHDCBUDRHFLGHVRDKFDFHXGKJFHCK")

            agent = IA[i]
            M.agents[i].nextAction(agent.act(M, reward))

        if len(M.activeAgents) == 0:
            q = IA[0].dead()
            break


        step += 1
        r, done = M.step()
        #time.sleep(0.001)

    M = Map(nagents=nagents, ncandies=n_candies, gridsize=40)
    e = Render(M, spacing=20)
    IA[0] = IA_rl.IA(0, q)
