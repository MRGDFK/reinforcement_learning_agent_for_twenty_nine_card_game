'''
    File name: rlcard_custom/games/twenty_nine/__init__.py
    Author: Arnob Das
    Date created: 18/03/2025
'''

from .card import TwentyNineCard
from .dealer import TwentyNineDealer
from .game import TwentyNineGame
from .judger import TwentyNineJudger
from .player import TwentyNinePlayer
from .utils import encode_observation  # We’ll define this in utils.py

# If ACTION_SPACE is needed, define it here or in utils.py
ACTION_SPACE = ['pass'] + [f"{bid}{suit}" for bid in range(16, 29) for suit in TwentyNineCard.suits]