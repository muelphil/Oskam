from PIL import ImageFont
from pathlib import Path

font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
font_body = ImageFont.truetype(font_path, 12)
font_header = ImageFont.truetype(font_path, 16)

def font(size=12):
  return ImageFont.truetype(font_path, size)