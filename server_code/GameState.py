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
  # random.shuffle(deck)
  update_cell(1,"Deck",deck)

# def make_hand(player_color):
  # """param deck is list of cards
  # returns list of cards
  # If deck doesn't have at least [hand_length] cards, returns []"""
  # deck=get_deck()
  # hand=[]
  # hand_length=7
  # if len(deck)<7:
  #   deck=make_decks()
  # for i in range(hand_length):
  #     card=deck.pop()
  #     hand.append(card)
  # update_cell(1,"Deck",deck)
  # update_cell(1,"GreenHand",hand) if player_color=="green" else update_cell(1,"BlueHand",hand)
  

# ----------------------------------------------------------------------------------------
# Functions Involving Playing Board
# ----------------------------------------------------------------------------------------
@anvil.server.callable
def load_board():
  """Returns playing board (as dict type called `model`) retrieved from DataTable
  If no board in DataTable, creates a new one"""
  model = []
  # If table isn't empty, load its contents into self.model
  # data_table=app_tables.board_state.search() # data_table is a SearchIterator
  data_table=app_tables.board_state.get(id=1)
  if data_table['Board'] is not None:
    model = data_table['Board']
  else: #Board is empty, create new one
    update_cell(1,"Board",model)
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
  print('Starting GameState.get_deck')
  data_table=app_tables.board_state.get(id=1)
  if data_table['Deck'] is None:
    make_decks() # updates data_table
  deck = data_table['Deck']
  print(f'GameState.get_deck retrieved a deck. Length: {len(deck)}')
  return deck

# ----------------------------------------------------------------------------------------
# Functions Involving Hands
# ----------------------------------------------------------------------------------------
# @anvil.server.callable
def make_hand(player):
  print('Starting GameState.make_hand')
  # deck = get_deck()
  # print(f'GameState.make_hand about to create hand. Length: {len(deck)}')
  # hand, deck = Cards.make_new_hand(deck)  
  # col_name="GreenHand" if player=="green" else "BlueHand"
  # make_hand(player)
  # update_cell(1,col_name,hand)
  # deck has also changed now, so it too needs to be updated
  # update_cell(1,"Deck",deck)
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
  print(f'GameState.make_hand has created {player} hand. Deck length: {len(deck)}')
  return hand
  
@anvil.server.callable
def get_hand(player):
  print('Starting GameState.get_hand')
  data_table=app_tables.board_state.get(id=1)
  if player=="green":
    if data_table['GreenHand'] is None:
      green_hand = make_hand("green")
      print('GameState.get_hand just created a green_hand')
    else:
      green_hand = data_table['GreenHand']
    return green_hand
  if player=="blue":
    if data_table['BlueHand'] is None:
      blue_hand = make_hand("blue")
      print('GameState.get_hand just created a blue_hand')
    else:
      blue_hand = data_table['BlueHand']
    return blue_hand

@anvil.server.callable
def update_hand(player_color, hand):
  """Adds card to hand, update data_table
  param (string) player_color = 'green' or 'blue'
  param (list) hand = player's hand, needing update at end of a play"""
  print('Starting GameState.update_hand')
  deck = get_deck()
  # Make sure there's a card in the deck
  if len(deck)==0:
    deck = make_decks()
  print(f'GameState.update_hand deck length: {len(deck)}')
  #Python counts None as part of hand; first make sure there's seven slots
  while len(hand)<7:
    hand.append(None)
  #then fill the slots
  for i in range(7):
    if hand[i] is None:
      hand[i] = deck.pop()
  print(f'GameState.update_hand just updated_hand. Deck length: {len(deck)}')
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
  # print(f'new_game called make_decks. Length: {len(deck)}')
  make_hand("green") #update_cell() part of this method
  make_hand("blue") #update_cell() part of this method
  update_cell(1,'IsGreenTurn',True)
  
 