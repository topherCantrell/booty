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

def weaveChest():
    """ For the display in the lid of the chest: 29x24 pixels.   
    """    

    ret = [] # [neo, index]
    for _ in range(29*24):
        ret.append([-1,-1])

    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            # n3[x*16+y] = im[y*29+x]
            # n3[(x+1)*16+(15-y)] = im[y*29+x+1]
            ret[y*29+x] = [2, x*16+y]
            ret[y*29+x+1] = [2, (x+1)*16+(15-y)]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 14:
            # n2[x*16+y] = im[y*29+x+16]
            ret[y*29+x+16] = [1, x*16+y]
            if x < 12:
                # n2[(x+1)*16+(15-y)] = im[y*29+x+1+16]
                ret[y*29+x+1+16] = [1, (x+1)*16+(15-y)]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 30:
            # n1[x*8+y] = im[(23-y)*29+(28-x)]
            ret[(23-y)*29+(28-x)] = [0, x*8+y]
            if x < 28:
                # n1[(x+1)*8+(7-y)] = im[(23-y)*29+(28-x-1)]
                ret[(23-y)*29+(28-x-1)] = [0, (x+1)*8+(7-y)]
            x += 2
        y += 1
    return ret

def weaveDev():
    """ For the larger dev board display: 32x24 pixels.
    """

    ret = [] # [neo, index]
    for _ in range(32*24):
        ret.append([-1,-1])
    
    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            # n3[x*16+y] = im[y*32+x]
            # n3[(x+1)*16+(15-y)] = im[y*32+x+1]
            ret[y*32+x] = [2, x*16+y]
            ret[y*32+x+1] = [2, (x+1)*16+(15-y)]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            # n2[x*16+y] = im[y*32+x+16]
            # n2[(x+1)*16+(15-y)] = im[y*32+x+1+16]
            ret[y*32+x+16] = [1, x*16+y]
            ret[y*32+x+1+16] = [1, (x+1)*16+(15-y)]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 32:
            # n1[x*8+y] = im[(23-y)*32+(31-x)]
            # n1[(x+1)*8+(7-y)] = im[(23-y)*32+(31-x-1)]
            ret[(23-y)*32+(31-x)] = [0, x*8+y]
            ret[(23-y)*32+(31-x-1)] = [0, (x+1)*8+(7-y)]
            x += 2
        y += 1

    return ret

def weaveChestDev():
    """ Simulate the smaller chest display on the larger dev board    
    """

    ret = [] # [neo, index]
    for _ in range(29*24):
        ret.append([-1,-1])

    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            # n3[x*16+y] = im[y*29+x]
            # n3[(x+1)*16+(15-y)] = im[y*29+x+1]
            ret[y*29+x] = [2, x*16+y]
            ret[y*29+x+1] = [2, (x+1)*16+(15-y)]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 14:
            # n2[x*16+y] = im[y*29+x+16]
            ret[y*29+x+16] = [1, x*16+y]
            if x < 12:
                # n2[(x+1)*16+(15-y)] = im[y*29+x+1+16]
                ret[y*29+x+1+16] = [1, (x+1)*16+(15-y)]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 30:
            # n1[x*8+(7-y)+24] = im[(23-y)*29+(28-x)]
            ret[(23-y)*29+(28-x)] = [0, x*8+(7-y)+24]
            if x < 28:
                # n1[(x+1)*8+y+24] = im[(23-y)*29+(28-x-1)]
                ret[(23-y)*29+(28-x-1)] = [0, (x+1)*8+y+24]
            x += 2
        y += 1

    return ret

def write_data(fname, data):
    """ Write the data to a file in a format that can be read by the C code. """
    with open(fname, 'wb') as f:
        for item in data:
            f.write(bytes(item))

d = weaveChest()
write_data("chest_display.bin", d)  
print("Weaved chest display:", d)

d = weaveDev()
write_data("dev_display.bin", d)  
print("Weaved dev display:", d)

d = weaveChestDev()
write_data("chestdev_display.bin", d)  
print("Weaved chestdev display:", d)