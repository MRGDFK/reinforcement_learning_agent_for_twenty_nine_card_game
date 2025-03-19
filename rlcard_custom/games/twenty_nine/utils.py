# rlcard_custom/games/twenty_nine/utils.py
from .card import TwentyNineCard

def get_card_by_string(card_str):
    """Convert a card string (e.g., '7S') to a TwentyNineCard object."""
    rank, suit = card_str[:-1], card_str[-1]
    return TwentyNineCard(suit, rank)

def is_valid_card(card_str):
    """Check if a card string is valid."""
    if len(card_str) != 2:
        return False
    rank, suit = card_str[:-1], card_str[-1]
    return suit in TwentyNineCard.suits and rank in TwentyNineCard.ranks

def list_all_cards():
    """Return a list of all card strings."""
    return [str(card) for card in TwentyNineCard.get_deck()]

def encode_observation(state):
    """Encode the game state for RL agents."""
    return {
        'hand': state['hand'],
        'trick': state['trick'],
        'trump': state['trump'] if state['trump'] else 'None',
        'bidding_team': state['bidding_team'] if state['bidding_team'] is not None else -1,
        'bid': state['bid'] if state['bid'] is not None else 0,
        'current_player': state['current_player']
    }

# Define ACTION_SPACE if __init__.py needs it
ACTION_SPACE = ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits]