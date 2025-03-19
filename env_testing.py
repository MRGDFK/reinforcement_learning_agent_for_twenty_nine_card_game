import random

class RandomAgent:
    def __init__(self, num_actions):
        self.num_actions = num_actions

    def eval_step(self, state):
        return self.step(state)

    def step(self, state):
        # Choose a random action (i.e., a card to play)
        return random.randint(0, len(state[0]) - 1)  # Choose a random card index to play
