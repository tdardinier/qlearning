import random as rd
import tree_strategy

depth=2

class IA():

    def __init__(self, agent_id, depth):
        self.name = "IA random"
        self.step = 0
        self.id = agent_id
        self.depth = depth

    def __str__(self):
        return self.name

    def act(self, state):
        return tree_strategy.minimax(self.id, self.id, state, self.depth)
    
