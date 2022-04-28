import gym
from gym import spaces
import numpy as np
from Tank_real_1D.Tank_1D.env_1D import Open_Ai, HEIGHT

class customENV_tank(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = Open_Ai()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.array([0,0,0,0]), np.array([HEIGHT,100,HEIGHT,100]))
    
    def reset(self):
        del self.pygame
        self.pygame = Open_Ai()
        obs = self.pygame.observe()
        return obs
    
    def step(self, action):
        self.action = action
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}
    
    def render(self, mode='human', close = False):
        self.pygame.view()
