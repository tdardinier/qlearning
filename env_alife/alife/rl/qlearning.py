from alife.rl.agent import Agent
from numpy import *
import random as rd

inter = 3
n_actions = 4
actions = range(n_actions)
n_states = inter ** 10
alpha = 0.1
gamma = 0.9
speed = 10
eps = 0.1

def convert_output(a):
    return [(2 * a - n_actions) * (pi / n_actions), speed]

def discretize_input(state):
    s = 0
    current = 1
    for x in state:
        conv = int((x - 0.001) * inter)
        s += current * conv
        current *= inter
    return s

class Qlearning(Agent):
    def choose_action(self, state):
        if rd.random() < eps:
            return rd.choice(actions)
        return argmax(self.q[discretize_input(state)])

    def __init__(self, obs_space, act_space, gen=1):

        self.prev_s = None
        self.prev_a = None
        self.q = zeros((n_states, n_actions))
        self.generation = gen
        self.min = 0
        self.max = 0

    def __str__(self):
        return ("Simple Qlearning agent: ", self.q)

    def act(self,s,reward,done=False):
        if not (self.prev_a is None):
            self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * max(self.q[discretize_input(s)]))
            self.max = max(self.q[self.prev_s][self.prev_a], self.max)
            self.min = min(self.q[self.prev_s][self.prev_a], self.min)
        a = self.choose_action(s)
        self.prev_a = a
        self.prev_s = discretize_input(s)
        print(self.min, self.max)
        return convert_output(a)

    def spawn_copy(self):
        b = Qlearning(None, None, self.generation+1)
        b.q = self.q
        return b

    def save(self, bin_path, log_path, obj_ID):
        header = [("X%d" % j) for j in range(self.log.shape[1])]
        header[-1] = "reward"
        fname = log_path+("/%d-%s-G%d.log" % (obj_ID,self.__class__.__name__,self.generation))
        savetxt(fname,self.log[0:self.t,:],fmt='%4.3f',delimiter=',',header=','.join(header),comments='')
        print("Saved log to '%s'." % fname)
