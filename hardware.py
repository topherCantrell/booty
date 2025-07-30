import board
import digitalio
import neopixel
import weavers


class Hardware:    

    def __init__(self, using_dev=False, simulate_chest=True):
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

        self.weaver = None
        
        if using_dev:
            # This is the larger dev board -- 32x24
            # Bottom panel (32x8)
            self.neo1 = neopixel.NeoPixel(board.GP0, 256, auto_write=False)
            # Upper right (16x16)
            self.neo2 = neopixel.NeoPixel(board.GP1, 256, auto_write=False)
            # Upper left (16x16)
            self.neo3 = neopixel.NeoPixel(board.GP2, 256, auto_write=False)
            if simulate_chest:
                # Pretend the display is the real chest
                self.weaver = weavers.weaveChestDev
            else:
                # We are using all the leds on the dev board
                self.weaver = weavers.weaveDev
        else:
            # This is the chest display (or simulated chest) -- 29x24
            # Bottom panel (29x8)
            self.neo1 = neopixel.NeoPixel(board.GP0, 232, auto_write=False)
            # Upper right (13x16)
            self.neo2 = neopixel.NeoPixel(board.GP1, 208, auto_write=False)
            # Upper left (16x16)
            self.neo3 = neopixel.NeoPixel(board.GP2, 256, auto_write=False)
            self.weaver = weavers.weaveChest

        # Blank the screen
        self.neo1.show()
        self.neo2.show()
        self.neo3.show()
    
    def get_neos(self):
        return self.neo1, self.neo2, self.neo3
    
    def get_buttons(self):
        return not self.bt_red.value, not self.bt_green.value, not self.bt_blue.value