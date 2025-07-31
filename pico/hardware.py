import os
import board
import digitalio
import neopixel

class Hardware:    

    def __init__(self):
        """ Initialize the neo strips and buttons.

        If you are writing code that runs on the chest hardware, then
        pass using_dev=False.

        If you are writing code that runs on the dev board, then
        pass using_dev=True. If you want to test code for the chest
        on the dev board, then also pass simulate_chest=True.

        Args:
            using_dev (bool): True if running on the dev board hardware, False for chest hardware.
            simulate_chest (bool): True if you want to simulate the chest display on the dev board.
        """

        self.bt_red = digitalio.DigitalInOut(board.GP3)
        self.bt_red.pull = digitalio.Pull.UP

        self.bt_green = digitalio.DigitalInOut(board.GP4)
        self.bt_green.pull = digitalio.Pull.UP

        self.bt_blue = digitalio.DigitalInOut(board.GP5)
        self.bt_blue.pull = digitalio.Pull.UP

        self.mode = os.getenv('FRAME_MODE', 'chest')

        self.mapping = None

        path = __file__
        i = path.rfind('/')
        if i >= 0:
            path = path[:i]
        else:
            path = ''

        self.height = 24
        if self.mode == 'chest':
            # This is the chest display -- 29x24
            # Bottom panel (29x8)
            self.neo1 = neopixel.NeoPixel(board.GP0, 232, auto_write=False)
            # Upper right (13x16)
            self.neo2 = neopixel.NeoPixel(board.GP1, 208, auto_write=False)
            # Upper left (16x16)
            self.neo3 = neopixel.NeoPixel(board.GP2, 256, auto_write=False)            
            with open(path+'/chest_display.bin', 'rb') as f:
                self.mapping = f.read()
            self.width = 29            
        else:            
            # This is the larger dev board -- 32x24
            # Bottom panel (32x8)
            self.neo1 = neopixel.NeoPixel(board.GP0, 256, auto_write=False)
            # Upper right (16x16)
            self.neo2 = neopixel.NeoPixel(board.GP1, 256, auto_write=False)
            # Upper left (16x16)
            self.neo3 = neopixel.NeoPixel(board.GP2, 256, auto_write=False)   
            if self.mode == 'simchest':
                # Simulate the chest display on the dev board
                with open(path+'/chestdev_display.bin', 'rb') as f:
                    self.mapping = f.read()
                self.width = 29
            else:
                # Use the full dev board display
                with open(path+'/dev_display.bin', 'rb') as f:
                    self.mapping = f.read()
                self.width = 32

        # Blank the screen
        self.neo1.show()
        self.neo2.show()
        self.neo3.show()

        # As a list
        self.neos = [self.neo1, self.neo2, self.neo3]

    def clear(self):
        self.neo1.fill((0, 0, 0))
        self.neo2.fill((0, 0, 0))
        self.neo3.fill((0, 0, 0))
        self.show()

    def show(self):
        """ Show the current state of the three neo strips. """
        self.neo1.show()
        self.neo2.show()
        self.neo3.show()

    def map_coordinates(self, x, y):
        """ Map 2D coordinates to a strip and index tuple.

        Args:
            x (int): X coordinate (0-31 for dev board, 0-28 for chest).
            y (int): Y coordinate (0-23).

        Returns:
            (strip, int): The neopixel strip and the pixel index into that strip.
        """
        ofs = (y * self.width + x)*2
        return self.neos[self.mapping[ofs]], self.mapping[ofs+1]    
    
    def get_buttons(self):
        return not self.bt_red.value, not self.bt_green.value, not self.bt_blue.value