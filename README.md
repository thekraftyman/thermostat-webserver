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

## Further Reading
Here are resources for further development:
- https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
