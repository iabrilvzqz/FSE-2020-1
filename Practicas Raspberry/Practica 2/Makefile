LD = ld 
AS = as 
ASFLAGS_THUMB = -mthumb-interwork
LDFLAGS_THUMB = --thumb-entry=_start

CC = gcc
CFLAGS = -O2 -Wall
LFLAGS =


all:	exit_asm hello compare submit clean  

exit_asm:	exit_asm.o
	$(LD) $(LDFLAGS) -o exit_asm exit_asm.o

exit_asm.o:	exit_asm.s
	$(AS) $(ASFLAGS) -o exit_asm.o exit_asm.s

hello:	hello.o
	$(LD) $(LDFLAGS) -o hello hello.o

hello.o: hello.s
	$(AS) $(ASFLAGS) -o hello.o hello.s

compare:	compare.o
	$(LD) $(LDFLAGS) -o compare compare.o

compare.o: compare.s
	$(AS) $(ASFLAGS) -o compare.o compare.s

submit:	compare.s Makefile README
	tar -czvf P3_FSEsubmit.tar.gz exit_asm.s hello.s compare.s Makefile README

clean:	
	rm -f *~ *.o compare exit_asm hello
