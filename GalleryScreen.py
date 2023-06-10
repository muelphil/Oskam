from utils import draw_cursor_at, get_resize_dimensions
from ScreenInterface import ScreenInterface
from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw
from os.path import isfile,join,getmtime
from time import strftime, localtime
from math import floor
from illumination import custom_bw_enhancement
from font import font_body, font_header, font
from peripherals import display, printer
from settings import settings
from get_current_index import get_current_index

class GalleryScreen(ScreenInterface):
  cursor_index = 0
  pictures = None
  #current_index = None

  def __init__(self, *args, **kwargs):
    # body of the constructor
    super().__init__(*args, **kwargs)
    self.pictures = listdir('photos')
    #current_index = get_current_index()

  def print_screen(self) -> str:
    """Load in the file for extracting text."""
    photo_filename = join('photos', self.pictures[self.cursor_index])
    with Image.open(photo_filename, "r") as photo, canvas(display) as draw:
      #draw.rectangle(device.bounding_box, outline="white", fill="black")
      draw.text((0,0), 'Gallery', font=font_header, fill="white")
      new_size = get_resize_dimensions(photo, display.width, display.height)
      draw.bitmap((0,20), photo.resize(new_size).convert("1"), fill="white")
      
      
      time = getmtime(photo_filename)
      #https://strftime.org/
      datestr = strftime('%-d.%-m.%y', localtime(time))
      timestr = strftime('%-H:%M', localtime(time))
      draw.text((0, 106), datestr, fill="white")
      draw.text((0, 116), timestr, fill="white")
      
      text_to_draw = f'{self.cursor_index+1}/{len(self.pictures)}'
      right_start = floor((display.width - draw.textlength(f'{len(self.pictures)}/{len(self.pictures)}', font=font_body)))
      draw.text((right_start, 116), text_to_draw, fill="white")
      
      #draw_cursor_at(draw, 0, 36+3-1+self.cursor_index*12, 2, 6) #-1 because most of the text is above the line

  def update(self, key: str) -> dict:
    """Extract text from the currently loaded file."""
    if key == 'down':
      self.cursor_index = (self.cursor_index + 1)  % len(self.pictures)
      self.print_screen()
    elif key == 'up':
      self.cursor_index = self.cursor_index - 1
      if self.cursor_index < 0:
        self.cursor_index = len(self.pictures) - 1
      self.print_screen()
    elif key == 'enter':
      photo_filename = join('photos', self.pictures[self.cursor_index])
      with Image.open(photo_filename) as photo:
        printer.wake()
        
        resized = photo.resize((384, floor(photo.size[1] * 384 / photo.size[0])))
        #enhanced = custom_bw_enhancement(resized)
        printer.printImage(resized, True)
        
        if settings['print_datetime']:
          time = getmtime(photo_filename)
          #https://strftime.org/
          #timestr = strftime('%A, %-d. %B %Y, %-H:%M', localtime(time))
          timestr = strftime('%a %-d. %b %y %-H:%M', localtime(time))
          printer.justify('R')
          printer.println(timestr)
          printer.justify('L')
        printer.feed(3)
        printer.sleep()
    elif key == 'b':
      print('calling pop')
      self.pop()
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
