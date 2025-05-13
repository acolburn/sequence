import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
# import Cards
import random
import constants


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
  deck = cards + cards
  random.shuffle(deck)
  random.shuffle(deck)
  update_cell(1,"Deck",deck)
  

# ----------------------------------------------------------------------------------------
# Functions Involving Playing Board
# ----------------------------------------------------------------------------------------
@anvil.server.callable
def load_board():
  """Returns playing board (as dict type called `model`) retrieved from DataTable
  If no board in DataTable, creates a new one"""
  model = []
  # If table isn't empty, load its contents into self.model
  data_table=app_tables.board_state.get(id=1)
  model = data_table['Board'] if data_table['Board'] is not None else update_cell(1,"Board",model)
  # if data_table['Board'] is not None:
  #   model = data_table['Board']
  # else: #Board is empty, create new one
  #   update_cell(1,"Board",model)
  return model
      
@anvil.server.callable
def save_board(model):
  """Save game board state, i.e., self.model
  :param model is self.model from Form1"""
  update_cell(1,"Board",model)



# ----------------------------------------------------------------------------------------
# Functions Involving Deck
# ----------------------------------------------------------------------------------------
    
@anvil.server.callable
def get_deck():
  """Gets deck (list) from data_table. If it can't find one, it creates a new deck."""
  data_table=app_tables.board_state.get(id=1)
  if data_table['Deck'] is None:
    make_decks() # updates data_table
  deck = data_table['Deck']
  return deck

# ----------------------------------------------------------------------------------------
# Functions Involving Hands
# ----------------------------------------------------------------------------------------
def make_hand(player):
  deck=get_deck()
  hand=[]
  hand_length=7
  if len(deck)<7:
    deck=make_decks()
  for i in range(hand_length):
      card=deck.pop(0)
      hand.append(card)
  update_cell(1,"Deck",deck)
  update_cell(1,"GreenHand",hand) if player=="green" else update_cell(1,"BlueHand",hand)
  return hand
  
@anvil.server.callable
def get_hand(player_color):
  data_table = app_tables.board_state.get(id=1)
  player_hands = {
    "green": "GreenHand",
    "blue": "BlueHand"
  }

  if player_color in player_hands:
    hand_key = player_hands[player_color]
    if data_table[hand_key] is None:
      return make_hand(player_color)
    else:
      return data_table[hand_key]

    return None  # or raise an exception if the player is invalid

# @anvil.server.callable
# def get_hand(player):
#   data_table=app_tables.board_state.get(id=1)
#   if player=="green":
#     if data_table['GreenHand'] is None:
#       green_hand = make_hand("green")
#     else:
#       green_hand = data_table['GreenHand']
#     return green_hand
#   if player=="blue":
#     if data_table['BlueHand'] is None:
#       blue_hand = make_hand("blue")
#     else:
#       blue_hand = data_table['BlueHand']
#     return blue_hand

@anvil.server.callable
def update_hand(player_color, hand):
  """Adds card to hand, update data_table
  param (string) player_color = 'green' or 'blue'
  param (list) hand = player's hand, needing update at end of a play"""
  deck = get_deck()
  # Make sure there's a card in the deck
  if len(deck)==0:
    deck = make_decks()
  #Python counts None as part of hand; first make sure there's seven slots
  while len(hand)<7:
    hand.append(None)
  #then fill the slots
  for i in range(7):
    if hand[i] is None:
      hand[i] = deck.pop()
  if player_color=="green":
    column_name="GreenHand"
  else:
    column_name="BlueHand"
  # update data_table
  update_cell(1,column_name,hand)
  # update deck
  update_cell(1,"Deck",deck)
  return hand # We updated green_hand or blue_hand in this module, and return hand for Form1 to display

# ----------------------------------------------------------------------------------------
# Functions Involving Turns
# ----------------------------------------------------------------------------------------

@anvil.server.callable
def green_turn():
  # global is_green_turn
  data_table=app_tables.board_state.get(id=1)
  if data_table['IsGreenTurn'] is None:
    is_green_turn = True
    data_table['IsGreenTurn'] = True
  else:
    is_green_turn = data_table['IsGreenTurn']
  return is_green_turn

@anvil.server.callable
def update_turn(is_green_turn):
  update_cell(1,"IsGreenTurn",is_green_turn)
  

# ----------------------------------------------------------------------------------------
# Other Code
# ----------------------------------------------------------------------------------------

@anvil.server.callable
def update_cell(row_id, column_name, new_value):
  # table has one row, with id=1
  row = app_tables.board_state.get(id=1)
  # validate data:
  if row:
    row[column_name]=new_value # direct modification
    return True
  return False

@anvil.server.callable
def update():
  return app_tables.board_state.get(id=1)

@anvil.server.callable
def new_game():
  """Starting new game"""
  model = []
  update_cell(1,'Board',model)
  make_decks()
  # deck=[]
  # update_cell(1,'Deck',deck)
  make_hand("green") #update_cell() part of this method
  make_hand("blue") #update_cell() part of this method
  update_cell(1,'IsGreenTurn',True)
  
 