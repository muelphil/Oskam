import threading
from logging import getLogger
import io
_log = getLogger(__name__)
from illumination import bw_pil_image_from_array
import numpy as np
from PIL import Image

class LumaPreview:

    def __init__(self, picam2, print_screen, position=(0,0), x=None, y=None, width=None, height=None, transform=None):
        """Initialise null preview

        :param x: X position, defaults to None
        :type x: int, optional
        :param y: Y position, defaults to None
        :type y: int, optional
        :param width: Width, defaults to None
        :type width: int, optional
        :param height: Height, defaults to None
        :type height: int, optional
        :param transform: Transform, defaults to None
        :type transform: libcamera.Transform, optional
        """
        # Ignore width and height as they are meaningless. We only accept them so as to
        # be a drop-in replacement for the Qt/DRM previews.
        self.size = (width, height)
        self._abort = threading.Event()
        self._started = threading.Event()
        self.picam2 = picam2
        self.print_screen = print_screen

    def thread_func(self, picam2):
        """Thread function

        :param picam2: picamera2 object
        :type picam2: Picamera2
        """
        import selectors

        sel = selectors.DefaultSelector()
        sel.register(picam2.notifyme_r, selectors.EVENT_READ, self.handle_request)
        self._started.set()

        while not self._abort.is_set():
            events = sel.select(0.2)
            for key, _ in events:
                picam2.notifymeread.read()
                callback = key.data
                callback(picam2)

    def start(self, picam2):
        """Starts null preview

        :param picam2: Picamera2 object
        :type picam2: Picamera2
        """
        print('Starting Luma Preview')
        self.picam2 = picam2
        picam2.attach_preview(self)
        self._started.clear()
        self._abort.clear()
        self.thread = threading.Thread(target=self.thread_func, args=(picam2,))
        self.thread.setDaemon(True)
        self.thread.start()
        self._started.wait()

    def set_overlay(self, overlay):
        """Sets overlay

        :param overlay: Overlay
        """
        # This only exists so as to have the same interface as other preview windows.

    i = 0
    
    def render_request(self, completed_request):
        """Draw the camera image. For the NullPreview, there is nothing to do."""
        if not self.paused:
          self.i = self.i+1
  
          #print('received completed_request! ', self.i)
          
          #print('Image=', raw_np_array, 'size=', raw_np_array.shape)
          #bw_image_data = raw_np_array[0:85, 0:64]
          #img = bw_pil_image_from_array(bw_image_data)
          #self.print_screen(img)
          
          
          # https://gist.github.com/RRMoelker/85fad327b9288bb45bb2ed4b33e871c9
          #RESOLUTION = (64, 85)
          #fwidth = (RESOLUTION[0] + 31) // 32 * 32
          #fheight = (RESOLUTION[1] + 15) // 16 * 16
          
          fwidth=256
          fheight=192
          
          buf = completed_request.make_buffer("lores")
          y_data = np.frombuffer(buf, dtype=np.uint8, count=fwidth*fheight).\
            reshape((fheight, fwidth))
          #https://numpy.org/doc/stable/reference/generated/numpy.rot90.html          
          y_data = np.rot90(y_data)
          #y_data = y_data[:RESOLUTION[1], :RESOLUTION[0]]  # crop numpy array to RESOLUTION
          im = Image.fromarray(y_data, mode='L')  # using luminance mode
          #print('saving...')
          #im.save('test.jpg')
          #im.save('test.bmp')
          self.print_screen(im)
              
          #img = completed_request.make_image("lores")
          #print('reived completed_request! ', self.i)
          pass

    def handle_request(self, picam2):
        """Handle requests

        :param picam2: picamera2 object
        :type picam2: Picamera2
        """
        try:
            picam2.process_requests(self)
        except Exception as e:
            _log.exception("Exception during process_requests()", exc_info=e)
            raise

    def stop(self):
        """Stop preview"""
        self._abort.set()
        self.thread.join()
        self.picam2.detach_preview()
        self.picam2 = None

    def set_title_function(self, function):
        pass
      
    paused = False
        
    def pause(self):
      self.paused = True
      
    def resume(self):
      self.paused = False