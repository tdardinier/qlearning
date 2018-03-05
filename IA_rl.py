from numpy import *
import random as rd
from pygame.locals import *
import pygame

MOVES = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1)
]

vision_max = 5
n_sensors = 8 # We don't use the other snakes first
n_actions = 4

epsilon = 0.1
tau = 0.5
alpha = 0.1
gamma = 0.99
actions = range(n_actions)
n_states = vision_max ** n_sensors
reward_dead = -10

use_epsilon_greedy = False # Softmax otherwise
use_sarsa = False # Q-Learning otherwise

class IA():

    def __init__(self, agent_id, save = None):

        self.prev_s = None
        self.prev_a = None
        self.id = agent_id

        self.q = ones((n_states, n_actions))
        if not (save is None):
            self.q = save

    def __str__(self):
        return ("Simple Qlearning agent: ", self.q)

    def numberize_state(self, s):
        r = 0
        m = 1
        for x in s:
            r += (x - 1) * m
            m *= vision_max
        return r

    def convert_input(self, M):
        head = M.agents[self.id].head()
        x = head[0]
        y = head[1]

        walls = [vision_max for _ in range(4)]
        snakes = [vision_max for _ in range(4)]
        candies = [vision_max for _ in range(4)]

        for i in range(len(MOVES)):
            (xx, yy) = MOVES[i]

            # Walls
            dist_wall = vision_max
            if xx == 1:
                dist_wall = M.gridsize - x
            elif xx == -1:
                dist_wall = x + 1
            elif yy == 1:
                dist_wall = M.gridsize - y
            elif yy == -1:
                dist_wall = y + 1
            else:
                print("ERROR: shouldn't happen")
            walls[i] = min(dist_wall, vision_max)

            # Candies
            dist_candy = M.gridsize
            for (a, b) in M.candies:
                if xx == 1:
                    if y == b and x < a:
                        dist_candy = min(dist_candy, a - x)
                elif xx == -1:
                    if y == b and x > a:
                        dist_candy = min(dist_candy, x - a)
                elif yy == 1:
                    if x == a and y < b:
                        dist_candy = min(dist_candy, b - y)
                elif yy == -1:
                    if x == a and y > b:
                        dist_candy = min(dist_candy, y - b)
                else:
                    print("ERROR: shouldn't happen")
            candies[i] = min(vision_max, dist_candy)

            # Snakes
            dist_snake = M.gridsize
            for agent in M.agents:
                for (a, b) in agent.pos:
                    if xx == 1:
                        if y == b and x < a:
                            dist_snake = min(dist_snake, a - x)
                    elif xx == -1:
                        if y == b and x > a:
                            dist_snake = min(dist_snake, x - a)
                    elif yy == 1:
                        if x == a and y < b:
                            dist_snake = min(dist_snake, b - y)
                    elif yy == -1:
                        if x == a and y > b:
                            dist_snake = min(dist_snake, y - b)
                    else:
                        print("ERROR: shouldn't happen")
            snakes[i] = min(vision_max, dist_snake)

        print("Walls", walls)
        print("Candies", candies)
        print("Snakes", snakes)
        #return walls + candies + snakes
        return walls + candies

    def proba_softmax(self, l):
        p = [exp(q_value / tau) for q_value in l]
        s = sum(p)
        return [x/s for x in p]

    def choose_action(self, s):
        print(self.q)
        l = self.q[s]
        if use_epsilon_greedy:
            if rd.random() < epsilon:
                return rd.choice(actions)
            return argmax(l)
        else:
            p = self.proba_softmax(l)
            somme = p[0]
            r = rd.random()
            i = 0
            while r > somme:
                i +=1
                somme += p[i]
            return i

    def act(self, M, reward):
        s = self.numberize_state(self.convert_input(M))
        a = self.choose_action(s)
        if not (self.prev_a is None):
            if use_sarsa:
                self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * self.q[s][a])
            else:
                self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * max(self.q[s]))
        self.prev_a = a
        self.prev_s = s
        return a

    def dead():
        self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * reward_dead
        return self.q

#    def act(self, state, reward, dead):
#        self.convert_input(state)
#        while True:
#            pygame.event.pump()
#            keys = pygame.key.get_pressed()
#            if (keys[K_RIGHT]):
#                return 0
#            if (keys[K_UP]):
#                return 1
#            if (keys[K_LEFT]):
#                return 2
#            if (keys[K_DOWN]):
#                return 3
        #return rd.randint(0, 3)
