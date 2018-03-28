import numpy as np
from pygame.locals import *
import pygame
import random as rd
from snake_env import Render, Map
from IA import IA_rl, IA_random, IA_minimax

n_agents = 2
n_candies = 10
gridsize = 30

IA = [IA_rl.IA(i) for i in range(n_agents)]

M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
e = Render(M, spacing=20)
q = None

while True:

    while True:

        e.render()

        if len(M.activeAgents) < n_agents:
            for i in range(n_agents):
                if not (i in M.activeAgents):
                    IA[i].dead()
            break

        for i in range(n_agents):
            M.agents[i].nextAction(IA[i].act(M))

        r, done = M.step()

    q = IA[0].q / n_agents

    for i in range(1, n_agents):
        q += IA[i].q / n_agents
    for i in range(n_agents):
        IA[i] = IA_rl.IA(i, q)

    M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)
