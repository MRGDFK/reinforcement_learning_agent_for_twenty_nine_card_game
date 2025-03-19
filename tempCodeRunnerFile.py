# /home/arnob/Documents/test/twenty_nine/test_game.py
import sys
sys.path.insert(0, '/home/arnob/Documents/test/twenty_nine')

from rlcard.envs import make
from rlcard_custom.agents.random_agent import CustomRandomAgent  # Use custom agent
from rlcard_custom.envs.twenty_nine import TwentyNineEnv
from rlcard.envs.registration import register, registry

env_id = 'twenty-nine'
if env_id not in registry.env_specs:
    register(
        env_id=env_id,
        entry_point='rlcard_custom.envs.twenty_nine:TwentyNineEnv'
    )
    print(f"Registered environment: {env_id}")
else:
    print(f"Environment {env_id} already registered")

env = make('twenty-nine', config={'seed': 42})
agents = [CustomRandomAgent(num_actions=env.num_actions) for _ in range(4)]
env.set_agents(agents)

trajectories, payoffs = env.run()
print("Payoffs:", payoffs)