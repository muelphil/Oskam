
from gpiozero import LED, Button
from time import sleep
from signal import pause

def printHello():
  print('hello!')

def main():
  print('start')
  
  from gpiozero import Button
  button = Button(26)
  #button.wait_for_press()
  
  def myfunc(x):
    print('You pushed me', x)
  
  button.when_pressed = lambda: myfunc('hi!')
  
  pause()
  print('end')
  

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass