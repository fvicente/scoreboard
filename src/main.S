;********************************************************************
;* Scoreboard
;*
;* Copyright 2011 AlferSoft
;*
;* www.alfersoft.com.ar
;*
;* Generate a VGA signal using an ATtiny45
;*
;* Version       : 1.0
;* Date          :
;* Author        :
;* Target MCU    : attiny45@20MHz
;********************************************************************

; To run at 20MHz we need an external oscillator, that will take PB2 and PB3.
; We still have 4 pins available, PB0 and PB1 will be used for the VGA HSYNC and
; VSYNC respectively, PB2 to generate the RGB (only black and white!).
; PB5 to get the input information that we want to display this comes from the TXD_UART pin of
; a bluetooth module configured at 2400,N,0

;
;                      ATtiny45
;                  +-----------------+
;                  |                 |
;           IN ----| 1 (PB5) (VCC) 8 |---- +5V
;    22pf          |                 |
;  +--||----+------| 2 (PB3) (PB2) 7 |---- RGB
;  |       [ ] XTAL|                 |
;  +--||----+------| 3 (PB4) (PB1) 6 |---- VSYNC
;  | 22pf          |                 |
;  +---------------| 4 (GND) (PB0) 5 |---- HSYNC
;  |               |                 |
; GND              +-----------------+
;

#define __SFR_OFFSET 0 /* needed to subtract 0x20 from I/O addresses */

#define HSYNC		0
#define VSYNC		1
#define RGB			2
#define INPUT		5
#define PORT		_SFR_IO_ADDR(PORTB)

#include <avr/io.h>

	.global maplines
	.global jmptable
	.global numtable
	.global main

; MACROS

.macro delay3x val
	ldi r16, \val
1:
	dec r16
	brne 1b
.endm


; Extract from http://www.linusakesson.net/scene/craft/

; Just like your average 80's home computer, the entire design is centered around the timing of the
; video signal.

; A typical VGA-based, low-resolution CRT monitor will redraw the screen 60 times per second using
; an electron beam, which is sweeping across the screen one line at a time. TFT monitors work
; differently, but the VGA signal is still based on the idea of an electron beam. Timing is crucial:
; One display line takes 24 μs, and is followed by a 7.75 μs break called the horizontal blanking
; period. After 480 such lines, there's a longer break (1428.75 μs, equal to 45 full display lines)
; before it all starts over. Two digital signals are used to synchronize the sender (graphics card,
; custom demo hardware etc.) and the receiver (monitor). They are called the horizontal sync and the
; vertical sync signals. It's OK to deviate a bit from the standard timing values as long as you keep
; the sync signals steady.

; The microcontroller is clocked at 20 MHz. If we convert the figures above into clock cycles, we
; get 480 cycles of visible pixels, 155 cycles of horizontal blanking and 45 full display lines worth
; of vertical blanking — but during those lines you need to keep generating the horizontal sync
; pulses. Due to rouding errors, we get a frame rate of 59.99 Hz, but that is well within the
; tolerance range of a computer monitor.


; More accurate timing from http://en.wikipedia.org/wiki/Video_Graphics_Array
;
; The horizontal timings are:
; +--------------------------+----------+------+
; | Parameter                | Value    | Unit |
; +--------------------------+----------+------+
; | Pixel clock frequency    | 25.175   | MHz  |
; | Horizontal frequency     | 31.4686  | kHz  |
; | Horizontal pixels        | 640      |      |
; | Horizontal sync polarity | Negative |      |
; | Total time for each line | 31.77    | µs   |
; | Front porch (A)          | 0.94     | µs   |
; | Sync pulse length (B)    | 3.77     | µs   |
; | Back porch (C)           | 1.89     | µs   |
; | Active video (D)         | 25.17    | µs   |
; +--------------------------+----------+------+

; (Total horizontal sync time 6.60 µs)
; |__|______|___|_____________________________________________________________________|
;  A    B     C                                   D
;

; The vertical timings are:
; +--------------------------+----------+------+
; | Parameter                | Value    | Unit |
; +--------------------------+----------+------+
; | Vertical lines           | 480      |      |
; | Vertical sync polarity   | Negative |      |
; | Vertical frequency       | 59.94    | Hz   |
; | Front porch (E)          | 0.35     | ms   |
; | Sync pulse length (F)    | 0.06     | ms   |
; | Back porch (G)           | 1.02     | ms   |
; | Active video (H)         | 15.25    | ms   |
; +--------------------------+----------+------+

; More VGA timing info:
; http://courses.engr.illinois.edu/ece412/MP_files/mp3/vga_timing.pdf

; About UART
; Running at 2400 bauds, one bit with last for 416.66μs
; Our loop will read the input every 635 cycles to keep the VGA horizontal frequency, this means
; every 31.75μs at 20Mhz, so 416.66 / 31.75 = 13.12, meaning each bit will be read about 13 times.
; We will take the read #7 as the valid one. We wont do any kind of checks.

; From the UART we expect to receive one byte, every byte is a command
; Valid commands:
; 0 0 0 1 D D D D		(character 1) [0-F] -> 0 1 2 3 4 5 6 7 8 9 (SPACE) B O G
; 0 0 1 0 D D D D		(character 2)
; 0 0 1 1 D D D D		(character 3)
; 0 1 0 0 D D D D		(character 4)
; 0 1 0 1 0 0 0 1		(serve A top)
; 0 1 0 1 0 0 1 0		(serve B bottom)
; 0 1 0 1 0 1 0 0		(serve A top)
; 0 1 0 1 1 0 0 0		(serve b bottom)

; More UART info at http://en.wikipedia.org/wiki/Universal_asynchronous_receiver/transmitter

;
; NOTES:
;
; - At 20Mhz, 1 cycle = 0.05μs
; - Total of vertical lines: 525 (480 lines + 45 lines of vertical blanking)
; - VSYNC timing in lines:
;   -> Front porch = 10 lines (8 lines of bottom border + 2 lines of front porch)
;   -> Sync pulse length = 2 lines
;   -> Back porch = 33 lines (25 lines of back porch + 8 lines of top border)
; - Does not works with .org 0x00
;

main:
	; Initialize stack

	ldi r16, hi8(RAMEND)
	out _SFR_IO_ADDR(SPH), r16
	ldi r16, lo8(RAMEND)
	out _SFR_IO_ADDR(SPL), r16

	; Disable interruptions

	cli

	; Initialize ports

	sbi _SFR_IO_ADDR(DDRB), 0x00	; output
	sbi _SFR_IO_ADDR(DDRB), 0x01	; output
	sbi _SFR_IO_ADDR(DDRB), 0x02	; output
	cbi _SFR_IO_ADDR(DDRB), INPUT	; make input

	; Initialize registers

	ldi r16, 0x00		; aux
	ldi r17, 0x00		; mapped line (between 0 and 11)
	ldi r18, 0x00		; aux to read input
	ldi r19, 0x00		; byte read from UART
	ldi r20, 0x00		; line counter - 0x00 = first half of the 480 visible lines
						;                0x01 = second half of the 480 visible lines
						;                0x02 = 45 non-visible lines
						;
	ldi r21, 0xFF		; line counter - from 0x00 to 0xF0 if r20 in (0x00, 0x01)
						;                from 0x00 to 0x2D if r20 == 0x02
						;
	ldi r22, 0x00		; ZERO
	ldi r23, 0x00		; character line data 1
	ldi r24, 0x00		; character line data 4
	ldi r25, 0x00		; UART input counter -	bit 0 to 3 = read counter (resets at 14)
						;						bit 4 to 7 = bits counter (resets when == 0x91)
						; 0x00000000 means waiting for start bit (low)
						;
	ldi r26, 0x00		; current player
	ldi r27, 0x00		; current line Y

	mov r1, r22			; number to display from 0 to 9 - 10 = space
	mov r2, r22			; number to display from 0 to 9 - 10 = space
	mov r3, r22			; number to display from 0 to 9 - 10 = space
	mov r4, r22			; number to display from 0 to 9 - 10 = space

	mov r6, r22			; character line data 2
	mov r7, r22			; character line data 3

loop:
	;
	; Horizontal blanking total: 6.60 µs * 20 = 132 cycles
	;

	; Front porch 0.94 µs = 18.8 cycles

	; check line counters

	; first check vertical blanking zone
	cpi r20, 0x02
	breq vzone

	; increment counter
	inc r21
	; determine current line
	ldi ZL, lo8(maplines)
	ldi ZH, hi8(maplines)
	add ZL, r21
	adc ZH, r22
	lpm				; lpm = 3 cycles
	mov r27, r0
	; increment r20 if necessary
	cpi r21, 0xF0
	brne checkline
	; we're starting the lower half part of the screen
	inc r20
	ldi r21, 0x00
	sbrc r20, 1
	ldi r27, 0x60
	rjmp hsyncstart

vzone:
	inc r21
	cpi r21, 0x2D
	breq cntreset

	cpi r21, 0x09
	breq vpulseon		; line 10 of the blanking zone

	cpi r21, 0x0B
	brne fp8togo
	breq vpulseoff		; line 12 of the blanking zone

vpulseon:
	sbi PORT, VSYNC		; sbi = 2 clocks
	nop
	nop
	nop
	nop
	nop
	nop
	rjmp hsyncstart

vpulseoff:
	cbi PORT, VSYNC		; turn VSYNC pulse off; cbi = 2 clocks
	nop
	nop
	nop
	rjmp hsyncstart

cntreset:
	ldi r20, 0x00
	ldi r21, 0x00
	rjmp fp8togo

fp8togo:
	nop
	nop

fp6togo:
	nop
	nop
	nop
	nop
	rjmp hsyncstart

checkline:
	; check if we're on the lower half of the screen
	cpi r20, 0x01
	breq addandgo
	nop
	rjmp hsyncstart

addandgo:
	; add offset to r27 - only 2 cycles left
	ldi r16, 0x30
	add r27, r16
	; fall thru

hsyncstart:
	; Sync pulse length 3.77 µs = 75.4 cycles
	; HSYNC pulse on
	sbi PORT, HSYNC		; sbi = 2 clocks

	mov r16, r27		; current line (between 0 and 96)
	; divide by 8 to get the mapped line number (between 0 and 11)
	lsr r16
	lsr r16
	lsr r16
	mov r17, r16
	; skip first line and ensure to ignore lines below 8
	dec r16
	cpi r16, 9
	brlo getchars
	ldi r16, 0			; first line is always empty

getchars:
	; get 1st character
	ldi ZL, lo8(numtable)
	ldi ZH, hi8(numtable)
	add ZL, r1
	adc ZH, r22
	add ZL, r16
	adc ZH, r22
	lpm
	mov r23, r0

	; get 2nd character
	ldi ZL, lo8(numtable)
	ldi ZH, hi8(numtable)
	add ZL, r2
	adc ZH, r22
	add ZL, r16
	adc ZH, r22
	lpm
	mov r6, r0

	; get 3rd character
	ldi ZL, lo8(numtable)
	ldi ZH, hi8(numtable)
	add ZL, r3
	adc ZH, r22
	add ZL, r16
	adc ZH, r22
	lpm
	mov r7, r0

	; get 4th character
	ldi ZL, lo8(numtable)
	ldi ZH, hi8(numtable)
	add ZL, r4
	adc ZH, r22
	add ZL, r16
	adc ZH, r22
	lpm
	mov r24, r0

	; 51 cycles

	;
	; UART read input
	;
	in r18, _SFR_IO_ADDR(PINB)		; 1 clock

	cpi r25, 0
	breq waitlow
	inc r25
	mov r16, r25
	andi r16, 0x0F
	cpi r16, 7
	brne chkfornext5togo
	lsr r19
	sbrc r18, INPUT
	ori r19, 0x80
	nop
	rjmp chkfornext
chkfornext5togo:
	nop
	nop
	nop
	nop
	nop
chkfornext:
	; 65 cycles
	cpi r16, 14
	brne chkend3togo
	subi r25, 0xEF	; add 17
	andi r25, 0xF1
	rjmp chkend
chkend3togo:
	nop
	nop
	nop
chkend:
	; 71 cycles
	nop
	rjmp hsyncoff

waitlow:
	; waiting for low
	sbrs r18, INPUT
	inc r25
	nop
	delay3x 4
	nop
	nop
	rjmp hsyncoff

hsyncoff:
	; 74 cycles

	; HSYNC pulse off
	cbi PORT, HSYNC		; cbi = 2 clocks

	; Back porch 1.89 µs = 37.8 cycles
	; We use the back to process the read byte from UART

	cpi r25, 0x91
	brne endbackporch25togo		; nothing read
procbyte:
	; byte just read, process it
	mov r16, r19
	swap r16
	andi r16, 0x0F
	andi r19, 0x0F
	; multiply by 8
	lsl r19
	lsl r19
	lsl r19
	;
	cpi r16, 0x01	; set charater 1
	brne chkchar2
	mov r1, r19
chkchar2:
	cpi r16, 0x02	; set charater 2
	brne chkchar3
	mov r2, r19
chkchar3:
	cpi r16, 0x03	; set charater 3
	brne chkchar4
	mov r3, r19
chkchar4:
	cpi r16, 0x04	; set charater 4
	brne cmdplayer
	mov r4, r19
cmdplayer:
	cpi r16, 0x05	; set current player
	brne endprocbyte
	mov r26, r19
endprocbyte:
	ldi r19, 0x00
	ldi r25, 0x00
	rjmp endbackporch

endbackporch25togo:
	delay3x 8
	nop

endbackporch:
	; 28 cycles of back porch
	; RGB off
	cbi PORT, RGB		; cbi = 2 clocks

	cpi r17, 1
	brne chkpl3
	sbrc r26, 3
	ori r23, 0x80		; player 1 selected
	sbrc r26, 4
	ori r24, 0x02		; player 2 selected
	nop
	rjmp line

line3togo:
	nop
	rjmp line

chkpl3:
	cpi r17, 9
	brne line3togo
	sbrc r26, 5
	ori r23, 0x80		; player 3 selected
	nop
	nop

line:
	;
	; Draw a line of pixels total: 25.17 µs * 20 = 503.4 cycles
	;

	; draw 1st 1/4 line
	ldi r16, 0x08
line14:
	rol r23
	brcc rgboff14
	nop
	; RGB on
	sbi PORT, RGB		; sbi = 2 clocks
	rjmp cont14
rgboff14:
	; RGB off
	cbi PORT, RGB		; cbi = 2 clocks
	nop
	nop
cont14:
	dec r16
	nop
	nop
	nop
	nop
	nop
	brne line14

	; draw 1st 2/4 line
	ldi r16, 0x08
line24:
	rol r6
	brcc rgboff24
	nop
	; RGB on
	sbi PORT, RGB		; sbi = 2 clocks
	rjmp cont24
rgboff24:
	; RGB off
	cbi PORT, RGB		; cbi = 2 clocks
	nop
	nop
cont24:
	dec r16
	nop
	nop
	nop
	nop
	nop
	brne line24

	; middle separation (checking player 4)
	cpi r17, 9
	brne drawsep
	nop
	nop
	nop
	sbi PORT, RGB		; RGB on
	sbrc r26, 6
	ori r24, 0x02		; player 4 selected
	nop
	cbi PORT, RGB		; RGB off
	nop
	nop
	nop
	rjmp contline

drawsep:
	; middle separation (no player checking)
	nop
	nop
	sbi PORT, RGB		; RGB on
	nop
	nop
	nop
	cbi PORT, RGB		; RGB off
	nop
	nop
	nop
	rjmp contline

contline:
	; draw 1st 3/4 line
	ldi r16, 0x08
line34:
	rol r7
	brcc rgboff34
	nop
	; RGB on
	sbi PORT, RGB		; sbi = 2 clocks
	rjmp cont34
rgboff34:
	; RGB off
	cbi PORT, RGB		; cbi = 2 clocks
	nop
	nop
cont34:
	dec r16
	nop
	nop
	nop
	nop
	nop
	brne line34

	; draw 1st 4/4 line
	ldi r16, 0x08
line44:
	rol r24
	brcc rgboff44
	nop
	; RGB on
	sbi PORT, RGB		; sbi = 2 clocks
	rjmp cont44
rgboff44:
	; RGB off
	cbi PORT, RGB		; cbi = 2 clocks
	nop
	nop
cont44:
	dec r16
	nop
	nop
	nop
	nop
	nop
	brne line44

	; ending line
	nop
	nop
	rjmp loop
