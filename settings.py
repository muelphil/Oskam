from peripherals import display,printer,pixels
import json

isOn = False
def toggleTorch():
  global isOn
  if isOn:
    pixels.fill((0, 0, 0))
  else:
    pixels.fill((255, 255, 255))
  pixels.show()
  isOn = not isOn

settings_blueprint = {
  'contrast': {
    'display_name': 'Display Contrast',
    'possible_values': [0,1],
    'possibity_displays':{0: 'Dim', 1:'Bright'},
    'default': 0,
    'on_change': lambda val: display.contrast(0 if val == 0 else 255),
    'initial': True
  },
  'display_sleep_on_start': {
    'display_name': 'Start with Display off',
    'possible_values': [1,0],
    'possibity_displays':{1: 'Yes', 0:'No'},
    'default': 0
  },
  'preview_on_start': {
    'display_name': 'Start in Preview Mode',
    'possible_values': [1,0],
    'possibity_displays':{1: 'Yes', 0:'No'},
    'default': 0
  },
  'print_datetime': {
    'display_name': 'Datum/ Uhrzeit drucken',
    'possible_values': [1,0],
    'possibity_displays':{1: 'Yes', 0:'No'},
    'default': 0
  },
  'feed': {
    'display_name': 'Feed Paper',
    'possible_values': [0],
    'possibity_displays':{0:'Go!'},
    'default': 0,
    'on_change': lambda val: printer.feed(3)
  },
  'torch': {
    'display_name': 'Toggle Torch',
    'possible_values': [0],
    'possibity_displays':{0:'Toggle!'},
    'default': 0,
    'on_change': lambda val: toggleTorch()
  },
}

settings = None

class SettingsDict(dict):
    def __setitem__(self, setting_id, value):
      global settings
      #print("You are changing the value of {} to {}!!".format(setting_id, value))
      super(SettingsDict, self).__setitem__(setting_id, value)
      setting = settings_blueprint[setting_id]
      if 'on_change' in setting :
        setting['on_change'](value)
      with open('settings.json', 'w') as settings_file:
        json.dump(settings, settings_file) 
        
        
def get_default_settings():
  default_settings = {}
  for setting in settings_blueprint.keys():
    default_settings[setting] = settings_blueprint[setting]['default']
  return default_settings
  
  
#############################################################
#                      Settings                             #
#############################################################
settings_file = None
try:
  settings_file = open("settings.json", "r")
  content = settings_file.read()
  settings = {**get_default_settings(), **json.loads(content)} # spread operator
  settings_file.close()
except:
  if settings_file is not None:
    settings_file.close()
  print('could not read settings, generating settings')
  settings = get_default_settings()

settings = SettingsDict(settings)

for setting in settings_blueprint.keys():
  setting_dict = settings_blueprint[setting]
  if 'on_change' in setting_dict and 'initial' in setting_dict and setting_dict['initial'] == True:
    print('calling on_change for setting ', setting)
    setting_dict['on_change'](settings[setting])