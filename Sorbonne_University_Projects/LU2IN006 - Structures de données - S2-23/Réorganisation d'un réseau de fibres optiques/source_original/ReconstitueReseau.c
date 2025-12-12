#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Reseau.h"

int main(int argc, char *argv[]){
    if (argc != 3) {
        printf("Usage: %s <fichier.cha> <methode>\n", argv[0]);
        printf("Methode :\n");
        printf("  1 : Liste\n");
        printf("  2 : Table de hachage\n");
        printf("  3 : Arbre\n");
        return EXIT_FAILURE;
    }

    FILE *fichier_cha = fopen(argv[1], "r");
    if (fichier_cha == NULL) {
        printf("Erreur lors de l'ouverture du fichier\n");
        return EXIT_FAILURE;
    }
    int methode = atoi(argv[2]);

    Chaines *C = lectureChaines(fichier_cha);
    if (C == NULL){
        printf("Erreur lors de la lecture du fichier %s\n", fichier_cha);
        return EXIT_FAILURE;
    }

    Reseau* R = NULL;

    switch (methode){
        case 1:
            R = reconstitueReseauListe(C);
            break;
    /*    case 2:
            R = reconstitueReseauTableHachage(C);
            break;
        case 3:
            R = reconstitueArbre(C);
            break;
    */
        default:
            printf("Methode non reconnue\n");
            return EXIT_FAILURE;
    }

    ecrireReseau(R, stdout);

    libererChaines(C);
    libererReseau(R);

    fclose(fichier_cha);

    return EXIT_SUCCESS;
}
