from utils import draw_cursor_at, get_resize_dimensions
from ScreenInterface import ScreenInterface
from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw
from pathlib import Path
import textwrap
from math import floor
from font import font_body, font_header
from peripherals import display, printer

class BluetoothScreen(ScreenInterface):
  cursor_index = 0
  
  def __init__(self, *args, **kwargs):
      # body of the constructor
      super().__init__(*args, **kwargs)
      

  def print_screen(self) -> str:
    """Load in the file for extracting text."""
    with canvas(display) as draw:
      #draw.rectangle(device.bounding_box, outline="white", fill="black")
      draw.text((0,0), 'Bluetooth', font=font_header, fill="white")
      draw.line([(0, 20),(127, 20)], fill= "white", width=3)
      draw.text((0,30), 'TODO', font=font_body, fill="white")

  def update(self, key: str) -> dict:
    """Extract text from the currently loaded file."""
    if key == 'down':
      self.cursor_index = (self.cursor_index + 1)  % len(self.settings_blueprint.keys())
      self.print_screen()
    elif key == 'up':
      self.cursor_index = self.cursor_index - 1
      if self.cursor_index < 0:
        self.cursor_index = len(self.settings_blueprint.keys()) - 1
      self.print_screen()
    elif key == 'enter':
      pass
    elif key == 'b':
      print('calling pop')
      self.pop()
      
      
      
      
