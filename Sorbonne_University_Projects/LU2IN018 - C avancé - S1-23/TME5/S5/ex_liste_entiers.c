#include <stdlib.h>
#include "liste.h"
#include "devel.h"
#include "fonctions_entiers.h"

int main(void) {
    // Créer une liste vide
    PListe maListe = (PListe)malloc(sizeof(Liste));
    maListe->elements = NULL;
    maListe->dupliquer = dupliquer_int;
    maListe->copier = copier_int;
    maListe->detruire = detruire_int;
    maListe->afficher = afficher_int;
    maListe->comparer = comparer_int;
    maListe->ecrire = ecrire_int;
    maListe->lire = lire_int;

    // Ajouter des éléments à la liste
    int val1 = 10 , val2 = 20 , val3 = 30;
    ajouter_liste(maListe, 3, dupliquer_int(&val1), dupliquer_int(&val2), dupliquer_int(&val3));

    // Afficher la liste
    printf("Liste après ajout d'éléments : \n");
    afficher_liste(maListe);

    // Insérer un élément en début de liste
    int val4 = 5;
    inserer_debut(maListe, dupliquer_int(&val4));

    // Afficher la liste après l'insertion en début
    printf("Liste après insertion en début : \n");
    afficher_liste(maListe);

    // Insérer un élément en fin de liste
    int val5 = 40;
    inserer_fin(maListe, dupliquer_int(&val5));

    // Afficher la liste après l'insertion en fin
    printf("Liste après insertion en fin : \n");
    afficher_liste(maListe);

    // Insérer un élément en place
    int val6 = 25;
    inserer_place(maListe, dupliquer_int(&val6));

    // Afficher la liste après l'insertion en place
    printf("Liste après insertion en place : \n");
    afficher_liste(maListe);

    // Rechercher un élément dans la liste
    PElement elementCherche = chercher_liste(maListe, dupliquer_int(&val2));
    if (elementCherche != NULL) {
        printf("Element trouvé : \n");
        afficher_int(elementCherche->data);
        printf("\n");
    } else {
        printf("Element non trouvé.\n");
    }

    // Détruire la liste
    detruire_liste(maListe);

    return 0;
}

