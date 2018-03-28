import random as rd

class IA():

    def __init__(self, agent_id):
        self.name = "IA random"
        self.step = 0
        self.id = agent_id

    def __str__(self):
        return self.name

    def act(self, state):
        return rd.randint(0, 3)

    def dead(self):
        return
