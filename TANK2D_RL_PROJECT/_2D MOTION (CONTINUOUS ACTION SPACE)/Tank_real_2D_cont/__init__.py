from gym.envs.registration import register

register(
    id='Tank_real_2D_cont-v1',
    entry_point='Tank_real_2D_cont.Tank_2D_cont.open_AI_env_2D_cont:customENV_tank',
    max_episode_steps=200000,
)