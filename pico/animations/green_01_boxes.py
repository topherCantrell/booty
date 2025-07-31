import random

async def run_task(hard, bts):

    hard.clear()

    for _ in range(200):
        x = random.randint(0, 28)
        y = random.randint(0, 23)
        width = random.randint(1, 10)
        height = random.randint(1, 10)
        color = (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))

        if x + width > 29:
            width = 29 - x
        if y + height > 24:
            height = 24 - y
        
        for i in range(x, x + width):
            for j in range(y, y + height):
                neo, ind = hard.map_coordinates(i, j)
                neo[ind] = color
    
        hard.show()
        await bts.pause_check_buttons(0.1)
