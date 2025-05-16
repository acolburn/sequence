from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .. import constants


import random


# @responsive.form
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.flag_model = []  # local variable to hold flag locations
    self.lines_model = []  # local variable to hold lines showing Sequences
    # using self.labels in self.mobile_screen_dimensions()
    self.labels = [
      self.label_1,
      self.label_2,
      self.label_3,
      self.label_4,
      self.label_5,
      self.label_6,
      self.label_7,
    ]
    # Find screen size for responsive layout
    # Load different size board and pieces if player is using small screen
    _mobile_screen_width = 650
    self.is_mobile = (
      True if anvil.js.window.innerWidth < _mobile_screen_width else False
    )
    

    self.message = {
      "your_turn": "It's your turn. Play whenever you're ready ...",
      "their_turn": "Waiting for your opponent to play ...",
    }

    # Select whether player is green or blue; players must agree to choose different colors
    self.player_color = alert(
      content="Will you be the GREEN or BLUE player?",
      title="Select Color",
      large=True,
      buttons=[
        ("GREEN", "green"),
        ("BLUE", "blue"),
      ],
    )
    self.mobile_screen_dimensions() if self.is_mobile else self.desktop_screen_dimensions()
    self.model = anvil.server.call("load_board")  # creates new board if not existing
    self.mark_sequences()
    self.hand = (
      anvil.server.call("get_hand", "green")
      if self.player_color == "green"
      else anvil.server.call("get_hand", "blue")
    )  # creates new hand if not existing
    self.is_green_turn = anvil.server.call("green_turn")
    self.display_turn_message()
    self.update_hand_display(self.hand)
    self.flow_panel_1.background = (
      constants.GREEN if self.player_color == "green" else constants.BLUE
    )
    for label in self.labels:
      label.background = (
        constants.GREEN if self.player_color == "green" else constants.BLUE
      )

    self.canvas_1.reset_context()  # must be called whenever canvas needs to be redrawn
    # turn timer ticker back on
    # variables are here to prevent mouse_down and update from happening
    # at same time, interfering with each other
    self.timer_1.interval = constants.TIMER_INTERVAL
    self.is_new_game = False

  def mobile_screen_dimensions(self):
    flag_img_path="_/theme/green_check_mark_small.png" if self.player_color=="green" else "_/theme/blue_check_mark_small.png"
    self.images = {
      "board": URLMedia("_/theme/sequence_board_320.png"),
      "flag": URLMedia(flag_img_path),
      "green_chip": URLMedia("_/theme/chipGreen_border_small.png"),
      "blue_chip": URLMedia("_/theme/chipBlue_border_small.png"),
    }
    self.IMAGE_WIDTH = 28
    self.IMAGE_HEIGHT = 28
    # canvas_size is width.
    # iPad 5th gen is 2048x1536, 9th gen is larger
    self.CANVAS_WIDTH = 288
    self.CANVAS_HEIGHT = 288
    self.canvas_size = self.CANVAS_WIDTH
    self.canvas_1.height = self.CANVAS_HEIGHT
    self.btn_dead_card.font_size = 12
    self.btn_new_game.font_size = 12
    self.btn_playable_cells.font_size = 12
    for label in self.labels:
      label.font_size = 16

  def desktop_screen_dimensions(self):
    # Preloading images helps prevent flicker when they're rendered on the Canvas
    flag_img_path="_/theme/green_check_mark.png" if self.player_color=="green" else "_/theme/blue_check_mark.png"
    self.images = {
      "board": URLMedia("_/theme/sequence_board.png"),
      "flag": URLMedia(flag_img_path),
      "green_chip": URLMedia("_/theme/chipGreen_border.png"),
      "blue_chip": URLMedia("_/theme/chipBlue_border.png"),
    }
    self.IMAGE_WIDTH = 64
    self.IMAGE_HEIGHT = 64
    # canvas_size is width.
    # iPad 5th gen is 2048x1536, 9th gen is larger
    self.CANVAS_WIDTH = 650
    self.CANVAS_HEIGHT = 650  # 64 px/cell, 10 cells
    self.canvas_size = self.CANVAS_WIDTH
    self.canvas_1.height = self.CANVAS_HEIGHT

  def is_within_clickable_area(self, x: int, y: int) -> bool:
    """
    Checks whether click is within canvas bounds
    param x: x-coordinate
    param y: y-coordinate
    """
    return (0 <= x <= self.canvas_size) and (0 <= y <= self.canvas_1.height)

  def card_color(self, card: str):
    return "black" if card[-1] in [constants.SPADES, constants.CLUBS] else "red"
    # if card[-1] == constants.SPADES or card[-1] == constants.CLUBS:
    #   return "black"
    # if card[-1] == constants.HEARTS or card[-1] == constants.DIAMONDS:
    # return "red"

  def update_hand_display(self, hand: list[str]):
    hand_length = len(hand)
    # (made this change b/c every once in awhile there's an error
    # IndexError: list index out of range. I think maybe this method is called
    # before data_table has fully updated hand?)
    for i in range(hand_length):
      card = hand[i]
      label = self.labels[i]
      label.text = card
      label.foreground = self.card_color(card)

  def canvas_1_reset(self, **event_args):
    # Adjust these coordinates if you want the drawing area to not be centered
    # self.canvas_offset = (self.canvas_1.get_width() - self.canvas_size)/2
    # self.canvas_1.translate(self.canvas_offset, 0)

    # self.model is list of everything that needs to be drawn on canvas
    # 'url' codes what kind of image is being drawn (the board, a flag, or a chip)
    path = None  # at start of game, when self.model=[], the for loop below goes through
    # an empty list, so the draw_image() method would generate an error without this line
    # and the code below because the variable path is unassigned
    # Draw board ... board's always drawn (first)
    self.canvas_1.draw_image(self.images["board"], 0, 0)
    # Draw chips
    for item in self.model:
      # if item["url"] == "green_chip" or item["url"] == "blue_chip":
      if item["url"] in ["green_chip", "blue_chip"]:
        path = (
          self.images["green_chip"]
          if item["url"] == "green_chip"
          else self.images["blue_chip"]
        )
        x, y = item["col"] * self.IMAGE_WIDTH + 7, item["row"] * self.IMAGE_HEIGHT + 7
      if path is not None:
        self.canvas_1.draw_image(path, x, y)
    # Draw flags
    path = None  # re-initialize variable
    for item in self.flag_model:
      if item["url"] == "flag":
        path = self.images["flag"]
        x, y = item["col"] * self.IMAGE_WIDTH + 7, item["row"] * self.IMAGE_HEIGHT + 7
      if path is not None:
        self.canvas_1.draw_image(path, x, y)
    # Draw lines
    for item in self.lines_model:
      # item[0] = start coordinate,
      # item[1] = end coordinate,
      # item[2] = player color to draw (green or blue)
      self.draw_line(item[0], item[1], item[2])

  def draw_line(self, start_location: list, end_location: list, player_color: str):
    displacement = 15 if self.is_mobile else 30
    line_width = 5 if self.is_mobile else 10
    self.canvas_1.stroke_style = "SteelBlue" if player_color == "blue" else "SeaGreen"

    self.canvas_1.begin_path()
    self.canvas_1.move_to(
      start_location[0] * self.IMAGE_WIDTH + displacement,
      start_location[1] * self.IMAGE_HEIGHT + displacement,
    )
    self.canvas_1.line_to(
      end_location[0] * self.IMAGE_WIDTH + displacement,
      end_location[1] * self.IMAGE_HEIGHT + displacement,
    )
    self.canvas_1.close_path()
    self.canvas_1.line_width = line_width
    self.canvas_1.stroke()

  def draw_flag(self, location: tuple):
    # location is a tuple with two coordinates, one for column, one for row
    col = location[0]
    row = location[1]
    flag = {"url": "flag", "col": col, "row": row}
    self.flag_model.append(
      flag
    ) if flag not in self.model else None  # preventing duplicate entries, which could result in flags getting drawn over and over

  def draw_flag_by_card(self, card: str):
    # card is a string representation of an individual playing card--card.rank+card.suit
    # locations (in constants) is dictionary with key=card.rank+card.suit (string), value=board locations for card (list of tuples)
    # locations[card] is the dictionary entry whose key=card parameter
    # the loop goes through both values in location
    for location in constants.locations[card]:
      self.draw_flag(location)

  def draw_flags_for_hand(self):
    # hand is a string list of card.ranks+card.suits in a player's hand
    for card in self.hand:
      self.draw_flag_by_card(card)

  def remove_all_flags(self):
    self.flag_model.clear()

  def is_cell_occupied(self, col: int, row: int) -> bool:
    for item in self.model:  # go through each item in the model
      if item["col"] == col and item["row"] == row:  # see if you can find one matching the given (col,row); if not, return False
        if item["url"] in ["green_chip", "blue_chip"]:  # if you do find one, make sure it's for a chip, not a flag; if it's a flag, return False
          return True  # you found an occupied cell, with a chip, at the given (col, row)
    return False

  def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    # Players can only play when it's their turn
    if not self.is_player_turn(): return
    # Turn off timer when it's your turn
    self.timer_1.interval = 0

    # Only respond to clicks/touches on the board itself, i.e., the clickable area
    if not self.is_within_clickable_area(x, y):
      self.reset_timer()
      return

    # Where did the player touch/click?
    location = self.get_location(x, y)  # location=(col,row) that were clicked
    # Validate location
    # if location is None:
    #   alert("Invalid location clicked; try again")
    #   self.reset_timer()
    #   return
    # What card is in that square?
    card = self.get_card_at_location(location)
    # Is something already in the square?
    cell_occupied = self.is_cell_occupied(location[0], location[1])
    # Cannot play corners
    if self.is_corner_square(location):
      alert("You cannot put a chip on a corner square")
      self.reset_timer()
      return

    try:
      if self.can_play_chip(card, cell_occupied):
        self.play_chip(card, location)  # removes card from deck, adds chip to self.model
      elif self.can_use_wild_card(cell_occupied):
        self.use_wild_card(location)  # playing red J in an empty square
      elif self.can_remove_chip(cell_occupied):
        self.remove_chip(location)  # playing black j
      elif card in self.hand and cell_occupied:
        alert("You have a card in your hand matching this cell, but the cell's already occupied")
        self.reset_timer()
        return  # turn's not over, player can click elsewhere
      else:
        alert("You cannot put a piece in this square.")
        self.reset_timer()
        return  # turn's not over, player can click elsewhere
    
        self.finalize_turn()
    except Exception as e:
      alert(f"An error occurred: {str(e)}")
      self.reset_timer()

  def is_player_turn(self):
    return (self.is_green_turn and self.player_color == "green") or (
      not self.is_green_turn and self.player_color == "blue"
    )

  def reset_timer(self):
    self.timer_1.interval = constants.TIMER_INTERVAL

  def get_location(self, x:int, y:int)->tuple:
    """Figure out the row and column values for the place on the screen that was touched/clicked"""
    row = y // self.IMAGE_HEIGHT
    col = x // self.IMAGE_WIDTH
    return (col, row)

  def get_card_at_location(self, location:tuple)->str:
    """Get card rank+suit for a given square (col, row) on the board"""
    for key, value in constants.locations.items():
      if location in value:
        return key
    return None

  def is_corner_square(self, location:tuple)->bool:
    return location in [(0, 0), (9, 0), (0, 9), (9, 9)]

  def can_play_chip(self, card:str, cell_occupied:bool)->bool:
    return card in self.hand and not cell_occupied

  def play_chip(self, card:str, location:tuple):
    self.hand.remove(card)
    # chip is the dictionary entry for self.model representing where
    # green_chip or blue_chip will go
    chip = {"url": f"{self.player_color}_chip", "col": location[0], "row": location[1]}
    self.model.append(chip)

  def can_use_wild_card(self, cell_occupied:bool)->bool:
    red_jacks = ["J" + constants.DIAMONDS, "J" + constants.HEARTS]
    for item in red_jacks:
      if item in self.hand and not cell_occupied:
        return alert(
          content=f"You are playing the {item} as a wild card. Continue?",
          title="Wild Card",
          large=True,
          buttons=[("Yes", True), ("No", False)],
        )

  def use_wild_card(self, location:tuple):
    # We alread know one of these cards is in hand
    J="J" + constants.DIAMONDS if "J" + constants.DIAMONDS in self.hand else "J" + constants.HEARTS
    self.play_chip(J, location)

  def can_remove_chip(self, cell_occupied:bool)->bool:
    black_jacks = ["J" + constants.SPADES, "J" + constants.CLUBS]
    for item in black_jacks:
      if item in self.hand and cell_occupied:
        return alert(
        content=f"You are playing the {item} to remove a chip. Bastard! Continue?",
        title="Remove a Chip",
        large=True,
        buttons=[("Yes", True), ("No", False)],
      )

  def remove_chip(self, location:tuple):
    card = "J" + constants.SPADES if "J" + constants.SPADES in self.hand else "J" + constants.CLUBS
    self.hand.remove(card)
    # keep everything in self.model except the value at location
    self.model = [item for item in self.model if not (item["col"] == location[0] and item["row"] == location[1])]

  def finalize_turn(self):
    self.remove_all_flags()
    anvil.server.call_s("save_board", self.model)
    self.canvas_1_reset()
    anvil.server.call_s("update_hand", self.player_color, self.hand)
    self.hand = anvil.server.call_s("get_hand", self.player_color)
    self.update_hand_display(self.hand)
    self.change_player()
    self.reset_timer()

  def change_player(self, **event_args):
    self.is_green_turn = not self.is_green_turn
    anvil.server.call_s("update_turn", self.is_green_turn)
    self.display_turn_message()

  def display_turn_message(self):
    if self.is_green_turn and self.player_color == "green":
      self.lbl_turn_message.text = self.message["your_turn"]
    elif self.is_green_turn and self.player_color == "blue":
      self.lbl_turn_message.text = self.message["their_turn"]
    elif not self.is_green_turn and self.player_color == "green":
      self.lbl_turn_message.text = self.message["their_turn"]
    elif not self.is_green_turn and self.player_color == "blue":
      self.lbl_turn_message.text = self.message["your_turn"]
    else:
      self.lbl_turn_message = "It's no one's turn right now. Hmm ..."

  def btn_playable_cells_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.draw_flags_for_hand()
    self.canvas_1_reset()

  def btn_dead_card_click(self, **event_args):
    """This method is called when players claim they have a dead card"""
    isDeadCard = False
    # Go through each card in player's hand
    for card in self.hand:
      match1 = False
      # ID the board cells for the given card
      if card[0] == "J":
        continue  # ignore Jacks; they're never dead cards
      if card[0] != "J":
        cell1 = constants.locations[card][0]
        cell2 = constants.locations[card][1]
      # See if both cells are occupied
      for item in self.model:
        # cell1[0] is col, cell1[1] is row
        if item["col"] == cell1[0] and item["row"] == cell1[1] and item["url"] in ["green_chip", "blue_chip"]:
          match1 = True
      # If first cell filled, see if second one is too
      if match1:
        for item in self.model:
          if (
            item["col"] == cell2[0]
            and item["row"] == cell2[1]
            and item["url"] in ["green_chip", "blue_chip"]
          ):
            alert(f"{card} is a dead card")
            self.hand.remove(card)
            anvil.server.call("update_hand", self.player_color, self.hand)
            self.hand = anvil.server.call("get_hand", self.player_color)
            self.update_hand_display(self.hand)
            isDeadCard = True
    if not isDeadCard:
      alert("No dead cards found")

  def btn_new_game_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call("new_game")  # clears board, creates new row, includes empty board
    self.model = []
    self.hand.clear()
    self.hand = anvil.server.call("get_hand", self.player_color)
    self.update_hand_display(self.hand)
    self.is_new_game = True  # set this for one time exception re: running self.update() whether or not it's your turn
    self.update()

  def update(self):
    # Update only happens when it's not your turn
    if (
      (self.is_green_turn and self.player_color == "blue")
      or (not self.is_green_turn and self.player_color == "green")
      or (self.is_new_game)
    ):
      # is_new_game exists so we can run update() at the start of the game, for both players, to update their displays
      # but after that one update, we don't want it to run when it's a player's turn
      if self.is_new_game:
        self.is_new_game = False
      with anvil.server.no_loading_indicator:
        game_state = anvil.server.call("update")
        if game_state is None:
          return
        if self.player_color == "green":
          if game_state["GreenHand"] != self.hand:
            self.hand = anvil.server.call("get_hand", "green")
        if self.player_color == "blue":
          if game_state["BlueHand"] != self.hand:
            self.hand = anvil.server.call("get_hand", "blue")
        if game_state["Board"] != self.model:
          self.model = game_state[
            "Board"
          ]  # doing this clears flags, too, even if it's mid-play
        if game_state["IsGreenTurn"] != self.is_green_turn:
          self.is_green_turn = game_state["IsGreenTurn"]

      self.display_turn_message()
      self.update_hand_display(self.hand)
      self.mark_sequences()
      self.canvas_1_reset()

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.update()

  def mark_sequences(self):
    self.lines_model.clear()
    self.sequence_check("green")
    self.sequence_check("blue")

  def sequence_check(self, player_color:str):
    """Checks for row, column, and diagonal Sequences for one player color, green or blue"""
    _matches = []
    chip = "green_chip" if player_color == "green" else "blue_chip"
    # _matches lists all the self.model entries for the player's chips
    for item in self.model:
      if item["url"] == chip:
        _matches.append(item)

    # _locations (inside methods) reduces _matches to [col, row] for each entry
    # start with corners
    _locations = [[0, 0], [9, 0], [9, 9], [0, 9]]
    _row_sequences = self.find_sequences(_matches, _locations, 5, True)
    _col_sequences = self.find_sequences(_matches, _locations, 5, False)
    _diag_sequences = self.find_diagonal_sequences(_matches)
    _total = [_row_sequences] + [_col_sequences] + [_diag_sequences]
    # _total has nested structure, lists inside lists ... unpack:
    for item in _total:  # one item for rows, one for cols, one for diags
      if len(item) == 1:
        # print(f'start: {item[0][0]}, end: {item[0][-1]}')
        t = (
          item[0][0],
          item[0][-1],
          player_color,
        )  # tuple with coordinates to start drawing, end drawing, and color to draw
        self.lines_model.append(t)
      elif len(item) > 1:  # more than one set of rows, or cols, or diags sequences
        for subitem in item:
          # print(f'start: {subitem[0]}, end: {subitem[-1]}')
          t = (
            subitem[0],
            subitem[-1],
            player_color,
          )  # tuple with coordinates to start drawing, end drawing, and color to draw
          self.lines_model.append(t)

  def find_diagonal_sequences(self, _matches):
    # Make _locations be in form [col, row] again
    # Convert to set for faster lookup operations
    _locations = [[0, 0], [9, 0], [9, 9], [0, 9]]
    for item in _matches:
      loc = [item["col"], item["row"]]
      _locations.append(loc)
    _locations = sorted(_locations)
    _locations_set = set(tuple(loc) for loc in _locations)
    diagonals = []

    # Check for top-left to bottom-right diagonals
    for col in range(10):  # Columns from 0 to 9
      for row in range(10):  # Rows from 0 to 9
        # Check if we can form a diagonal starting from (col, row)
        diagonal = []
        for i in range(5):
          if (col + i, row + i) in _locations_set:
            diagonal.append([col + i, row + i])
          else:
            break
          if len(diagonal) == 5:
            diagonals.append(diagonal)

    # Check for bottom-left to top-right diagonals
    for col in range(10):  # Columns from 0 to 9
      for row in range(10):  # Rows from 0 to 9
        # Check if we can form a diagonal starting from (col, row)
        diagonal = []
        for i in range(5):
          if (col + i, row - i) in _locations_set:
            diagonal.append([col + i, row - i])
          else:
            break
          if len(diagonal) == 5:
            diagonals.append(diagonal)

    # print(f'Diagonal sequence: {diagonals}')
    return diagonals

    """
    I wrote code to find row sequences and code sequences, then asked AI to refactor to [this] single function
    Parameters
    ----------
      matches: The list of matches to process (will always be _matches).
      initial_locations: The initial list of locations (will be the four corners).
      count_threshold: The minimum number of chips required to consider a row or column (will always be 5)
      is_row_check: A boolean indicating whether to check for rows (True) or columns (False).
    """

  def find_sequences(self, matches, initial_locations, count_threshold, is_row_check):
    # if not is_row_check: print('*****************This is a column check!***************************')
    return_list = []
    # Initialize locations
    _locations = initial_locations.copy()

    # Reduce dictionary items to list of tuples showing just row and col for each chip
    for item in matches:
      loc = [item["row"], item["col"]] if is_row_check else [item["col"], item["row"]]
      _locations.append(loc)

      # Sort locations
    _locations = sorted(_locations)
    # print(f'_locations: {_locations}')

    # Count occurrences in either rows or columns
    # Only need to pay attention to rows/cols with at least 5 chips
    count_dict = {}
    for item in _locations:
      key = item[0]  # row if is_row_check is True, else column
      if key not in count_dict:
        count_dict[key]=0
      count_dict[key]+=1
    # print(f'count_dict: {count_dict}')
    matches_list = []
    for key, value in count_dict.items():
      # print(f'Key: {key}, value: {value}')
      if value >= count_threshold:  # if there's more than 5 chips in row/col
        for item in _locations:  # go through all the chip locations
          if item[0] == key:  # and if a location is in a row/col with at least 5 chips
            matches_list.append(item)  # add it to this list
        # print(f'matches_list: {matches_list}')
      # Make a list with just the col values (for a row with 5 chips) or row values (for a col with 5 chips)
      sequence_check_list = [item[1] for item in matches_list]
      # Now find out if they're sequential
      # print(f'sequence_check_list: {sequence_check_list}')
      result = []
      for i in range(len(sequence_check_list) - 4):
        if all(
          sequence_check_list[i + j] + 1 == sequence_check_list[i + j + 1]
          for j in range(4)
        ):
          result.append(sequence_check_list[i : i + 5])
          # print(f'result.append; seq_check_list[i]={sequence_check_list[i]}, [i+5]={sequence_check_list[i+4]}')
        matches_list.clear()

      if result:
        # print(f'result: {result}'), e.g., [[4,5,6,7,8],[5,6,7,8,9]] if there are two sequences in given row/column
        # result[0]=[4,5,6,7,8,] ... result[1]=[5,6,7,8]
        for i in range(0,len(result)):
          result_locations = [[item, key] for item in result[i]] if is_row_check else [[key, item] for item in result[i]]
          return_list.append(result_locations)
          # if is_row_check:
          #   result_locations = [[item, key] for item in result[i]]
          #   return_list.append(result_locations)
          #   # print(f"Row sequence: {result_locations}")
          #   # return result_locations
          # else:
          #   result_locations = [[key, item] for item in result[i]]
          #   return_list.append((result_locations))
          #   # print(f"Column sequence: {result_locations}")

    return return_list
