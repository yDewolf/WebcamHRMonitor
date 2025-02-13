from threading import Thread
from flask import Flask, jsonify, render_template
from configparser import ConfigParser
from utils.hr_monitor import HRMonitor
import logging

class FlaskServer:
    app: Flask
    PORT: int
    threads: list[Thread] = []

    debug: bool
    update_frame_rate: int
    hr_monitor: HRMonitor

    def __init__(self, import_name, cfg: ConfigParser):
        self.hr_monitor = HRMonitor(cfg)
        self.update_frame_rate = cfg.getint("CalculationParameters", "bpmCalculationFrequency")
        self.debug = cfg.getboolean("Server", "DebugMode")
        
        self.PORT = cfg.getint("Server", "HttpPort")

        # Create server
        self.app = Flask(import_name, template_folder="static")

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/get_current_hr', 'get_current_hr', self.get_current_hr)

    def run(self):
        self.threads.append(
            Thread(target=self.start_server)
        )
        
        self.threads.append(
            Thread(target=self.update_hr)
        )

        for thread in self.threads:
            thread.start()
            print(f"Threads {thread} started")
            thread.join(0.1)

    def start_server(self):
        self.app.run(port=self.PORT, debug=self.debug)


    def index(self):
        return render_template("index.html")
    
    def get_current_hr(self):
        return jsonify({"bpm": self.hr_monitor.current_bpm}), 200

    def update_hr(self):
        i = 0
        while True:
            i += 1
            if i >= self.update_frame_rate:
                i = 0
                self.hr_monitor.update()
            