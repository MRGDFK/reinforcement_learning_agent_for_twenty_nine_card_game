# rlcard_custom/games/twenty_nine/card.py
class TwentyNineCard:
    """Represents a card in Twenty-Nine."""
    suits = ['S', 'H', 'C', 'D']  # Spades, Hearts, Clubs, Diamonds
    ranks = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']  # 7 to Ace
    points = {'7': 0, '8': 0, '9': 2, 'T': 1, 'J': 3, 'Q': 0, 'K': 0, 'A': 1}  # Point values

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.string = f"{rank}{suit}"  # e.g., "7S", "JH"

    def get_point(self):
        return self.points[self.rank]

    def __str__(self):
        return self.string

    @staticmethod
    def get_deck():
        return [TwentyNineCard(suit, rank) for suit in TwentyNineCard.suits for rank in TwentyNineCard.ranks]