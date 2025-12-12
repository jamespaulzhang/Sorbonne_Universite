IPCPATH = /Infos/lmd/2022/licence/ue/LU3IN010-2023fev/libipc/libipc/lib
CFLAGS = -Wall -I$(IPCPATH)

all: demo-ipc 

demo-ipc: demo-ipc.o
	gcc -o demo-ipc demo-ipc.o -L$(IPCPATH) -lIPC

demo-ipc.o: demo-ipc.c
	gcc -c  $(CFLAGS) demo-ipc.c
clean:
	rm -f demo-ipc demo-ipc.o
