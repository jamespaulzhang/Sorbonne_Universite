#include <stdio.h>
#include <stdlib.h>  // Pour atoi

int main(int argc, char *argv[]) {
    // Vérifier qu'il y a au moins un argument (le programme lui-même compte comme un argument)
    if (argc < 2) {
        printf("Veuillez passer au moins un entier en argument.\n");
        return 1;  // Code de sortie 1 pour erreur
    }

    // Initialiser la variable pour le maximum
    int max = atoi(argv[1]);  // Initialiser max avec le premier argument converti en entier

    // Parcourir les autres arguments
    for (int i = 2; i < argc; i++) {
        int current = atoi(argv[i]);
        if (current > max) {
            max = current;  // Mettre à jour le maximum si on trouve une valeur plus grande
        }
    }

    // Afficher le résultat
    printf("Le maximum est : %d\n", max);

    return 0;  // Code de sortie 0 pour succès
}
