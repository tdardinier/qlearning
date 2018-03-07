import numpy as np
from pygame.locals import *
import pygame
import random as rd
from snake_env import Render, Map
import time
from IA import IA_keyboard, IA_random, IA_rl

n_agents = 2
n_candies = 10
gridsize = 30


file_to_use = "current_snake.csv"
load_from_file = False

timestep = None

last_saved = time.time()
timestep_to_save = 1800

M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
IA = [IA_rl.IA(i) for i in range(n_agents)]
e = Render(M, spacing=20)
q = None

step_by_step = False

def press():
    pygame.event.pump()
    return pygame.key.get_pressed()

def get_q():
    q = 0
    for i in range(n_agents):
        q += IA[i].q / n_agents
    return q

def init_snakes_with_q(q):
    for i in range(n_agents):
        IA[i] = IA_rl.IA(i, q)

if load_from_file:
    init_snakes_with_q(np.loadtxt(file_to_use))

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

        e.render()
        if len(M.activeAgents) < n_agents:
            q = 0
            for i in range(n_agents):
                if not (i in M.activeAgents):
                    IA[i].dead()
            break

        for i in range(n_agents):
            a = IA[i].act(M)
            M.agents[i].nextAction(a)

        if time.time() - last_saved > timestep_to_save:
            q = get_q()
            print("Saving...")
            np.savetxt(file_to_use, q, fmt='%.2f')
            last_saved = time.time()
            print("Saved!")

        keys = press()
        if keys[K_DOWN]:
            step_by_step = True

        r, done = M.step()
        if not timestep is None:
            time.sleep(timestep)

    M = Map(nagents=n_agents, ncandies=n_candies, gridsize=gridsize)
    e = Render(M, spacing=20)
    q = get_q()
    init_snakes_with_q(q)
