from gym.envs.registration import load_env_plugins as _load_env_plugins
from gym.envs.registration import register

# Hook to load plugins from entry points
_load_env_plugins()

register(
    id="DaskGame-v0",
    entry_point="games.dask_env:DaskEnv",
    max_episode_steps=200,
    reward_threshold=195.0,
)
