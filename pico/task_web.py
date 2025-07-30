import biplane
import asyncio
import os

import logging

LOGGER = logging.getLogger(__name__)


server = biplane.Server()


@server.route("/", "GET")
def do_root(query_parameters, headers, body):
    with open('index.html') as f:
        content = f.read()
    return biplane.Response(content, content_type="text/html")


class WebServer:
    
    async def run_task(self):
        LOGGER.info('Starting run_task for WebServer')
        for _ in server.circuitpython_start_wifi_ap(
                os.getenv('CIRCUITPY_WIFI_SSID'),
                os.getenv('CIRCUITPY_WIFI_PASSWORD'), 
                'app'):
            await asyncio.sleep(0)  # let other tasks run
