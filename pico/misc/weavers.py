# NeoPixel strips are organized into grids by weaving the strips back
# and forth. You need a bit of math (the weave functions below) to map
# a single 2D image onto the three strips. 
#
# The dev board has 3 extra columns of pixels. These extra columns were
# cut (with scissors) from the grids to make them fit in the chest.
#
# The weavers below allow you to map a 29x24 image onto the chest hardware.
# Or you can map a 32x24 image onto the dev board hardware.
# Or you can simulate the 29x24 chest display on the 32x24 dev board.
#
# Here is how the strips are organized on the chest hardware and on the 
# dev board:

# ----- CHEST DISPLAY 29x24 in 3 strips -----
# 0..............X|0............
# 1...............|1............
# 2...............|2............
# ................|.............
# ................|.............
# ................|.............
# ....neo3........|....neo2.....
# ................|.............
# ................|.............
# ................|.............
# ................|.............
# ................|.............
# .c..............|.c...........
# .b..............|.b...........
# .a..............|.a...........
# F0..............|F0..........X
# ----------------+-------------
# X..........................87
# ...........................9.
# ....neo1...................A.
# .............................
# ............................3
# ............................2
# ............................1
# ............................0

# ----- DEV BOARD DISPLAY 32x24 in 3 strips -----
# 0..............X|0...............
# 1...............|1...............
# 2...............|2...............
# ................|................
# ................|................
# ................|................
# ....neo3........|....neo2........
# ................|................
# ................|................
# ................|................
# ................|................
# ................|................
# .c..............|.c..............
# .b..............|.b..............
# .a..............|.a..............
# F0..............|F0.............X
# ----------------+----------------
# X.............................87
# ..............................9.
# .......neo1...................A.
# ................................
# ...............................3
# ...............................2
# ...............................1
# ...............................0

def weaveChest(im, n1=None, n2=None, n3=None):
    """ For the display in the lid of the chest: 29x24 pixels.

    Args:
       im: a 696 pixel image as a bytearray (29x24)
       n1, n2, n3: optional bytearrays to fill in. If None, new ones are created.

    Returns:
       n1, n2, and n3 for neo1, neo2, and neo3
    """

    if n1 is None:
        n1 = bytearray(232)  # bottom right, but upside down
        n2 = bytearray(208)  # upper right
        n3 = bytearray(256)  # upper left

    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            n3[x*16+y] = im[y*29+x]
            n3[(x+1)*16+(15-y)] = im[y*29+x+1]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 14:
            n2[x*16+y] = im[y*29+x+16]
            if x < 12:
                n2[(x+1)*16+(15-y)] = im[y*29+x+1+16]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 30:
            n1[x*8+y] = im[(23-y)*29+(28-x)]
            if x < 28:
                n1[(x+1)*8+(7-y)] = im[(23-y)*29+(28-x-1)]
            x += 2
        y += 1
    return n1, n2, n3

def weaveDev(im, n1=None, n2=None, n3=None):
    """ For the larger dev board display: 32x24 pixels.

    Args:
       im: a 768 pixel image as a bytearray (32x24)
       n1, n2, n3: optional bytearrays to fill in. If None, new ones are created.

    Returns:
       n1, n2, and n3 for neo1, neo2, and neo3
    """
    if n1 is None:
        n1 = bytearray(256)  # bottom right, but upside down
        n2 = bytearray(256)  # upper right
        n3 = bytearray(256)  # upper left

    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            n3[x*16+y] = im[y*32+x]
            n3[(x+1)*16+(15-y)] = im[y*32+x+1]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            n2[x*16+y] = im[y*32+x+16]
            n2[(x+1)*16+(15-y)] = im[y*32+x+1+16]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 32:
            n1[x*8+y] = im[(23-y)*32+(31-x)]
            n1[(x+1)*8+(7-y)] = im[(23-y)*32+(31-x-1)]
            x += 2
        y += 1

    return n1, n2, n3

def weaveChestDev(im, n1=None, n2=None, n3=None):
    """ Simulate the smaller chest display on the larger dev board 

    Args:
       im: a 696 pixel image as a bytearray (29x24)
       n1, n2, n3: optional bytearrays to fill in. If None, new ones are created.

    Returns:
       n1, n2, and n3 for neo1, neo2, and neo3
    """
    if n1 is None:
        # A little trickery here. There are 3 extra columns at the beginning of this
        # strip on the dev board. We make a full 256 pixel array that includes the pad.
        n1 = bytearray(256)  # bottom right, but upside down
        n2 = bytearray(208)  # upper right
        n3 = bytearray(256)  # upper left

    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            n3[x*16+y] = im[y*29+x]
            n3[(x+1)*16+(15-y)] = im[y*29+x+1]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 14:
            n2[x*16+y] = im[y*29+x+16]
            if x < 12:
                n2[(x+1)*16+(15-y)] = im[y*29+x+1+16]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 30:
            n1[x*8+(7-y)+24] = im[(23-y)*29+(28-x)]
            if x < 28:
                n1[(x+1)*8+y+24] = im[(23-y)*29+(28-x-1)]
            x += 2
        y += 1
    return n1, n2, n3

