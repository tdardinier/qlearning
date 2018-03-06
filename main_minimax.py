import numpy as np
from pygame.locals import *
import pygame
import random as rd
from snake_env import Render, Map
from IA import IA_rl, IA_random, IA_minimax

n_agents = 2
n_candies = 10
gridsize = 30
n_total_iter = 5000
size_chunk = 100

IA_learning = IA_minimax.IA(0)
adversary = IA_minimax.IA(1)

M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
e = Render(M, spacing=20)

result = []
current_result = 0

for match in range(1, n_total_iter + 1):

    while True:

        e.render()

        if len(M.activeAgents) < n_agents:
            if 0 in M.activeAgents:
                current_result += 1
            break
        
        
        M.agents[0].nextAction(IA_learning.act(M))
        M.agents[1].nextAction(adversary.act(M))

        r, done = M.step()

    if match % size_chunk == 0:
        print(current_result)
        result.append(current_result / size_chunk)
        print(result)
        current_result = 0

    M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)

print(result)
