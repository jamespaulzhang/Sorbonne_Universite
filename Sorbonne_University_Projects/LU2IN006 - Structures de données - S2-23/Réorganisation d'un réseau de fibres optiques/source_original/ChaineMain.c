#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Chaine.h"
#include "SVGwriter.h"

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s input_file output_file\n", argv[0]);
        return 1;
    }

    // Ouvrir le fichier d'entrée en mode lecture
    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL) {
        perror("Erreur lors de l'ouverture du fichier d'entrée");
        return 1;
    }

    // Lire les données du fichier
    Chaines *chaines = lectureChaines(input_file);
    fclose(input_file);

    // Vérifier si la lecture des chaînes a réussi
    if (chaines == NULL) {
        fprintf(stderr, "Erreur lors de la lecture des chaînes.\n");
        libererChaines(chaines); // Libérer la mémoire allouée pour les chaînes
        return 1;
    }

    // Ouvrir le fichier de sortie en mode écriture
    FILE *output_file = fopen(argv[2], "w");
    if (output_file == NULL) {
        perror("Erreur lors de l'ouverture du fichier de sortie");
        libererChaines(chaines); // Libérer la mémoire allouée pour les chaînes
        return 1;
    }

    // Écrire les données dans le fichier de sortie
    ecrireChaines(chaines, output_file);
    fclose(output_file);

    // Appeler la fonction pour afficher les chaînes au format SVG
    afficheChainesSVG(chaines, "output.svg");

    // Libérer la mémoire allouée pour les chaînes
    libererChaines(chaines);

    return 0;
}
