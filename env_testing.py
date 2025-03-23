'''
    File name: env_testing.py
    Author: Arnob Das
    Date created: 18/03/2025
'''

'''
    Author: Sharjil
    Work : bidding bug fixed for twenty nine game.

'''

import random

class RandomAgent:
    def __init__(self, num_actions):
        self.num_actions = num_actions

    def eval_step(self, state):
        return self.step(state)

    def step(self, state):
        # Choose a random action (i.e., a card to play)
        return random.randint(0, len(state[0]) - 1)  # Choose a random card index to play
