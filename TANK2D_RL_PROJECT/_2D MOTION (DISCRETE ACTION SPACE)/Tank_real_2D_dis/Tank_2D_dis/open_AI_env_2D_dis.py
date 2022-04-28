import gym
from gym import spaces
import numpy as np
import math
from Tank_real_2D_dis.Tank_2D_dis.env_2D_dis import Open_Ai, WIDTH, HEIGHT

class customENV_tank(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = Open_Ai()
        self.action_space = spaces.Discrete(6)# action: [forward,backward,steer_left,steer_right,shoot,no-op]
        self.observation_space = spaces.Box(np.array([0,0,-math.inf,0,False,-math.inf,0,0,-math.inf,0,False]), np.array([WIDTH,HEIGHT,math.inf,100,True,math.inf,WIDTH,HEIGHT,math.inf,100,True])) 


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
    
    def render(self, mode='rgbarray', close = False):

        self.pygame.view()
