import random

async def run_task(hard, bts):    
    for _ in range(150):
        for _ in range(150):
            x = random.randint(0, 28)
            y = random.randint(0, 23)
            neo, ind = hard.map_coordinates(x, y)
            neo[ind] = (random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))
        hard.show()       
        await bts.pause_check_buttons(0.1)
