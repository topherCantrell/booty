import os
import asyncio
from task_web import WebServer

async def chest_task():

    animations = {
        'red': [],
        'green': [],
        'blue': []
    }

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

    for _, value in animations.items():
        value.sort(key=lambda x: x['position']) 

    print("Animations loaded:", animations)

    while True:
        print("Chest task running...")
        await asyncio.sleep(1)

web_server = WebServer()

asyncio.run(asyncio.gather(web_server.run_task(), chest_task()))
