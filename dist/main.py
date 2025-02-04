import asyncio
import configparser
import threading
from network.websocket_server import SimpleWSServer
from network.http_server import SimpleHttpServer

CONFIG_PATH = "config.ini"

cfg = configparser.ConfigParser()
cfg.read(CONFIG_PATH)

http_server = SimpleHttpServer(cfg)
ws_server = SimpleWSServer(cfg)

threads = [
    threading.Thread(target=http_server.start_server),
    threading.Thread(target=ws_server.start_server)
]

for thread in threads:
    thread.start()
    print(f"Threads {thread} started")
    thread.join(0.1)

# http_server.start_server()