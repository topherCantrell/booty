# Some default colors
DEFAULT_COLORS = [
    (0, 0, 0),     # Black
    (10, 0, 0),    # Red
    (0, 10, 0),    # Green
    (0, 0, 10),    # Blue
    (10, 10, 0),   # Yellow
    (10, 0, 10),   # Purple
    (0, 10, 10),   # Teal
    (10, 10, 10),  # White
]

class Frame:
    """ Presents the three display strips as a single 2D grid with 256 pixels.

    You create a Frame from an existing Hardware instance that has been configured
    for the hardware you are using (actual chest, simulated chest, or development board).

    Args:
        hardware: configured instance of Hardware that provides access to the NeoPixel strips.
    """

    def __init__(self, hardware):
        """ Create a Frame object over the given hardware.

        Args:
            hardware: configured instance of Hardware that provides access to the NeoPixel strips.
        """
        self.hardware = hardware

        # The panel is built from three separate strips
        self.neo1, self.neo2, self.neo3 = hardware.get_neos()

        self.color_palette = [(0,0,2)] * 256  # Make space for 256 colors
        for i in range(len(DEFAULT_COLORS)):
            self.color_palette[i] = DEFAULT_COLORS[i]

        self.cache_neo1 = None
        self.cache_neo2 = None
        self.cache_neo3 = None

    def set_color(self, index, color):
        """ Set the RGB color value for one of the 256 colors in the palette."""
        self.color_palette[index] = color

    def get_color(self, index):
        """ Get the RGB color value for one of the 256 colors in the palette."""
        return self.color_palette[index]
    
    def show(self, grid):
        """ Draw the 2D image onto the three neo strips.
        
        The incoming image is a bytearray or any object with a buffer
        that is a bytearray (like the Grid class in this library).
        """
        # We can work with bytearrays or anything that has a bytearray
        if hasattr(grid, 'buffer'):                
            grid = grid.buffer        
        s1, s2, s3 = self.hardware.weaver(grid, self.cache_neo1, self.cache_neo2, self.cache_neo3)
        if self.cache_neo1 is None:
            # The data isn't important in the cache, just the size and space
            self.cache_neo1 = s1
            self.cache_neo2 = s2
            self.cache_neo3 = s3
        self.show_strips(s1, s2, s3)


    def show_strips(self, s1, s2, s3):
        """Draw the woven image (three pixel arrays) onto the the three neo strips.

        This skips the weaving if you already have the data prepared.
        """

        # Chase the pointers into local variables for faster access        
        n1 = self.neo1
        n2 = self.neo2
        n3 = self.neo3
        pal = self.color_palette

        # WHILE loops are faster than range iteration -- when every
        # cycle counts.

        y = 0
        size_s1 = len(s1)
        size_s2 = len(s2)
        size_s3 = len(s3)

        while y < size_s1:
            n1[y] = pal[s1[y]]
            y += 1
        y = 0
        while y < size_s2:
            n2[y] = pal[s2[y]]
            y += 1
        y = 0
        while y < size_s3:
            n3[y] = pal[s3[y]]
            y += 1

        # Update all the panels
        n1.show()
        n2.show()
        n3.show()
