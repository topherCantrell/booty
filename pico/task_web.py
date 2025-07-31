import biplane
import asyncio
import os

import logging

LOGGER = logging.getLogger(__name__)


server = biplane.Server()

def return_root():
    with open('index.html') as f:
        content = f.read()
    return biplane.Response(content, content_type="text/html")

@server.route("/", "GET")
def do_root(query_parameters, headers, body):
    return return_root()    

@server.route("/red", "GET")
def do_red(query_parameters, headers, body):
    BTS.inject_press('red')
    return return_root()

@server.route("/green", "GET")
def do_green(query_parameters, headers, body):
    BTS.inject_press('green')
    return return_root()

@server.route("/blue", "GET")
def do_blue(query_parameters, headers, body):
    BTS.inject_press('blue')
    return return_root()


class WebServer:

    def __init__(self, bts):
        global BTS
        BTS = bts
    
    async def run_task(self):
        LOGGER.info('Starting run_task for WebServer')
        for _ in server.circuitpython_start_wifi_ap(
                os.getenv('CIRCUITPY_WIFI_SSID'),
                os.getenv('CIRCUITPY_WIFI_PASSWORD'), 
                'app'):            
            await asyncio.sleep(0)  # let other tasks run
