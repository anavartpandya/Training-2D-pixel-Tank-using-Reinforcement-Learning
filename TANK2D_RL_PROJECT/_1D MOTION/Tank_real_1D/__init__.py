from gym.envs.registration import register

register(
    id='Tank_real_1D-v1',
    entry_point='Tank_real_1D.Tank_1D.open_AI_env_1D:customENV_tank',
    max_episode_steps=200000,
)