CC = gcc
CFLAGS = -Wall

all: maintab

maintab: maintab.o tab.o
	$(CC) $(CFLAGS) -o maintab maintab.o tab.o

maintab.o: maintab.c tab.h
	$(CC) $(CFLAGS) -c maintab.c

tab.o: tab.c tab.h
	$(CC) $(CFLAGS) -c tab.c

clean:
	rm -f *.o maintab
