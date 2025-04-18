import random
import constants

class Card:
    """Represents a single playing card."""
    suits = [constants.HEARTS, constants.DIAMONDS, constants.CLUBS, constants.SPADES]
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    """Represents a deck of playing cards."""
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def deal(self):
        """Deals one card from the deck."""
        return self.cards.pop() if self.cards else None

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)