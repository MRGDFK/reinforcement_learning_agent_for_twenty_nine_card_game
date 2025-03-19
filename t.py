import random
import rlcard
from rlcard.envs import Env

# Define the deck with 32 cards
RANKS = ['J', '9', 'A', '10', 'K', 'Q', '8', '7']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
DECK = [f'{rank} of {suit}' for suit in SUITS for rank in RANKS]

# Points for each card
CARD_POINTS = {'J': 3, '9': 2, 'A': 1, '10': 1, 'K': 0, 'Q': 0, '8': 0, '7': 0}

class TwentyNineEnv(Env):
    def __init__(self, config=None):
        super().__init__(config)
        
        self.num_players = 4
        self.players = [{'hand': [], 'score': 0, 'bid': 0, 'marriage_declared': False} for _ in range(self.num_players)]
        self.deck = DECK.copy()
        self.state = None
        self.current_player = 0
        self.trump_suit = None
        self.highest_bid = 15
        self.bid_winner = None
        self.team_scores = {0: 0, 1: 0}  # Track scores for two teams
        self.double_called = False
        self.redouble_called = False
        self.pips = {0: 0, 1: 0}  # Track pip scores for both teams
        self.marriage_bonus = 0
        self.reset()

    def reset(self):
        self.deck = DECK.copy()
        random.shuffle(self.deck)
        self.deal_initial_cards()
        self.bidding_phase()
        self.state = self.get_state()
        return self.state

    def deal_initial_cards(self):
        # Deal 7 cards to each player
        for player in self.players:
            player['hand'] = [self.deck.pop(0) for _ in range(7)]

    def bidding_phase(self):
        # Handle the bidding phase
        self.highest_bid = 15
        self.bid_winner = None
        bids = [0, 0, 0, 0]

        for i in range(self.num_players):
            bid = random.randint(0, 28)  # Random bid for testing
            bids[i] = bid
            if bid > self.highest_bid:
                self.highest_bid = bid
                self.bid_winner = self.players[i]

        self.trump_suit = 'Spades'  # Example: Set the trump suit (could be chosen by the winner)

    def get_state(self):
        # Return the hands of each player as the state representation
        return [player['hand'] for player in self.players]

    def step(self, action):
        """
        Take a step in the game based on the action
        """
        player = self.players[self.current_player]
        card_played = player['hand'].pop(action)  # Player plays a card
        self.current_player = (self.current_player + 1) % self.num_players

        # Check if the game is over (e.g., after all players have played their cards)
        done = self.is_over()

        # Calculate payoffs (simplified for now)
        payoffs = [player['score'] for player in self.players]

        return self.get_state(), payoffs, done

    def is_over(self):
        # Game is over if all players have no cards left
        return all(len(player['hand']) == 0 for player in self.players)

    def get_payoffs(self):
        # For simplicity, just return a dummy payoff
        return [player['score'] for player in self.players]

