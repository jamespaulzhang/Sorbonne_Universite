#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "arbre_lexicographique_tab.h"

PNoeudTab creer_noeud(char lettre) {
  PNoeudTab pnt = (PNoeudTab)malloc(sizeof(NoeudTab));
  if (pnt == NULL) {
    printf("Impossible d'allouer un noeud\n");
    return NULL;
  }
  pnt->lettre = lettre;
  pnt->fin_de_mot = non_fin;
  memset(pnt->fils, 0, 26 * sizeof(PNoeudTab)); 
  return pnt;
}

PNoeudTab ajouter_mot(PNoeudTab racine, char *mot) {
  if (mot == NULL || strlen(mot) == 0) {
    return racine;
  }

  PNoeudTab n = racine;
  int a = 'a';

  for (int i = 0; mot[i] != '\0'; i++) {
    int index = mot[i] - a;

    if (n->fils[index] == NULL) {
      n->fils[index] = creer_noeud(mot[i]);
    }

    n = n->fils[index];

    if (mot[i + 1] == '\0') {
      n->fin_de_mot = fin;
    }
  }

  return racine;
}

void afficher_mots(PNoeudTab n, char mot_en_cours[LONGUEUR_MAX_MOT], int index) {
  if (n == NULL)
    return;

  char *mot;
  mot = (char *)malloc((LONGUEUR_MAX_MOT) * sizeof(char));
  if (mot == NULL) {
    printf("Impossible de créer la chaine de caractères");
    return;
  }

  strncpy(mot, mot_en_cours, index);
  mot[index] = n->lettre;

  if (n->fin_de_mot == fin) {
    mot[index + 1] = '\0';
    printf("%s\n", mot);
  }

  for (int i = 0; i < 26; i++) {
    afficher_mots(n->fils[i], mot, index + 1);
  }

  free(mot);
}

void afficher_dico(PNoeudTab racine) {
  int index = 0;
  char *mot = (char *)malloc((LONGUEUR_MAX_MOT) * sizeof(char));

  for (int i = 0; i < 26; i++) {
    afficher_mots(racine->fils[i], mot, index);
  }

  free(mot);
}

void detruire_dico(PNoeudTab dico) {
  if (dico == NULL)
    return;

  for (int i = 0; i < 26; i++) {
    if (dico->fils[i] != NULL)
      detruire_dico(dico->fils[i]);
  }

  free(dico);
}

PNoeudTab chercher_lettre(PNoeudTab n, char lettre) {
  if (n == NULL) {
    return NULL;
  }

  if (n->lettre == lettre) {
    return n;
  }

  return NULL;
}

int rechercher_mot(PNoeudTab dico, char *mot) {
  PNoeudTab n = chercher_lettre(dico, mot[0]);
  if (n == NULL) {
    return 0;
  }

  if (strlen(mot) == 1) {
    return n->fin_de_mot == fin;
  }

  int m = mot[1];
  int a = 'a';

  return rechercher_mot(n->fils[m - a], mot + 1);
}

PNoeudTab lire_dico(const char *nom_fichier) {
  FILE *f = fopen(nom_fichier, "r");
  if (f == NULL) {
    printf("Erreur lors de l'ouverture du fichier %s\n", nom_fichier);
    return NULL;
  }

  PNoeudTab pnt = creer_noeud('\0');
  if (pnt == NULL) {
    printf("Erreur lors de l'allocation de la racine du trie\n");
    fclose(f);
    return NULL;
  }

  char mot[100];
  if (f == NULL) {
    printf("Erreur lors de l'ouverture du fichier %s\n", nom_fichier);
    return NULL;
  }

  while (fgets(mot, 100, f)) {
    mot[strlen(mot) - 1] = '\0';
    pnt = ajouter_mot(pnt, mot);
  }

  fclose(f);
  return pnt;
}

