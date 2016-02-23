#!/bin/sh
avr-gcc  -mmcu=attiny45 -mmcu=attiny45 -Wall -gdwarf-2 -Os -std=gnu99 -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums -MD -MP -MT main.o -MF main.o.d  -x assembler-with-cpp -Wa,-gdwarf2 -c main.S const.S
avr-gcc -mmcu=attiny45 -Wl,-Map=scoreboard.map main.o const.o     -o scoreboard.elf
avr-objcopy -O ihex -R .eeprom -R .fuse -R .lock -R .signature  scoreboard.elf scoreboard.hex
avr-objcopy -j .eeprom --set-section-flags=.eeprom="alloc,load" --change-section-lma .eeprom=0 --no-change-warnings -O ihex scoreboard.elf scoreboard.eep || exit 0
avr-objdump -h -S scoreboard.elf > scoreboard.lss
rm *.o
rm *.o.d
rm scoreboard.eep
rm scoreboard.elf
rm scoreboard.lss
rm scoreboard.map
