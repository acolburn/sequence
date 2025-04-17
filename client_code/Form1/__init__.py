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
    # self.images = {
    #   'board': URLMedia('_/theme/sequence_board.png')
    # }

    self.model = [{'url':'_/theme/sequence_board.png', 'x':0, 'y':0}]
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

    self.location={'AH':[(5,1),(6,4)],
                  'KH':[(6,1),(6,5)],
                  'QH':[(7,1),(6,6)],
                  '10H':[(8,1),(5,6)],
                  '9H':[(4,6),(8,2)],
                  '8H':[(3,6),(8,3)],
                  }
    
    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn


  def canvas_1_reset(self, **event_args):
    # Adjust these coordinates if you want the drawing area to not be centered
    # self.canvas_offset = (self.canvas_1.get_width() - self.canvas_size)/2
    # self.canvas_1.translate(self.canvas_offset, 0)

    for item in self.model:
        self.canvas_1.draw_image(URLMedia(item['url']), item['x'], item['y'])

  def draw_flag(self, col, row):
    flag = {'url':'_/theme/flag.png', 'x': col*self.IMAGE_WIDTH+7, 'y': row*self.IMAGE_HEIGHT+7}
    self.model.append(flag) if flag not in self.model else None #preventing duplicate entries, which could result in flags getting drawn over and over
    # self.canvas_1.draw_image(URLMedia('_/theme/flag.png'), col*self.IMAGE_WIDTH+7, row*self.IMAGE_HEIGHT+7)
    # self.canvas_1_reset()

  def remove_flag(self, col, row):
    flag = {'url':'_/theme/flag.png', 'x': col*self.IMAGE_WIDTH+7, 'y': row*self.IMAGE_HEIGHT+7}
    self.model.remove(flag) if flag in self.model else None
    # self.canvas_1_reset()

  def draw_flag_by_card(self, card):
    # card is a string representation of an individual playing card
    if card=='AH':
      self.draw_flag(5,1)
      self.draw_flag(6,4)
    if card=='KH':
      self.draw_flag(6,1)
      self.draw_flag(6,5)
    if card=='QH':
      self.draw_flag(7,1)
      self.draw_flag(6,6)
    if card=='10H':
      self.draw_flag(8,1)
      self.draw_flag(5,6)
    if card=='9H':
      self.draw_flag(4,6)
      self.draw_flag(8,2)
    if card=='8H':
      self.draw_flag(3,6)
      self.draw_flag(8,3)
    if card=='7H':
      self.draw_flag(3,5)
      self.draw_flag(8,4)
    if card=='6H':
      self.draw_flag(3,4)
      self.draw_flag(8,5)
    if card=='5H':
      self.draw_flag(4,4)
      self.draw_flag(8,6)
    if card=='4H':
      self.draw_flag(5,4)
      self.draw_flag(8,7)
    if card=='3H':
      self.draw_flag(5,5)
      self.draw_flag(8,8)
    if card=='2H':
      self.draw_flag(4,5)
      self.draw_flag(7,8)

  def remove_flag_by_card(self,card):
    # Hearts
    if card=='AH':
      self.remove_flag(5,1)
      self.remove_flag(6,4)
    if card=='KH':
      self.remove_flag(6,1)
      self.remove_flag(6,5)
    if card=='QH':
      self.remove_flag(7,1)
      self.remove_flag(6,6)
    if card=='10H':
      self.remove_flag(8,1)
      self.remove_flag(5,6)
    if card=='9H':
      self.remove_flag(4,6)
      self.remove_flag(8,2)
    if card=='8H':
      self.remove_flag(3,6)
      self.remove_flag(8,3)
    if card=='7H':
      self.remove_flag(3,5)
      self.remove_flag(8,4)
    if card=='6H':
      self.remove_flag(3,4)
      self.remove_flag(8,5)
    if card=='5H':
      self.remove_flag(4,4)
      self.remove_flag(8,6)
    if card=='4H':
      self.remove_flag(5,4)
      self.remove_flag(8,7)
    if card=='3H':
      self.remove_flag(5,5)
      self.remove_flag(8,8)
    if card=='2H':
      self.remove_flag(4,5)
      self.remove_flag(7,8)
    # Spades
    if card=='AS':
      self.remove_flag(5,1)
      self.remove_flag(6,4)
    if card=='KS':
      self.remove_flag(6,1)
      self.remove_flag(6,5)
    if card=='QS':
      self.remove_flag(7,1)
      self.remove_flag(6,6)
    if card=='10S':
      self.remove_flag(8,1)
      self.remove_flag(5,6)
    if card=='9S':
      self.remove_flag(4,6)
      self.remove_flag(8,2)
    if card=='8S':
      self.remove_flag(3,6)
      self.remove_flag(8,3)
    if card=='7S':
      self.remove_flag(3,5)
      self.remove_flag(8,4)
    if card=='6S':
      self.remove_flag(3,4)
      self.remove_flag(8,5)
    if card=='5S':
      self.remove_flag(4,4)
      self.remove_flag(8,6)
    if card=='4S':
      self.remove_flag(5,4)
      self.remove_flag(8,7)
    if card=='3S':
      self.remove_flag(5,5)
      self.remove_flag(8,8)
    if card=='2S':
      self.remove_flag(4,5)
      self.remove_flag(7,8)
    

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
    print(f"col = {col}, row = {row}")
    # Draw green chip where user clicks
    # self.canvas_1.draw_image(URLMedia('_/theme/chipGreen_border.png'),x-30,y-30)
    green_chip = {'url':'_/theme/chipGreen_border.png', 'x':x-24, 'y':y-24}
    blue_chip = {'url':'_/theme/chipBlue_border.png', 'x':x-24, 'y':y-24}
    
    if self.is_green_turn:
      self.model.append(green_chip) if green_chip not in self.model else None
    else:
      self.model.append(blue_chip) if blue_chip not in self.model else None
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



    
   
    
  
    
  

  