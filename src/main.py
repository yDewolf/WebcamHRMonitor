import configparser
from api.flask_api import FlaskServer

CONFIG_PATH = "config.ini"

cfg = configparser.ConfigParser()
cfg.read(CONFIG_PATH)

server = FlaskServer("__main__", cfg)
server.run()