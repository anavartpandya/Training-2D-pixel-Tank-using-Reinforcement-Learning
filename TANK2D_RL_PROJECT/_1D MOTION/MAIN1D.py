import pygame

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.cmd_util import make_vec_env

import gym
from Tank_real_1D.Tank_1D.env_1D import Open_Ai , HEIGHT

env_name = 'Tank_real_1D-v1'
env = gym.make(env_name)

env = make_vec_env(env_name, n_envs=1, seed=0)

env = VecFrameStack(env, n_stack = 4)
 
#uncomment the next 3 and comment out the 4th line from here if you want to train the model again. The again comment the 3 lines and uncomment the 4th line to test your model. Note the the model path model.load(path) should be correct. 
#model = PPO("MlpPolicy", env, verbose=1)
#model.learn(total_timesteps=1000000)
#model.save('_1D MOTION\Trained Model_1D\PPO_tank_1D_1M_2_timesteps')
model = PPO.load('_1D MOTION\Trained Model_1D\PPO_tank_1D_1M_timesteps.zip', env = env)

#test the agent

clock = pygame.time.Clock()                   
obs = env.reset()

score_tot = 0
num_trials = 5
for i in range(num_trials):
    score = 0
    while True:
        action, _x = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        score += rewards
        if done == True:
            break
    print('Score: ' + str(score))
    env.close()
    score_tot += score
print('Avg Score = ' + str(score_tot/num_trials))
env.close()
