from os import listdir
from os.path import isfile, join,getmtime

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