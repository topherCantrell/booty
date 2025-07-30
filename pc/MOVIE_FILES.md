The treasure chest runs a movie-player that reads frame information from a binary
file. The format of that binary file is given below.

There is also a text-to-binary compiler that reads a text file to generate the binary.
Or you can write your own binary file maker!

I use other programs to draw sprites in the text format and compile that into binary.

# Binary Format

The binary file is a list of records. Every record begins with a byte TYPE followed
by two bytes for the remaining size, little-end first. The size is the remaining
bytes in the record (not counting the TYPE or SIZE).

When the player reaches the end of the file, it automatically restarts at the beginning.

## Set Color Palette

Use this record to set the colors of one or more palette values

```
01 nn nn aa xx rr gg bb yy rr gg bb ...
```

The record is a list of 4 items:
  - index into the palette (color number)
  - red
  - green
  - blue

## Pause

Use this record to pause the movie between frames

```
02 nn nn aa bb
```

The length is always 00 02. aa bb is the number of miliseconds to pause.

## Pixel Frame

```
03 nn nn ww ww .......
```

This is a single frame of pixels. ww is the width of the frame (little end first). The height of the
frame is the total size of the data divided by the width.

The rest of the data in the record is one byte per pixel -- top left to bottom right.

# Text Format

```

# Everything after the pound sign is a comment. Comments can be entire
# lines or the end of a line.

# The "~" begins a command line. Anything else is considered a pixel frame.

# The "color" command sets the palette for a given color index. Multiple
# color specifications are gathered together into a single record in the
# movie.

~ color 1 (10,0,0)  # Red
~ color X (0,10,0)  # Green

# Variables to be used later (for delays between frames)

~ set delay1 1000
~ set delay2 delay1 / 10

# Blank lines are ignored. Blanks at the beginning and end of any line are ignored.

# Movie frames are defined in ascii art with one character per pixel. The "." character
# maps to 0 by default, but it can be remapped with a color command.

# White space is ignored. The "|" and "-" characters are ignored (can be used for reference
# lines in a frame)
......X.
.1....X.
..1...X.
...1..X.

# Every frame ends with another command or the end of the file.

# The pause command halts the player between frames. The numberical value is 
# the number of miliseconds.

~ pause 1000  # Pause for 1 second

......X.
.1....X.
..1...X.
...1..X.

~ pause (delay2 + delay1) * 2 # Expressions and variables are allowed

# Automatically repeats to top
```


