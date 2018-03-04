import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from copy import deepcopy

from pygame.locals import *
import pygame
import time
from copy import deepcopy

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

        def inGrid(self, grid_size):
            head = self.head()
            if head[0]<=0 or head[1]<=0 or head[0] >= grid_size or head[1] >= grid_size:
                return False
            return True


        def _draw(self, surface, image, image_head, spacing):
            surface.blit(image_head, (self.pos[0][0]*spacing, self.pos[0][1]*spacing))
            for i in range(1, self.size):
                surface.blit(image, (self.pos[i][0]*spacing, self.pos[i][1]*spacing))

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


class SnakeEnv(gym.Env):
    AGENT_COLORS = [
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]



    def __init__(self, num_agents=2, ncandies=3, window_dimension=800, spacing=20, init_size=3):
        self._running = True

        self._display_surf = None
        self._image_surf = None
        self._fruit_surf = None


        self.active_agents = num_agents
        self.num_agents = num_agents
        self.ncandies = ncandies
        self.init_size = init_size

        self.agents = []
        self.candies = set()

        self.window_dimension = window_dimension
        self.spacing = spacing
        self.grid_size = window_dimension/spacing-1


        assert self.window_dimension % self.spacing == 0, "window_dimension needs to be a multiple of spacing"

        self.max_spawn_idx = self.window_dimension / self.spacing - self.init_size
        for i in range(self.num_agents):
            agent = self._create_agent(i, self.init_size)
            self.agents.append(agent)


        while len(self.candies)<self.ncandies:
            self.candies.add(self._rangen_candy())


        self.reward_range = (-1.0, 1.0)

        self._pygame_init()


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def step(self):
        new_obs = []
        killed_on_step = [False] * len(self.agents)
        rewards = [0.0] * self.num_agents

#        for i in range(self.num_agents):
#            print('snake number ' + str(i))
#            print(self.agents[i])


        for s in self.agents:
            s.update()

        for i, s in enumerate(self.agents):
            # Did a snake eat an apple?
            if not self.agents[i].alive: 
                continue

            toRemove = []
            for c_i, c in enumerate(self.candies):
                if s.onSnake(c):
                    toRemove.append(c)
                    rewards[i] = 1.0
                    s.eat_candy(1)
            for c in toRemove:
                self.candies.remove(c)

            # does snake hit a wall?
            if not s.inGrid(self.grid_size):
                killed_on_step[i] = True


            # does snake collide with another agent?
            for snake in self.agents:
                if snake.alive:
                    if s.alive and s.id != snake.id and s.interSnake(snake):
                        print('kill ' +str(s.id) + ' ' + str(snake.id))
                        killed_on_step[i]=True

        for i, k in enumerate(killed_on_step):
            if k:
                self._add_candies(self.agents[i].prev_pos)
                rewards[i] = -100.0
                self.active_agents -= 1
                self.agents[i].alive = False


        done = False
        if self.active_agents == 0:
            done = True

        self._check_ncandies()

#        for i in range(self.num_agents):
#            ob = self._generate_obs(i)
#            new_obs.append(ob)

        return deepcopy(new_obs), deepcopy(rewards), done, {}


    def render(self, mode='human'):
        print('pygame_init ' + str(self._running))
        if self._pygame_init() == False:
            self._running = False

        self._draw_env()

        for i, s in enumerate(self.agents):
            print(s)

        for i, f in enumerate(self.candies):
            self._pygame_draw(self._display_surf, self._fruit_surf, (f[0]*self.spacing, f[1]*self.spacing))

        for i, s in enumerate(self.agents):
            if not self.agents[i].alive: 
                continue
            s._draw(self._display_surf, self._agent_surfs[s.color_i], self._agent_surfs[-1], self.spacing)

        pygame.display.flip()


    def reset(self):
        for i, p in enumerate(self.agents):
            self.agents[i].alive = True

            x = np.random.randint(1, self.max_spawn_idx - 1) * self.spacing
            y = np.random.randint(1, self.max_spawn_idx - 1) * self.spacing
            direction = np.random.randint(0, 1)

            p._reset(x, y, direction)

        for f in range(self.ncandies):
            self.candies[f] = self._generate_goal()

        self.active_agents = self.num_agents


    def close(self):
        pygame.quit()


    def _create_agent(self, i, init_size):

        x = np.random.randint(init_size, self.grid_size - init_size)
        y = np.random.randint(init_size, self.grid_size - init_size)
        direction = np.random.randint(0, 4)

        agent = Snake(i, (x,y), direction=direction, size=init_size)
        agent.color_i = i % len(self.AGENT_COLORS)
        agent.nextAction(direction)

#        print('Snake ' + str(i))
#        print(self.actions[i])

        return deepcopy(agent)


    def _draw_env(self):
        self._display_surf.fill((0,0,0))

        for i in range(0, self.window_dimension, self.spacing):
            self._display_surf.blit(self._wall_surf, (0, i))
            self._display_surf.blit(self._wall_surf, (self.window_dimension - self.spacing, i))

        for i in range(0, self.window_dimension, self.spacing):
            self._display_surf.blit(self._wall_surf, (i, 0))
            self._display_surf.blit(self._wall_surf, (i, self.window_dimension - self.spacing))


    def _rangen_candy(self):

        x = np.random.randint(1, self.grid_size)
        y = np.random.randint(1, self.grid_size)

        return (x, y)

    def _add_candies(self, pos):
        self.candies = self.candies.union(pos)

    def _check_ncandies(self):
        while len(self.candies)<self.ncandies:
            self.candies.add(self._rangen_candy())


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


    def _pygame_draw(self, surface, image, pos):
        surface.blit(image, (pos[0], pos[1]))


    def _pygame_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_dimension, self.window_dimension), pygame.HWSURFACE)
        self._agent_surfs = []
        self._running = True

        for i, p in enumerate(self.agents):
            image_surf = pygame.Surface([self.spacing - 4, self.spacing - 4])
            image_surf.fill(self.AGENT_COLORS[i % len(self.AGENT_COLORS)])
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

class Map(np.ndarray):
    def __new__(cls, height, width):
        return np.zeros((height, width))

    def set(self, pos, value):
        self[pos]=value
