import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .Cards import *

class Player:
  def __init__(self, deck):
    self.hand=Hand(deck)

  def update_hand(self):
    self.hand.update_hand()

  def get_hand(self):
    return self.hand.hand

  def remove_card(self, card):
    self.hand.remove_card(card)

  # def deal_card(self, player):
  #   """Removes a card from the deck and adds it to a player's hand"""
  #   card=self.deck.deal()
  #   # End of deck? Start over
  #   if card is None:
  #     self.deck = Deck()
  #     card=self.deck.deal()
  #   # player.hand.append(card.rank+card.suit)
  #   return card.rank+card.suit

  # def deal_hand(self):
  #   self.hand.clear()
  #   for i in range(7):
  #     card=self.deal_card()
  #     self.hand.append(card)

  # def update_hand(self):
  #   while len(self.hand)<7:
  #     card=self.deal_card()
  #     self.hand.append(card)
    