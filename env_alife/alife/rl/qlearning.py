from alife.rl.agent import Agent
from numpy import *
import random as rd

n_sensors = 9 # we discount the energy

inter = 5
n_actions = 4
speed = 10

epsilon = 0.1
tau = 0.5
alpha = 0.1
gamma = 0.99

actions = range(n_actions)
n_states = inter ** n_sensors

use_epsilon_greedy = False # Softmax otherwise
use_sarsa = False # Q-Learning otherwise

class Qlearning(Agent):

    def proba_softmax(self, l):
        p = [exp(q_value / tau) for q_value in l]
        s = sum(p)
        return [x/s for x in p]

    def convert_output(self, a):
        return [(2 * a - n_actions) * (pi / n_actions), speed]

    def unconvert_state(self, state):
        x = [0 for _ in range(n_sensors)]
        i = 0
        while state > 0:
            x[i] = state % inter
            state = state // inter
            i += 1
        return x

    def print_state(self, s):
        state = self.unconvert_state(s)
        print("STATE")
        print("Left antenna: ", (state[0], state[1], state[2]))
        print("Right antenna: ", (state[3], state[4], state[5]))
        print("Body: ", (state[6], state[7], state[8]))

    def discretize_input(self, state):
        s = 0
        current = 1
        i = 0
        while i < n_sensors:
            x = state[i]
            conv = int((x - 0.001) * inter)
            s += current * conv
            current *= inter
            i += 1
        return s

    def choose_action(self, state):
        s = self.discretize_input(state)
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

    def __init__(self, obs_space, act_space, gen=1):

        self.prev_s = None
        self.prev_a = None
        self.q = zeros((n_states, n_actions))
        self.generation = gen
        self.min = 0
        self.max = 0
        self.s_max = 0
        self.a_max = 0

    def __str__(self):
        return ("Simple Qlearning agent: ", self.q)

    def act(self,s,reward,done=False):
        a = self.choose_action(s)
        if not (self.prev_a is None):
            if use_sarsa:
                self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * self.q[self.discretize_input(s)][a])
            else:
                self.q[self.prev_s][self.prev_a] = (1 - alpha) * self.q[self.prev_s][self.prev_a] + alpha * (reward + gamma * max(self.q[self.discretize_input(s)]))
            if self.q[self.prev_s][self.prev_a] >= self.max:
                self.max = self.q[self.prev_s][self.prev_a]
                self.s_max = self.prev_s
                self.a_max = self.prev_a
            self.min = min(self.q[self.prev_s][self.prev_a], self.min)
        self.prev_a = a
        self.prev_s = self.discretize_input(s)
        #if self.max > 0:
            #self.print_state(self.prev_s)
            #print(self.prev_a, self.max, self.min)
        return self.convert_output(a)

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
