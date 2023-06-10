from utils import draw_cursor_at, get_resize_dimensions
from ScreenInterface import ScreenInterface
from SettingsScreen import SettingsScreen
from GalleryScreen import GalleryScreen
from PromptScreen import PromptScreen
from PreviewScreen import PreviewScreen
from GalleryScreen import GalleryScreen
from BluetoothScreen import BluetoothScreen
import textwrap
from math import floor

from peripherals import display

from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw

from font import font_body

class MainScreen(ScreenInterface):
  cursor_index = 0
  
  def __init__(self, *args, **kwargs):
    # body of the constructor
    super().__init__(*args, **kwargs)
  
  submenus = [
    {'name': 'Camera', 'clazz': PreviewScreen},
    {'name': 'Gallery', 'clazz': GalleryScreen}, 
    {'name': 'Bluetooth Print', 'clazz': BluetoothScreen}, 
    {'name': 'Prompt', 'clazz': PromptScreen}, 
    {'name': 'Settings', 'clazz': SettingsScreen}
  ]
  
  def print_screen(self) -> str:
    """Load in the file for extracting text."""
    with canvas(display) as draw:
      #draw.rectangle(device.bounding_box, outline="white", fill="black")
      with Image.open("images/header_neu.bmp") as photo:
        draw.bitmap((0,0), photo.convert('1'), fill="white")
        
      current_y = 30
      for index, submenu in enumerate(self.submenus):
        display_name = submenu['name']
        lines = textwrap.wrap(display_name, width=10)
        for line in lines:
          text_length = draw.textlength(line, font=font_body)
          start_pos = floor((display.width - text_length) / 2)
          is_selected = index == self.cursor_index
          if is_selected:
            draw.rectangle([(start_pos-2, current_y), (display.width-start_pos, current_y+12)], fill="white")
          draw.text((start_pos,current_y), line, font=font_body, fill="black" if is_selected else "white")
          current_y = current_y + 11
        current_y = current_y + 5


  def update(self, key: str) -> dict:
    """Extract text from the currently loaded file."""
    if key == 'down':
      self.cursor_index = (self.cursor_index + 1)  % len(self.submenus)
      self.print_screen()
    elif key == 'up':
      self.cursor_index = self.cursor_index - 1
      if self.cursor_index < 0:
        self.cursor_index = len(self.submenus) - 1
      self.print_screen()
    elif key == 'enter':
      self.push(self.submenus[self.cursor_index]['clazz'])