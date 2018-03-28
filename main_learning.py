import numpy as np
from pygame.locals import *
import pygame
import random as rd
from snake_env import Render, Map
from IA import IA_rl, IA_random, IA_minimax

n_agents = 2
n_candies = 10
gridsize = 30
n_total_iter = 2000
sliding_window = 100
step = 10

IA_learning = IA_rl.IA(0)
adversary = IA_random.IA(1)
#adversary = IA_minimax.IA(1)

M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
e = Render(M, spacing=20)
q = None

current_result = 0
all_results = []
result = []

for match in range(1, n_total_iter + 1):

    while True:

        #e.render()

        if len(M.activeAgents) < n_agents:
            if 0 in M.activeAgents:
                current_result += 1
            else:
                IA_learning.dead()
            break

        M.agents[0].nextAction(IA_learning.act(M))
        M.agents[1].nextAction(adversary.act(M))

        r, done = M.step()


    if match % step == 0:
        print(match)
        all_results.append(current_result)
        current_result = 0
        result.append(sum(all_results) / len(all_results))

    M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)
    IA_learning = IA_rl.IA(0, IA_learning.q)

print(result)
