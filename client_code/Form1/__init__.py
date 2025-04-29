from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..constants import *
from ..Cards import *
# from ..Player import *
import random


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Preloading images helps prevent flicker when they're rendered on the Canvas
    self.images = {
      'board': URLMedia('_/theme/sequence_board.png'),
      'flag': URLMedia('_/theme/flag.png'),
      'green_chip': URLMedia('_/theme/chipGreen_border.png'),
      'blue_chip': URLMedia('_/theme/chipBlue_border.png')
    }
    # turn off update during __init__
    # self.timer_1.interval=constants.TIMER_INTERVAL
    
    self.message = {
      'your_turn': 'It\'s your turn. Play whenever you\'re ready ...',
      'their_turn': 'Waiting for your opponent to play ...'
    }
    self.labels=[self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7]
    
    # Select whether player is green or blue; players must agree to choose different colors
    self.player_color = alert(content="Will you be the GREEN or BLUE player?",
               title="Select Color",
               large=True,
               buttons=[
                 ("GREEN", "green"),
                 ("BLUE", "blue"),
               ])
    self.model = anvil.server.call('load_board') # creates new board if not existing
    self.flag_model = [] # local variable to hold flag locations
    # self.deck = anvil.server.call('get_deck') # creates and shuffles deck, or loads current game deck state
    if self.player_color=="green":
      self.hand = anvil.server.call('get_hand','green') # creates hand if not existing
    else:
      self.hand = anvil.server.call('get_hand','blue')
    self.is_green_turn = anvil.server.call('green_turn')
    self.display_turn_message()
    self.update_hand_display(self.hand)
    self.flow_panel_1.background=constants.GREEN if self.player_color=="green" else constants.BLUE
    for label in self.labels:
        label.background=constants.GREEN if self.player_color=="green" else constants.BLUE

    # canvas_size is width. 
    # iPad 5th gen is 2048x1536, 9th gen is larger
    self.canvas_size = 650
    self.canvas_1.height = 650 #64 px/cell, 10 cells

    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn
    # turn timer ticker back on
    self.timer_1.interval=constants.TIMER_INTERVAL

  def is_within_clickable_area(self, x, y):
    """
    Checks whether click is within canvas bounds
    param x: x-coordinate
    param y: y-coordinate
    """
    return(0<=x<=self.canvas_size) and (0<=y<=self.canvas_1.height)
    
  def card_color(self,card):
    if card[-1]==SPADES or card[-1]==CLUBS:
      return "black"
    if card[-1]==HEARTS or card[-1]==DIAMONDS:
      return "red"

  def update_hand_display(self, hand):
    """
    Makes seven card hand, adding additional card(s) 
    if the hand isn't full, i.e., after a card has been played during a turn.
    Parameter player_color (string) = "green" or "blue"
    """ 
    # hand = self.green_hand if self.player_color=="green" else self.blue_hand
    for i in range(7):
      # card = player.get_hand()[i]
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
    path = None # at start of game, when self.model=[], the for loop below goes through
    # an empty list, so the draw_image() method would generate an error without this line
    # and the code below because the variable path is unassigned
    # self.timer_1.interval=0
    # Draw board ... board's always drawn (first)
    self.canvas_1.draw_image((URLMedia('_/theme/sequence_board.png')),0,0)
    for item in self.model:
      # if item['url']=='flag':
      #   path = '_/theme/flag.png'
      #   x=item['col']*constants.IMAGE_WIDTH+7
      #   y=item['row']*constants.IMAGE_HEIGHT+7
      if item['url']=='green_chip' or item['url']=='blue_chip':
        path = self.images['green_chip'] if item['url']=='green_chip' else self.images['blue_chip']
        x=item['col']*constants.IMAGE_WIDTH+7
        y=item['row']*constants.IMAGE_HEIGHT+7
      # elif item['url']=='board':
      #   path = '_/theme/sequence_board.png'
      #   x=0
      #   y=0
      # self.canvas_1.draw_image(URLMedia(self.images[item['url']]), x, y)
      if path is not None:
        self.canvas_1.draw_image(path,x,y)
    path=None #re-initialize variable
    for item in self.flag_model:
      if item['url']=='flag':
        path = self.images['flag']
        x=item['col']*constants.IMAGE_WIDTH+7
        y=item['row']*constants.IMAGE_HEIGHT+7
      if path is not None:
        self.canvas_1.draw_image(path,x,y)
    # self.timer_1.interval=constants.TIMER_INTERVAL

  def draw_flag(self, location):
    # location is a tuple with two coordinates, one for column, one for row
    col=location[0]
    row=location[1]
    flag = {'url':'flag', 'col':col, 'row':row}
    self.flag_model.append(flag) if flag not in self.model else None #preventing duplicate entries, which could result in flags getting drawn over and over

  def draw_flag_by_card(self, card):
   # card is a string representation of an individual playing card--card.rank+card.suit
    # locations (in constants) is dictionary with key=card.rank+card.suit (string), value=board locations for card (list of tuples)
    # locations[card] is the dictionary entry whose key=card parameter
    # the loop goes through both values in location
    for location in locations[card]:
      self.draw_flag(location)

  def draw_flags_for_hand(self, player_color):
    # hand is a list of card.ranks+card.suits in a player's hand
    # print(f'Drawing: {player.hand}')
    # hand=self.green_hand if player_color=="green" else self.blue_hand
    for card in self.hand:
      self.draw_flag_by_card(card)
    
  def remove_all_flags(self):
    # Use a list comprehension to filter out entries with 'url' equal to 'flag'
    # self.model = [entry for entry in self.model if entry['url'] != 'flag']
    # Thank you, duck.ai :-)
    self.flag_model.clear()

  def is_cell_occupied(self, col, row):
    for item in self.model:
        if item['col'] == col and item['row'] == row:
            if item['url'] in ['green_chip', 'blue_chip']:
                return True
    return False
    # Thank you again, duck.ai

  def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    if self.is_green_turn and self.player_color=="blue":
      alert("It looks like you are the blue player, and it's green's turn. Sorry, blue dude. You gotta' wait.")
      return
    if not self.is_green_turn and self.player_color=="green":
      alert("It looks like you are the green player, and it's blue's turn. Sorry, green dude. You gotta' wait.")
      return
    # self.timer_1.interval=0
    if not self.is_within_clickable_area(x,y):
      return
    # row and col are 0-based; upper left corner is (0,0)
    row = y//constants.IMAGE_HEIGHT
    col = x//constants.IMAGE_WIDTH
    # Which cell was clicked?
    location=(col,row)
    # What card.rank+card.suit was clicked?
    for key,value in locations.items():
      if location in value:
        card=key
    # We need to check whether there's already a chip at the selected location
    cell_occupied = self.is_cell_occupied(col, row)
    # Here are the dictionary entries for self.model representing where
    # the green or blue chips will go
    green_chip = {'url':'green_chip', 'col':col, 'row':row}
    blue_chip = {'url':'blue_chip', 'col':col, 'row':row}
    
    # hand=self.green_hand if self.is_green_turn else self.blue_hand
    # Cannot play corners
    if location==(0,0) or location==(9,0) or location==(0,9) or location==(9,9):
      alert("You cannot put a chip on a corner square")
      return
    # If player has card in hand matching square with chip, and there's no chip
    # already in the spot, remove the card from hand
    # and then play the chip
    if card in self.hand and not cell_occupied:
      self.hand.remove(card)
      self.model.append(green_chip) if self.player_color=="green" else self.model.append(blue_chip)
    # If player's using a wild card in an empty square, remove the card from hand
    # and then play the chip
    elif 'J'+DIAMONDS in self.hand and not cell_occupied:
      result = alert(content='You are playing the J of Diamonds as a wild card. Continue?',
               title="Wild Card",
               large=True,
               buttons=[
                 ("Yes", True),
                 ("No", False),
               ])
      if result:
        self.hand.remove('J'+DIAMONDS)
        self.model.append(green_chip) if self.player_color=="green" else self.model.append(blue_chip)
      else:
        return
    elif 'J'+HEARTS in self.hand and not cell_occupied:
      result = alert(content='You are playing the J of Hearts as a wild card. Continue?',
               title="Wild Card",
               large=True,
               buttons=[
                 ("Yes", True),
                 ("No", False),
               ])
      if result:
        self.hand.remove('J'+HEARTS)
        self.model.append(green_chip) if self.player_color=="green" else self.model.append(blue_chip)
      else:
        return
    # Black Jacks used to remove chips; no chips _added_
    elif 'J'+SPADES in self.hand and cell_occupied:
      result = alert(content='You are playing the J of Spades to remove a chip. Bastard! Continue?',
               title="Remove a Chip",
               large=True,
               buttons=[
                 ("Yes", True),
                 ("No", False),
               ])
      if result:
        self.hand.remove('J'+SPADES)
        # Need to remove chip at [location]
        for item in self.model:
          if item['col'] == col and item['row'] == row:
              if item['url'] in ['green_chip', 'blue_chip']:
                  self.model.remove(item)
      else:
        return   
    elif 'J'+CLUBS in self.hand and cell_occupied:
      result = alert(content='You are playing the J of Clubs to remove a chip. Bastard! Continue?',
               title="Remove a Chip",
               large=True,
               buttons=[
                 ("Yes", True),
                 ("No", False),
               ])
      if result:
        self.hand.remove('J'+CLUBS)
        # Need to remove chip at [location]
        for item in self.model:
          if item['col'] == col and item['row'] == row:
              if item['url'] in ['green_chip', 'blue_chip']:
                  self.model.remove(item) 
      else:
        return
    elif card in self.hand and cell_occupied:
      alert('You have a card in your hand matching this cell, but the cell\'s already occupied')
      return
    else:
      # If player's trying to put chip in an illegal spot, alert
      # them and then exit the method. Nothing else will happen, it'll still
      # be their turn.
      alert('You cannot put a piece in this square.')
      return
    
    self.remove_all_flags()
    #Let's turn off update() while contacting server
    # self.timer_1.interval=0
    # Save self.model to database, redraw board
    anvil.server.call_s('save_board',self.model)
    self.canvas_1_reset()
    # Save hand to database, redraw hand
    self.hand = anvil.server.call_s('update_hand',self.player_color,self.hand)
    self.update_hand_display(self.hand)
    
    self.change_player()

    # self.timer_1.interval=constants.TIMER_INTERVAL

  def change_player(self, **event_args):
    # self.timer_1.interval=0
    self.is_green_turn = not self.is_green_turn
    anvil.server.call_s('update_turn',self.is_green_turn)
    # player_color="green" if self.is_green_turn else "blue"
    self.display_turn_message()
    # self.timer_1.interval=constants.TIMER_INTERVAL

  def display_turn_message(self):
    if self.is_green_turn and self.player_color=="green":
      self.lbl_turn_message.text=self.message['your_turn']
    elif self.is_green_turn and self.player_color=="blue":
      self.lbl_turn_message.text=self.message['their_turn']
    elif not self.is_green_turn and self.player_color=="green":
      self.lbl_turn_message.text=self.message['their_turn']
    elif not self.is_green_turn and self.player_color=="blue":
      self.lbl_turn_message.text=self.message['your_turn']
    else:
      self.lbl_turn_message="It's no one's turn right now. Hmm ..."

    

  def btn_playable_cells_click(self, **event_args):
    """This method is called when the button is clicked"""
    player_color="green" if self.is_green_turn else "blue"
    self.draw_flags_for_hand(player_color) 
    self.canvas_1_reset()

  def btn_dead_card_click(self, **event_args):
    """This method is called when players claim they have a dead card"""
    # Whose turn is it?
    # player_color="green" if self.is_green_turn else "blue"
    # hand=self.green_hand if self.is_green_turn else self.blue_hand
    isDeadCard=False
    # Go through each card in player's hand
    for card in self.hand:
      match1=False
      # ID the board cells for the given card
      if card[0]!='J':
        cell1=locations[card][0]
        cell2=locations[card][1]
      # See if both cells are occupied
      for item in self.model:
        #cell1[0] is col, cell1[1] is row
        if item['col']==cell1[0] and item['row']==cell1[1] and item['url'] in ['green_chip','blue_chip']:
          match1=True
      # If first cell filled, see if second one is too
      if match1:
        for item in self.model:
          if item['col']==cell2[0] and item['row']==cell2[1] and item['url'] in ['green_chip','blue_chip']:
            alert(f'{card} is a dead card')
            self.hand.remove(card)
            self.hand =anvil.server.call('update_hand',self.player_color,self.hand)
            self.update_hand_display(self.hand)
            isDeadCard=True
    if not isDeadCard:
      alert('No dead cards found')

  def btn_new_game_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Pause self.update() while this method taking place
    # self.timer_1.interval = 0
    anvil.server.call('new_game') # clears board, creates new row, includes empty board
    # self.model = [{'url':'board', 'col':0, 'row':0}]
    self.model=[]
    # self.update()
    self.hand = anvil.server.call('get_hand',self.player_color)
    self.update_hand_display(self.hand)
    self.canvas_1.reset_context()
    # Turn timer back on 
    # self.timer_1.interval=constants.TIMER_INTERVAL
    

  def update(self):
    with anvil.server.no_loading_indicator: 
      game_state = anvil.server.call('update')
      if game_state is None:
        return
      if self.player_color=="green":
        if game_state['GreenHand']!=self.hand:
          self.hand = anvil.server.call('update_hand',"green",self.hand)
      else:
        if game_state['BlueHand']!=self.hand:
          self.hand = anvil.server.call('update_hand',"blue",self.hand)
      if game_state['Board'] != self.model:
        self.model = game_state['Board'] # doing this clears flags, too, even if it's mid-play
      if game_state['IsGreenTurn']!=self.is_green_turn:
        self.is_green_turn = game_state['IsGreenTurn']
    
    self.display_turn_message()
    # if self.player_color=="green" and self.is_green_turn:
    #   self.draw_flags_for_hand(self.player_color) # add flags back to board
    # if self.player_color=="blue" and not self.is_green_turn:
    #   self.draw_flags_for_hand((self.player_color))
    self.update_hand_display(self.hand)
    self.canvas_1_reset()
    

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.update()
            
        
          
    



    
   
    
  
    
  

  