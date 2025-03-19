# games/twenty_nine/player.py
class TwentyNinePlayer:
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []
        self.tricks_won = []  # Cards won in tricks

    def play_card(self, card_str):
        card = next(c for c in self.hand if str(c) == card_str)
        self.hand.remove(card)
        return card

    def add_trick(self, trick):
        self.tricks_won.extend(trick)

    def get_points(self):
        return sum(card.get_point() for card in self.tricks_won)