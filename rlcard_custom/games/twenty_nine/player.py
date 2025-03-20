'''
    File name: rlcard_custom/games/twenty_nine/player.py
    Author: Arnob Das
    Date created: 18/03/2025
'''

# # games/twenty_nine/player.py
# class TwentyNinePlayer:
#     def __init__(self, player_id):
#         self.player_id = player_id
#         self.hand = []
#         self.tricks_won = []  # Cards won in tricks

#     def play_card(self, card_str):
#         card = next(c for c in self.hand if str(c) == card_str)
#         self.hand.remove(card)
#         return card

#     def add_trick(self, trick):
#         self.tricks_won.extend(trick)

#     def get_points(self):
#         return sum(card.get_point() for card in self.tricks_won)

class TwentyNinePlayer:
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []
        self.tricks = []  # List of won tricks

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self, card_str):
        for i, card in enumerate(self.hand):
            if str(card) == card_str:
                return self.hand.pop(i)
        raise ValueError(f"Card {card_str} not in hand")

    def add_trick(self, trick):
        self.tricks.append(trick)