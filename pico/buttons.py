import asyncio

class ButtonPressedAbort(Exception):
    pass

class Buttons:
        
    def __init__(self, hardware):
        self.hardware = hardware
        self._last_red, self._last_green, self._last_blue = hardware.get_buttons()

    async def wait_no_button(self):
        """ Wait until no buttons are pressed. """
        while True:
            v_red, v_green, v_blue = self.hardware.get_buttons()
            self._last_red, self._last_green, self._last_blue = v_red, v_green, v_blue
            if not v_red and not v_green and not v_blue:
                return
            await asyncio.sleep(0.1)
        
    async def pause_check_buttons(self, t):
        """ Wait the given time or until a button is pressed.
        
        If a button is pressed, raise ButtonPressedAbort with the color of the button.
        
        Args:
            t: Time to wait in seconds (float) 
        """
        t = int(t*10)  # whole number of 100ths of a second
        while True:
            v_red, v_green, v_blue = self.hardware.get_buttons()
            if v_red and not self._last_red:
                self._last_red = v_red
                raise ButtonPressedAbort('red')
            if v_green and not self._last_green:
                self._last_green = v_green
                raise ButtonPressedAbort('green')
            if v_blue and not self._last_blue:
                self._last_blue = v_blue
                raise ButtonPressedAbort('blue')
            self._last_red, self._last_green, self._last_blue = v_red, v_green, v_blue
            if t <= 0:
                return
            await asyncio.sleep(0.1)
            t -= 1