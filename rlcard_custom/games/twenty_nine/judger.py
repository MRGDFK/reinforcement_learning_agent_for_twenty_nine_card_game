# games/twenty_nine/judger.py
from .card import TwentyNineCard

class TwentyNineJudger:
    @staticmethod
    def judge_trick(cards_played, trump_suit):
        # Find the winning card: trumps beat non-trumps, highest rank wins within same suit
        lead_suit = cards_played[0].suit
        winning_card = cards_played[0]
        winner = 0
        for i, card in enumerate(cards_played[1:], 1):
            if card.suit == trump_suit and winning_card.suit != trump_suit:
                winning_card = card
                winner = i
            elif card.suit == trump_suit and winning_card.suit == trump_suit:
                if TwentyNineCard.ranks.index(card.rank) > TwentyNineCard.ranks.index(winning_card.rank):
                    winning_card = card
                    winner = i
            elif card.suit == lead_suit and winning_card.suit == lead_suit:
                if TwentyNineCard.ranks.index(card.rank) > TwentyNineCard.ranks.index(winning_card.rank):
                    winning_card = card
                    winner = i
        return winner

    @staticmethod
    def judge_game(players, bidding_team, bid):
        team_points = players[bidding_team].get_points() + players[(bidding_team + 2) % 4].get_points()
        return 1 if team_points >= bid else -1  # +1 for success, -1 for failure