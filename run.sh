#!/bin/bash

cd /home/pi/thermostat-webserver/ && sudo python3 main.py > /tmp/webserver_error.log 2>&1
