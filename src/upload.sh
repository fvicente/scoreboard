#!/bin/sh
#PORT=/dev/cu.usbserial-A8008VmU
PORT=/dev/ttyUSB0
avrdude -F -P $PORT -p attiny45 -c avrisp -b 19200 -U flash:w:scoreboard.hex
# fuses
#avrdude -F -P /dev/ttyUSB0 -p t45 -c avrisp -Ulfuse:w:0xce:m -Uhfuse:w:0xdf:m -Uefuse:w:0xff:m
