import board
import digitalio
import neopixel
import random
import time

# Bottom panel (29x8)
neo1 = neopixel.NeoPixel(board.GP0, 232, auto_write=False)
# Upper right (13x16)
neo2 = neopixel.NeoPixel(board.GP1, 208, auto_write=False)
# Upper left (16x16)
neo3 = neopixel.NeoPixel(board.GP2, 256, auto_write=False)

# For debugging -- show the separate panels
# neo1.fill((2, 0, 0))  # Red
# neo2.fill((0, 2, 0))  # Green
# neo3.fill((0, 0, 2))  # Blue
# neo1.show()
# neo2.show()
# neo3.show()
# raise Exception("STOP")

# The buttons are pulled up. They are TRUE when not pressed
# and FALSE when pressed.

bt_red = digitalio.DigitalInOut(board.GP3)
bt_red.pull = digitalio.Pull.UP

bt_green = digitalio.DigitalInOut(board.GP4)
bt_green.pull = digitalio.Pull.UP

bt_blue = digitalio.DigitalInOut(board.GP5)
bt_blue.pull = digitalio.Pull.UP

while True:

    # Use the buttons to set sold colors
    if not bt_red.value:
        neo1.fill((2, 0, 0))  # Red
        neo2.fill((2, 0, 0))  # Red
        neo3.fill((2, 0, 0))  # Red
        neo1.show()
        neo2.show()
        neo3.show()
        time.sleep(1)
    elif not bt_green.value:
        neo1.fill((0, 2, 0))  # Green
        neo2.fill((0, 2, 0))  # Green
        neo3.fill((0, 2, 0))  # Green
        neo1.show()
        neo2.show()
        neo3.show()
        time.sleep(1)
    elif not bt_blue.value:
        neo1.fill((0, 0, 2))  # Blue
        neo2.fill((0, 0, 2))  # Blue
        neo3.fill((0, 0, 2))  # Blue
        neo1.show()
        neo2.show()
        neo3.show()
        time.sleep(1)

    # Randomly set 50 pixels on each panel (150 total)
    for _ in range(50):
        neo1[random.randint(0, 231)] = (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))
        neo2[random.randint(0, 207)] = (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))
        neo3[random.randint(0, 255)] = (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))
    neo1.show()
    neo2.show()
    neo3.show()
    