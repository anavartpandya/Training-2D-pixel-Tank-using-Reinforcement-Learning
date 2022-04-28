import gym
from gym import spaces
import numpy as np
import math
from Tank_real_2D_cont.Tank_2D_cont.env_2D_cont import Open_Ai, WIDTH, HEIGHT

class customENV_tank(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = Open_Ai()
        self.action_space = spaces.Box(np.array([-10,-1,0]), np.array([10,1,1]))  # action: [acceleration,steer,shoot]
        self.observation_space = spaces.Box(np.array([0,0,-math.inf,0,False,0,0,-math.inf,0,False]), np.array([WIDTH,HEIGHT,math.inf,100,True,WIDTH,HEIGHT,math.inf,100,True])) # [player_x, player_y, player_x_vel, player_y_vel, player_x_accl, player_y_accl, player_angle, player_health, enemy_x, enemy_y, enemy_x_vel, enemy_y_vel, enemy_x_accl, enemy_x_accl, enemy_angle, enemy_health]

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
        #if not close:
            #self.pygame.action(self.action)
            #self.pygame.view()
        self.pygame.view()
