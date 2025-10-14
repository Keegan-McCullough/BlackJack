import random

# --- Constants and Basic Strategy Data ---

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
NUM_DECKS = 3

# Basic strategy tables (H=Hit, S=Stand, D=Double, P=Split)
# Player Hand Total vs. Dealer Up-Card
HARD_STRATEGY = {
    8: {2:'H', 3:'H', 4:'H', 5:'H', 6:'H', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    9: {2:'H', 3:'D', 4:'D', 5:'D', 6:'D', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    10: {2:'D', 3:'D', 4:'D', 5:'D', 6:'D', 7:'D', 8:'D', 9:'D', 10:'H', 11:'H'},
    11: {2:'D', 3:'D', 4:'D', 5:'D', 6:'D', 7:'D', 8:'D', 9:'D', 10:'D', 11:'D'},
    12: {2:'H', 3:'H', 4:'S', 5:'S', 6:'S', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    13: {2:'S', 3:'S', 4:'S', 5:'S', 6:'S', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    14: {2:'S', 3:'S', 4:'S', 5:'S', 6:'S', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    15: {2:'S', 3:'S', 4:'S', 5:'S', 6:'S', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    16: {2:'S', 3:'S', 4:'S', 5:'S', 6:'S', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
} # Totals of 17+ are always 'Stand'

SOFT_STRATEGY = {
    13: {2:'H', 3:'H', 4:'H', 5:'D', 6:'D', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'}, # A,2
    14: {2:'H', 3:'H', 4:'H', 5:'D', 6:'D', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'}, # A,3
    15: {2:'H', 3:'H', 4:'D', 5:'D', 6:'D', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'}, # A,4
    16: {2:'H', 3:'H', 4:'D', 5:'D', 6:'D', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'}, # A,5
    17: {2:'H', 3:'D', 4:'D', 5:'D', 6:'D', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'}, # A,6
    18: {2:'S', 3:'S', 4:'S', 5:'S', 6:'S', 7:'S', 8:'S', 9:'H', 10:'H', 11:'H'}, # A,7
} # Soft 19+ is always 'Stand'

SPLIT_STRATEGY = {
    'Ace': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'P', 8:'P', 9:'P', 10:'P', 11:'P'},
    '8': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'P', 8:'P', 9:'P', 10:'P', 11:'P'},
    '9': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'S', 8:'P', 9:'P', 10:'S', 11:'S'},
    '7': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'P', 8:'H', 9:'H', 10:'H', 11:'H'},
    '6': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    '5': {2:'D', 3:'D', 4:'D', 5:'D', 6:'D', 7:'D', 8:'D', 9:'D', 10:'H', 11:'H'}, # Never split 5s
    '4': {2:'H', 3:'H', 4:'H', 5:'P', 6:'P', 7:'H', 8:'H', 9:'H', 10:'H', 11:'H'},
    '3': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'P', 8:'H', 9:'H', 10:'H', 11:'H'},
    '2': {2:'P', 3:'P', 4:'P', 5:'P', 6:'P', 7:'P', 8:'H', 9:'H', 10:'H', 11:'H'},
    '10': {2:'S', 3:'S', 4:'S', 5:'S', 6:'S', 7:'S', 8:'S', 9:'S', 10:'S', 11:'S'}, # Never split 10s
}

# --- Core Game Classes ---

class Card:
    """Represents a single playing card."""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    def get_numeric_value(self):
        """Returns the integer value of the card."""
        if self.value in ['Jack', 'Queen', 'King']:
            return 10
        if self.value == 'Ace':
            return 11
        return int(self.value)

class Deck:
    """Represents the shoe of cards."""
    def __init__(self):
        self.cards = [Card(value, suit) for _ in range(NUM_DECKS) for suit in SUITS for value in VALUES]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) < 20: # Reshuffle when deck penetration is low
            self.__init__()
        return self.cards.pop()

class Player:
    """Represents a player at the table."""
    def __init__(self, is_dealer=False):
        self.hand = []
        self.is_dealer = is_dealer

    def add_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []
        
    def get_value(self):
        """Calculates the value of the hand, handling Aces correctly."""
        total = sum(card.get_numeric_value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.value == 'Ace')
        
        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1
        return total

    @property
    def is_soft(self):
        """Checks if the hand is soft (contains an Ace counted as 11)."""
        total = sum(card.get_numeric_value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.value == 'Ace')
        return total != self.get_value() and num_aces > 0


class Dealer(Player):
    """Represents the dealer, with specific rules."""
    def __init__(self):
        super().__init__(is_dealer=True)

    def get_up_card(self):
        return self.hand[0]

class Game:
    """Manages the logic for a single round of Blackjack."""
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()

    def _get_player_decision(self, hand, dealer_up_card_value):
        """Determines the player's move based on basic strategy."""
        player_value = self.player.get_value()
        
        # Check for splits first
        if len(hand) == 2 and hand[0].value == hand[1].value:
            return SPLIT_STRATEGY.get(hand[0].value, {}).get(dealer_up_card_value, 'H')

        # Soft hands
        if self.player.is_soft:
            if player_value >= 19: return 'S'
            return SOFT_STRATEGY.get(player_value, {}).get(dealer_up_card_value, 'H')
        
        # Hard hands
        if player_value >= 17: return 'S'
        if player_value <= 8: return 'H'
        return HARD_STRATEGY.get(player_value, {}).get(dealer_up_card_value, 'H')

    def play_round(self, bet_amount):
        """Plays one full round and returns the net winnings."""
        self.player.clear_hand()
        self.dealer.clear_hand()

        # Initial deal
        self.player.add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card()) # Dealer's up-card
        self.player.add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card()) # Dealer's hole card
        
        player_value = self.player.get_value()
        dealer_value = self.dealer.get_value()
        
        # Check for naturals (Blackjack)
        is_player_bj = player_value == 21 and len(self.player.hand) == 2
        is_dealer_bj = dealer_value == 21 and len(self.dealer.hand) == 2

        if is_player_bj and not is_dealer_bj:
            return bet_amount * 1.5 # Player Blackjack pays 3:2
        if is_dealer_bj and not is_player_bj:
            return -bet_amount
        if is_player_bj and is_dealer_bj:
            return 0 # Push

        # --- Player's Turn ---
        dealer_up_card_value = self.dealer.get_up_card().get_numeric_value()
        
        while True:
            player_value = self.player.get_value()
            if player_value > 21:
                return -bet_amount # Player busts

            decision = self._get_player_decision(self.player.hand, dealer_up_card_value)
            
            if decision == 'S': # Stand
                break
            elif decision == 'D': # Double Down
                # Note: True doubling down rules mean you only get one more card.
                # We assume the bet is doubled by the simulation manager.
                self.player.add_card(self.deck.draw_card())
                break
            elif decision == 'H': # Hit
                self.player.add_card(self.deck.draw_card())
            else: # Fallback to hit if something is wrong
                self.player.add_card(self.deck.draw_card())

        player_final_value = self.player.get_value()
        if player_final_value > 21:
            return -bet_amount

        # --- Dealer's Turn ---
        while self.dealer.get_value() < 17:
            self.dealer.add_card(self.deck.draw_card())
        
        dealer_final_value = self.dealer.get_value()

        # --- Determine Winner ---
        if dealer_final_value > 21 or player_final_value > dealer_final_value:
            return bet_amount
        elif player_final_value < dealer_final_value:
            return -bet_amount
        else:
            return 0 # Push