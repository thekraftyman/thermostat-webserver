# (Raspberry Pi) Thermostat Webserver
This is the repo containing the python-based webserver that will be ran on a Raspberry Pi which will act as the "hub" of my thermostat modifications. Here we will read temperature values, and communicate with an arduino that controls the thermostat via i2c.

## Setup
To set the libraries up, simply run `python3 -m pip install -r requirements.txt`.

## Running the Web Server
To run the web server, simply run `main.py` which should automatically set up everything.

## Other requirements
This repo only contains the code necessary to run the web server, and nothing more. So an automated installation and running process will have to be set up elsewhere.

## Working with the Virtual Environment
To activate the python virtual environment, simply run (from the base dir):
```
$ source env/bin/activate
(env) $
```

To deactivate the environment, simply run (from the base dir):
```
(env) $ deactivate
$
```

## Wiring
Here is the wiring diagram for the circuit. Please note that __not all parts shown are accurate__, they're just what was available on TinkerCad...

![Wiring Diagram](src/img/wiring_diagram.png)

## Further Reading
Here are resources for further development:
- https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
- https://medium.com/@camilloaddis/smart-air-conditioner-with-raspberry-pi-an-odissey-2a5b438fe984
- https://www.raspberrypi.org/forums/viewtopic.php?t=235256
- https://devkimchi.com/2020/08/12/turning-raspberry-pi-into-remote-controller/
