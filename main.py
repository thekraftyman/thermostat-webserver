from core.webserver import *

if __name__ == '__main__':
    ws = Webserver(port=5000, debug=True)
    ws.run()
