from flask import Flask

class Webserver:

    def __init__(self, port=80, host='0.0.0.0', debug=False):
        self.app = Flask(__name__)
        self.port = port
        self.host = host
        self.debug = debug

    def run(self):
        self.add_routes()
        self.app.run(debug=self.debug, port=self.port, host=self.host)

    def add_routes(self):
        @self.app.route('/')
        def index():
            return "<h1>Hello, world!</h1>"
