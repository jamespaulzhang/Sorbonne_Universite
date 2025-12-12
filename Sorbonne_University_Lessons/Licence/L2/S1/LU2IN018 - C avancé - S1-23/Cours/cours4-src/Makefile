
GCC_FLAGS = -Wall -g

all: main_arbre main_arbre1

main_arbre: main_arbre.o arbre.o liste.o pile.o file.o
	gcc $(GCC_FLAGS) -o main_arbre main_arbre.o arbre.o liste.o pile.o file.o

main_arbre.o: main_arbre.c
	gcc $(GCC_FLAGS) -c main_arbre.c

main_arbre1: main_arbre1.o arbre.o 
	gcc $(GCC_FLAGS) -o main_arbre1 main_arbre1.o arbre.o liste.o pile.o file.o

main_arbre1.o: main_arbre1.c
	gcc $(GCC_FLAGS) -c main_arbre1.c

arbre.o: arbre.c
	gcc $(GCC_FLAGS) -c arbre.c

liste.o: liste.c
	gcc $(GCC_FLAGS) -c liste.c

file.o: file.c
	gcc $(GCC_FLAGS) -c file.c

pile.o: pile.c
	gcc $(GCC_FLAGS) -c pile.c

clean:
	rm -f *.o *~ main_arbre main_arbre1