from configparser import ConfigParser
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import os

## These two classes are from https://stackoverflow.com/questions/73089846/python-3-simple-http-server-with-get-functional

class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""

    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath

class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""

    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)



class SimpleHttpServer:
    PORT: int
    httpd: HTTPServer

    def __init__(self, cfg: ConfigParser):
        self.PORT = cfg.getint("Server", "HttpPort")

        self.httpd = HTTPServer(cfg.get("Server", "WebPagePath"), ("", self.PORT))

    def start_server(self):
        print(f"\Http server started at port: {self.PORT}")

        self.httpd.serve_forever()