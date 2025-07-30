import board
import digitalio
import neopixel
import time

# The panel is built from three separate strips
neo1 = neopixel.NeoPixel(board.GP0, 232, auto_write=False)  # Bottom
neo2 = neopixel.NeoPixel(board.GP1, 208, auto_write=False)  # Upper right
neo3 = neopixel.NeoPixel(board.GP2, 256, auto_write=False)  # Upper left

# TODO push buttons for red.bin, green.bin, blue.bin


def play_movie(filename):
    colors = [(0, 0, 0)]*256
    with open(filename, 'rb') as f:
        while True:
            data = f.read(3)
            if not data:
                break
            typ = data[0]
            ln = data[1]+(data[2] << 8)
            msg = f.read(ln)
            if typ == 1:
                # Colors
                pos = 0
                while pos < len(msg):
                    colors[msg[pos]] = (msg[pos+1], msg[pos+2], msg[pos+3])
                    pos += 4
            elif typ == 2:
                # Pause
                delay = msg[0] + (msg[1] << 8)
                time.sleep(delay/1000)
            elif typ == 3:
                # Pixel frame
                pos = 0
                while pos < 232:
                    neo1[pos] = colors[msg[pos]]
                    pos += 1
                pos = 0
                while pos < 208:
                    neo2[pos] = colors[msg[pos+232]]
                    pos += 1
                pos = 0
                while pos < 256:
                    neo3[pos] = colors[msg[pos+440]]
                    pos += 1
                neo1.show()
                neo2.show()
                neo3.show()


while True:
    play_movie('pac.bin')
