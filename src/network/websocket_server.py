import asyncio
import json

from websockets.asyncio.server import broadcast, serve
from utils.hr_monitor import HRMonitor
from configparser import ConfigParser

# Idk how to make websocket servers, sorry if this is awful
# Also I think it doesn't need a websocket server and I should just use the http one
# to host the overlay and update it, but ofc idk how to do this in http

class SimpleWSServer:
    hr_monitor: HRMonitor
    update_freq: int
    show_bpm_updates: bool

    CONNECTIONS: set
    PORT: int

    def __init__(self, cfg: ConfigParser):
        self.CONNECTIONS = set()
        self.PORT = cfg.getint("Server", "WSServerPort")
        self.load_config(cfg)

        self.hr_monitor = HRMonitor(cfg)
    
    def load_config(self, cfg: ConfigParser):
        self.update_freq = cfg.getint("CalculationParameters", "bpmCalculationFrequency")
        self.show_bpm_updates = cfg.getboolean("Console", "BpmUpdates")

    def start_server(self):
        asyncio.run(self.main())

    async def register(self, websocket):
        self.CONNECTIONS.add(websocket)
        print(f"Connected to {websocket}")

        # Send the current bpm for new connections
        event = {
            "type": "bpm_update",
            "value": self.hr_monitor.current_bpm
        }
        await websocket.send(json.dumps(event))

        try:
            await websocket.wait_closed()
        finally:
            self.CONNECTIONS.remove(websocket)
            print(f"Disconnected {websocket}")

    async def update_bpm(self):
        while True:
            previous_bpm = self.hr_monitor.current_bpm

            self.hr_monitor.update()
            event = {
                "type": "bpm_update",
                "value": self.hr_monitor.current_bpm
            }

            if previous_bpm != self.hr_monitor.current_bpm:
                if self.show_bpm_updates:
                    print(f"Current bpm: {self.hr_monitor.current_bpm} | Update rate: {self.update_freq} frames/second")
                
                for websocket in self.CONNECTIONS:
                    await websocket.send(json.dumps(event))
                    # print(f"Sent message to: {websocket} | Message: {str(event)}")

                continue
            
            await asyncio.sleep(0.1)

    async def main(self):
        print(f"Websocket server started at port: {self.PORT}")
        async with serve(self.register, "localhost", int(self.PORT)):
            await self.update_bpm()