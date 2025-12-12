#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "arbre_lexicographique.h"

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <mot_a_chercher> <nombre_repetitions>\n", argv[0]);
        return 1;
    }

    char *mot_a_chercher = argv[1];
    int nombre_repetitions = atoi(argv[2]);
    PNoeud pn = lire_dico("french_za");
    if (pn == NULL) {
        fprintf(stderr, "Erreur lors de la lecture du dictionnaire.\n");
        return 1;
    }
        
    clock_t debut = clock();

    for (int i = 1; i <= nombre_repetitions; i++) {
        if (rechercher_mot(pn, mot_a_chercher) != 0) {
            printf("Nombre_repetitions: %d\n", i);
        }
    }

    clock_t fin = clock();
    double temps_ecoule = ((double)(fin - debut)) / CLOCKS_PER_SEC;

    printf("Temps écoulé pour %d répétitions : %f secondes\n", nombre_repetitions, temps_ecoule);

    detruire_dico(pn);

    return 0;
}

