import random

# Define the deck with 32 cards
RANKS = ['J', '9', 'A', '10', 'K', 'Q', '8', '7']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
DECK = [f'{rank} of {suit}' for suit in SUITS for rank in RANKS]

# Points for each card
CARD_POINTS = {'J': 3, '9': 2, 'A': 1, '10': 1, 'K': 0, 'Q': 0, '8': 0, '7': 0}

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bid = 0
        self.points = 0
        self.marriage_declared = False

    def reset(self):
        self.hand = []
        self.bid = 0
        self.points = 0
        self.marriage_declared = False

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def calculate_hand_points(self):
        return sum(CARD_POINTS[card.split(' of ')[0]] for card in self.hand)

    def has_only_zero_point_cards(self):
        return all(CARD_POINTS[card.split(' of ')[0]] == 0 for card in self.hand)

    def has_marriage(self, trump_suit):
        has_king = any(card == f'K of {trump_suit}' for card in self.hand)
        has_queen = any(card == f'Q of {trump_suit}' for card in self.hand)
        return has_king and has_queen

    def place_bid(self, min_bid, max_bid=28):
        print(f"{self.name}'s current hand: {self.hand}")
        while True:
            try:
                bid = int(input(f"{self.name}, enter your bid (minimum {min_bid}, max {max_bid}, or pass 0): "))
                if bid == 0 or min_bid <= bid <= max_bid:
                    self.bid = bid
                    return self.bid
                else:
                    print("Invalid bid. Please enter a valid bid.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def play_card(self, round_suit, trump_suit, trump_revealed):
        print(f"{self.name}'s hand: {self.hand}")
        if round_suit and not any(card.endswith(round_suit) for card in self.hand):
            if not trump_revealed:
                print(f"{self.name} does not have {round_suit}. Trump suit {trump_suit} is now revealed!")
                trump_revealed = True
        while True:
            try:
                choice = int(input(f"{self.name}, choose a card to play (0-{len(self.hand)-1}): "))
                if 0 <= choice < len(self.hand):
                    return self.hand.pop(choice), trump_revealed
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input. Enter a number.")

# 29 Card Game class
class TwentyNineGame:
    def __init__(self):
        self.players = [Player(f'Player {i+1}') for i in range(4)]
        self.teams = [[self.players[0], self.players[2]], [self.players[1], self.players[3]]]
        self.trump_suit = None
        self.highest_bid = 15
        self.bid_winner = None
        self.deck = DECK.copy()
        self.trump_revealed = False
        self.team_scores = {0: 0, 1: 0}
        self.double_called = False
        self.redouble_called = False
        self.pips = {0: 0, 1: 0}
        self.marriage_bonus = 0
        self.start_game()

    def start_game(self):
        while abs(self.pips[0]) < 6 and abs(self.pips[1]) < 6:
            self.reset_game()
        print("\n--- Match Over ---")
        if self.pips[0] >= 6:
            print("Team 1 (Player 1 & 3) wins the match!")
        else:
            print("Team 2 (Player 2 & 4) wins the match!")

    def reset_game(self):
        for player in self.players:
            player.reset()
        self.deck = DECK.copy()
        random.shuffle(self.deck)

        while True:
            self.distribute_initial_cards()
            if self.check_initial_conditions():
                break
            random.shuffle(self.deck)
            for player in self.players:
                player.reset()

        self.bidding_phase()
        self.distribute_remaining_cards()

        if not self.check_full_hand_conditions():
            self.reset_game()
        else:
            self.ask_double_redouble()
            self.play_game()

    def distribute_initial_cards(self):
        for _ in range(4):
            for player in self.players:
                player.receive_cards([self.deck.pop(0)])

    def distribute_remaining_cards(self):
        for _ in range(4):
            for player in self.players:
                player.receive_cards([self.deck.pop(0)])

    def check_initial_conditions(self):
        if self.players[0].calculate_hand_points() == 0:
            print(f"{self.players[0].name} has no points in initial hand. Restarting game.")
            return False
        return True

    def check_full_hand_conditions(self):
        for player in self.players:
            if player.has_only_zero_point_cards():
                print(f"{player.name} has 8 zero-point cards. Restarting game.")
                return False
        return True

    def bidding_phase(self):
        print("\n--- Bidding Phase ---")
        highest_bid = 15
        bid_winner = None
        bids = [0, 0, 0, 0]

        while True:
            for i, player in enumerate(self.players):
                min_bid = highest_bid if highest_bid > 15 else 15
                bid = player.place_bid(min_bid, 28)
                bids[i] = bid
                if bid > highest_bid:
                    highest_bid = bid
                    bid_winner = player

            active_bids = [b for b in bids if b != 0]
            if len(active_bids) == 1:
                break

            pass_count = bids.count(0)
            if pass_count >= 3:
                break

        if bid_winner is None:
            print("Dealer is forced to bid 15.")
            self.highest_bid = 15
            self.bid_winner = self.players[3]
        else:
            self.highest_bid = highest_bid
            self.bid_winner = bid_winner
            self.trump_suit = input(f"{bid_winner.name}, choose a trump suit ({', '.join(SUITS)}): ")

    def ask_double_redouble(self):
        print("\n--- Double / Redouble Phase ---")
        opposing_team = self.teams[0] if self.bid_winner in self.teams[1] else self.teams[1]
        bidder_team = self.teams[0] if self.bid_winner in self.teams[0] else self.teams[1]

        response = input(f"{opposing_team[0].name} and {opposing_team[1].name}, do you want to DOUBLE the bid? (yes/no): ").lower()
        if response == 'yes':
            self.double_called = True
            response = input(f"{bidder_team[0].name} and {bidder_team[1].name}, do you want to REDOUBLE? (yes/no): ").lower()
            if response == 'yes':
                self.redouble_called = True

    def play_game(self):
        print("\n--- Game Starts ---")
        team_points = {0: 0, 1: 0}
        starter_index = self.players.index(self.bid_winner)

        for trick_number in range(8):
            print(f"\n--- Trick {trick_number + 1} ---")
            played_cards = []
            round_suit = None
            winning_card = None
            winning_player = None

            for i in range(4):
                player_index = (starter_index + i) % 4
                player = self.players[player_index]
                card, self.trump_revealed = player.play_card(round_suit, self.trump_suit, self.trump_revealed)
                rank, suit = card.split(' of ')

                if round_suit is None:
                    round_suit = suit
                played_cards.append((player, card, rank, suit))

                if winning_card is None:
                    winning_card = card
                    winning_player = player
                    winning_rank = rank
                    winning_suit = suit
                else:
                    winning_player, winning_card, winning_rank, winning_suit = self.compare_cards(
                        winning_player, winning_card, winning_rank, winning_suit,
                        player, card, rank, suit
                    )

            trick_points = sum(CARD_POINTS[rank] for _, _, rank, _ in played_cards)
            team_index = 0 if winning_player in self.teams[0] else 1
            team_points[team_index] += trick_points
            print(f"{winning_player.name} wins the trick and earns {trick_points} points.")

            self.check_marriage_declaration()

            starter_index = self.players.index(winning_player)

        self.determine_winner(team_points)

    def check_marriage_declaration(self):
        if self.trump_revealed:
            for team_index, team in enumerate(self.teams):
                for player in team:
                    if not player.marriage_declared and player.has_marriage(self.trump_suit):
                        declare = input(f"{player.name}, you have a marriage in {self.trump_suit}. Do you want to declare? (yes/no): ").lower()
                        if declare == 'yes':
                            player.marriage_declared = True
                            if player in self.teams[team_index]:
                                if player in self.teams[0] and self.bid_winner in self.teams[0]:
                                    self.marriage_bonus -= 4
                                    print("Marriage declared by bidding team! They need 4 fewer points to win (min 16).")
                                elif player in self.teams[1] and self.bid_winner in self.teams[1]:
                                    self.marriage_bonus -= 4
                                    print("Marriage declared by bidding team! They need 4 fewer points to win (min 16).")
                                else:
                                    self.marriage_bonus += 4
                                    print("Marriage declared by opponent team! Bidding team needs 4 more points to win (max 28).")

    def compare_cards(self, win_player, win_card, win_rank, win_suit, new_player, new_card, new_rank, new_suit):
        if self.trump_revealed:
            if new_suit == self.trump_suit:
                if win_suit != self.trump_suit or RANKS.index(new_rank) < RANKS.index(win_rank):
                    return new_player, new_card, new_rank, new_suit
            elif win_suit != self.trump_suit and new_suit == win_suit and RANKS.index(new_rank) < RANKS.index(win_rank):
                return new_player, new_card, new_rank, new_suit
        else:
            if new_suit == win_suit and RANKS.index(new_rank) < RANKS.index(win_rank):
                return new_player, new_card, new_rank, new_suit
        return win_player, win_card, win_rank, win_suit

    def determine_winner(self, team_points):
        print("\n--- Game Over ---")
        print(f"Team 1 (Player 1 & 3) points: {team_points[0]}")
        print(f"Team 2 (Player 2 & 4) points: {team_points[1]}")

        bidding_team_index = 0 if self.bid_winner in self.teams[0] else 1
        bidding_team_points = team_points[bidding_team_index]

        bid_value = self.highest_bid + self.marriage_bonus
        bid_value = max(16, min(28, bid_value))

        if self.double_called:
            bid_value *= 2
        if self.redouble_called:
            bid_value *= 2

        opponent_team_index = 1 - bidding_team_index

        if bidding_team_points >= bid_value:
            print(f"Team {bidding_team_index + 1} (Bidders) wins the round!")
            self.pips[bidding_team_index] += 1
        else:
            print(f"Team {bidding_team_index + 1} (Bidders) failed to reach their bid and loses the round!")
            self.pips[bidding_team_index] -= 1
            self.pips[opponent_team_index] += 1

        print(f"Current Pip Score - Team 1: {self.pips[0]} (Red: {max(0, self.pips[0])}, Black: {max(0, -self.pips[0])}), Team 2: {self.pips[1]} (Red: {max(0, self.pips[1])}, Black: {max(0, -self.pips[1])})")

if __name__ == "__main__":
    game = TwentyNineGame()
