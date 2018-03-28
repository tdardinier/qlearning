from numpy import *
import random as rd
import time

use_vision_walls = True
use_odorat_candies = True
use_odorat_snakes = True

vision_walls_max = 2
odorat_candies_max = 8
odorat_snakes_max = 4

epsilon = 0.01
tau = 0.1
alpha = 0.2
gamma = 0.9
reward_dead = -10
reward_candy = 1

use_epsilon_greedy = False # Softmax otherwise
use_sarsa = False # Q-Learning otherwise

MOVES = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1)
]

sensors = [vision_walls_max for _ in range(4)] * use_vision_walls + [odorat_candies_max for _ in range(4)] * use_odorat_candies + [odorat_snakes_max for _ in range(4)] * use_odorat_snakes
n_sensors = len(sensors)
n_actions = 4
actions = range(n_actions)
n_states = (vision_walls_max ** (4 * use_vision_walls)) * (odorat_candies_max ** (4 * use_odorat_candies)) * (odorat_snakes_max ** (4 * use_odorat_snakes))
delimiter = ","

class IA():

    def __init__(self, agent_id, save = None):

        self.id = agent_id

        self.prev_s = None
        self.prev_a = None

        if save is None:
            self.q = zeros((n_states, n_actions))
        else:
            self.q = save

    def load(self, fichier):
        self.q = loadtxt(fichier, delimiter = delimiter)
        self.prev_s = None
        self.prev_a = None

    def save(self, fichier):
        savetxt(fichier, self.q, delimiter = delimiter)

    def numberize_state(self, s):
        r = 0
        m = 1
        for i in range(n_sensors):
            x = s[i]
            if (x <= 0 or x > sensors[i]):
                #print(i, x)
                #raise Exception("Error: Bad sensor value")
                x = 1
            r += (x - 1) * m
            m *= sensors[i]
        return r

    def distance_to_candy(self, x, y, M):
        d = odorat_candies_max - 1
        for (a, b) in M.candies:
            d = min(d, abs(x - a) + abs(y - b))
        return d + 1

    def distance_to_snake(self, x, y, M):
        d = odorat_snakes_max - 1
        for agent in M.agents:
            if agent.id != self.id:
                for (a, b) in agent.pos:
                    d = min(d, abs(x - a) + abs(y - b))
        return d + 1

    def convert_input(self, M):

        head = M.agents[self.id].getHead()
        x = head[0]
        y = head[1]
        values = []

        if use_vision_walls:
            vision_walls = []
            # Walls
            for i in range(len(MOVES)):
                (xx, yy) = MOVES[i]
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
                vision_walls.append(min(dist_wall, vision_walls_max))
            values += vision_walls

        if use_odorat_candies:
            odorat_candies = []
            odorat_candies.append(self.distance_to_candy(x + 1, y, M))
            odorat_candies.append(self.distance_to_candy(x, y - 1, M))
            odorat_candies.append(self.distance_to_candy(x - 1, y, M))
            odorat_candies.append(self.distance_to_candy(x, y + 1, M))
            values += odorat_candies

        if use_odorat_snakes:
            odorat_snakes = []
            odorat_snakes.append(self.distance_to_snake(x + 1, y, M))
            odorat_snakes.append(self.distance_to_snake(x, y - 1, M))
            odorat_snakes.append(self.distance_to_snake(x - 1, y, M))
            odorat_snakes.append(self.distance_to_snake(x, y + 1, M))
            values += odorat_snakes

        return values

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
        print("Espace de choix")
        print(spaces + l[1])
        print(l[2] + spaces + l[0])
        print(spaces + l[3])
        print("")

    def candy_found(self, M):
        return M.agents[self.id].has_eaten

    def act(self, M):
        reward = reward_candy * self.candy_found(M)
        s = self.numberize_state(self.convert_input(M))
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
