#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include "Chaine.h"
#include "SVGwriter.h" 

Chaines* lectureChaines(FILE *f) {
    // Allouer une instance de Chaines
    Chaines *chaines = (Chaines*)malloc(sizeof(Chaines));
    if (chaines == NULL) {
        fprintf(stderr, "Erreur d'allocation de mémoire pour Chaines.\n");
        return NULL;
    }

    // Lire les données du fichier
    int nbChaines, gamma;
    if (fscanf(f, "NbChain: %d\nGamma: %d\n", &nbChaines, &gamma) != 2) {
        fprintf(stderr, "Erreur de lecture du nombre de chaînes et du nombre maximal de fibres par câble.\n");
        free(chaines); // Libérer la mémoire allouée pour Chaines
        return NULL;
    }

    // Initialiser les champs de Chaines
    chaines->gamma = gamma;
    chaines->nbChaines = nbChaines;
    chaines->chaines = NULL;

    // Lire chaque chaîne
    for (int i = 0; i < nbChaines; ++i) {
        // Allouer une nouvelle cellule de chaîne
        CellChaine *nouvelleChaine = (CellChaine*)malloc(sizeof(CellChaine));
        if (nouvelleChaine == NULL) {
            fprintf(stderr, "Erreur d'allocation de mémoire pour CellChaine.\n");
            libererChaines(chaines); // Libérer la mémoire allouée pour Chaines et ses chaînes précédentes
            return NULL;
        }

        // Lire le numéro de la chaîne
        if (fscanf(f, "%d", &(nouvelleChaine->numero)) != 1) {
            fprintf(stderr, "Erreur de lecture du numéro de la chaîne.\n");
            free(nouvelleChaine); // Libérer la mémoire allouée pour la nouvelle chaîne
            libererChaines(chaines); // Libérer la mémoire allouée pour Chaines et ses chaînes précédentes
            return NULL;
        }

        // Initialiser les points de la chaîne à NULL
        nouvelleChaine->points = NULL;

        // Lire le nombre de points de la chaîne
        int nbPoints;
        if (fscanf(f, "%d", &nbPoints) != 1) {
            fprintf(stderr, "Erreur de lecture du nombre de points de la chaîne.\n");
            free(nouvelleChaine); // Libérer la mémoire allouée pour la nouvelle chaîne
            libererChaines(chaines); // Libérer la mémoire allouée pour Chaines et ses chaînes précédentes
            return NULL;
        }

        // Lire chaque point de la chaîne
        for (int j = 0; j < nbPoints; ++j) {
            // Allouer une nouvelle cellule de point
            CellPoint *nouveauPoint = (CellPoint*)malloc(sizeof(CellPoint));
            if (nouveauPoint == NULL) {
                fprintf(stderr, "Erreur d'allocation de mémoire pour CellPoint.\n");
                libererChaines(chaines); // Libérer la mémoire allouée pour Chaines et ses chaînes précédentes
                return NULL;
            }

            // Lire les coordonnées du point
            if (fscanf(f, "%lf %lf", &(nouveauPoint->x), &(nouveauPoint->y)) != 2) {
                fprintf(stderr, "Erreur de lecture des coordonnées du point de la chaîne.\n");
                free(nouveauPoint); // Libérer la mémoire allouée pour le nouveau point
                libererChaines(chaines); // Libérer la mémoire allouée pour Chaines et ses chaînes précédentes
                return NULL;
            }

            // Ajouter le point à la liste des points de la chaîne
            nouveauPoint->suiv = nouvelleChaine->points;
            nouvelleChaine->points = nouveauPoint;
        }

        // Ajouter la nouvelle chaîne à la liste des chaînes
        nouvelleChaine->suiv = chaines->chaines;
        chaines->chaines = nouvelleChaine;
    }

    return chaines;
}


void ecrireChaines(Chaines *C, FILE *f) {
    // Écrire le nombre maximal de fibres par câble et le nombre de chaînes
    fprintf(f, "NbChain: %d\nGamma: %d\n", C->nbChaines, C->gamma);

    // Parcourir la liste chaînée des chaînes
    CellChaine *chaine = C->chaines;
    while (chaine != NULL) {
        // Écrire le numéro de la chaîne
        fprintf(f, "%d %d\n", chaine->numero, comptePointsTotal(C));

        // Parcourir la liste chaînée des points de la chaîne
        CellPoint *point = chaine->points;
        while (point != NULL) {
            // Écrire les coordonnées du point
            fprintf(f, "%.2f %.2f ", point->x, point->y);
            point = point->suiv;
        }
        fprintf(f, "\n");

        chaine = chaine->suiv;
    }
}


void libererChaines(Chaines *C) {
    // Parcourir la liste chaînée des chaînes
    CellChaine *chaine = C->chaines;
    while (chaine != NULL) {
        // Libérer la mémoire allouée pour chaque cellule de point de la chaîne
        CellPoint *point = chaine->points;
        while (point != NULL) {
            CellPoint *temp = point;
            point = point->suiv;
            free(temp);
        }
        
        // Libérer la mémoire allouée pour chaque cellule de chaîne
        CellChaine *tempChaine = chaine;
        chaine = chaine->suiv;
        free(tempChaine);
    }

    // Libérer la mémoire allouée pour la structure Chaines
    free(C);
}


int comptePointsTotal(Chaines *C) {
    int totalPoints = 0;
    // Parcourir la liste chainée des chaînes
    CellChaine *chaine = C->chaines;
    while (chaine != NULL) {
        // Parcourir la liste chainée des points de la chaîne
        CellPoint *point = chaine->points;
        while (point != NULL) {
            totalPoints++;
            point = point->suiv;
        }
        chaine = chaine->suiv;
    }
    return totalPoints;
}

void afficheChainesSVG(Chaines *C, char* nomInstance){
    //int i;
    double maxx=0,maxy=0,minx=1e6,miny=1e6;
    CellChaine *ccour;
    CellPoint *pcour;
    double precx,precy;
    SVGwriter svg;
    ccour=C->chaines;
    while (ccour!=NULL){
        pcour=ccour->points;
        while (pcour!=NULL){
            if (maxx<pcour->x) maxx=pcour->x;
            if (maxy<pcour->y) maxy=pcour->y;
            if (minx>pcour->x) minx=pcour->x;
            if (miny>pcour->y) miny=pcour->y;  
            pcour=pcour->suiv;
        }
    ccour=ccour->suiv;
    }
    SVGinit(&svg,nomInstance,500,500);
    ccour=C->chaines;
    while (ccour!=NULL){
        pcour=ccour->points;
        SVGlineRandColor(&svg);
        SVGpoint(&svg,500*(pcour->x-minx)/(maxx-minx),500*(pcour->y-miny)/(maxy-miny)); 
        precx=pcour->x;
        precy=pcour->y;  
        pcour=pcour->suiv;
        while (pcour!=NULL){
            SVGline(&svg,500*(precx-minx)/(maxx-minx),500*(precy-miny)/(maxy-miny),500*(pcour->x-minx)/(maxx-minx),500*(pcour->y-miny)/(maxy-miny));
            SVGpoint(&svg,500*(pcour->x-minx)/(maxx-minx),500*(pcour->y-miny)/(maxy-miny));
            precx=pcour->x;
            precy=pcour->y;    
            pcour=pcour->suiv;
        }
        ccour=ccour->suiv;
    }
    SVGfinalize(&svg);
}

// Fonction qui calcule la distance entre deux points
double distance(CellPoint *p1, CellPoint *p2) {
    return sqrt(pow(p2->x - p1->x, 2) + pow(p2->y - p1->y, 2));
}

// Fonction qui calcule la longueur physique d'une chaîne
double longueurChaine(CellChaine *c) {
    double longueur = 0.0;
    CellPoint *point1 = c->points;
    CellPoint *point2 = point1->suiv;
    
    // Parcourir la chaîne et calculer la distance entre chaque paire de points
    while (point2 != NULL) {
        longueur += distance(point1, point2);
        point1 = point2;
        point2 = point2->suiv;
    }
    return longueur;
}

// Fonction qui calcule la longueur physique totale des chaînes
double longueurTotale(Chaines *C) {
    double longueur_totale = 0.0;
    CellChaine *chaine = C->chaines;
    
    // Parcourir chaque chaîne et ajouter sa longueur à la longueur totale
    while (chaine != NULL) {
        longueur_totale += longueurChaine(chaine);
        chaine = chaine->suiv;
    }
    return longueur_totale;
}