; bitbang.s: export uint8_t* output_frame(uint8_t*) writing on HUB75 bus
; Copyright (C) 2018  Andrea Simonetto <self@andrea.simonetto.name>

; This program is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.

; This program is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.

; You should have received a copy of the GNU General Public License
; along with this program.  If not, see <https://www.gnu.org/licenses/>.

.macro out_row winc1, winc2
    .rept 64
	mov #0x0200, w1

	; R1
	mov.b \winc1, w2
	and.b w2, w4, w3
	cpslt.b w3, w7
	ior.b #0x01, w1

	; G1
	lsr w2, #2, w2
	and.b w2, w4, w3
	cpslt.b w3, w7
	ior.b #0x04, w1

	; B1
	lsr w2, #2, w2
	and.b w2, w4, w3
	cpslt.b w3, w7
	ior.b #0x10, w1

	; R2
	mov.b \winc2, w2
	and.b w2, w4, w3
	cpslt.b w3, w7
	ior.b #0x02, w1

	; G2
	lsr w2, #2, w2
	and.b w2, w4, w3
	cpslt.b w3, w7
	ior.b #0x08, w1

	; B2
	lsr w2, #2, w2
	and.b w2, w4, w3
	cpslt.b w3, w7
	ior.b #0x20, w1

	mov w1, _PORTB
	ior.b w1, w6, w1
	mov w1, _PORTB
	and.b w1, w5, w1
	mov w1, _PORTB
    .endr

    ; LAT = 1
    mov #0x0300, w1
    mov w1, _PORTB

    ; LAT = 0
    mov #0x0200, w1
    mov w1, _PORTB
.endm

.section .text,code
.align 2
.global _output_frame ; export
.type _output_frame, @function

_output_frame:
.set ___PA___, 1
    push  w1
    push  w2
    push  w3
    push  w4
    push  w5
    push  w6
    push  w7
    push  w8
    push  w9
    push  w10

    mov   #0x00, w3
    mov   #0x03, w4
    mov   #0x3f, w5
    mov   #0x40, w6
    mov   #0x01, w7
    disi  #0x3FFF
    output_frame_layer_loop:
	mov #0x00, w10
	output_frame_loop:
	    mov w10, _PORTA

	    mov #16, w8
	    sub w8, w10, w8
	    sl w8, #6, w8
	    add w8, w0, w8
	    mov #1024, w9
	    add w9, w8, w9

	    out_row [--w9], [--w8]

	    sl w10, #6, w8
	    mov #2048, w9
	    add w8, w9, w8
	    add w8, w0, w8
	    mov #1024, w9
	    add w9, w8, w9

	    out_row [w8++], [w9++]

	    ; OE = 0
	    mov #0x0000, w1
	    mov w1, _PORTB

	    ; Delay
	    mov #8, w1
	    sl w1, w7, w1
	    output_frame_delay_loop:
		dec w1, w1
		bra nz, output_frame_delay_loop

	    ; OE = 1
	    mov #0x0200, w1
	    mov w1, _PORTB

	    inc w10, w10
	    cp w10, #16
	    bra lt, output_frame_loop

	inc w7, w7
	cp w7, #4
	bra lt, output_frame_layer_loop

    disi  #0

    pop   w10
    pop   w9
    pop   w8
    pop   w7
    pop   w6
    pop   w5
    pop   w4
    pop   w3
    pop   w2
    pop   w1
    return
