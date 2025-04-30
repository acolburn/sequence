import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random
import constants

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
    deck=make_decks()
  for i in range(hand_length):
      card=deal_card(deck)
      hand.append(card)
  return hand, deck

# def update_hand(hand, deck):
  """Adds card(s) after a play.
  Hand and deck lists are parameters,
  returns hand list, deck list. If the deck is empty,
  makes a new deck."""
  # while len(hand)<7: ... can't do it this way; code is counting "None" as part of list's length
  # So, first, let's make sure there's 7 slots in the hand
  # while len(hand)<7:
  #   hand.append(None)
  # # Now, fill the slots
  # for i in range(7):
  #   if hand[i] is None:
  #     if deck is None:
  #       deck = make_decks()
  #     card=deal_card(deck)
  #     hand[i]=card
  # return hand, deck
