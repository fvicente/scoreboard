#!/bin/sh
#PORT=/dev/cu.usbserial-A8008VmU
PORT=/dev/ttyUSB0
avrdude -F -P $PORT -p attiny45 -c avrisp -b 19200 -U flash:w:scoreboard.hex
# fuses
#avrdude -F -P /dev/ttyUSB0 -p t45 -c avrisp -Ulfuse:w:0xce:m -Uhfuse:w:0xdf:m -Uefuse:w:0xff:m
# WARNING: next line will set the fuses with PB5 as I/O port (won't be able to program again unless you reset the fuses with HV programmer)
#avrdude -F -P $PORT -p attiny45 -c avrisp -b 19200 -U flash:w:scoreboard.hex -Ulfuse:w:0xce:m -Uhfuse:w:0x5f:m -Uefuse:w:0xff:m
