# from .player import TwentyNinePlayer
# from .dealer import TwentyNineDealer
# from .judger import TwentyNineJudger
# from .card import TwentyNineCard

# class TwentyNineGame:
#     def __init__(self):
#         self.players = [TwentyNinePlayer(i) for i in range(4)]
#         self.dealer = TwentyNineDealer()
#         self.current_trick = []
#         self.trump_suit = None
#         self.bidding_team = None
#         self.bid = None
#         self.current_player = 0
#         self.action_space = ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits] + \
#                             [str(card) for card in TwentyNineCard.get_deck()]
#         self.action_to_id = {action: i for i, action in enumerate(self.action_space)}

#     def get_num_actions(self):
#         return len(self.action_space)  # 85

#     def get_player_id(self):
#         return self.current_player

#     def init_game(self):
#         self.dealer.deal_cards(self.players)
#         self.current_player = 0
#         self.current_trick = []
#         self.trump_suit = None
#         self.bidding_team = None
#         self.bid = None
#         return self.get_state(self.current_player), self.current_player

#     def step(self, action):
#         if self.bidding_team is None:
#             if action == 'pass':
#                 self.current_player = (self.current_player + 1) % 4
#                 if self.current_player == 0:  # All passed
#                     self.bidding_team = 0
#                     self.bid = 16
#                     self.trump_suit = 'S'
#             else:
#                 self.bid = int(action[:-1])
#                 self.trump_suit = action[-1]
#                 self.bidding_team = self.current_player
#                 self.current_player = (self.current_player + 1) % 4
#         else:
#             card = self.players[self.current_player].play_card(action)
#             self.current_trick.append(card)
#             if len(self.current_trick) == 4:
#                 winner = TwentyNineJudger.judge_trick(self.current_trick, self.trump_suit)
#                 self.players[winner].add_trick(self.current_trick)
#                 self.current_trick = []
#                 self.current_player = winner
#             else:
#                 self.current_player = (self.current_player + 1) % 4

#         state = self.get_state(self.current_player)
#         # Return only state and next player ID, reward is handled by get_reward()
#         return state, self.current_player

#     def get_state(self, player_id):
#         return {
#             'hand': [str(card) for card in self.players[player_id].hand],
#             'trick': [str(card) for card in self.current_trick],
#             'trump': self.trump_suit,
#             'bidding_team': self.bidding_team,
#             'bid': self.bid,
#             'current_player': self.current_player
#         }

#     def get_legal_actions(self, player_id):
#         if self.bidding_team is None:
#             return ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits]
#         hand = self.players[player_id].hand
#         if not self.current_trick or not hand:
#             return [str(card) for card in hand]
#         lead_suit = self.current_trick[0].suit
#         return [str(card) for card in hand if card.suit == lead_suit] or [str(card) for card in hand]

#     def is_over(self):
#         return self.bidding_team is not None and all(len(p.hand) == 0 for p in self.players)

#     def get_reward(self):
#         if not self.is_over():
#             return 0
#         return TwentyNineJudger.judge_game(self.players, self.bidding_team, self.bid)

#     def get_num_players(self):
#         return 4



import logging
from .player import TwentyNinePlayer
from .dealer import TwentyNineDealer
from .judger import TwentyNineJudger
from .card import TwentyNineCard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game_log.txt'),  # Log to file
        logging.StreamHandler()               # Log to console
    ]
)

class TwentyNineGame:
    def __init__(self):
        self.players = [TwentyNinePlayer(i) for i in range(4)]
        self.dealer = TwentyNineDealer()
        self.current_trick = []
        self.trump_suit = None
        self.bidding_team = None
        self.bid = None
        self.current_player = 0
        self.action_space = ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits] + \
                            [str(card) for card in TwentyNineCard.get_deck()]
        self.action_to_id = {action: i for i, action in enumerate(self.action_space)}
        logging.info("Game initialized with 4 players and action space size: %d", len(self.action_space))

    def get_num_actions(self):
        return len(self.action_space)

    def get_player_id(self):
        return self.current_player

    def init_game(self):
        self.dealer.deal_cards(self.players)
        self.current_player = 0
        self.current_trick = []
        self.trump_suit = None
        self.bidding_team = None
        self.bid = None
        state = self.get_state(self.current_player)
        logging.info("Game started. Initial state for Player %d: %s", self.current_player, state)
        return state, self.current_player

    def step(self, action):
        logging.info("Player %d takes action: %s", self.current_player, action)
        if self.bidding_team is None:
            if action == 'pass':
                self.current_player = (self.current_player + 1) % 4
                if self.current_player == 0:  # All passed
                    self.bidding_team = 0
                    self.bid = 16
                    self.trump_suit = 'S'
                    logging.info("All players passed. Bidding team: %d, Bid: %d, Trump: %s", 
                                 self.bidding_team, self.bid, self.trump_suit)
            else:
                self.bid = int(action[:-1])
                self.trump_suit = action[-1]
                self.bidding_team = self.current_player
                self.current_player = (self.current_player + 1) % 4
                logging.info("Bid made: %d%s by Player %d. Trump: %s", 
                             self.bid, self.trump_suit, self.bidding_team, self.trump_suit)
        else:
            card = self.players[self.current_player].play_card(action)
            self.current_trick.append(card)
            logging.info("Player %d played card: %s. Current trick: %s", 
                         self.current_player, action, [str(c) for c in self.current_trick])
            if len(self.current_trick) == 4:
                winner = TwentyNineJudger.judge_trick(self.current_trick, self.trump_suit)
                self.players[winner].add_trick(self.current_trick)
                logging.info("Trick won by Player %d: %s", winner, [str(c) for c in self.current_trick])
                self.current_trick = []
                self.current_player = winner
            else:
                self.current_player = (self.current_player + 1) % 4

        state = self.get_state(self.current_player)
        logging.info("Next state for Player %d: %s", self.current_player, state)
        return state, self.current_player

    def get_state(self, player_id):
        return {
            'hand': [str(card) for card in self.players[player_id].hand],
            'trick': [str(card) for card in self.current_trick],
            'trump': self.trump_suit,
            'bidding_team': self.bidding_team,
            'bid': self.bid,
            'current_player': self.current_player
        }

    def get_legal_actions(self, player_id):
        actions = (['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits] 
                   if self.bidding_team is None else 
                   [str(card) for card in self.players[player_id].hand] 
                   if not self.current_trick or not self.players[player_id].hand else 
                   [str(card) for card in self.players[player_id].hand if card.suit == self.current_trick[0].suit] or 
                   [str(card) for card in self.players[player_id].hand])
        logging.info("Legal actions for Player %d: %s", player_id, actions)
        return actions

    def is_over(self):
        return self.bidding_team is not None and all(len(p.hand) == 0 for p in self.players)

    def get_reward(self):
        if not self.is_over():
            return 0
        reward = TwentyNineJudger.judge_game(self.players, self.bidding_team, self.bid)
        logging.info("Game ended. Reward: %d", reward)
        return reward

    def get_num_players(self):
        return 4