from utils import draw_cursor_at, get_resize_dimensions
from ScreenInterface import ScreenInterface
from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw
from pathlib import Path
import textwrap
from math import floor
from settings import settings, settings_blueprint
from camera_settings import camera_settings, camera_settings_blueprint
from font import font_body, font_header
from peripherals import display, camera
  
def generate_screen_for_settings(settings, blueprint):

  class SettingsScreen1(ScreenInterface):
    cursor_index = 0
    setting_ids = None
    
    def __init__(self, *args, **kwargs):
        # body of the constructor
        super().__init__(*args, **kwargs)
        self.setting_ids = list(blueprint.keys())
        #print('settings=', self.setting_ids)
        #print('settings[0]=', self.setting_ids[0])
        
  
    def print_screen(self) -> str:
      """Load in the file for extracting text."""
      with canvas(display) as draw:
        #draw.rectangle(display.bounding_box, outline="white", fill="black")
        draw.text((0,0), 'Settings', font=font_header, fill="white")
        draw.line([(0, 20),(127, 20)], fill= "white", width=3)
        
        #for index, setting in enumerate(blueprint):
        settings_text_y = 30
        setting_id = self.setting_ids[self.cursor_index]
        setting = blueprint[setting_id]
        display_name = setting['display_name']
        lines = textwrap.wrap(display_name, width=10)
        for index2, line in enumerate(lines[:3]):
          draw.text((1, settings_text_y+index2*12), line, font=font_body, fill="white")
          
        current_x = 4
        options_y = settings_text_y + 12 * 3 + 10
        
        #draw.line([(4, options_y -6 ),(123, options_y - 6)], fill= "white")
        
        for option in setting['possible_values']:
          #print('option:', option)
          option_display_name = setting['possibity_displays'][option]
          is_active = option == settings[setting_id]
          length = draw.textlength(option_display_name, font=font_body)
          if is_active:
            draw.rectangle([(current_x, options_y),(current_x+length+4, options_y+12)], fill="white")
          draw.text((current_x+2, options_y), option_display_name,font = font_body, fill="black" if is_active else "white")
          current_x = current_x + length + 4 + 2
          
        text_to_draw = f'{self.cursor_index+1}/{len(blueprint)}'
        center_start = floor((display.width - draw.textlength('W/4', font=font_body)) / 2)
        draw.text((center_start, 110), text_to_draw, fill="white")
          
        #if self.cursor_index == index:
        #  draw.rectangle([(0,36+index*12), (127, 36+index*12+12)], fill="white")
        #draw.text((1,36+index*12), blueprint[setting]['display_name'], font=font_body, fill="black" if self.cursor_index == index else "white")
        
        
        #draw_cursor_at(draw, 0, 36+3-1+self.cursor_index*12, 2, 6) #-1 because most of the text is above the line
  
    def update(self, key: str) -> dict:
      """Extract text from the currently loaded file."""
      if key == 'down':
        self.cursor_index = (self.cursor_index + 1)  % len(blueprint.keys())
        self.print_screen()
      elif key == 'up':
        self.cursor_index = self.cursor_index - 1
        if self.cursor_index < 0:
          self.cursor_index = len(blueprint.keys()) - 1
        self.print_screen()
      elif key == 'enter':
        setting_id = self.setting_ids[self.cursor_index]
        setting = blueprint[setting_id]
        options = setting['possible_values']
        current_value = settings[setting_id]
        current_index = options.index(current_value)
        next_value = options[(current_index+1)%len(options)]
        settings[setting_id] = next_value
        self.print_screen()
      elif key == 'b':
        #print('calling pop')
        self.pop()
        
  return SettingsScreen1


SettingsScreen = generate_screen_for_settings(settings, settings_blueprint)
CameraSettingsScreen = generate_screen_for_settings(camera_settings, camera_settings_blueprint)
