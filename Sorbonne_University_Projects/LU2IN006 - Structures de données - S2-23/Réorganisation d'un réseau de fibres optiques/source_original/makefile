# Compilateur
CC = gcc

# Options de compilation
CFLAGS = -Wall -Wextra -std=c99

# Fichiers source
SRCS = ChaineMain.c Chaine.c Reseau.c SVGwriter.c ReconstitueReseau.c

# Fichiers objets correspondants
OBJS = $(SRCS:.c=.o)

# Nom de l'exécutable
EXEC = ChaineMain ReconstitueReseau

# Règle par défaut pour l'exécutable
all: $(EXEC)

# Règle de compilation pour l'exécutable
ReconstitueReseau: ReconstitueReseau.o Reseau.o Chaine.o SVGwriter.o
	$(CC) $^ -o $@ -lm

ChaineMain: ChaineMain.o Chaine.o SVGwriter.o
	$(CC) $^ -o $@ -lm

# Règle de compilation pour chaque fichier objet
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Nettoyage des fichiers objets et de l'exécutable
clean:
	rm -f $(OBJS) $(EXEC)
