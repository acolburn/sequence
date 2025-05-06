from anvil.js import window
from anvil.js import get_dom_node

def set_css(comp, property_name, property_value,important=False):
  """Sets the CSS property of a component with an optional argument to specify if it is important"""
  if important:
    priority='important'
  else:
    priority='undefined'
    get_dom_node(comp).style.setProperty(property_name,property_value,priority)


current_mode='pc'
pc_width_threshold=660
forms=[]

def form(form):
  original_init=form.__init__
  def __init__(self,**properties):
    original_init(self,**properties)
    forms.append(self)
    if current_mode=='pc' and hasattr(self,'on_pc'):
      self.on_pc()

    elif current_mode=='mobile' and hasattr(self,'on_mobile'):
      self.on_mobile() 

    form.__init__=__init__
  return form

def switch_to_mobile():
  global current_mode
  current_mode='mobile'
  for form in forms:
    if hasattr(form,'on_mobile'):
      form.on_mobile()

def switch_to_pc():
  global current_mode
  current_mode='pc'
  for form in forms:
    if hasattr(form,'on_pc'):
      form.on_pc()

def on_resize(*args):
  if current_mode == 'mobile' and window.innerWidth>pc_width_threshold:
    switch_to_pc()

  elif current_mode == 'pc' and window.innerWidth < pc_width_threshold:
    switch_to_mobile()

on_resize()

window.addEventListener('resize',on_resize)