from utils import draw_cursor_at, get_resize_dimensions,get_current_index
from ScreenInterface import ScreenInterface
from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw
from os import listdir
from math import floor
from os.path import isfile, join
import asyncio
import time
from font import font_body, font_header
from LumaPreview import LumaPreview
from peripherals import display, camera, capture_config, preview_config, pixels,printer
from SettingsScreen import CameraSettingsScreen
from camera_settings import camera_settings
import time
from take_picture import take_picture
from get_current_index import get_current_index
from illumination import custom_bw_enhancement

#def print_imagev2():
#  with Image.open("images/example.jpeg") as photo, canvas(device) as draw:
#    new_size = get_resize_dimensions(photo)
#    resized = photo.resize(new_size)
#    my_photo = resized.convert("1")
#    draw.bitmap((0,0), my_photo, fill="white")
#    draw.text((0,100), 'v2', font=font_body, fill="white")


class DefaultMode:
  description = 'default'

  def process_picture(self, image):
    if camera_settings['print']:
      to_print = image
      printer.wake()
      if camera_settings['nightmode']:
        to_print = custom_bw_enhancement(image)
      resized = to_print.resize((384, floor(to_print.size[1] * 384 / to_print.size[0])))
      printer.printImage(resized, True)
      printer.feed(3)

class TwoByTwoMode:
  images = []
  description = '2x2 - 0'
  
  def process_picture(self, image):
    self.images.append(custom_bw_enhancement(image) if camera_settings['nightmode'] else image)
    self.description = f'2x2 - {len(self.images)}'
    
    if len(self.images) == 4:
      print('4 images taken! ???')
      collage = Image.new('RGB', (2*image.size[0], 2*image.size[1]))
      collage.paste(self.images[0], (0, 0))
      collage.paste(self.images[1], (image.size[0]+1, 0))
      collage.paste(self.images[2], (0, image.size[1]+1))
      collage.paste(self.images[3], (image.size[0]+1, image.size[1]+1))
      resized = collage.resize((384, floor(collage.size[1] * 384 / collage.size[0])))
      printer.wake()
      printer.printImage(resized, True)
      printer.feed(3)
      self.images = []
      self.description = f'2x2 - 0'

modes = [DefaultMode, TwoByTwoMode]

class PreviewScreen(ScreenInterface):
  cursor_index = 0
  pictures = None
  preview = None
  current_index = get_current_index()
  mode_index = 0
  mode = modes[0]()
  index = get_current_index()
  
  def __init__(self, *args, **kwargs):
    # body of the constructor
    super().__init__(*args, **kwargs)
    self.preview = LumaPreview(camera, lambda i: self.print_screen(i), (0,20)) # device
    self.preview.start(camera)
    camera.start()
    camera.switch_mode(preview_config)
    print('index=', self.index)
    
  def release(self) -> str:
    """Extract text from the currently loaded file."""
    print('PreviewScreen::release called!')
    self.preview.stop()
    camera.stop()
    #preview.stop()

  def pause(self):
    self.preview.pause()
    
  def resume(self):
    self.preview.resume()

  def print_screen(self, image = None) -> str:
    """Load in the file for extracting text."""
    #if image is not None:
    #  print('received image with dimensions:', image.size)
    with canvas(display) as draw:
      draw.text((0,0), 'Camera', font=font_header, fill="white")
      if image is not None:
        new_size = get_resize_dimensions(image, display.width, display.height)
        draw.bitmap((0,20), image.resize(new_size).convert("1"), fill="white")
      #else:
      #  with Image.open(join('photos', self.pictures[self.cursor_index])) as photo:
      #    new_size = get_resize_dimensions(photo, display.width, display.height)
      #    draw.bitmap((0,20), photo.resize(new_size, Image.NEAREST).convert("1"), fill="white")
      #draw_cursor_at(draw, 0, 36+3-1+self.cursor_index*12, 2, 6) #-1 because most of the text is above the line
      
      mode_length = draw.textlength('Mode', font=font_body)
      if self.cursor_index == 0:
        draw.rectangle([(0, 106),(mode_length+2, 106+10)], fill="white")
      draw.text((1,106), 'Mode', font=font_body, fill="black" if self.cursor_index == 0 else "white")
      draw.text((mode_length+4,106), self.mode.description, font=font_body, fill="white")
      
      settings_length = draw.textlength('Settings', font=font_body)
      if self.cursor_index == 1:
        draw.rectangle([(0, 117),(settings_length+2, 117+10)], fill="white")
      draw.text((1,117), 'Settings', font=font_body, fill="black" if self.cursor_index == 1 else "white")


  # TODO
  async def save_image(self, image):
  
    image.save(f'photos/image{self.index:03}.jpeg')
    self.index = self.index + 1

  def update(self, key: str) -> dict:
    """Extract text from the currently loaded file."""
    global modes
    if key == 'down':
      self.cursor_index = (self.cursor_index + 1)  % 2
      self.print_screen()
    elif key == 'up':
      self.cursor_index = self.cursor_index - 1
      if self.cursor_index < 0:
        self.cursor_index = 2 - 1
      self.print_screen()
    elif key == 'enter':
      if self.cursor_index == 0:
        self.mode_index = (self.mode_index + 1) % len(modes)
        self.mode = modes[self.mode_index]()
        self.print_screen()
      elif self.cursor_index == 1:
        self.push(CameraSettingsScreen)
      pass
    elif key == 'c':
      index = self.current_index 
      self.current_index = self.current_index + 1
      self.preview.pause()
      with canvas(display) as draw:
        draw.rectangle([(0,0), (63,127)], fill="white")
      with canvas(display) as draw:
        draw.rectangle([(0,0), (63,127)], fill="black")
      print(f'TAKING PICTURE! (saving into image{index:03}.jpeg)')
      #image = camera.switch_mode_and_capture_image(capture_config).transpose(Image.ROTATE_270)
      
      if camera_settings['flashlight']:
        pixels.fill((255, 255, 255))
        pixels.show()
      
      # TODO ausserhalb von preview
      image = camera.switch_mode_and_capture_image(capture_config)\
        .transpose(Image.ROTATE_90)
      
      if camera_settings['flashlight']:
        pixels.fill((0, 0, 0))
        pixels.show()
        
      # image = camera.capture_image('main').transpose(Image.ROTATE_270)
      asyncio.run(self.save_image(image))

      
      #print('PICTURE TAKEN!')
      with canvas(display) as draw:
        new_size = get_resize_dimensions(image, display.width, display.height)
        draw.bitmap((0,20), image.resize(new_size).convert("1"), fill="white")
      
      self.mode.process_picture(image)
      
      #print('PICTURE SAVED!')
      self.preview.resume()
      # Print
      
    elif key == 'b':
      print('calling pop')
      self.pop()
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      