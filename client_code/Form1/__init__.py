from ._anvil_designer import Form1Template
from anvil import *
from ..constants import *
from ..Cards import *
from ..Player import *
import random


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.player_green=Player()
    self.player_blue=Player()
    self.deck = Deck() # creates and shuffles deck
    self.deal_hand()
    
    
    
    self.IMAGE_WIDTH = 64
    # self.IMAGE_HEIGHT = 107
    self.IMAGE_HEIGHT = 64
    # self.GRID_COLS = 10
    # self.GRID_ROWS = 10
    
   
    self.images = {
      'board': '_/theme/sequence_board.png',
      'flag': '_/theme/flag.png',
      'green_chip': '_/theme/chipGreen_border.png',
      'blue_chip': '_/theme/chipBlue_border.png'
    }

    self.model = [{'url':'board', 'col':0, 'row':0}]
    # for row in range(self.GRID_ROWS):
      # for col in range(self.GRID_COLS):
        # self.model.append({'type':'AH',
                          # 'x':col*self.IMAGE_WIDTH,
                          # 'y':row*self.IMAGE_HEIGHT})
    
      
    

    # canvas_size is width. Using image_height because cards are taller than wider
    # self.canvas_size = self.GRID_ROWS * self.IMAGE_HEIGHT 
    # self.canvas_1.height = self.canvas_size
    # iPad 5th gen is 2048x1536, 9th gen is larger
    self.canvas_size = 800
    self.canvas_1.height = 650 #64 px/cell, 10 cells

    self.is_green_turn = True

    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn

  def card_color(self,card):
    if card[-1]==SPADES or card[1]==CLUBS:
      return "black"
    if card[-1]==HEARTS or card[-1]==DIAMONDS:
      return "red"

  def deal_card(self):
    card=self.deck.deal()
    self.hand.append(card.rank+card.suit)
    return card.rank+card.suit

  def deal_hand(self):
    self.hand.clear()
    #deal_card() appends card.rank+card.suit to self.hand
    #it returns card.rank+card.suit
    card=self.deal_card() 
    self.label_1.text = card
    self.label_1.foreground = self.card_color(card)
    card=self.deal_card()
    self.label_2.text = card
    self.label_2.foreground = self.card_color(card)
    card=self.deal_card()
    self.label_3.text = card
    self.label_3.foreground = self.card_color(card)
    card=self.deal_card()
    self.label_4.text = card
    self.label_4.foreground = self.card_color(card)
    card=self.deal_card()
    self.label_5.text = card
    self.label_5.foreground = self.card_color(card)
    card=self.deal_card()
    self.label_6.text = card
    self.label_6.foreground = self.card_color(card)
    card=self.deal_card()
    self.label_7.text = card
    self.label_7.foreground = self.card_color(card)

  def update_hand(self):
    labels=[self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7]
    for i in range(7):
      # if there's a card in self.hand at the given position,
      # display it
      # the items in self.hand each have card.rank+card.suit
      if len(self.hand)>i:
        card=self.hand[i]
        label=labels[i]
        label.text=card
        label.foreground=self.card_color(card)
      # and if there's no card at the given position,
      # deal one to fill the space
      else:
        card = self.deal_card() #addds card.rank+card.suit to self.hand
        label=labels[i]
        label.text=card
        label.foreground=self.card_color(card)
        
        
    
  def canvas_1_reset(self, **event_args):
    # Adjust these coordinates if you want the drawing area to not be centered
    # self.canvas_offset = (self.canvas_1.get_width() - self.canvas_size)/2
    # self.canvas_1.translate(self.canvas_offset, 0)

    for item in self.model:
      if item['url']=='flag':
        x=item['col']*self.IMAGE_WIDTH+7
        y=item['row']*self.IMAGE_HEIGHT+7
      elif item['url']=='green_chip' or item['url']=='blue_chip':
        x=item['col']*self.IMAGE_WIDTH+7
        y=item['row']*self.IMAGE_HEIGHT+7
      elif item['url']=='board':
        x=0
        y=0
      self.canvas_1.draw_image(URLMedia(self.images[item['url']]), x, y)

  def draw_flag(self, location):
    col=location[0]
    row=location[1]
    flag = {'url':'flag', 'col':col, 'row':row}
    self.model.append(flag) if flag not in self.model else None #preventing duplicate entries, which could result in flags getting drawn over and over
    # self.canvas_1.draw_image(URLMedia('_/theme/flag.png'), col*self.IMAGE_WIDTH+7, row*self.IMAGE_HEIGHT+7)
    # self.canvas_1_reset()

  def remove_flag(self, location):
    col=location[0]
    row=location[1]
    flag = {'url':'flag', 'col': col, 'row': row}
    self.model.remove(flag) if flag in self.model else None
    # self.canvas_1_reset()

  def draw_flag_by_card(self, card):
   # card is a string representation of an individual playing card; card.rank+card.suit
    # locations (in constants) is dictionary with key=card.rank+card.suit, value=board locations for card
    # locations[card] is the dictionary entry whose key=card parameter
    # the loop goes through both values in location
    for location in locations[card]:
      self.draw_flag(location)
    

  def remove_flag_by_card(self,card):
    for location in locations[card]:
      self.remove_flag(location)
    

  def draw_flags_for_hand(self, hand):
    # hand is a list of card.ranks+card.suits in a player's hand
    for card in hand:
      self.draw_flag_by_card(card)

  def remove_flags_for_hand(self, hand):
    for card in hand:
      self.remove_flag_by_card(card)
    

  def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    # row and col are 0-based; upper left corner is (0,0)
    row = y//self.IMAGE_HEIGHT
    col = x//self.IMAGE_WIDTH
    # Which cell was clicked?
    location=(col,row)
    # What card.rank+card.suit was clicked?
    for key,value in locations.items():
      if location in value:
        card=key
        
    # Draw green chip where user clicks
    # self.canvas_1.draw_image(URLMedia('_/theme/chipGreen_border.png'),x-30,y-30)
    green_chip = {'url':'green_chip', 'col':col, 'row':row}
    blue_chip = {'url':'blue_chip', 'col':col, 'row':row}
    
    if self.is_green_turn:
      # if there's a blue chip in this square, remove it
      if blue_chip in self.model:
        self.model.remove(blue_chip) 
      else:
        # add a green chip, if it's not already in the model
        self.model.append(green_chip)
    else: # it's blue's turn
      # if there's a green chip in this square, remove it
      if green_chip in self.model:
        self.model.remove(green_chip)
      else:
        # add a blue chip
        self.model.append(blue_chip)
    self.remove_flags_for_hand(self.hand)
    # remove the played card from player's hand
    self.hand.remove(card)
    # update player's hand
    self.update_hand()
    self.change_player()
    self.canvas_1_reset()

  def change_player(self, **event_args):
    labels=[self.label_1,self.label_2,self.label_3,self.label_4,self.label_5,self.label_6,self.label_7]
    self.is_green_turn = not self.is_green_turn
    if self.is_green_turn:
      self.btn_player_turn.background='#8fef8f'
      self.btn_player_turn.text="Green's Turn"
      for label in labels:
        label.background="#8fef8f"
    else:
      self.btn_player_turn.background='#a8c2e1'
      self.btn_player_turn.text="Blue's Turn"
      for label in labels:
        label.background="#a8c2e1"

  def btn_playable_cells_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.draw_flags_for_hand(self.hand) 
    self.canvas_1_reset()



    
   
    
  
    
  

  