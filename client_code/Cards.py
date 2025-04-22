import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random
import constants

class Card:
    suits = [constants.HEARTS, constants.DIAMONDS, constants.CLUBS, constants.SPADES]
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        # Two decks
        self.cards = self.cards + self.cards
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def deal(self):
        """Deals one card from the deck."""
        return self.cards.pop() if self.cards else None

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class Hand:
  def __init__(self, deck):
    self.hand=[]
    self.hand_length=7
    self.deck=deck
    self.deal_hand() # create new hand

  def clear_hand(self):
    self.hand.clear()

  def deal_card(self):
    """Removes a card from the deck
    Returns card (rank+suit)"""
    card=self.deck.deal()
    # End of deck? Start over
    if card is None:
      self.deck = Deck()
      card=self.deck.deal()
    return card.rank+card.suit

  def deal_hand(self):
    self.hand.clear()
    for i in range(self.hand_length):
      card=self.deal_card()
      self.hand.append(card)

  def update_hand(self):
    while len(self.hand)<7:
      card=self.deal_card()
      self.hand.append(card)

  def remove_card(self,card):
    if card in self.hand:
      self.hand.remove(card)

  def card_in_hand(self,card):
    return card in self.hand
