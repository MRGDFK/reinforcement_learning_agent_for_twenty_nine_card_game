'''
    File name: rlcard_custom/envs/twenty_nine.py
    Author: Arnob Das
    Date created: 18/03/2025
'''

# from rlcard.envs import Env
# from rlcard_custom.games.twenty_nine.game import TwentyNineGame

# class TwentyNineEnv(Env):
#     def __init__(self, config):
#         self.name = 'twenty-nine'
#         self.game = TwentyNineGame()
#         super().__init__(config)
#         self.action_space = self.game.action_space  # For reference

#     def _extract_state(self, state):
#         # Get the current player's legal actions as strings (raw actions)
#         raw_legal_actions = self.game.get_legal_actions(self.game.current_player)
#         # Map legal action strings to their IDs
#         legal_action_ids = [self.game.action_to_id[action] for action in raw_legal_actions]
        
#         # Create the state dictionary
#         extracted_state = {
#             'hand': state['hand'],
#             'trick': state['trick'],
#             'trump': state['trump'] if state['trump'] else 'None',
#             'bidding_team': state['bidding_team'] if state['bidding_team'] is not None else -1,
#             'bid': state['bid'] if state['bid'] is not None else 0,
#             'current_player': state['current_player'],
#             'legal_actions': legal_action_ids,      # List of action IDs
#             'raw_legal_actions': raw_legal_actions  # List of raw action strings
#         }
#         return extracted_state

#     def _decode_action(self, action_id):
#         # Convert action ID to action string
#         return self.game.action_space[action_id]

#     def get_payoffs(self):
#         if not self.game.is_over():
#             return [0] * 4
#         reward = self.game.get_reward()
#         payoffs = [0] * 4
#         payoffs[self.game.bidding_team] = reward
#         payoffs[(self.game.bidding_team + 2) % 4] = reward
#         payoffs[(self.game.bidding_team + 1) % 4] = -reward
#         payoffs[(self.game.bidding_team + 3) % 4] = -reward
#         return payoffs


import logging
from rlcard.envs import Env
from rlcard_custom.games.twenty_nine.game import TwentyNineGame

class TwentyNineEnv(Env):
    def __init__(self, config):
        self.name = 'twenty-nine'
        self.game = TwentyNineGame()
        super().__init__(config)
        self.action_space = self.game.action_space
        logging.info("Environment initialized with action space size: %d", len(self.action_space))

    def _extract_state(self, state):
        raw_legal_actions = self.game.get_legal_actions(self.game.current_player)
        legal_action_ids = [self.game.action_to_id[action] for action in raw_legal_actions]
        extracted_state = {
            'hand': state['hand'],
            'trick': state['trick'],
            'trump': state['trump'] if state['trump'] else 'None',
            'bidding_team': state['bidding_team'] if state['bidding_team'] is not None else -1,
            'bid': state['bid'] if state['bid'] is not None else 0,
            'current_player': state['current_player'],
            'bidding_phase': state['bidding_phase'],
            'legal_actions': legal_action_ids,
            'raw_legal_actions': raw_legal_actions
        }
        logging.info("Extracted state for Player %d: %s", self.game.current_player, extracted_state)
        return extracted_state

    def _decode_action(self, action_id):
        action = self.game.action_space[action_id]
        logging.info("Decoded action ID %d to: %s", action_id, action)
        return action

    def get_payoffs(self):
        if not self.game.is_over():
            return [0] * 4
        reward = self.game.get_reward()
        payoffs = [0] * 4
        payoffs[self.game.bidding_team] = reward
        payoffs[(self.game.bidding_team + 2) % 4] = reward
        payoffs[(self.game.bidding_team + 1) % 4] = -reward
        payoffs[(self.game.bidding_team + 3) % 4] = -reward
        logging.info("Payoffs calculated: %s", payoffs)
        return payoffs