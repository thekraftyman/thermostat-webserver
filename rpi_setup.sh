#!/bin/bash

echo "Configuring one-wire..."
echo "dtoverlay=w1-gpio" >> /boot/config.txt
echo "Config added, a reboot is required to make the one-wire work"
