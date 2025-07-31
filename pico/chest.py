import os
import asyncio
from task_web import WebServer
from hardware import Hardware

import buttons

async def chest_task(hard, bts):
    """ Main task for the chest animations. 

    This task will run animations based on button presses.    
    """

    # Three different sets of animations. Each set mapped to a button.
    animations = {
        'red': [],
        'green': [],
        'blue': []
    }

    # Load animations from files in the 'animations' directory.
    # The module names include the name, color, and position in the sequence.
    files = os.listdir('animations')
    for file in files:
        try:
            module_name = file[:-3]  # Remove .py extension
            parts = module_name.split('_',3)
            color = parts[0]
            if color not in ['red', 'green', 'blue']:
                raise ValueError(f'Invalid color {color}')
            position = int(parts[1])
            name = parts[2]
            module = __import__(f'animations.{module_name}')
            sub_module = getattr(module, module_name)
            task_function = getattr(sub_module, 'run_task', None)
            if not callable(task_function):
                raise ValueError(f'Function run_task not found in {file}')
            animations[color].append({
                'name': name,
                'position': position,
                'task': task_function
            })
        except Exception as e:
            print(f"Ignoring file {file}: {e}")

    # Sort each of the three lists by position
    for _, value in animations.items():
        value.sort(key=lambda x: x['position']) 

    print("Animations loaded:", animations)

    # Start with the first animation in the red set
    current_color = 'red'
    current_position = 0

    while True:
        if current_position >= len(animations[current_color]):
            # Done with the current set? Advance to the first entry in the next button set.
            current_color = 'green' if current_color == 'red' else 'blue' if current_color == 'green' else 'red'
            current_position = 0
            # This continue lets us ignore empty sets of animations.
            continue
        animation = animations[current_color][current_position]
        print(f"{current_color} {current_position} {animation['name']} running...")
        try:
            # Run the animation task until it completes or a button is pressed.            
            await animation['task'](hard, bts)            
            # Advance to the next animation
            current_position += 1            
            await asyncio.sleep(1)  # Short pause to let other tasks run
        except buttons.ButtonPressedAbort as e:
            e = str(e)
            print(f"Button pressed: {e}")
            if e == current_color:
                # Advance to the next animation in the current color set
                current_position += 1
                if current_position >= len(animations[current_color]):
                    # Stay within the same color set                    
                    current_position = 0
            else:
                # Advance to the next color set
                current_color = e
                current_position = 0

# The hardware object manages the three neo strips and buttons.
hard = Hardware()

# This object tracks the button states and pauses while watching for button presses.
bts = buttons.Buttons(hard)

# Create the web server and buttons objects.
web_server = WebServer(bts)

# Two tasks: one for the web server and one for the chest animations.
asyncio.run(asyncio.gather(web_server.run_task(), chest_task(hard, bts)))
