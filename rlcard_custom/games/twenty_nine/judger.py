from .card import TwentyNineCard

class TwentyNineJudger:
    @staticmethod
    def judge_trick(trick, trump_suit):
        # Card rank values specific to your Twenty-Nine rules
        rank_values = {'J': 11, '9': 10, 'A': 9, 'T': 8, 'K': 7, 'Q': 6, '8': 5, '7': 4}
        
        # Lead suit is the suit of the first card
        lead_suit = trick[0].suit
        
        # Find highest trump card, if any
        trump_cards = [(i, card) for i, card in enumerate(trick) if card.suit == trump_suit]
        if trump_cards:
            # Among trumps, highest rank wins
            winner_idx, _ = max(trump_cards, key=lambda x: rank_values[x[1].rank])
            return (trick[0].player_id + winner_idx) % 4
        
        # If no trumps, find highest card in lead suit
        lead_cards = [(i, card) for i, card in enumerate(trick) if card.suit == lead_suit]
        winner_idx, _ = max(lead_cards, key=lambda x: rank_values[x[1].rank])
        return (trick[0].player_id + winner_idx) % 4

    @staticmethod
    def judge_game(players, bidding_team, bid):
        # Point values: J=3, 9=2, A=1, T=1, others=0
        point_values = {'J': 3, '9': 2, 'A': 1, 'T': 1, 'K': 0, 'Q': 0, '8': 0, '7': 0}
        
        # Calculate total points for bidding team from tricks won
        team_points = 0
        for player in [players[bidding_team], players[(bidding_team + 2) % 4]]:
            for trick in player.tricks:
                for card in trick:
                    team_points += point_values.get(card.rank, 0)
        
        # Return 1 if bid met or exceeded, -1 if not
        return 1 if team_points >= bid else -1