import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json
import locale
from signal import pause
#locale.setlocale(locale.LC_ALL, 'de_DE.utf8') # swedish

from settings import settings

from math import floor, ceil
from MainScreen import MainScreen
from PreviewScreen import PreviewScreen
from SettingsScreen import SettingsScreen
from PromptScreen import PromptScreen
from utils import draw_cursor_at, get_resize_dimensions,get_current_index

from peripherals import display, camera,capture_config

#from qt_gl_preview import *

from sshkeyboard import listen_keyboard
from luma.core.render import canvas
from PIL import ImageFont, Image, ImageDraw

#    splash = Image.open(img_path) \
#        .transform((device.width, device.height), Image.AFFINE, (1, 0, 0, 0, 1, 0), Image.BILINEAR) \
#        .convert(device.mode)


display_sleeping = False

def main():
  global display_sleeping
  
  #############################################################
  #                      Screen                               #
  #############################################################
  screen_stack = []
  def pop_screen():
    old_screen = screen_stack.pop()
    old_screen.release()
    next_screen = screen_stack[-1]
    next_screen.resume()
    next_screen.print_screen()
  
  def push_screen(screen_class):
    if len(screen_stack) :
      screen_stack[-1].pause()
    screen = screen_class(push_screen, pop_screen)
    screen_stack.append(screen)
    screen.print_screen()

  push_screen(MainScreen)
  
  #############################################################
  #                      Settings2                            #
  #############################################################
  
  if settings['display_sleep_on_start']:
    # https://github.com/rm-hull/luma.core/blob/master/luma/core/device.py
    display.hide()
    display_sleeping = True
  
  if settings['preview_on_start']:
    push_screen(PreviewScreen)


  #############################################################
  #                         Temp                              #
  #############################################################
  #push_screen(PromptScreen)
  
  #############################################################
  #                      React to Keys                        #
  #############################################################
  def press(key):
    print(f"'{key}' pressed")
    global display_sleeping
    if display_sleeping:
      display_sleeping = False
      display.show()
    elif len(screen_stack) == 1 and key == 'b':
      display_sleeping = True
      display.hide()
    elif key == 'c' and not isinstance(screen_stack[-1], PreviewScreen):
      #taking picture anywhere
      print('taking picture!', type(screen_stack[-1]))  
      camera.start()
      camera.switch_mode(capture_config)
      image = camera.capture_image('main').convert('RGB')
      camera.stop()
      index = get_current_index()
      image.save(f'photos/image{index:03}.jpeg')
      print('picture taken!')
    else:
      screen_stack[len(screen_stack)-1].update(key)
  
  #############################################################
  #                      SSH Keyboard                         #
  #############################################################
  def release(key):
    pass
  listen_keyboard(on_press=press, on_release=release)

  #############################################################
  #                      Start                                #
  #############################################################
  screen_stack[len(screen_stack)-1].print_screen()

  #############################################################
  #                      GPIO Buttons                         #
  #############################################################
                                     
  #b1.when_pressed = lambda: press('up')                                     
  #b2.when_pressed = lambda: press('down')                                     
  #b3.when_pressed = lambda: press('enter')                                     
  #b4.when_pressed = lambda: press('b')
  #pause()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
