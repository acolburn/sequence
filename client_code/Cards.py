import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random
import constants

# class Card:
#     suits = [constants.HEARTS, constants.DIAMONDS, constants.CLUBS, constants.SPADES]
#     ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

#     def __init__(self, suit, rank):
#         self.suit = suit
#         self.rank = rank

#     def __str__(self):
#         return f"{self.rank}{self.suit}"

# class Deck:
suits = [constants.HEARTS, constants.DIAMONDS, constants.CLUBS, constants.SPADES]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
  
def make_decks():
  """ Makes two decks, shuffles the cards, returns deck.
  Cards are string objects, self.rank+self.suit"""
  cards=[]
  for suit in suits:
    for rank in ranks:
      card=f"{rank}{suit}"
      cards.append(card)
  # Two decks
  cards = cards + cards
  random.shuffle(cards)
  return cards

def deal_card(deck):
  """Deals one card from the deck.
  deck is a list of cards. 
  Returns one card, unless deck is empty in which case returns None"""
  return deck.pop() if len(deck)>0 else None

def make_new_hand(deck):
  """param deck is list of cards
  returns list of cards
  If deck doesn't have at least [hand_length] cards, returns []"""
  hand=[]
  hand_length=7
  if len(deck)<7:
    return hand
  for i in range(hand_length):
      card=deal_card(deck)
      hand.append(card)
  return hand

  # def deal_card(self):
  #   """Removes a card from the deck
  #   Returns card (rank+suit)"""
  #   # card=self.deck.deal()
  #   card=self.deck.pop() if len(self.deck)>0 else None
  #   # End of deck? Start over
  #   if card is None:
  #     self.deck = Deck()
  #     card=self.deck.deal()
  #   return card

# def deal_hand(self):
#   self.hand.clear()
#   for i in range(self.hand_length):
#     card=self.deal_card()
#     self.hand.append(card)

def update_hand(hand, deck):
  """Adds card(s) after a play.
  Hand and deck lists are parameters,
  returns hand list. If the deck is empty,
  returns hand as is."""
  while len(hand)<7:
    if deck is not None:
      card=deal_card(deck)
      hand.append(card)
  return hand

  # def remove_card(self,card):
  #   if card in self.hand:
  #     self.hand.remove(card)

  # def card_in_hand(self,card):
  #   return card in self.hand
