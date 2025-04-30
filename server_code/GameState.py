import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import Cards

# deck = []
# green_hand=[]
# blue_hand=[]
# is_green_turn=True

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
  deck=[]
  data_table=app_tables.board_state.get(id=1)
  if data_table['Deck'] is None:
    deck = Cards.make_decks()
    update_cell(1,'Deck',deck)
    print(f'GameState.get_deck made a new deck. Length: {len(deck)}')
  else:
    deck = data_table['Deck']
    print(f'GameState.get_deck retrieved a deck. Length: {len(deck)}')
  return deck

# ----------------------------------------------------------------------------------------
# Functions Involving Hands
# ----------------------------------------------------------------------------------------
# @anvil.server.callable
def make_hand(player):
  print('Starting GameState.make_hand')
  deck = get_deck()
  if len(deck)<7:
    deck = Cards.make_decks()
    update_cell(1,'Deck',deck)
    print(f'GameState.make_hand called Cards.make_decks. Length: {len(deck)}')
  print(f'GameState.make_hand about to create hand. Length: {len(deck)}')
  hand, deck = Cards.make_new_hand(deck)  
  col_name="GreenHand" if player=="green" else "BlueHand"
  update_cell(1,col_name,hand)
  # deck has also changed now, so it too needs to be updated
  update_cell(1,"Deck",deck)
  print(f'GameState.make_hand has created {col_name}. Deck length: {len(deck)}')
  return hand
  
@anvil.server.callable
def get_hand(player):
  print('GameState.get_hand started')
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
    else:
      blue_hand = data_table['BlueHand']
    return blue_hand

@anvil.server.callable
def update_hand(player_color, hand):
  """Adds cards to assure proper hand length, updates data_table
  param string player = 'green' or 'blue', player color
  param list hand = player's hand, probably needing update at end of a play"""
  # global green_hand, blue_hand, deck
  print('GameState.update_hand started')
  deck = get_deck()
  print(f'GameState.update_hand deck length: {len(deck)}')
  hand = Cards.update_hand(hand, deck)
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
  deck = Cards.make_decks()
  update_cell(1,'Deck',deck)
  print(f'new_game called make_decks. Length: {len(deck)}')
  make_hand("green") #update_cell() part of this method
  make_hand("blue") #update_cell() part of this method
  update_cell(1,'IsGreenTurn',True)
  
 