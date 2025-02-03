import asyncio
from websockets.asyncio.server import broadcast, serve

import configparser

from utils.hr_monitor import HRMonitor

CONFIG_PATH = "config.ini"

cfg = configparser.ConfigParser()
cfg.read(CONFIG_PATH)

heart_rate_monitor = HRMonitor(cfg)
frequency = int(cfg.get("CalculationParameters", "bpmCalculationFrequency"))

CONNECTIONS = set()

async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

async def update_bpm():
    i = 0
    while True:
        heart_rate_monitor.update()
        i = i + 1

        if i >= frequency:
            message = str(heart_rate_monitor.current_bpm)
            broadcast(CONNECTIONS, message)
            i = 0

            await asyncio.sleep(0.1)

async def main():
    async with serve(register, "localhost", int(cfg.get("Server", "ServerPort"))): 
        await update_bpm()

asyncio.run(main())