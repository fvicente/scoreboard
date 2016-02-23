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
; TODO: Using an external clock (a crystal that generates TTL) we can save PB2!
; We still have 4 pins available, PB0 and PB1 will be used for the VGA HSYNC and
; VSYNC respectively, PB2 to generate the RGB (only black and white!).
; PB5 to get the input information that we want to display, hopefully this will
; come from a bluetooth module specially tuned for this, or from another ATtiny
; in the worst case.

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

	.global maplines1
	.global maplines2
	.global jmptable
	.global number0
	.global number1
	.global number2
	.global number3
	.global number4
	.global number5
	.global number6
	.global number7
	.global number8
	.global number9
	.global space
	.global zerobyte
	.global main

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

	sbi DDRB, 0x00	; output
	sbi DDRB, 0x01	; output
	sbi DDRB, 0x02	; output

	; Initialize used registers

	ldi r16, 0x00		; aux
	ldi r17, 0x00		; aux
	ldi r18, 0x00		; temporary for delays
	ldi r19, 0x00		; blank line indicator

	ldi r20, 0xFF		; line counter
	ldi r21, 0x02		; line counter * 256

	ldi r22, 0x00		; ZERO

	ldi r23, 0x00		;

	ldi r24, 0x00		; return address aux 1
	ldi r25, 0x00		; return address aux 2

	mov r1, r22			; number to display from 0 to 9 - 10 = space
	mov r2, r22			; number to display from 0 to 9 - 10 = space
	mov r3, r22			; number to display from 0 to 9 - 10 = space
	mov r4, r22			; number to display from 0 to 9 - 10 = space

	mov r5, r22			; character line data
	mov r6, r22			; character line data
	mov r7, r22			; character line data
	mov r8, r22			; character line data

	; TODO: following lines are to add some default values for tests
	ldi r16, 0x06
	mov r1, r16
	ldi r16, 0x0c
	mov r2, r16
	ldi r16, 0x12
	mov r3, r16
	ldi r16, 0x18
	mov r4, r16
	ldi r16, 0x00

loop:
	;
	; Horizontal blanking total: 6.60 µs * 20 = 132 cycles
	;

	; Front porch 0.94 µs = 18.8 cycles
	; Use the front porch cycles to determine r17
	; r17 is the character line number (between 1 and 10) mapped on the maplines

	; check counters
	; if r21 == 2 we may be inside the drawing zone
	; if r21 == 1 we may be inside the drawing / vertical blanking zone
	; if r21 == 0 we may need to reset the counters

	cpi r21, 0x02		; cpi = 1 clock
	breq chkline		; brne = 1 clock if cond == false else 2

	cpi r21, 0x01		; cpi = 1 clock
	brne resetorgo		; if true, this means that r21 == 0

	; we use the line counters to determine when to turn the VSYNC pulse on and off
	; if line == 491 turn VSYNC pulse on

	cpi r20, 0x15		; cpi = 1 clock
	breq vpulseon		; exactly 491 lines; breq = 1 clock if cond == false else 2

	cpi r20, 0x13		; cpi = 1 clock
	breq vpulseoff		; exactly 493 lines; brne = 1 clock if cond == false else 2

	mov r16, r20		; mov = 1 clock
	cpi r16, 0x51		; sub = 1 clock
	brlo fp7togo		; brlo = 1 clock if cond == false else 2

	com r16
	ldi ZL, lo8(maplines2)
	ldi ZH, hi8(maplines2)
	add ZL, r16			; add = 1 clock
	adc ZH, r22
	nop
	rjmp hsyncstart

vpulseon:
	sbi PORT, VSYNC		; sbi = 2 clocks
	rjmp fp8togo

vpulseoff:
	cbi PORT, VSYNC		; turn VSYNC pulse off; cbi = 2 clocks
	rjmp fp6togo

chkline:
	cpi r20, 0xCC		; cpi = 1 clock
	brsh fp13togo		; brsh = 1 clock if cond == false else 2

	mov r16, r20
	subi r16, 0xCC
	com r16
	ldi ZL, lo8(maplines1)
	ldi ZH, hi8(maplines1)
	add ZL, r16
	adc ZH, r22
	nop
	nop
	nop
	nop
	nop
	rjmp hsyncstart

resetorgo:
	; we have 14 cycles to check and reset or continue
	; if line == 526
	cpi r20, 0xF1		; cpi = 1 clock
	brne fp11togo		; not 526 lines; brne = 1 clock if cond == false else 2
	; reset to line counter to 0
	ldi r20, 0xFF		; line counter; ldi = 1 clock
	ldi r21, 0x02		; line counter * 256; ldi = 1 clock
	rjmp fp8togo

fp13togo:
	nop
	nop

fp11togo:
	nop
	nop
	nop

fp8togo:
	nop

fp7togo:
	nop

fp6togo:
	nop
	nop
	; to enforce the lpm return 0
	ldi ZL, lo8(zerobyte)
	ldi ZH, hi8(zerobyte)
	rjmp hsyncstart

hsyncstart:
	; Sync pulse length 3.77 µs = 75.4 cycles
	; HSYNC pulse on
	sbi PORT, HSYNC		; sbi = 2 clocks

	lpm
	mov r17, r0
	; r17 has the character line (from 1 to 10)
	; We have 71 cycles to set R5, R6, R7 and R8
	; Each of this registers represents 1/4 of the line to paint
	; according to the current characters in R1, R2, R3 and R4

getlines:
	; use r16 as parameter for our function that retrieves the line (in r0)
	mov r16, r1
	rcall getlinefornum
	mov r5, r0			; store result
	mov r16, r2
	rcall getlinefornum
	mov r6, r0			; store result
	mov r16, r3
	rcall getlinefornum
	nop
	nop
	nop
	; 74 cycles used - we will need to get the last line during the back porch

	; HSYNC pulse off
	cbi PORT, HSYNC		; cbi = 2 clocks

	; Back porch 1.89 µs = 37.8 cycles
	; We use the back porch cycles to determine if we need to draw a blank line or a number line

	mov r7, r0			; store result
	mov r16, r4
	rcall getlinefornum
	mov r8, r0			; store result
	; 15 cycles left
	; RGB off
	cbi PORT, RGB		; cbi = 2 clocks
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop

line:
	;
	; Draw a line of pixels total: 25.17 µs * 20 = 503.4 cycles
	;

	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	; draw 1st 1/4 line
	ldi r16, 0x08
line14:
	rol r5
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
	rol r8
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
	nop
	nop
	rjmp decandgo	; decandgo will use 6 cycles

decandgo:
	; decrement line counters
	dec r20				; decrement line counter; dec = 1 clock
	brne back			; if not zero, repeat loop; brne = 1 clock if cond == false else 2
	ldi r20, 0xFF		; reset line counter
	dec r21				; decrement line counter * 256
	rjmp loop

back:
	nop					; nop = 1 clock
	rjmp loop

;
; functions
;
getlinefornum:
	ldi ZL, lo8(pm(numtable))
	ldi ZH, hi8(pm(numtable))
	add ZL, r16
	adc ZH, r22
	ijmp

numtable:

linefor0:
	ldi ZL, lo8(number0)
	ldi ZH, hi8(number0)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor1:
	ldi ZL, lo8(number1)
	ldi ZH, hi8(number1)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor2:
	ldi ZL, lo8(number2)
	ldi ZH, hi8(number2)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor3:
	ldi ZL, lo8(number3)
	ldi ZH, hi8(number3)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor4:
	ldi ZL, lo8(number4)
	ldi ZH, hi8(number4)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor5:
	ldi ZL, lo8(number5)
	ldi ZH, hi8(number5)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor6:
	ldi ZL, lo8(number6)
	ldi ZH, hi8(number6)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor7:
	ldi ZL, lo8(number7)
	ldi ZH, hi8(number7)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor8:
	ldi ZL, lo8(number8)
	ldi ZH, hi8(number8)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

linefor9:
	ldi ZL, lo8(number9)
	ldi ZH, hi8(number9)
	add ZL, r17
	adc ZH, r22
	lpm
	ret

lineforspace:
	ldi ZL, lo8(space)
	ldi ZH, hi8(space)
	add ZL, r17
	adc ZH, r22
	lpm
	ret
