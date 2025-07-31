from frame import Frame
from grid import Grid

import ascii_art

async def run_task(hard, bts):

    fr = Frame(hard)
    fr.set_color(8,(0, 0, 10)) # Scared ghost body
    fr.set_color(9,(10, 0, 0)) # Scared ghost eyes

    grid = Grid(29,24)

    lines = ascii_art.load_art_lines('/animations/sprites.txt')
    img = ascii_art.make_images(lines)

    ghosts_width = img['GHOSTS']['width']
    ghosts_height = img['GHOSTS']['height']
    ghosts_images = img['GHOSTS']['images']
    
    pac_width = img['PACMAN']['width']
    pac_height = img['PACMAN']['height']
    pac_images = img['PACMAN']['images']

    
    # Left to right
    ghosts = [2,3] # ghost facing right (2 animations)
    pacs = [3,2,8,2] # pacman facing right (4 animations)
    for i in range(-30,30):
        grid.fill(0)  # Clear the grid
        grid.draw_image(ghosts_images[ghosts[i%2]], i, 5, ghosts_width, ghosts_height)    
        grid.draw_image(pac_images[pacs[i%4]], i+14, 5, pac_width, pac_height, transparent_color=0, color_offset=3)  
        fr.show(grid)
        await bts.pause_check_buttons(0.1)

    # Right to left
    ghosts = [8, 9] # scared ghost (2 animations)
    pacs = [7, 6, 8, 6] # pacman facing left (4 animations)
    for i in range(30,-30,-1):
        grid.fill(0)  # Clear the grid
        grid.draw_image(ghosts_images[ghosts[i%2]], i, 5, ghosts_width, ghosts_height,transparent_color=0, color_offset=7)    
        grid.draw_image(pac_images[pacs[i%4]], i+14, 5, pac_width, pac_height, transparent_color=0, color_offset=3)  
        fr.show(grid)
        await bts.pause_check_buttons(0.1)