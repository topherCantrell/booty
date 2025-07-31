class Grid:
    """Handles drawing on a 2D grid of pixels.

    The internal storage is a bytearray where each pixel is represented by a single byte.
    This class provides methods to get and set pixel values at specific coordinates.

    This class contains the drawing primitives for pixels, lines, rectangles, text,
    images, and more.

    Pass an instance of this class to the `Frame` class to render the grid on the display.
    Note that `Frame` expects it to be perfectly sized.    
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = bytearray(width*height)

    def get(self, x, y):
        """Get the pixel value at the specified (x, y) coordinates."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None  # Ignore out-of-bounds coordinates
        return self.buffer[self.width*y+x]

    def set(self, x, y, value):
        """Set the pixel value at the specified (x, y) coordinates."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return  # Ignore out-of-bounds coordinates
        self.buffer[self.width*y+x] = value

    def clear(self):
        """Clear the grid by setting all pixel values to 0."""
        self.fill(0)

    def fill(self, value):
        """Fill the grid with the specified value."""
        for i in range(len(self.buffer)):
            self.buffer[i] = value

    def draw_line(self, x1, y1, x2, y2, color):
        """Draw a line from (x1, y1) to (x2, y2) with the specified color."""
        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.set(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            err2 = err * 2
            if err2 > -dy:
                err -= dy
                x1 += sx
            if err2 < dx:
                err += dx
                y1 += sy
        

    def draw_rect(self, x, y, width, height, color, fill=False):
        # TODO
        raise NotImplementedError("draw_rect not implemented yet")

    def draw_text(self, text, x, y, color):
        # TODO
        raise NotImplementedError("draw_text not implemented yet")

    def draw_image(self,image, x, y, width, height, color_offset=0,transparent_color=None):
        """Draw an image on the grid at the specified (x, y) coordinates.

        The image is a 2D array of pixel values in a flat bytearray. The width and height
        of the image is passed in.

        Images are clipped to the grid boundaries, so if the image extends beyond the grid,
        only the part that fits within the grid will be drawn (great for objects that move
        onto and off the grid).

        Args:
            image: The image data (width * height bytes).
            x: The x-coordinate to start drawing the image.
            y: The y-coordinate to start drawing the image.
            width: The width of the image.
            height: The height of the image.
            color_offset: An optional offset to add to each pixel value (default is 0).
            transparent_color: The color that should be treated as transparent (default is None).
        
        """
        for j in range(height):
            yy = y + j
            if yy < 0 or yy >= self.height:
                continue
            for i in range(width):
                xx = x + i
                if xx < 0 or xx >= self.width:
                    continue
                pixel = image[j * width + i]
                if pixel != transparent_color:
                    # Only set the pixel if it's not the transparent color
                    # Manipulate the pixel directly to avoid the bounds check in the set method
                    self.buffer[self.width*yy+xx] = pixel + color_offset                    
