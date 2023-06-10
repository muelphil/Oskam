#from luma.core import cmdline, error
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import neopixel
import board

#from demo_opts import get_device
# i2cdetect -y 1 # gives 0x3C

serial = i2c(port=1, address=0x3C)
display = ssd1306(serial, rotate=1)


from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
printer.sleep()

from gpiozero import LED, Button

b1 = Button(5) # hoch
b2 = Button(6) # runter
b3 = Button(13) # enter
b4 = Button(26) # back

from picamera2 import Picamera2
from libcamera import controls

#############################################################
#                      Camera                               #
#############################################################

#https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
camera = Picamera2()
camera.set_controls({"FrameRate": 1})
#???
#config = picam2.create_still_configuration(lores={"size": (320, 240)}, display="lores")
#from libcamera import Transform
#preview_config = picam2.create_preview_configuration(transform=Transform(hflip=True))
#preview_config = picam2.create_preview_configuration({"size": (64, 85)}) #(640, 480)
preview_config = camera.create_preview_configuration(lores={"size": (256, 192), "format": "YUV420"}) #(640, 480)
#capture_config = camera.create_still_configuration({"size": (1920, 1080)})
capture_config = camera.create_still_configuration({"size": (1280, 960)})
camera.configure(preview_config) 

pixels = neopixel.NeoPixel(board.D10, 12, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)