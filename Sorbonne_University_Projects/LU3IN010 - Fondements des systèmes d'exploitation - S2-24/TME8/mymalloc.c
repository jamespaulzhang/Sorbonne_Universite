#include "affiche_tas.h"
#include <stdio.h>
#include <string.h>

char tas[TAILTAS  +1];
int libre;

/* A COMPLETER */

int first_fit(int taille, int *pred) {
    int current = libre;
    int previous = -1;

    while (current != -1) {
        int TL = tas[current]; // Taille de la zone libre

        if (TL >= taille) {
            *pred = previous;
            return current;
        }

        previous = current;
        current = tas[current + 1];

        // S'assurer que l'indice ne dépasse pas les limites
        if (current >= TAILTAS || tas[current + 1] < 0) break; // zones mémoire invalides
    }

    return -1; // Aucun bloc ne convient
}


char *tas_malloc(unsigned int taille) {
    if (taille < 1 || taille + 1 > TAILTAS) return NULL; // Vérification de la taille

    int pred, adresse_libre = first_fit(taille, &pred);

    if (adresse_libre == -1) return NULL; // Pas de mémoire disponible

    int TL = tas[adresse_libre];
    int reste = TL - (taille + 1);

    if (reste >= TAILMIN) {
        // Séparer la zone restante en un nouveau bloc libre
        int nouvelle_zone_libre = adresse_libre + taille + 1;
        tas[nouvelle_zone_libre] = reste;
        tas[nouvelle_zone_libre + 1] = tas[adresse_libre + 1];
        tas[adresse_libre] = taille;
    } else {
        // Mettre à jour la liste des blocs libres
        tas[adresse_libre] = taille + reste;

        if (pred == -1) {
            libre = tas[adresse_libre + 1];
        } else {
            tas[pred + 1] = tas[adresse_libre + 1];
        }
    }

    return &tas[adresse_libre + 1]; // Retourne l'adresse après la taille
}


int tas_free(char *ptr) {
    if (ptr < tas || ptr >= tas + TAILTAS) return -1;

    int adresse = ptr - tas - 1;
    int TD = tas[adresse];
    int nouvelle_taille = TD + 1; // Taille bloc libre incluant l'octet taille

    int current = libre;
    int prev = -1;

    // Trouver où insérer ce bloc dans la liste des zones libres
    while (current != -1 && current < adresse) {
        prev = current;
        current = tas[current + 1];
    }

    // Fusion avec la zone libre suivante si possible
    if (current == adresse + nouvelle_taille) {
        nouvelle_taille += tas[current];
        tas[adresse + 1] = tas[current + 1];
    } else {
        tas[adresse + 1] = current;
    }

    // Fusion avec la zone libre précédente si possible
    if (prev != -1 && prev + tas[prev] == adresse) {
        tas[prev] += nouvelle_taille;
        tas[prev + 1] = tas[adresse + 1];
    } else {
        tas[adresse] = nouvelle_taille;
        if (prev == -1) {
            libre = adresse;
        } else {
            tas[prev + 1] = adresse;
        }
    }

    return 0;
}


int main() {
    tas_init();
    printf("État initial du tas :\n");
    afficher_tas();

    // Jeu d'essai Q1.2
    char *p1, *p2, *p3, *p4;

    p1 = (char *) tas_malloc(10);
    printf("Après allocation de p1 (10 octets) :\n");
    afficher_tas();
    
    p2 = (char *) tas_malloc(9);
    printf("Après allocation de p2 (9 octets) :\n");
    afficher_tas();
    
    p3 = (char *) tas_malloc(5);
    printf("Après allocation de p3 (5 octets) :\n");
    afficher_tas();

    strcpy(p1, "tp 1");
    strcpy(p2, "tp 2");
    strcpy(p3, "tp 3");

    tas_free(p2);
    printf("Après libération de p2 :\n");
    afficher_tas();

    p4 = (char *) tas_malloc(8);
    printf("Après allocation de p4 (8 octets) :\n");
    afficher_tas();

    strcpy(p4, "systeme");

    return 0;
}