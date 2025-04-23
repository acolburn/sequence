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
def update_board():
  """Returns playing board (as dict type called `model`) retrieved from DataTable
  If no board in DataTable, creates a new one"""
  model = [{'url':'board', 'col':0, 'row':0}]
  # If table isn't empty, load its contents into self.model
  data_table=app_tables.board_state.search() # data_table is a SearchIterator
  # Make sure there's a table to work with; at the start of a game there isn't
  # convert data_table to a list, see if the lists's length is 0
  is_empty_data_table = len(list(data_table)) == 0
  if not is_empty_data_table:
    # Table has only one row; access it as row[0]
    for row in data_table:
      temp = row[0] # temp is a list
      # temp[0] has value 'Board' (column name(?)); temp[1] is the list of dicts that is self.model
      model = temp[1]
      # TODO Table should include
  return model
      
@anvil.server.callable
def save_board(model):
  """Save game board state, i.e., self.model
  :param model is self.model from Form1"""
  app_tables.board_state.delete_all_rows()
  app_tables.board_state.add_row(Board=model)

@anvil.server.callable
def clear_board():
  """Starting new game"""
  app_tables.board_state.delete_all_rows()

# ----------------------------------------------------------------------------------------
# Functions Involving Deck
# ----------------------------------------------------------------------------------------
@anvil.server.callable
def make_deck():
  _deck = Deck()
  # convert _deck to something serializable (deck, a list of strings)
  for item in _deck.cards:
    deck.append(item)
  return deck # deck is global
    
@anvil.server.callable
# TODO load deck if it exists, or make new one if it's the start of a game
def get_deck():
  return deck

# ----------------------------------------------------------------------------------------
# Functions Involving Hands
# ----------------------------------------------------------------------------------------
@anvil.server.callable
def make_hand():
  hand=[]
  _hand = Hand(deck)
  for item in _hand.hand:
    hand.append(item)
  return hand
  
@anvil.server.callable
def get_hand(player):
  if player=="green":
    return green_hand
  if player=="blue":
    return blue_hand

@anvil.server.callable
def update_hand(player):
  _hand=green_hand if player=="green" else blue_hand
  while len(_hand)<7:
    # Remove card from deck
    card=deck.pop() if len(deck)>0 else None
    # End of deck? Start over
    if card is None:
      deck = make_deck()
      card=deck.pop()
    # Add card to hand
    _hand.append(card)
  return _hand # We updated green_hand or blue_hand in this module, and return hand for Form1 to display
  

# ----------------------------------------------------------------------------------------
# Initialization Code
# ----------------------------------------------------------------------------------------
def init():
  # Initialize deck
  # TODO Load deck from db
  global deck
  # deck = anvil.server.call('make_deck')
  deck = make_deck()
  # Initialize hands, convert to something seializable (green_hand, blue_hand: list of strings)
  # TODO Load hands from db
  global green_hand, blue_hand
  # green_hand=anvil.server.call('make_hand')
  green_hand=make_hand()
  # blue_hand=anvil.server.call('make_hand')
  blue_hand=make_hand()
  
  # Initialize turn
  # TODO Load turn from db
  is_green_turn=True

# call init when server starts
init()


  





