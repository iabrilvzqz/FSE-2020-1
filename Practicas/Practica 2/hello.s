	.text
	.global _start

_start:
	mov	r7,#4 @ Llamadas al sistema de escritura
	mov	r0,#1 @ stdout (monitor)
	ldr	r1,=message @ Indica la direccion en donde se encuentra el mensaje
	mov 	r2,#19 @Longitud de la cadena
	svc	#0
	mov	r7,#1 @ Llamadas al sistema exit
	mov	r0,#0 @ stdin (teclado)
	svc	#0 @Retorno
       .data

message:
       .ascii "FSE2020-1 is cool\n"
