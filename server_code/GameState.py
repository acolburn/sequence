import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .Cards import Deck, Hand

deck = []
green_hand=[]
blue_hand=[]
is_green_turn=True





# ----------------------------------------------------------------------------------------
# Functions Involving Playing Board
# ----------------------------------------------------------------------------------------
@anvil.server.callable
def load_board():
  """Returns playing board (as dict type called `model`) retrieved from DataTable
  If no board in DataTable, creates a new one"""
  model = [{'url':'board', 'col':0, 'row':0}]
  # If table isn't empty, load its contents into self.model
  data_table=app_tables.board_state.search() # data_table is a SearchIterator
  # Make sure there's a table to work with; at the start of a game there isn't
  # convert data_table to a list, see if the lists's length is 0
  # is_empty_data_table = len(list(data_table)) == 0
  if data_table[0]['Board'] is not None:
  # if not is_empty_data_table:
    # Table has only one row; access it as row[0]
    for row in data_table:
      temp = row[0] # temp is a list
      # temp[0] has value 'Board' (column name); temp[1] is the list of dicts that is self.model
      model = temp[1]
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
# @anvil.server.callable
def make_deck():
  global deck
  _deck = Deck()
  # convert _deck to something serializable (deck, a list of strings)
  for item in _deck.cards:
    deck.append(item)
  update_cell(1,"Deck",deck)
  return deck 
    
@anvil.server.callable
def get_deck():
  global deck
  data_table=app_tables.board_state.search()
  if data_table[0]['Deck'] is None:
    make_deck()
  else:
    deck = data_table[0]['Deck']
  return deck

# ----------------------------------------------------------------------------------------
# Functions Involving Hands
# ----------------------------------------------------------------------------------------
# @anvil.server.callable
def make_hand(player):
  global green_hand
  global blue_hand
  hand=[]
  _hand = Hand(deck)
  for item in _hand.hand:
    hand.append(item)
  if player=="green":
    green_hand=hand
  else:
    blue_hand=hand
  col_name="GreenHand" if player=="green" else "BlueHand"
  update_cell(1,col_name,hand)
  return hand
  
@anvil.server.callable
def get_hand(player):
  global green_hand
  global blue_hand
  data_table=app_tables.board_state.search()
  
  if player=="green":
    if data_table[0]['GreenHand'] is None:
      green_hand = make_hand("green")
    else:
      green_hand = data_table[0]['GreenHand']
    return green_hand
  if player=="blue":
    if data_table[0]['BlueHand'] is None:
      blue_hand = make_hand("blue")
    else:
      blue_hand = data_table[0]['BlueHand']
    return blue_hand

@anvil.server.callable
def update_hand(player_color, hand):
  """Adds cards to assure proper hand length, updates data_table
  
  param string player = 'green' or 'blue', player color
  param list hand = player's hand, probably needing update at end of a play"""
  global green_hand, blue_hand, deck
  while len(hand)<7:
    # Remove card from deck
    card=deck.pop() if len(deck)>0 else None
    # End of deck? Start over
    if card is None:
      deck = make_deck()
      card=deck.pop()
    # Add card to hand
    hand.append(card)
    if player_color=="green":
      green_hand=hand
      column_name="GreenHand"
    else:
      blue_hand=hand
      column_name="BlueHand"
    # updaate data_table
    update_cell(1,column_name,hand)
  return hand # We updated green_hand or blue_hand in this module, and return hand for Form1 to display
  

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
def new_game():
  """Starting new game"""
  app_tables.board_state.delete_all_rows()
  
# def init():
#   # Initialize deck
#   # TODO Load deck from db
#   global deck
#   # deck = anvil.server.call('make_deck')
#   deck = get_deck() if len(deck)>0 else make_deck()
#   # Initialize hands, convert to something seializable (green_hand, blue_hand: list of strings)
#   # TODO Load hands from db
#   global green_hand, blue_hand
#   # green_hand=anvil.server.call('make_hand')
#   green_hand=get_hand("green")
#   if len(green_hand)==0:
#     green_hand=update_hand("green")
#   # blue_hand=anvil.server.call('make_hand')
#   blue_hand=get_hand("blue")
#   if len(blue_hand)==0:
#     blue_hand=update_hand("blue")
  
  # Initialize turn
  # TODO Load turn from db
  # is_green_turn=True

# call init when server starts
# init()


  





