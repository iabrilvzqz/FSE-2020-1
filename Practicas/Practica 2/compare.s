	.text
	.global _start

_start:
	mov	r1,#1
	mov	r2,#1
	cmp	r1, r2 @ Hace la compración entre r1 y r2
	beq 	iguales @ Si Z = 1, se dirige a la etiqueta iguales
	cmp	r1, r2
	bgt	r1mayor @ Salta si r1 es mayor

r2mayor:
        mov     r7,#4
        mov     r0,#1
        ldr     r1,=message3
        mov     r2,#14
        svc     #0
        mov     r7,#1
        mov     r0,#0
        svc     #0
       .data
iguales:
	mov	r7,#4
	mov	r0,#1
	ldr	r1,=message1
	mov 	r2,#14
	svc	#0
	mov	r7,#1
	mov	r0,#0
	svc	#0
       .data

r1mayor:
        mov     r7,#4
        mov     r0,#1
        ldr     r1,=message2
        mov     r2,#14
        svc     #0
        mov     r7,#1
        mov     r0,#0
        svc     #0
       .data

message1:
       .ascii "Son iguales\n"

message2:
	.ascii "R1 es mayor\n"

message3:
        .ascii "R2 es mayor\n"


