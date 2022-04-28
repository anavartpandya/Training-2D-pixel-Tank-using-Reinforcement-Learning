import pygame

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.cmd_util import make_vec_env

import gym
from Tank_real_2D_dis.Tank_2D_dis.env_2D_dis import Open_Ai

env_name = 'Tank_real_2D_dis-v1'
env = gym.make(env_name)
alpha = 1.3877787807814457e-16
env = make_vec_env(env_name, n_envs=1, seed=0)
env = VecFrameStack(env, n_stack = 4)

#uncomment the next 3 and comment out the 4th line from here if you want to train the model again. The again comment the 3 lines and uncomment the 4th line to test your model. Note the the model path model.load(path) should be correct. 
#model = PPO('MlpPolicy', env, verbose = 1, clip_range= 0.1*alpha, vf_coef=1, ent_coef=0.01, gamma=0.7, batch_size= 32*8, gae_lambda=0.95, n_epochs=3, learning_rate= (2.5e-4)*0.7, n_steps=128)
#model.learn(total_timesteps=10000000)
#model.save('_2D MOTION (DISCRETE ACTION SPACE)\Trained Model_2D_dis\PPO_2D_dis_10M_1_timesteps')
model = PPO.load('_2D MOTION (DISCRETE ACTION SPACE)\Trained Model_2D_dis\PPO_2D_dis_10M_timesteps.zip', env = env)

clock = pygame.time.Clock()    
obs = env.reset()
score_tot = 0
num_trials = 50
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
