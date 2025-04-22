import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# Functions Involving Playing Board
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




