# Create the environment and agents
from t import TwentyNineEnv
from rlcard.agents import RandomAgent
env = TwentyNineEnv()
agents = [RandomAgent(num_actions=7) for _ in range(4)]  # Assuming each player has 7 cards

# Set the agents in the environment
env.set_agents(agents)

# Run the game for 1 episode
state = env.reset()
done = False

while not done:
    action = random.randint(0, 6)  # Randomly select an action
    next_state, payoffs, done = env.step(action)
    print(f"State: {state}, Action: {action}, Payoffs: {payoffs}")
    state = next_state
