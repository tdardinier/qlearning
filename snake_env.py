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



class SnakeEnv(gym.Env):
    AGENT_COLORS = [
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]

    class Snake:
        def __init__(self, pos, size=2, direction=0):
            self.init_size = size
            self.size = size
            self.alive = True

            self.direction = direction

            self.update_count_max = 2
            self.update_count = 0
            self.build_pos(pos, direction)
            self.new_pos=deque()

            

        def build_pos(self, pos, direction):
            self.pos = deque()
            x=pos[0]
            y=pos[1]
            
            for i in range(self.size):
           # initial positions, no collision.
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


        def _act(self, action):
            if action == 0:
                if self.direction == 1:
                    return

                self.direction = 0

            elif action == 1:
                if self.direction == 0:
                    return

                self.direction = 1

            elif action == 2:
                if self.direction == 3:
                    return

                self.direction = 2

            elif action == 3:
                if self.direction == 2:
                    return

                self.direction = 3

            else:
                # Should never reach
                pass
            
        def update(self, move):
            head = self.head()
            self.new_pos.clear()
            for i in range(move.norm):
                self.pos.popleft()
            for i in range(1,move.norm+1):
                p=(head[0]+i*self.direction[0], head[1]+i*self.direction[1])
                self.pos.append(p)
                self.new_pos.append(p)
        
        def interSnake(self, snake):
            for pos in self.new_pos:
                if pos in snake.pos:
                    return True
            return False
                
                
                
        def onSnake(self, pos):
            return pos in self.position
        
        def inGrid(self, grid_size):
            head = self.head()
            if head[0]<0 or head[1]<0 or head[0] >= grid_size[0] or head[1] >= grid_size[1]:
                return False
            return True


        def _update(self):
            self.update_count = self.update_count + 1
            if self.update_count > self.update_count_max:

                # update previous positions
                for i in range(self.length, 0, -1):
                    self.x[i] = self.x[i-1]
                    self.y[i] = self.y[i-1]

                # update position of head of snake
                if self.direction == 0:
                    self.x[0] = self.x[0] + self.step
                if self.direction == 1:
                    self.x[0] = self.x[0] - self.step
                if self.direction == 2:
                    self.y[0] = self.y[0] - self.step
                if self.direction == 3:
                    self.y[0] = self.y[0] + self.step

                self.update_count = 0

        
        def _draw(self, surface, image, image_head, spacing):
            surface.blit(image_head, (self.pos[0][0]*spacing, self.pos[0][1]*spacing))
            for i in range(1, self.size):
                surface.blit(image, (self.pos[i][0]*spacing, self.pos[i][0]*spacing))
        
        def head(self):
            return self.pos[0]
        
        def next_pos(self, move):
            return move.apply(self.head())
        
        
    class Move:
        
        def __init__(self, direction, norm):
            self.dir = direction
            self.norm = norm
            
        def apply(self, point):
            return (point[0]+self.norm*self.direction[0], point[1]+self.norm*self.direction[1])
            
    class Map(np.ndarray):
        def __new__(cls, height, width):
            return np.zeros((height, width))
        
        def set(self, pos, value):
            self[pos]=value
            


    def __init__(self, num_agents=2, num_fruits=3, window_dimension=616, spacing=22, init_size=3):
        self._running = True

        self._display_surf = None
        self._image_surf = None
        self._fruit_surf = None

        self.agents = []
        self.fruits = []
        self.num_agents = num_agents
        self.active_agents = num_agents
        self.num_fruits = num_fruits
        self.init_size = init_size

        self.window_dimension = window_dimension
        self.spacing = spacing
        self.grid_size = window_dimension/spacing

        assert self.window_dimension % self.spacing == 0, "window_dimension needs to be a multiple of spacing"

        self.max_spawn_idx = self.window_dimension / self.spacing - self.init_size
        for i in range(self.num_agents):
            agent = self._create_agent(i, self.init_size)
            self.agents.append(agent)


        # Initialize goals
        for f in range(num_fruits):
            self.fruits.append(self._generate_goal())


        self.reward_range = (-1.0, 1.0)

        self._pygame_init()


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def step(self, actions):
        new_obs = []
        killed_on_step = [False] * self.num_agents
        rewards = [0.0] * self.num_agents

        for i, move in enumerate(actions):
            if not self.agents[i].alive: continue
            self.agents[i].update(move)

        for i, s in enumerate(self.agents):
            # Did a snake eat an apple?
            if not self.agents[i].alive: continue
        
            for f_i, f in enumerate(self.fruits):
                if s.onSnake(f):
                    self.fruits[f_i] = self._generate_goal()
                    s.size=s.size+1
                    rewards[i] = 1.0

            # does snake hit a wall?
            if not s.inGrid(self.grid_size):
                killed_on_step[i] = True
                

            # does snake collide with another agent?
            for agent_i in range(len(self.agents)):
                if s.interSnake(agent_i):
                    killed_on_step[i]=True

        for i, k in enumerate(killed_on_step):
            if k:
                rewards[i] = -100.0
                self.active_agents -= 1
                self.agents[i].alive = False

        done = False
        if self.active_agents == 0:
            done = True

        for i in range(self.num_agents):
            ob = self._generate_obs(i)
            new_obs.append(ob)

        return deepcopy(new_obs), deepcopy(rewards), done, {}


    def render(self, mode='human'):
        if self._pygame_init() == False:
            self._running = False

        self._draw_env()

        for i, f in enumerate(self.fruits):
            self._pygame_draw(self._display_surf, self._fruit_surf, f)

        for i, s in enumerate(self.agents):
            if not self.agents[i].alive: 
                continue
            s._draw(self._display_surf, self._agent_surfs[s.color_i], self._agent_surfs[-1], self.spacing)

        pygame.display.flip()


    def reset(self):
        for i, p in enumerate(self.agents):
            self.killed[i] = False

            x = np.random.randint(1, self.max_spawn_idx - 1) * self.spacing
            y = np.random.randint(1, self.max_spawn_idx - 1) * self.spacing
            direction = np.random.randint(0, 1) # TODO: Fix vertical spawning

            p._reset(x, y, direction)

        for f in range(self.num_fruits):
            self.fruits[f] = self._generate_goal()

        self.active_agents = self.num_agents


    def close(self):
        pygame.quit()


    def _check_collision(self, x1, y1, x2, y2):
        bounding_box = 20

        if x1 >= x2 and x1 <= x2 + bounding_box:
            if y1 >= y2 and y1 <= y2 + bounding_box:
                return True

        return False


    def _create_agent(self, i, init_size):
        x = np.random.randint(init_size, self.grid_size - init_size) 
        y = np.random.randint(init_size, self.grid_size - init_size) 
        direction = np.random.randint(0, 4) # TODO: Fix Vertical spawning

        agent = self.Snake((x,y), direction=direction, size=init_size)
        agent.color_i = i % len(self.AGENT_COLORS)

        return deepcopy(agent)


    def _draw_env(self):
        self._display_surf.fill((0,0,0))

        for i in range(0, self.window_dimension, self.spacing):
            self._display_surf.blit(self._wall_surf, (0, i))
            self._display_surf.blit(self._wall_surf, (self.window_dimension - self.spacing, i))

        for i in range(0, self.window_dimension, self.spacing):
            self._display_surf.blit(self._wall_surf, (i, 0))
            self._display_surf.blit(self._wall_surf, (i, self.window_dimension - self.spacing))


    def _generate_goal(self):
        x = np.random.randint(0, self.grid_size) 
        y = np.random.randint(1, self.grid_size) 

        return (x, y)


    def _generate_obs(self, agent):
        obs = np.zeros((self.window_dimension, self.window_dimension))

        if self.killed[agent]: return -1 * np.ones((self.window_dimension, self.window_dimension))

        for i in range(self.agents[agent].size):
            obs[self.agents[agent].x[i]][self.agents[agent].y[i]] = 1

        for i, p in enumerate(self.agents):
            if self.killed[i]: continue
            for j in range(p.length):
                obs[p.x[j]][p.y[j]] = 2

        for i, f in enumerate(self.fruits):
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