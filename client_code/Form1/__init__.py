from ._anvil_designer import Form1Template
from anvil import *
import random


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.IMAGE_WIDTH = 80*0.8
    # self.IMAGE_HEIGHT = 107
    self.IMAGE_HEIGHT = 80*0.8
    # self.GRID_COLS = 10
    # self.GRID_ROWS = 10
    self.images = {
      'board': URLMedia('_/theme/sequence_board.png')
    }

    self.model = [{'url':'_/theme/sequence_board.png', 'x':0, 'y':0}]
    # for row in range(self.GRID_ROWS):
      # for col in range(self.GRID_COLS):
        # self.model.append({'type':'AH',
                          # 'x':col*self.IMAGE_WIDTH,
                          # 'y':row*self.IMAGE_HEIGHT})
    
      
    

    # canvas_size is width. Using image_height because cards are taller than wider
    # self.canvas_size = self.GRID_ROWS * self.IMAGE_HEIGHT 
    # self.canvas_1.height = self.canvas_size
    self.canvas_size = 800
    self.canvas_1.height = 800
    
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
    self.canvas_1_reset()

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

  def draw_flag_by_hand(self, hand):
    # hand is a list of cards in a player's hand
    for card in hand:
      self.draw_flag_by_card(card)
    

  def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    # row and col are 0-based; upper left corner is (0,0)
    row = y//self.IMAGE_HEIGHT
    col = x//self.IMAGE_WIDTH
    print(f"col = {col}, row = {row}")
    # Draw green chip where user clicks
    # self.canvas_1.draw_image(URLMedia('_/theme/chipGreen_border.png'),x-30,y-30)
    chip = {'url':'_/theme/chipGreen_border.png', 'x':x-24, 'y':y-24}
    self.model.append(chip) if chip not in self.model else None
    # Draw flags for A, K, Q, and 10 of Hearts
    self.draw_flag_by_hand(['AH','KH','QH','10H']) #this method ultimately calls canvas1_reset()

    
   
    
  
    
  

  