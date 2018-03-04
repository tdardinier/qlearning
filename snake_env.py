from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from copy import deepcopy

import pygame

from collections import deque

class Snake:
        def __init__(self, id, pos, size=2, direction=0):
            self.init_size = size
            self.size = size
            self.alive = True
            self.id=id

            self.direction = direction

            self.update_count_max = 2
            self.update_count = 0
            self.build_pos(pos, direction)
            self.new_pos = deque()
            self.prev_pos = deque()

            

        def build_pos(self, pos, direction):
            self.pos = deque()
            x=pos[0]
            y=pos[1]
            self.next_action=direction
            
            for i in range(self.size):
                
                if self.direction == 0:
                    self.pos.append((x - i, y))

                if self.direction == 1:
                    self.pos.append((x + i, y))

                if self.direction == 2:
                    self.pos.append((x, y - i))

                if self.direction == 3:
                    self.pos.append((x, y + i))
                    
            
        def _reset(self, pos, direction):
            self.size = self.init_size

            self.update_count = 0
            self.direction = direction
            
            self.build_pos(pos, direction)
            
        def update(self):
            self.prev_pos=self.pos.copy()
            move = Move(self.next_action)
            head = self.head()
            self.new_pos.clear()
            for i in range(move.norm):
                self.pos.pop()
            for i in range(1,move.norm+1):
                p=(head[0]+i*move.dir[0], head[1]+i*move.dir[1])
                self.pos.appendleft(p)
                self.new_pos.appendleft(p)
        
        def interSnake(self, snake):
            for position in self.new_pos:
                if position in snake.pos:
                    return True
            return False
                
                
                
        def onSnake(self, pos):
            return pos in self.pos
        
        def inGrid(self, gridsize):
            head = self.head()
            if head[0]<0 or head[1]<0 or head[0] >= gridsize or head[1] >= gridsize:
                return False
            return True
        
        def inGridMove(self, gridsize, move):
            next_head = move.apply(self.head())
            if next_head[0]<0 or next_head[1]<0 or next_head[0] >= gridsize or next_head[1] >= gridsize:
                return False
            return True

        def head(self):
            return self.pos[0]
        
        def tail(self):
            return self.pos[-1]
        
        def next_pos(self, move):
            return move.apply(self.head())
        
        def eat_candy(self, bonus):
            self.size += bonus
            tail_pos = self.tail()
            for i in range(bonus):
                self.pos.append(tail_pos)
                
        def nextAction(self, move_type):
            self.next_action = move_type
                
                
        
        def __str__(self):
            s='Snake ' + str(self.id)
            if self.alive:
                s += ' is alive and positionned at '
                for p in self.pos:
                    s += str(p) + ' ' 
            else:
                s+= ' is not more alive and the last known position is'
                for p in self.pos:
                    s += str(p) + ' ' 
            return s
        

class Render():

    def __init__(self, M, spacing=20):
        self._running = True

        self._display_surf = None
        self._image_surf = None
        self._fruit_surf = None

        self.window_dimension = (M.gridsize+2)*spacing
        self.spacing = spacing
        
        self.map = M
        

        assert self.window_dimension % self.spacing == 0, "window_dimension needs to be a multiple of spacing"

        self._pygame_init()

    def render(self, mode='human'):
        print('pygame_init ' + str(self._running))
        if self._pygame_init() == False:
            self._running = False

        self._draw_env()
        
        for i, s in enumerate(self.map.agents):
            print(s)

        for i, f in enumerate(self.map.candies):
            print(f)
            self._pygame_draw(self._display_surf, self._fruit_surf, f)

        for i, s in enumerate(self.map.agents):
            if s.alive: 
                self._draw_snake(s)

        pygame.display.flip()
        
    def _draw_snake(self, snake):
        if snake.alive:
            self._pygame_draw(self._display_surf, self._agent_surfs[-1], snake.pos[0])
            for i in range(1, (len(snake.pos))):
                self._pygame_draw(self._display_surf, self._agent_surfs[snake.color_i], snake.pos[i])

                
    def _pygame_draw(self, surface, image, pos):
        surface.blit(image, ((pos[0]+1)*self.spacing, (pos[1]+1)*self.spacing))

    def close(self):
        pygame.quit()   
    


    def _draw_env(self):
        self._display_surf.fill((0,0,0))

        for i in range(0, self.window_dimension, self.spacing):
            self._display_surf.blit(self._wall_surf, (0, i))
            self._display_surf.blit(self._wall_surf, (self.window_dimension - self.spacing, i))

        for i in range(0, self.window_dimension, self.spacing):
            self._display_surf.blit(self._wall_surf, (i, 0))
            self._display_surf.blit(self._wall_surf, (i, self.window_dimension - self.spacing))

    def _generate_obs(self, agent):
        obs = np.zeros((self.window_dimension, self.window_dimension))

        if not self.agents[agent].alive: 
            return -1 * np.ones((self.window_dimension, self.window_dimension))

        for i in range(self.agents[agent].size):
            
            obs[self.agents[agent].pos[i]] = 1

        for i, p in enumerate(self.agents):
            if self.killed[i]: continue
            for j in range(p.length):
                obs[p.pos[j]] = 2
        for i, f in enumerate(self.candies):
            obs[f[0]][f[1]] = 3

        obs[:][0] = -1
        obs[:][self.window_dimension -1] = -1

        obs[0][:] = -1
        obs[self.window_dimension -1][:] = -1

        return deepcopy(obs)



    def _pygame_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_dimension, self.window_dimension), pygame.HWSURFACE)
        self._agent_surfs = []
        self._running = True

        for i, p in enumerate(self.map.agents):
            image_surf = pygame.Surface([self.spacing - 4, self.spacing - 4])
            image_surf.fill(self.map.COLORS[i % len(self.map.COLORS)])
            self._agent_surfs.append(image_surf)
        
        image_surf = pygame.Surface([self.spacing - 4, self.spacing - 4])
        image_surf.fill((150,150,150))
        self._agent_surfs.append(image_surf)

        self._fruit_surf = pygame.Surface([self.spacing - 4, self.spacing - 4])
        self._fruit_surf.fill((255, 0, 0))

        self._wall_surf = pygame.Surface([self.spacing - 4, self.spacing - 4])
        self._wall_surf.fill((255, 255, 255))
        
        
class Move:

    
    def __init__(self, move_type):
        self.type = move_type
        if move_type==0:
            self.dir=(1,0)
        if move_type==1:
            self.dir=(0,-1)
        if move_type==2:
            self.dir=(-1,0)
        if move_type==3:
            self.dir=(0,1)
        self.norm=1
            
        
    def apply(self, point):
        return (point[0]+self.norm*self.direction[0], point[1]+self.norm*self.direction[1])
    
    def __str__(self):
        return 'Direction ' + str(self.dir) + ' with norm '  + str(self.norm)
    
    
    
class Map():
    COLORS = [
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]
    MOVES = [
        Move((1,0)),
        Move((0,-1)),
        Move((-1,0)),
        Move((0,1))
    ]
    
    def __init__(self, nagents=2, ncandies=3, gridsize=40, max_iter=100):

        self.gridsize = gridsize
        self.nagents = nagents
        self.ncandies = ncandies
        self.iters=0
        self.max_iter=max_iter
        
        self.agents = []
        self.activeAgents = set()
        self.candies = set()
        
        self.createAgents()
        self.createCandies()
        


        self.reward_range = (-1.0, 1.0)
        
    def createAgents(self):
        for i in range(self.nagents):
            agent = self.genAgent(i)
            self.agents.append(agent)
            self.activeAgents.add(i)
    
    def createCandies(self):
        for i in range(self.ncandies):
            candy = self.genCandy()
            self.candies.add(candy)
        
    def genAgent(self, i, init_size=2):
        
        noIntersection=False
        while not noIntersection:
            #Draw initial head position and direction
            x = np.random.randint(init_size-1, self.gridsize - init_size) 
            y = np.random.randint(init_size-1, self.gridsize - init_size)
            direction = np.random.randint(0, 4)
    
            agent = Snake(i, (x,y), direction=direction, size=init_size)
            noIntersection=True
            for point in agent.pos:
                if self.interElements(point):
                   noIntersection=False 
            
        agent.color_i = i % len(self.COLORS)
        agent.nextAction(direction)
            
    #        print('Snake ' + str(i))
    #        print(self.actions[i])

        return agent
    
    #generate a candy randomly located among the free locations
    def genCandy(self):
        while True:
            x = np.random.randint(0, self.gridsize) 
            y = np.random.randint(0, self.gridsize) 
            point = (x,y)
            if not self.interElements(point):
                return point
            
    def addCandies(self, pos):
        for point in pos:
            self.candies.add(point)
    
    #chech if there is the right number of candies on the board
    def chechCandies(self):
        while len(self.candies)<self.ncandies:
            self.candies.add(self.genCandy())
    
    #Test if a position is free
    def interElements(self, point):
        if point in self.candies:
            return True
        for s in self.agents:
            if s.onSnake(point):
                return True
        return False
    
    def setValue(self, pos, value):
        self[pos]=value
        
    def step(self):
        self.iters += 1 
        killed = [False] * self.nagents
        rewards = [0.0] * self.nagents


        for i in self.activeAgents:
            self.agents[i].update()

        for i in self.activeAgents:
            s=self.agents[i]
            toRemove = []
            for c in self.candies:
                if s.onSnake(c):
                    toRemove.append(c)
                    rewards[s.id] = 1.0
                    s.eat_candy(1)
            for c in toRemove:
                self.candies.remove(c)

            # does snake hit a wall?
            if not s.inGrid(self.gridsize):
                killed[s.id] = True                

            # does snake collide with another agent?
            for j in self.activeAgents:
                if s.id != self.agents[j].id and s.interSnake(self.agents[j]):
                        print('kill ' +str(s.id) + ' ' + str(self.agents[j].id))
                        killed[s.id]=True

        for i, k in enumerate(killed):
            if k:
                self.addCandies(self.agents[i].prev_pos)
                rewards[i] = -100.0
                self.activeAgents.remove(i)
                self.agents[i].alive = False
                
        done = False
        if len(self.activeAgents)== 0:
            done = True
            
        self.chechCandies()


        return rewards, done
    
    def win(self, agent_id):
        return len(self.activeAgents)==1 and agent_id in self.activeAgents
    
    def lose(self, agent_id):
        return len(self.activeAgents)==0 or not agent_id in self.activeAgents
    
    def finish(self):
        self.iters == self.max_iter
    
    
        
    def score(self, agent_id):
        if self.win(agent_id):
            return self.gridsize**2
        if self.lose(agent_id):
            return -self.gridsize**2
        return self.agents[agent_id].size
    
    def possiblesMoves(self, agent):
        moves = []
        for move in self.MOVES:
            if agent.inGridMove(self.gridsize, move) and move.type != agent.next_action:
                moves.append(move)
        return moves
    


    