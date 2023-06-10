from utils import draw_cursor_at, get_resize_dimensions
from ScreenInterface import ScreenInterface
from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw
from pathlib import Path
import textwrap
from math import floor
from font import font_body, font_header, font
from utils import draw_cursor_at, get_resize_dimensions
import random
import json
from peripherals import display, printer

class PromptScreen(ScreenInterface):
  cursor_index = 0
  
  tags = ['Friends', 'Family', 'Date', 'Spicy']
  active_tags = ['Friends'] # TODO
  tag_count = {}
  prompts = []
  
  current_prompts = []
  current_prompt_index = 0
  
  def update_current_prompts(self):
    self.current_prompts = [
      prompt['question'] 
      for prompt in self.prompts 
      #if any([tag in self.active_tags for tag in prompt['tags']])
    ]
    random.shuffle(self.current_prompts)
    print('self.current_prompts=', self.current_prompts)
    current_prompt_index = 0
    
  def __init__(self, *args, **kwargs):
    # body of the constructor
    super().__init__(*args, **kwargs)
    
    with open("prompts.json", "r") as prompts_file:
      self.prompts = json.loads(prompts_file.read())
    
    for tag in self.tags:
      self.tag_count[tag] = 0
      
    for prompt in self.prompts:
      for tag in prompt['tags']:
        self.tag_count[tag] = self.tag_count[tag] + 1
    
    # TODO eventuell vorherige Einstellung laden?
    self.update_current_prompts()

  font_print = font(16)

  def print_screen(self) -> str:
    """Load in the file for extracting text."""
    with canvas(display) as draw:
      #draw.rectangle(device.bounding_box, outline="white", fill="black")
      draw.text((0,0), 'Prompt', font=font_header, fill="white")
      draw.line([(0, 20),(127, 20)], fill= "white", width=3)
      
      print_button_text = 'PRINT'
      text_length = draw.textlength(print_button_text, font=self.font_print)
      start_pos = floor((display.width - text_length) / 2)
      if self.cursor_index == 0:
        draw.rectangle([(start_pos-2,34),(display.width-start_pos,48)], fill="white")  
      draw.text((start_pos,34), print_button_text, font=self.font_print, fill="black" if self.cursor_index == 0 else "white")
      
      start_y= 60
      padding = 4
      for index, tag in enumerate(self.tags):
        black ="black" # todo make 0 and 255
        white ="white"
        is_selected = self.cursor_index -1 == index
        is_active = tag in self.active_tags

        
        if is_selected:
          draw.rectangle([(0,start_y-1+(12+padding)*index),(63, start_y+11+(12+padding)*index)], fill="white")
          black = "white"
          white = "black" 
        
        draw.rectangle([(1,start_y+1+(12+padding)*index),(8, start_y+1+7+(12+padding)*index)], outline=white, fill=black)
        if is_active:
          draw.rectangle([(3,start_y+1+2+(12+padding)*index),(6, start_y+1+5+(12+padding)*index)], fill=white)
        draw.text((12, start_y+(12+padding)*index), tag, fill=white)
        
        
        #count = str(self.tag_count[tag])
        #textlength = draw.textlength(count, font=font_body)
        #draw.text((self.device.width- textlength, 36+12*index), count, fill="white")
      #draw_cursor_at(draw, 0, 36+3-1+self.cursor_index*12, 3, 6) #-1 because most of the text is above the line
      

  def update(self, key: str) -> dict:
    """Extract text from the currently loaded file."""
    if key == 'down':
      self.cursor_index = (self.cursor_index + 1)  % (len(self.tags)+1)
      self.print_screen()
    elif key == 'up':
      self.cursor_index = self.cursor_index - 1
      if self.cursor_index < 0:
        self.cursor_index = len(self.tags)
      self.print_screen()
    elif key == 'enter':
      if self.cursor_index == 0:
        prompt = self.current_prompts[self.current_prompt_index]
        if prompt:
          printer.wake()
          printer.println(prompt)
          printer.feed(3)
          printer.sleep()
          current_prompt_index = (self.current_prompt_index +1) % len(self.current_prompts)
        #print('Prompt!')
      else:
        tag = self.tags[self.cursor_index-1]
        if tag in self.active_tags:
          self.active_tags.remove(tag)
        else:
          self.active_tags.append(tag)
      
      self.print_screen()
    
      pass
    elif key == 'b':
      print('calling pop')
      self.pop()
      
      
      
      
