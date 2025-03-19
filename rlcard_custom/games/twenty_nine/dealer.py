# rlcard_custom/games/twenty_nine/dealer.py
import random
from .card import TwentyNineCard

class TwentyNineDealer:
    def __init__(self):
        self.deck = TwentyNineCard.get_deck()
        random.shuffle(self.deck)

    def deal_cards(self, players, num_cards=8):
        for player in players:
            for _ in range(num_cards):
                if self.deck:  # Ensure deck isn’t empty
                    player.add_card(self.deck.pop())