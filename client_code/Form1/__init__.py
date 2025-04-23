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
    self.images = {
      'board': '_/theme/sequence_board.png',
      'flag': '_/theme/flag.png',
      'green_chip': '_/theme/chipGreen_border.png',
      'blue_chip': '_/theme/chipBlue_border.png'
    }
    self.labels=[self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7]
    
    self.deck = anvil.server.call('get_deck') # creates and shuffles deck, or loads current game deck state
    # Select whether player is green or blue; players must agree to choose different colors
    player_color = alert(content="Will you be the GREEN or BLUE player?",
               title="Select Color",
               large=True,
               buttons=[
                 ("GREEN", "green"),
                 ("BLUE", "blue"),
               ])

    self.green_hand = anvil.server.call('get_hand','green')
    self.blue_hand = anvil.server.call('get_hand','blue')
    self.is_green_turn = True # Green goes first
    self.update_hand_display(player_color) # Green goes first
    self.btn_player_turn.background=constants.GREEN
    self.flow_panel_1.background=constants.GREEN
    self.btn_player_turn.text="Green"
    
    for label in self.labels:
        label.background=constants.GREEN

    self.model = anvil.server.call('load_board')
    
    # canvas_size is width. 
    # iPad 5th gen is 2048x1536, 9th gen is larger
    self.canvas_size = 650
    self.canvas_1.height = 650 #64 px/cell, 10 cells

    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn

  def is_within_clickable_area(self, x, y):
    """
    Checks whether click is within canvas bounds
    param x: x-coordinate
    param y: y-coordinate
    """
    return(0<=x<=self.canvas_size) and (0<=y<=self.canvas_1.height)
    
  def card_color(self,card):
    if card[-1]==SPADES or card[1]==CLUBS:
      return "black"
    if card[-1]==HEARTS or card[-1]==DIAMONDS:
      return "red"

  # def deal_card(self, player):
  #   """Removes a card from the deck and adds it to a player's hand"""
  #   card=self.deck.deal()
  #   # End of deck? Start over
  #   if card is None:
  #     self.deck = Deck()
  #     card=self.deck.deal()
  #   player.hand.append(card.rank+card.suit)
  #   return card.rank+card.suit

  # def deal_hand(self, player):
  #   """
  #   Creates hand by dealing individual cards and adding them to 
  #   the hand (via self.deal_card()) and displaying the cards in labels in the GUI
  #   """
  #   player.hand.clear()
  #   #deal_card() appends card.rank+card.suit to player.hand
  #   #it returns card.rank+card.suit
  #   card=self.deal_card(player) 
  #   self.label_1.text = card
  #   self.label_1.foreground = self.card_color(card)
  #   card=self.deal_card(player)
  #   self.label_2.text = card
  #   self.label_2.foreground = self.card_color(card)
  #   card=self.deal_card(player)
  #   self.label_3.text = card
  #   self.label_3.foreground = self.card_color(card)
  #   card=self.deal_card(player)
  #   self.label_4.text = card
  #   self.label_4.foreground = self.card_color(card)
  #   card=self.deal_card(player)
  #   self.label_5.text = card
  #   self.label_5.foreground = self.card_color(card)
  #   card=self.deal_card(player)
  #   self.label_6.text = card
  #   self.label_6.foreground = self.card_color(card)
  #   card=self.deal_card(player)
  #   self.label_7.text = card
  #   self.label_7.foreground = self.card_color(card)

  def update_hand_display(self, player_color):
    """
    Makes seven card hand, adding additional card(s) 
    if the hand isn't full, i.e., after a card has been played during a turn.
    Parameter player_color (string) = "green" or "blue"
    """ 
    # hand = anvil.server.call('update_hand', player_color) 
    hand = self.green_hand if player_color=="green" else self.blue_hand
    for i in range(7):
      # card = player.get_hand()[i]
      card = hand[i]
      label = self.labels[i]
      label.text = card
      label.foreground = self.card_color(card)
    
    # # labels=[self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7]
    # for i in range(7):
    #   # if there's a card in self.hand at the given position,
    #   # display it
    #   # the items in self.hand each have card.rank+card.suit
    #   if len(player.hand)>i:
    #     card=player.hand[i]
    #     label=self.labels[i]
    #     label.text=card
    #     label.foreground=self.card_color(card)
    #   # and if there's no card at the given position,
    #   # deal one to fill the space
    #   else:
    #     card = self.deal_card(player) #addds card.rank+card.suit to self.hand
    #     label=self.labels[i]
    #     label.text=card
    #     label.foreground=self.card_color(card)
        
        
    
  def canvas_1_reset(self, **event_args):
    # Adjust these coordinates if you want the drawing area to not be centered
    # self.canvas_offset = (self.canvas_1.get_width() - self.canvas_size)/2
    # self.canvas_1.translate(self.canvas_offset, 0)

    # self.model is list of everything that needs to be drawn on canvas
    # 'url' codes what kind of image is being drawn (the board, a flag, or a chip)
    for item in self.model:
      if item['url']=='flag':
        x=item['col']*constants.IMAGE_WIDTH+7
        y=item['row']*constants.IMAGE_HEIGHT+7
      elif item['url']=='green_chip' or item['url']=='blue_chip':
        x=item['col']*constants.IMAGE_WIDTH+7
        y=item['row']*constants.IMAGE_HEIGHT+7
      elif item['url']=='board':
        x=0
        y=0
      self.canvas_1.draw_image(URLMedia(self.images[item['url']]), x, y)

  def draw_flag(self, location):
    # location is a tuple with two coordinates, one for column, one for row
    col=location[0]
    row=location[1]
    flag = {'url':'flag', 'col':col, 'row':row}
    self.model.append(flag) if flag not in self.model else None #preventing duplicate entries, which could result in flags getting drawn over and over

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
    hand=self.green_hand if player_color=="green" else self.blue_hand
    for card in hand:
      self.draw_flag_by_card(card)
    
  def remove_all_flags(self):
    # Use a list comprehension to filter out entries with 'url' equal to 'flag'
    self.model = [entry for entry in self.model if entry['url'] != 'flag']
    # Thank you, duck.ai :-)

  def is_cell_occupied(self, col, row):
    for item in self.model:
        if item['col'] == col and item['row'] == row:
            if item['url'] in ['green_chip', 'blue_chip']:
                return True
    return False
    # Thank you again, duck.ai

  def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
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
    
    hand=self.green_hand if self.is_green_turn else self.blue_hand
    # Cannot play corners
    if location==(0,0) or location==(9,0) or location==(0,9) or location==(9,9):
      alert("You cannot put a chip on a corner square")
      return
    # If player has card in hand matching square with chip, and there's no chip
    # already in the spot, remove the card from hand
    # and then play the chip
    if card in hand and not cell_occupied:
      hand.remove(card)
      self.model.append(green_chip) if self.is_green_turn else self.model.append(blue_chip)
    # If player's using a wild card in an empty square, remove the card from hand
    # and then play the chip
    elif 'J'+DIAMONDS in hand and not cell_occupied:
      alert('You are playing the J of Diamonds as a wild card')
      hand.remove('J'+DIAMONDS)
      self.model.append(green_chip) if self.is_green_turn else self.model.append(blue_chip)
    elif 'J'+HEARTS in hand and not cell_occupied:
      alert('You are playing the J of Hearts as a wild card')
      hand.remove('J'+HEARTS)
      self.model.append(green_chip) if self.is_green_turn else self.model.append(blue_chip)
    # Black Jacks used to remove chips; no chips _added_
    elif 'J'+SPADES in hand and cell_occupied:
      alert('You are playing the J of Spades to remove a chip')
      hand.remove('J'+SPADES)
      # Need to remove chip at [location]
      for item in self.model:
        if item['col'] == col and item['row'] == row:
            if item['url'] in ['green_chip', 'blue_chip']:
                self.model.remove(item)
    elif 'J'+CLUBS in hand and cell_occupied:
      alert ('You are using the J of Clubs to remove a chip')
      hand.remove('J'+CLUBS)
      # Need to remove chip at [location]
      for item in self.model:
        if item['col'] == col and item['row'] == row:
            if item['url'] in ['green_chip', 'blue_chip']:
                self.model.remove(item)  
    elif card in hand and cell_occupied:
      alert('You have a card in your hand matching this cell, but the cell\'s already occupied')
      return
    else:
      # If player's trying to put chip in an illegal spot, alert
      # them and then exit the method. Nothing else will happen, it'll still
      # be their turn.
      alert('You cannot put a piece in this square.')
      return
    
    self.remove_all_flags()
    self.change_player()
    # Save self.model to database
    anvil.server.call('save_board',self.model)
    # TODO Save hand to database
    self.canvas_1_reset()

  def change_player(self, **event_args):
    # TODO This ... including saving player turn to database
    self.is_green_turn = not self.is_green_turn
    player_color="green" if self.is_green_turn else "blue"
    self.update_hand_display(player_color)
    # change button text+color, and label colors
    # labels=[self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7]
    if self.is_green_turn:
      self.btn_player_turn.background='#8fef8f'
      self.flow_panel_1.background='#8fef8f'
      self.btn_player_turn.text="Green"
      for label in self.labels:
        label.background="#8fef8f"
    else:
      self.btn_player_turn.background='#a8c2e1'
      self.flow_panel_1.background='#a8c2e1'
      self.btn_player_turn.text="Blue"
      for label in self.labels:
        label.background="#a8c2e1"

  def btn_playable_cells_click(self, **event_args):
    """This method is called when the button is clicked"""
    player_color="green" if self.is_green_turn else "blue"
    self.draw_flags_for_hand(player_color) 
    self.canvas_1_reset()

  def btn_dead_card_click(self, **event_args):
    """This method is called when players claim they have a dead card"""
    # Whose turn is it?
    player_color="green" if self.is_green_turn else "blue"
    isDeadCard=False
    # Go through each card in player's hand
    for card in player.get_hand():
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
          print(f'Match for {card} at {cell1[0]},{cell1[1]}')
      # If first cell filled, see if second one is too
      if match1:
        for item in self.model:
          if item['col']==cell2[0] and item['row']==cell2[1] and item['url'] in ['green_chip','blue_chip']:
            alert(f'{card} is a dead card')
            player.remove_card(card)
            self.deal_card(player_color)
            isDeadCard=True
    if not isDeadCard:
      alert('No dead cards found')

  def btn_new_game_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('new_game')
    self.model = [{'url':'board', 'col':0, 'row':0}]
    self.canvas_1.reset_context()
            
        
          
    



    
   
    
  
    
  

  