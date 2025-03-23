'''
    File name: rlcard_custom/games/twenty_nine/game.py
    Author: Arnob Das
    Date created: 18/03/2025
'''
import logging
from .player import TwentyNinePlayer
from .dealer import TwentyNineDealer
from .judger import TwentyNineJudger
from .card import TwentyNineCard

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('\Thesis_4732\game_log.txt'), logging.StreamHandler()]
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
        self.trick_count = 0
        self.bidding_phase = True
        self.bids = []  # Track bids during bidding phase
        self.action_space = ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits] + \
                            [str(card) for card in TwentyNineCard.get_deck()]
        self.action_to_id = {action: i for i, action in enumerate(self.action_space)}
        logging.info("Game initialized with 4 players and action space size: %d", len(self.action_space))

    def get_num_actions(self):
        return len(self.action_space)

    def get_player_id(self):
        return self.current_player

    def init_game(self):
        # Initial deal: 4 cards per player
        self.dealer.deal_cards(self.players, num_cards=4)
        self.current_player = 0
        self.current_trick = []
        self.trump_suit = None
        self.bidding_team = None
        self.bid = None
        self.bidding_phase = True
        self.bids = []
        state = self.get_state(self.current_player)
        logging.info("Game started. Initial state for Player %d: %s", self.current_player, state)
        return state, self.current_player

    def step(self, action):
        logging.info("Player %d takes action: %s", self.current_player, action)
        '''action_str = self.action_space[action]
        if self.bidding_phase:
            if action_str == 'pass':
                self.bids.append((self.current_player, 'pass', None))
            else:
                try:
                    bid_value = int(action[:-1])
                    suit = action[-1]
                    self.bids.append((self.current_player, bid_value, suit))
                except (ValueError, IndexError):
                    logging.warning("Invalid bid: %s, treating as pass", action_str)
                    self.bids.append((self.current_player, 'pass', None)) '''
        if self.bidding_phase:
            if action == 'pass':
                self.bids.append((self.current_player, 'pass', None))
            else:
                bid_value = int(action[:-1])
                suit = action[-1]
                self.bids.append((self.current_player, bid_value, suit))
            
            self.current_player = (self.current_player + 1) % 4
            # End bidding after all 4 players have acted
            if len(self.bids) == 4:
                # Find highest bid
                valid_bids = [(player, bid, suit) for player, bid, suit in self.bids if bid != 'pass']
                if not valid_bids:  # All passed
                    self.bidding_team = 0
                    self.bid = 16
                    self.trump_suit = 'S'
                    logging.info("All players passed. Default bid: 16S by Player 0")
                else:
                    winner_idx, highest_bid, trump = max(valid_bids, key=lambda x: x[1])
                    self.bidding_team = winner_idx
                    self.bid = highest_bid
                    self.trump_suit = trump
                    logging.info("Bidding ended. Highest bid: %d%s by Player %d", 
                                 self.bid, self.trump_suit, self.bidding_team)
                
                # Deal remaining 4 cards
                self.dealer.deal_cards(self.players, num_cards=4)
                self.bidding_phase = False
            
        else:  # Trick-taking phase
            card = self.players[self.current_player].play_card(action)
            card.player_id = self.current_player  # Attach player ID to card
            self.current_trick.append(card)
            logging.info("Player %d played card: %s. Current trick: %s", 
                         self.current_player, action, [str(c) for c in self.current_trick])
            
            if len(self.current_trick) == 4:
                winner = TwentyNineJudger.judge_trick(self.current_trick, self.trump_suit)
                self.players[winner].add_trick(self.current_trick)
                logging.info("Trick won by Player %d: %s", winner, [str(c) for c in self.current_trick])
                self.current_trick = []
                self.trick_count += 1
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
            'current_player': self.current_player,
            'bidding_phase': self.bidding_phase
        }

    def get_legal_actions(self, player_id):
        if self.bidding_phase:
            return ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits]
        hand = self.players[player_id].hand
        '''
        if not self.current_trick or not hand:
            return [str(card) for card in hand]
        lead_suit = self.current_trick[0].suit
        return [str(card) for card in hand if card.suit == lead_suit] or [str(card) for card in hand]
        '''
        if not hand or self.trick_count >= 8:
            return ['pass']
    
        if not self.current_trick:  # Leading the trick
            return [str(card) for card in hand]
    
        lead_suit = self.current_trick[0].suit
        lead_suit_cards = [str(card) for card in hand if card.suit == lead_suit]
    
        if lead_suit_cards:  # Must follow lead suit if possible
            logging.info("Player %d has lead suit cards: %s", player_id, lead_suit_cards)
            return lead_suit_cards
    
        trump_cards = [str(card) for card in hand if card.suit == self.trump_suit]
        if trump_cards:  # Play trump if no lead suit
            logging.info("Player %d has no lead suit, trump cards: %s", player_id, trump_cards)
            return trump_cards
    
        logging.info("Player %d has no lead suit or trump, all cards: %s", player_id, [str(card) for card in hand])
        return [str(card) for card in hand]
    
    def is_over(self):
        return not self.bidding_phase and all(len(p.hand) == 0 for p in self.players)

    def get_reward(self):
        if not self.is_over():
            return 0
        return TwentyNineJudger.judge_game(self.players, self.bidding_team, self.bid)

    def get_num_players(self):
        return 4