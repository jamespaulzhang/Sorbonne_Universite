#include "Reseau.h"
#include "Chaine.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "SVGwriter.h"

Noeud* rechercheCreeNoeudListe(Reseau *R, double x, double y){
    CellNoeud *current = R->noeuds;
    while (current != NULL){
        if (current->nd->x == x && current->nd->y == y){
            return current->nd;
        }
        current = current->suiv;
    }

    Noeud *newNode = (Noeud*)malloc(sizeof(Noeud));
    if (newNode == NULL){
        exit(EXIT_FAILURE);
    }

    newNode->x = x;
    newNode->y = y;
    newNode->num = R->nbNoeuds + 1;
    newNode->voisins = NULL;

    CellNoeud *newCell = (CellNoeud*)malloc(sizeof(CellNoeud));
    if (newCell == NULL){
        free(newNode);
        exit(EXIT_FAILURE);
    }
    newCell->nd = newNode;
    newCell->suiv = R->noeuds;
    R->noeuds = newCell;

    R->nbNoeuds++;

    return newNode;
}

Reseau* reconstitueReseauListe(Chaines *C) {
    Reseau* R = (Reseau*)malloc(sizeof(Reseau));
    if (R == NULL) {
        exit(EXIT_FAILURE);
    }
    R->nbNoeuds = 0;
    R->gamma = C->gamma;
    R->noeuds = NULL;
    R->commodites = NULL;

    // Parcourir chaque chaîne dans C
    for (CellChaine *chaineCell = C->chaines; chaineCell != NULL; chaineCell = chaineCell->suiv) {
        CellPoint *pointCell = chaineCell->points;
        Noeud *prevNode = NULL;
        
        // Parcourir chaque point dans la chaîne
        while (pointCell != NULL) {
            // Rechercher ou créer le noeud correspondant au point
            Noeud *currentNode = rechercheCreeNoeudListe(R, pointCell->x, pointCell->y);
            
            // Ajouter une liaison entre le noeud actuel et le noeud précédent
            if (prevNode != NULL) {
                // Créer la liaison entre les nœuds voisins
                CellNoeud *newNeighborCell1 = (CellNoeud*)malloc(sizeof(CellNoeud));
                if (newNeighborCell1 == NULL){
                    exit(EXIT_FAILURE);
                }
                newNeighborCell1->nd = prevNode;
                newNeighborCell1->suiv = currentNode->voisins;
                currentNode->voisins = newNeighborCell1;

                CellNoeud *newNeighborCell2 = (CellNoeud*)malloc(sizeof(CellNoeud));
                if (newNeighborCell2 == NULL){
                    exit(EXIT_FAILURE);
                }
                newNeighborCell2->nd = currentNode;
                newNeighborCell2->suiv = prevNode->voisins;
                prevNode->voisins = newNeighborCell2;
            }

            prevNode = currentNode;
            pointCell = pointCell->suiv;
        }
    }

    return R;
}


// Fonction pour écrire le réseau dans un fichier
void ecrireReseau(Reseau *R, FILE *f){
    fprintf(f, "Nombre de noeuds: %d\n", R->nbNoeuds);
    fprintf(f, "Nombre maximal de fibres par câble: %d\n", R->gamma);

    // Parcourir la liste des noeuds et écrire les informations de chaque noeud
    CellNoeud *current = R->noeuds;
    while (current != NULL){
        fprintf(f, "Noeud %d: Coordonnées (%f, %f)\n", current->nd->num, current->nd->x, current->nd->y);
        current = current->suiv;
    }

    fprintf(f, "Nombre de liaisons: %d\n", nbLiaisons(R));
    fprintf(f, "Nombre de commodites: %d\n", nbCommodites(R));
}


// Fonction pour compter le nombre de liaisons dans le réseau
int nbLiaisons(Reseau *R) {
    int count = 0;
    CellNoeud *current = R->noeuds;
    while (current != NULL) {
        CellNoeud *neighbor = current->nd->voisins;
        while (neighbor != NULL) {
            count++;
            neighbor = neighbor->suiv;
        }
        current = current->suiv;
    }

    // Chaque liaison est comptée deux fois (une fois pour chaque extrémité), donc diviser par 2
    return count / 2;
}


// Fonction pour compter le nombre de commodités dans le réseau
int nbCommodites(Reseau *R) {
    int count = 0;

    // Parcourir la liste des commodités
    CellCommodite *current = R->commodites;
    while (current != NULL) {
        count++;
        current = current->suiv;
    }

    return count;
}


// Fonction pour libérer la mémoire allouée pour le réseau
void libererReseau(Reseau* R){
    CellNoeud* currentNoeud = R->noeuds;
    while (currentNoeud != NULL){
        CellNoeud* tempNoeud = currentNoeud;
        currentNoeud = currentNoeud->suiv;
        free(tempNoeud->nd);
        free(tempNoeud);
    }

    CellCommodite* currentCommodite = R->commodites;
    while (currentCommodite != NULL){
        CellCommodite* tempCommodite = currentCommodite;
        currentCommodite = currentCommodite->suiv;
        free(tempCommodite);
    }

    R->nbNoeuds = 0;
    R->gamma = 0;
    R->noeuds = NULL;
    R->commodites = NULL;
}

void afficheReseauSVG(Reseau *R, char* nomInstance){
    CellNoeud *courN,*courv;
    SVGwriter svg;
    double maxx=0,maxy=0,minx=1e6,miny=1e6;

    courN=R->noeuds;
    while (courN!=NULL){
        if (maxx<courN->nd->x) maxx=courN->nd->x;
        if (maxy<courN->nd->y) maxy=courN->nd->y;
        if (minx>courN->nd->x) minx=courN->nd->x;
        if (miny>courN->nd->y) miny=courN->nd->y;
        courN=courN->suiv;
    }
    SVGinit(&svg,nomInstance,500,500);
    courN=R->noeuds;
    while (courN!=NULL){
        SVGpoint(&svg,500*(courN->nd->x-minx)/(maxx-minx),500*(courN->nd->y-miny)/(maxy-miny));
        courv=courN->nd->voisins;
        while (courv!=NULL){
            if (courv->nd->num<courN->nd->num)
                SVGline(&svg,500*(courv->nd->x-minx)/(maxx-minx),500*(courv->nd->y-miny)/(maxy-miny),500*(courN->nd->x-minx)/(maxx-minx),500*(courN->nd->y-miny)/(maxy-miny));
            courv=courv->suiv;
        }
        courN=courN->suiv;
    }
    SVGfinalize(&svg);
}