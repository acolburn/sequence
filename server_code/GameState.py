import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import Cards

deck = []
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
  # model = [{'url':'board', 'col':0, 'row':0}]
  model = []
  # If table isn't empty, load its contents into self.model
  # data_table=app_tables.board_state.search() # data_table is a SearchIterator
  data_table=app_tables.board_state.get(id=1)
  # Make sure there's a table to work with; at the start of a game there isn't
  # convert data_table to a list, see if the lists's length is 0
  # is_empty_data_table = len(list(data_table)) == 0
  if data_table['Board'] is not None:
    model = data_table['Board']
  # if not is_empty_data_table:
    # Table has only one row; access it as row[0]
    # for row in data_table:
      # temp = row[0] # temp is a list
      # temp[0] has value 'Board' (column name); temp[1] is the list of dicts that is self.model
      # model = temp[1]
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
  deck.clear()
  deck = Cards.make_decks()
  # _deck = Deck()
  # convert _deck to something serializable (deck, a list of strings)
  # for item in _deck.cards:
    # deck.append(item)
  update_cell(1,"Deck",deck)
  return deck 
    
@anvil.server.callable
def get_deck():
  global deck
  data_table=app_tables.board_state.get(id=1)
  if data_table['Deck'] is None:
    deck = make_deck()
  else:
    deck = data_table['Deck']
  return deck

# ----------------------------------------------------------------------------------------
# Functions Involving Hands
# ----------------------------------------------------------------------------------------
# @anvil.server.callable
def make_hand(player):
  # global green_hand
  # global blue_hand
  global deck
  # hand=[]
  # deck = get_deck()
  # _hand = Hand(deck)
  # for item in _hand.hand:
    # hand.append(item)

  # Cards.make_new_hand returns hand; if deck doesn't have 7 cards, returns []
  if len(deck)<7:
    deck = make_deck() #updates data_table
  hand = Cards.make_new_hand(deck)
  # if player=="green":
    # green_hand=hand
  # else:
    # blue_hand=hand
  col_name="GreenHand" if player=="green" else "BlueHand"
  update_cell(1,col_name,hand)
  # deck has also changed now, so it too needs to be updated
  update_cell(1,"Deck",deck)
  return hand
  
@anvil.server.callable
def get_hand(player):
  # global green_hand
  # global blue_hand
  global deck
  deck = get_deck()
  # data_table=app_tables.board_state.search()
  data_table=app_tables.board_state.get(id=1)
  if player=="green":
    if data_table['GreenHand'] is None:
      green_hand = make_hand("green")
    else:
      green_hand = data_table['GreenHand']
      # green_hand = Cards.update_hand(green_hand,deck)
    return green_hand
  if player=="blue":
    if data_table['BlueHand'] is None:
      blue_hand = make_hand("blue")
    else:
      blue_hand = data_table['BlueHand']
      # blue_hand = Cards.update_hand(blue_hand,deck)
    return blue_hand

@anvil.server.callable
def update_hand(player_color, hand):
  """Adds cards to assure proper hand length, updates data_table
  param string player = 'green' or 'blue', player color
  param list hand = player's hand, probably needing update at end of a play"""
  # global green_hand, blue_hand, deck
  global deck
  deck = get_deck()
  hand = Cards.update_hand(hand, deck)
  if len(hand)<7:
    deck=Cards.make_decks()
    Cards.update_hand(hand, deck)
  # while len(hand)<7:
  #   # Remove card from deck
  #   print(f'Length of deck: {len(deck)}')
  #   card=deck.pop() if len(deck)>0 else None
  #   # End of deck? Start over
  #   if card is None:
  #     print('Making deck, line 129')
  #     deck = make_deck()
  #     card=deck.pop()
  #   # Add card to hand
  #   hand.append(card)
  if player_color=="green":
    # green_hand=hand
    column_name="GreenHand"
  else:
    # blue_hand=hand
    column_name="BlueHand"
  # update data_table
  update_cell(1,column_name,hand)
  # update deck, too!
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
  # clear data table
  # app_tables.board_state.delete_all_rows()
  # add row
  # app_tables.board_state.add_row(id=1)
  # add new board to table
  # model = [{'url':'board', 'col':0, 'row':0}]
  global deck
  model = []
  update_cell(1,'Board',model)
  deck = Cards.make_decks()
  update_cell(1,'Deck',deck)
  make_hand("green") #update_cell() part of this method
  make_hand("blue") #update_cell() part of this method
  update_cell(1,'IsGreenTurn',True)
  
 