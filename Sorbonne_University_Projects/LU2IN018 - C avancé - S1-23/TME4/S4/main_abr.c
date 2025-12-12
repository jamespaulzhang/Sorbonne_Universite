#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "abr.h"
#include "liste.h"

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <mot_a_chercher> <nombre_repetitions>\n", argv[0]);
        return 1;
    }
    
    // Mot à rechercher et nombre de répétitions
    const char *mot_a_chercher = argv[1];
    int nombre_repetitions = atoi(argv[2]);

    // Lecture du dictionnaire depuis un fichier
    Lm_mot *lm = lire_dico_Lmot("french_za");
    if (lm == NULL) {
        fprintf(stderr, "Erreur lors de la lecture du dictionnaire.\n");
        return 1;
    }

    // Construction de l'ABR à partir de la liste de mots
    Nd_mot *abr = Lm2abr(lm);

    // Mesure du temps de recherche
    clock_t debut = clock();

    for (int i = 1; i <= nombre_repetitions; i++) {
        if (chercher_Nd_mot(abr, mot_a_chercher) != NULL) {
            printf("Nombre_repetitions: %d\n", i);
        }
    }

    // Mesure du temps écoulé
    clock_t fin = clock();
    double temps_ecoule = ((double) (fin - debut)) / CLOCKS_PER_SEC;

    // Affichage du temps écoulé
    printf("Temps écoulé pour %d répétitions : %f secondes\n", nombre_repetitions, temps_ecoule);

    // Libération de la mémoire
    detruire_abr_mot(abr);

    return 0;
}

