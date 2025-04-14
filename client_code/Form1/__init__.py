from ._anvil_designer import Form1Template
from anvil import *
import random


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.IMAGE_WIDTH = 80
    # self.IMAGE_HEIGHT = 107
    self.IMAGE_HEIGHT = 80
    self.GRID_COLS = 10
    self.GRID_ROWS = 10
    self.images = {
      'AH': URLMedia('_/theme/cardHeartsA.png')
    }

    self.model = []
    for row in range(self.GRID_ROWS):
      for col in range(self.GRID_COLS):
        self.model.append({'type':'AH',
                          'x':col*self.IMAGE_WIDTH,
                          'y':row*self.IMAGE_HEIGHT})
    
      
    

    # canvas_size is width. Using image_height because cards are taller than wider
    self.canvas_size = self.GRID_ROWS * self.IMAGE_HEIGHT 
    self.canvas_1.height = self.canvas_size
    
    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn


  def canvas_1_reset(self, **event_args):
    self.canvas_1.draw_image(URLMedia('_/theme/sequence_board.png'),0,0)
    # Adjust these coordinates if you want the drawing area to not be centered
    # self.canvas_offset = (self.canvas_1.get_width() - self.canvas_size)/2
    # self.canvas_1.translate(self.canvas_offset, 0)

    # for shape in self.model:
      # if shape['type'] in self.images:
        # self.canvas_1.draw_image(self.images[shape['type']], shape['x'], shape['y'])

  def canvas_1_mouse_down(self, x, y, button, keys, **event_args):
    """This method is called when a mouse button is pressed on this component"""
    # row and col are 0-based; upper left corner is (0,0)
    row = y//self.IMAGE_HEIGHT
    col = x//self.IMAGE_WIDTH
    print(f"row = {row}, col = {col}")
  
    
  

  