class ScreenInterface:
  push = None
  pop = None
  device = None
  printer = None
  camera = None

  def __init__(self, push, pop):
      # body of the constructor
      self.push = push
      self.pop = pop
      #print('ScreenInterface::constructor called!')

  def print_screen(self) -> str:
    """Load in the file for extracting text."""
    #print('ScreenInterface::print_screen called!')

  def update(self, key: str) -> dict:
    """Extract text from the currently loaded file."""
    #print('ScreenInterface::update called!')
    
  def release(self) -> str:
    """Extract text from the currently loaded file."""
    print('ScreenInterface::release called!')
    
  def pause(self):
    pass
  
  def resume(self):
    pass