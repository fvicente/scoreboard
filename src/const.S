
; tables

	.global maplines
	.global numtable
	.global jmptable

maplines:
    ; map current line number (0-240) to (0-48)
	.byte 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01
	.byte 0x02, 0x02, 0x02, 0x02, 0x02, 0x03, 0x03, 0x03, 0x03, 0x03
	.byte 0x04, 0x04, 0x04, 0x04, 0x04, 0x05, 0x05, 0x05, 0x05, 0x05
	.byte 0x06, 0x06, 0x06, 0x06, 0x06, 0x07, 0x07, 0x07, 0x07, 0x07
	.byte 0x08, 0x08, 0x08, 0x08, 0x08, 0x09, 0x09, 0x09, 0x09, 0x09
	.byte 0x0a, 0x0a, 0x0a, 0x0a, 0x0a, 0x0b, 0x0b, 0x0b, 0x0b, 0x0b
	.byte 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0d, 0x0d, 0x0d, 0x0d, 0x0d
	.byte 0x0e, 0x0e, 0x0e, 0x0e, 0x0e, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f
	.byte 0x10, 0x10, 0x10, 0x10, 0x10, 0x11, 0x11, 0x11, 0x11, 0x11
	.byte 0x12, 0x12, 0x12, 0x12, 0x12, 0x13, 0x13, 0x13, 0x13, 0x13
	.byte 0x14, 0x14, 0x14, 0x14, 0x14, 0x15, 0x15, 0x15, 0x15, 0x15
	.byte 0x16, 0x16, 0x16, 0x16, 0x16, 0x17, 0x17, 0x17, 0x17, 0x17
	.byte 0x18, 0x18, 0x18, 0x18, 0x18, 0x19, 0x19, 0x19, 0x19, 0x19
	.byte 0x1a, 0x1a, 0x1a, 0x1a, 0x1a, 0x1b, 0x1b, 0x1b, 0x1b, 0x1b
	.byte 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1d, 0x1d, 0x1d, 0x1d, 0x1d
	.byte 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f
	.byte 0x20, 0x20, 0x20, 0x20, 0x20, 0x21, 0x21, 0x21, 0x21, 0x21
	.byte 0x22, 0x22, 0x22, 0x22, 0x22, 0x23, 0x23, 0x23, 0x23, 0x23
	.byte 0x24, 0x24, 0x24, 0x24, 0x24, 0x25, 0x25, 0x25, 0x25, 0x25
	.byte 0x26, 0x26, 0x26, 0x26, 0x26, 0x27, 0x27, 0x27, 0x27, 0x27
	.byte 0x28, 0x28, 0x28, 0x28, 0x28, 0x29, 0x29, 0x29, 0x29, 0x29
	.byte 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2b, 0x2b, 0x2b, 0x2b, 0x2b
	.byte 0x2c, 0x2c, 0x2c, 0x2c, 0x2c, 0x2d, 0x2d, 0x2d, 0x2d, 0x2d
	.byte 0x2e, 0x2e, 0x2e, 0x2e, 0x2e, 0x2f, 0x2f, 0x2f, 0x2f, 0x2f
	.byte 0x30, 0x30, 0x30, 0x30, 0x30, 0xff, 0xff, 0xff, 0xff, 0xff

numtable:
	.byte 0b00000000
	.byte 0b00111000
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b00111000

	.byte 0b00000000
	.byte 0b00010000
	.byte 0b00110000
	.byte 0b00010000
	.byte 0b00010000
	.byte 0b00010000
	.byte 0b00010000
	.byte 0b00111000

	.byte 0b00000000
	.byte 0b00111000
	.byte 0b01000100
	.byte 0b00000100
	.byte 0b00001000
	.byte 0b00010000
	.byte 0b00100000
	.byte 0b01111100

	.byte 0b00000000
	.byte 0b01111100
	.byte 0b00001000
	.byte 0b00010000
	.byte 0b00001000
	.byte 0b00000100
	.byte 0b01000100
	.byte 0b00111000

	.byte 0b00000000
	.byte 0b00001000
	.byte 0b00011000
	.byte 0b00101000
	.byte 0b01001000
	.byte 0b01111100
	.byte 0b00001000
	.byte 0b00001000

	.byte 0b00000000
	.byte 0b01111100
	.byte 0b01000000
	.byte 0b01111000
	.byte 0b00000100
	.byte 0b00000100
	.byte 0b01000100
	.byte 0b00111000

	.byte 0b00000000
	.byte 0b00011000
	.byte 0b00100000
	.byte 0b01000000
	.byte 0b01111000
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b00111000

	.byte 0b00000000
	.byte 0b01111100
	.byte 0b00000100
	.byte 0b00001000
	.byte 0b00010000
	.byte 0b00100000
	.byte 0b00100000
	.byte 0b00100000

	.byte 0b00000000
	.byte 0b00111000
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b00111000
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b00111000

	.byte 0b00000000
	.byte 0b00111000
	.byte 0b01000100
	.byte 0b01000100
	.byte 0b00111100
	.byte 0b00000100
	.byte 0b00001000
	.byte 0b00110000

	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000

	.byte 0b00000000
	.byte 0b01111100
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b01111100
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b01111100

	.byte 0b00000000
	.byte 0b00111100
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b00111100

	.byte 0b00000000
	.byte 0b00111110
	.byte 0b01000000
	.byte 0b01000000
	.byte 0b01011100
	.byte 0b01000010
	.byte 0b01000010
	.byte 0b00111110

	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
	.byte 0b00000000
