from peripherals import display
import json

camera_settings_blueprint = {
  'flashlight': {
    'display_name': 'Use Flashlight',
    'possible_values': [1,0],
    'possibity_displays':{1: 'Yes', 0:'No'},
    'default': 0
  },
  'nightmode': {
    'display_name': 'Use Nightmode TODO?',
    'possible_values': [1,0],
    'possibity_displays':{1: 'Yes', 0:'No'},
    'default': 0
  },
  'print': {
    'display_name': 'Print Image',
    'possible_values': [1,0],
    'possibity_displays':{1: 'Yes', 0:'No'},
    'default': 1
  }
  
}

camera_settings = None

class SettingsDict(dict):
    def __setitem__(self, setting_id, value):
      global camera_settings
      #print("You are changing the value of {} to {}!!".format(setting_id, value))
      super(SettingsDict, self).__setitem__(setting_id, value)
      setting = camera_settings_blueprint[setting_id]
      if 'on_change' in setting:
        setting['on_change'](value, display)
      with open('camera_settings.json', 'w') as settings_file:
        json.dump(camera_settings, settings_file) 
        
        
def get_default_settings():
  default_settings = {}
  for setting in camera_settings_blueprint.keys():
    default_settings[setting] = camera_settings_blueprint[setting]['default']
  return default_settings
  
  
#############################################################
#                      Settings                             #
#############################################################
settings_file = None
try:
  settings_file = open("camera_settings.json", "r")
  content = settings_file.read()
  camera_settings = {**get_default_settings(), **json.loads(content)} # spread operator
  settings_file.close()
except:
  if settings_file is not None:
    settings_file.close()
  print('could not read settings, generating settings')
  camera_settings = get_default_settings()

camera_settings = SettingsDict(camera_settings)

for setting in camera_settings_blueprint.keys():
  setting_dict = camera_settings_blueprint[setting]
  if 'on_change' in setting_dict:
    setting_dict['on_change'](camera_settings[setting], display)