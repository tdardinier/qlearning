import numpy as np
from pygame.locals import *
import pygame
import random as rd
from snake_env import Render, Map
from IA import IA_rl, IA_random, IA_minimax, IA_keyboard
import time

n_agents = 3
n_candies = 10
gridsize = 30

IA = []
print("Loading trained snake, it can take up to two minutes...")
q = np.loadtxt("snake.csv")
IA.append(IA_rl.IA(0, q))
#IA.append(IA_minimax.IA(0))
IA.append(IA_minimax.IA(1))
IA.append(IA_keyboard.IA(2))

M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
e = Render(M, spacing=20)
q = None

while True:

    while True:

        e.render()

        if not (2 in M.activeAgents):
            break

        for i in range(n_agents):
            M.agents[i].nextAction(IA[i].act(M))

        r, done = M.step()

        time.sleep(0.05)


    M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)
