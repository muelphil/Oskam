from PIL import ImageFont, Image, ImageDraw
from peripherals import display, camera, capture_config, preview_config, pixels
from camera_settings import camera_settings
import asyncio
from illumination import custom_bw_enhancement

def take_picture(from_preview = False):
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
  asyncio.run(print_and_save(image))
  return image
  
  # TODO
async def print_and_save(image):
  image.save(f'photos/image{index:03}.jpeg')
  
  