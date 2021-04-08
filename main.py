from core.webserver import *
from waitress import serve

if __name__ == '__main__':
    ws = Webserver(port=5000, debug=False)
    serve(ws.app, host="0.0.0.0", port=5000)
