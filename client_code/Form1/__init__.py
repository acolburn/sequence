from ._anvil_designer import Form1Template
from anvil import *
import random


class Form1(Form1Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.model = [
    {'type': 'square', 'x': 100, 'y': 100, 'width': 50, 'stroke': True, 'fill': False},
    {'type': 'circle', 'x': 300, 'y': 100, 'radius': 20, 'stroke': True, 'fill': True},
    {'type': 'card', 'x': 50, 'y': 50, 'width': 50, 'height': 100, 'stroke': True, 'fill': False},
    ]


    self.canvas_size = 640
    self.canvas_1.height = self.canvas_size # going to make a square canvas, 500x500
    self.canvas_1.reset_context() # must be called whenever canvas needs to be redrawn
    self.x = 10
    self.y = 10

  def canvas_1_reset(self, **event_args):
    # Adjust these coordinates if you want the drawing area to not be centered
    self.canvas_offset = (self.canvas_1.get_width() - self.canvas_size)/2
    self.canvas_1.translate(self.canvas_offset, 0)
  
    # Restrict drawing to the section that we want visible
    self.canvas_1.begin_path()
    self.canvas_1.move_to(0, 0)
    self.canvas_1.line_to(self.canvas_size, 0)
    self.canvas_1.line_to(self.canvas_size,self.canvas_size)
    self.canvas_1.line_to(0, self.canvas_size)
    self.canvas_1.close_path()        
    self.canvas_1.clip()
  
    for shape in self.model:
      if shape['type'] == 'square':
        self.canvas_1.begin_path()
        self.canvas_1.move_to(shape['x'], shape['y'])
        self.canvas_1.line_to(shape['x']+shape['width'],shape['y'])
        self.canvas_1.line_to(shape['x']+shape['width'],shape['y']+shape['width'])
        self.canvas_1.line_to(shape['x'], shape['y']+shape['width'])
        self.canvas_1.close_path()

      if shape['type'] == 'card':
        self.canvas_1.begin_path()
        self.canvas_1.move_to(shape['x'], shape['y'])
        self.canvas_1.line_to(shape['x']+shape['width'],shape['y'])
        self.canvas_1.line_to(shape['x']+shape['width'],shape['y']+shape['height'])
        self.canvas_1.line_to(shape['x'], shape['y']+shape['height'])
        self.canvas_1.close_path()
      
  
      if shape['type'] == 'circle':
          self.canvas_1.begin_path()
          self.canvas_1.arc(shape['x'], shape['y'], shape['radius'])
          self.canvas_1.close_path()
  
      if shape['stroke']:
          self.canvas_1.stroke()  
  
      if shape['fill']:
          self.canvas_1.fill() 
  
      if shape['fill']:
          self.canvas_1.fill()

  def add_square_click(self, **event_args):
    """This method is called when the button is clicked"""
    x=random.randint(0, self.canvas_size-50)
    y=random.randint(0, self.canvas_size-50)
    self.model.append({
    'type': 'square',
    'x': x,
    'y': y,
    'width': 50,
    'stroke': True,
    'fill': False
    })
    self.canvas_1.reset_context()


  def add_circle_click(self, **event_args):
    """This method is called when the button is clicked"""
    x = random.randint(0,self.canvas_size-50)
    y = random.randint(0,self.canvas_size-50)
    self.model.append({
        'type': 'circle',
        'x': x,
        'y': y,
        'radius': 50,
        'stroke': True,
        'fill': False
    })
    self.canvas_1.reset_context()

  def add_card_click(self, **event_args):
    """This method is called when the button is clicked"""
    # x=random.randint(0, self.canvas_size-50)
    # y=random.randint(0, self.canvas_size-50)
    self.x += 50
    
    self.model.append({
    'type': 'card',
    'x': self.x,
    'y': self.y,
    'width': 40,
    'height': 70,
    'stroke': True,
    'fill': False
    })
    self.canvas_1.reset_context()


    
