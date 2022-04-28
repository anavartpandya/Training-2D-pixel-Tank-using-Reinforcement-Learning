from gym.envs.registration import register

register(
    id='Tank_real_2D_dis-v1',
    entry_point='Tank_real_2D_dis.Tank_2D_dis.open_AI_env_2D_dis:customENV_tank',
    max_episode_steps=200000,
)