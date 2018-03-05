from numpy import *
import random as rd
from pygame.locals import *
import pygame
import time

MOVES = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1)
]

vision_walls_max = 2
odorat_candies_max = 8
odorat_snake_max = 10

sensors = [vision_walls_max for _ in range(4)] + [odorat_candies_max for _ in range(4)]
n_sensors = len(sensors)
n_actions = 4

epsilon = 0.1
tau = 0.1
alpha = 0.2
gamma = 0.9
actions = range(n_actions)
n_states = (vision_walls_max ** 4) * (odorat_candies_max ** 4)
reward_dead = -10

use_epsilon_greedy = False # Softmax otherwise
use_sarsa = False # Q-Learning otherwise

class IA():

    def __init__(self, agent_id, save = None):

        self.prev_s = None
        self.prev_a = 0
        self.last_x = 0
        self.last_y = 0
        self.id = agent_id
        self.current_input = None

        self.q = ones((n_states, n_actions)) * 0.5
        if not (save is None):
            self.q = save

    def __str__(self):
        return ("Simple Qlearning agent: ", self.q)

    def numberize_state(self, s):
        r = 0
        m = 1
        for i in range(n_sensors):
            x = s[i]
            r += (x - 1) * m
            m *= sensors[i]
        return r

    def distance_to_candy(self, x, y, M):
        d = odorat_candies_max
        for (a, b) in M.candies:
            d = min(d, abs(x - a) + abs(y - b))
        return d

    def convert_input(self, M):

        head = M.agents[self.id].getHead()

        x = head[0]
        y = head[1]

        self.last_x = x
        self.last_y = y

        walls = [vision_walls_max for _ in range(4)]
        snakes = [odorat_snake_max for _ in range(4)]

        odorat_candies = []
        odorat_candies.append(self.distance_to_candy(x + 1, y, M))
        odorat_candies.append(self.distance_to_candy(x, y - 1, M))
        odorat_candies.append(self.distance_to_candy(x - 1, y, M))
        odorat_candies.append(self.distance_to_candy(x, y + 1, M))

        for i in range(len(MOVES)):
            (xx, yy) = MOVES[i]

            # Walls
            dist_wall = vision_walls_max
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
            walls[i] = min(dist_wall, vision_walls_max)

            # Snakes
            # TODO
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
            snakes[i] = min(odorat_snake_max, dist_snake)

        #print("Walls", walls)
        #print("Candies", candies)
        #print("Snakes", snakes)
        #return walls + candies + snakes
        return walls + odorat_candies

    def proba_softmax(self, l):
        p = [exp(q_value / tau) for q_value in l]
        s = sum(p)
        return [x/s for x in p]

    def choose_action(self, s):
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

    def print_choix(self, s):
        spaces = " " * 4
        l = ["%.2f" % x for x in self.q[s]]
        print("")
        print((self.last_x, self.last_y))
        print(self.current_input)
        print("Espace de choix")
        print(spaces + l[1])
        print(l[2] + spaces + l[0])
        print(spaces + l[3])
        print(l)
        print("")

    def act(self, M, reward):
        self.current_input = self.convert_input(M)
        s = self.numberize_state(self.current_input)
        a = self.choose_action(s)
        if not (self.prev_s is None):
            if use_sarsa:
                self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * self.q[s][a])
            else:
                self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * max(self.q[s]))
        self.prev_a = a
        self.prev_s = s
        return a

    def dead(self):
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
