import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .Cards import Deck

_deck = []

@anvil.server.callable
def make_deck():
  _deck = Deck()
  # convert _deck to something serializable
  result=[]
  for item in _deck.cards:
    result.append(item)
  return result

# Functions Involving Playing Board
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

# Functions Involving Hands





