from ._anvil_designer import Form1Template
from anvil import *
import random


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
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

    self.locations={'AH':[(5,1),(6,4)],
                   'KH':[(6,1),(6,5)],
                   'QH':[(7,1),(6,6)],
                   '10H':[(8,1),(5,6)],
                   '9H':[(4,6),(8,2)],
                   '8H':[(3,6),(8,3)],
                   '7H':[(3,5),(8,4)],
                   '6H':[(3,4),(8,5)],
                   '5H':[(4,4),(8,6)],
                   '4H':[(5,4),(8,7)],
                   '3H':[(5,5),(8,8)],
                   '2H':[(4,5),(7,8)],
                   '2S':[(1,0),(6,8)],
                   '3S':[(2,0),(5,8)],
                   '4S':[(3,0),(4,8)],
                   '5S':[(4,0),(3,8)],
                   '6S':[(5,0),(3,8)],
                   '7S':[(6,0),(1,8)],
                   '8S':[(7,0),(1,7)],
                   '9S':[(8,0),(1,6)],
                   '10S':[(9,1),(1,5)],
                   'QS':[(9,2),(1,4)],
                   'KS':[(9,3),(1,3)],
                   'AS':[(9,4),(1,2)],
                   'AD':[(1,9),(6,7)],
                   'KD':[(2,9),(7,7)],
                    'QD':[(3,9),(7,6)],
                    '10D':[(4,9),(7,5)],
                    '9D':[(5,9),(7,4)],
                    '8D':[(6,9),(7,3)],
                    '7D':[(7,9),(7,2)],
                    '6D':[(8,9),(6,2)],
                    '5D':[(9,8),(5,2)],
                    '4D':[(9,7),(4,2)],
                    '3D':[(9,6),(3,2)],
                    '2D':[(9,5),(2,2)],
                    'AC':[(0,8),(5,7)],
                    'KC':[(0,7),(4,7)],
                    'QC':[(0,6),(3,7)],
                    '10C':[(0,5),(2,7)],
                    '9C':[(0,4),(2,6)],
                    '8C':[(0,3),(2,5)],
                    '7C':[(0,2),(2,4)],
                    '6C':[(0,1),(2,3)],
                    '5C':[(1,1),(3,3)],
                    '4C':[(2,1),(4,3)],
                    '3C':[(3,1),(5,3)],
                    '2C':[(4,1),(6,3)]
                  }
    
    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn


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
   # card is a string representation of an individual playing card
    for location in self.locations[card]:
      self.draw_flag(location)
    

  def remove_flag_by_card(self,card):
    for location in self.locations[card]:
      self.remove_flag(location)
    

  def draw_flags_for_hand(self, hand):
    # hand is a list of cards in a player's hand
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
    # Draw green chip where user clicks
    # self.canvas_1.draw_image(URLMedia('_/theme/chipGreen_border.png'),x-30,y-30)
    green_chip = {'url':'green_chip', 'col':col, 'row':row}
    blue_chip = {'url':'blue_chip', 'col':col, 'row':row}
    
    if self.is_green_turn:
      # if there's a blue chip in this square, remove it
      if blue_chip in self.model:
        self.model.remove(blue_chip) 
      else:
        self.model.append(green_chip)
        # add a green chip, if it's not already in the model
        # self.model.append(green_chip) if green_chip not in self.model else self.model.remove(green_chip)
    else: # it's blue's turn
      # if there's a green chip in this square, remove it
      if green_chip in self.model:
        self.model.remove(green_chip)
      else:
        self.model.append(blue_chip)
      # self.model.append(blue_chip) if blue_chip not in self.model else self.model.remove(blue_chip)
    self.remove_flags_for_hand(['5H','4H','3H','2H','AH'])
    self.change_player()
    self.canvas_1_reset()

  def change_player(self, **event_args):
    self.is_green_turn = not self.is_green_turn
    if self.is_green_turn:
      self.btn_player_turn.background='#8fef8f'
      self.btn_player_turn.text="Green's Turn"
    else:
      self.btn_player_turn.background='#a8c2e1'
      self.btn_player_turn.text="Blue's Turn"

  def btn_playable_cells_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.draw_flags_for_hand(['5H','4H','3H','2H','AH']) 
    self.canvas_1_reset()



    
   
    
  
    
  

  