class Grid:
    """Represents a 2D grid of pixels.

    The internal storage is a bytearray where each pixel is represented by a single byte.
    This class provides methods to get and set pixel values at specific coordinates.
    
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = bytearray(width*height)

    def get(self, x, y):
        """Get the pixel value at the specified (x, y) coordinates."""
        return self.buffer[self.height*y+x]

    def set(self, x, y, value):
        """Set the pixel value at the specified (x, y) coordinates."""
        self.buffer[self.height*y+x] = value
