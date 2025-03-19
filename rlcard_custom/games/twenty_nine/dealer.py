# rlcard_custom/games/twenty_nine/dealer.py
import random
from .card import TwentyNineCard

class TwentyNineDealer:
    def __init__(self):
        self.deck = TwentyNineCard.get_deck()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_cards(self, players):
        self.shuffle()
        for i, card in enumerate(self.deck):
            players[i % 4].hand.append(card)