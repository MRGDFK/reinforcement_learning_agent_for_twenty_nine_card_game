'''
    File name: rlcard_custom/agents/random_agent.py
    Author: Arnob Das
    Date created: 18/03/2025
'''

import numpy as np
from rlcard.agents import RandomAgent as BaseRandomAgent

class CustomRandomAgent(BaseRandomAgent):
    def __init__(self, num_actions):
        super().__init__(num_actions=num_actions)

    def eval_step(self, state):
        legal_actions = state['legal_actions']  # Expecting a list
        probs = np.ones(len(legal_actions)) / len(legal_actions)
        action = np.random.choice(legal_actions)
        info = {
            'probs': {state['raw_legal_actions'][i]: probs[i] for i in range(len(legal_actions))}
        }
        return action, info