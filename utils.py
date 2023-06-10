from math import floor, ceil
from os import listdir
from os.path import isfile, join

def get_resize_dimensions(image, width, height):
  image_ratio = image.size[0] / image.size[1]
  device_ratio = width / height
  if image_ratio > device_ratio: # image ist kuerzer als screen
    return (width, int(width / image.size[0] * image.size[1]))
  else:
    return (int(height / image.size[1] * image.size[0]), height)
    
def resize_image_to_width(image, width):
  return image.resize((width, image.size[1] * width / image.size[0]))

def draw_cursor_at(draw,x,y,width,height):
  draw.line([(x,y), (x+width,y+floor(height/2))], fill="white")
  draw.line([(x,y+height), (x+width, y+ceil(height/2))], fill="white")

# TODO this belongs in camera
def get_current_index():
  current_index = 0
  pictures_dir = 'photos'
  for fileOrDir in listdir(pictures_dir):
    if isfile(join(pictures_dir, fileOrDir)) and fileOrDir.startswith('image') and fileOrDir.endswith('.jpeg'):
      try:
        index = int(fileOrDir[5:-5])
        if current_index == 0 or current_index <= index:
          current_index = index + 1
      except ValueError:
        pass
  return current_index