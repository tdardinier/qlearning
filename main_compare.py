import numpy as np
from pygame.locals import *
import pygame
import random as rd
from snake_env import Render, Map
from IA import IA_rl, IA_random, IA_minimax

n_agents = 2
n_candies = 10
gridsize = 30
n_total_iter = 1000
max_iter_match = 1000


q = np.loadtxt("current_snake.csv")
adv_0 = IA_rl.IA(0, q)
#adv_0 = IA_minimax.IA(0)
adv_1 = IA_minimax.IA(1)
#adv_1 = IA_random.IA(1)

avg_size_0 = []
n_victory_0 = 0
avg_size_1 = []
n_victory_1 = 0

for match in range(1, n_total_iter + 1):

    M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)

    adv_0 = IA_rl.IA(0, adv_0.q)

    for step in range(max_iter_match):

        e.render()

        if len(M.activeAgents) < n_agents:
            break

        M.agents[0].nextAction(adv_0.act(M))
        M.agents[1].nextAction(adv_1.act(M))

        r, done = M.step()

    if len(M.activeAgents) < n_agents:
        if 0 in M.activeAgents:
            n_victory_0 += 1
        elif 1 in M.activeAgents:
            n_victory_1 += 1
    else:
        s0 = len(M.agents[0].pos)
        s1 = len(M.agents[1].pos)
        avg_size_0.append(s0 / (s0 + s1))
        avg_size_1.append(s1 / (s0 + s1))
    print(match, n_victory_0, np.average(avg_size_0), n_victory_1, np.average(avg_size_1))

print(avg_size_0, avg_size_1)
