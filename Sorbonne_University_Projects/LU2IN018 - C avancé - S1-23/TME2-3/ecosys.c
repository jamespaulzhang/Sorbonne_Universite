#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ecosys.h"

//On peut modifier les variables globaux suivants pour avoir les differents cas
float p_ch_dir=0.01;
float p_reproduce_proie=0.4;
float p_reproduce_predateur=0.5;
int temps_repousse_herbe=-15;

/* PARTIE 1*/
/* Fourni: Part 1, exercice 4, question 2 */
Animal *creer_animal(int x, int y, float energie) {
  Animal *na = (Animal *)malloc(sizeof(Animal));
  assert(na);
  na->x = x;
  na->y = y;
  na->energie = energie;
  na->dir[0] = rand() % 3 - 1;
  na->dir[1] = rand() % 3 - 1;
  na->suivant = NULL;
  return na;
}

/* Fourni: Part 1, exercice 4, question 3 */
Animal *ajouter_en_tete_animal(Animal *liste, Animal *animal) {
  assert(animal);
  assert(!animal->suivant);
  animal->suivant = liste;
  return animal;
}

/* A faire. Part 1, exercice 6, question 2 */
void ajouter_animal(int x, int y, float energie, Animal **liste_animal) {
    /*A Completer*/
    assert(0 <= x && x < SIZE_X);
    assert(0 <= y && y < SIZE_Y);

    Animal *na = creer_animal(x, y, energie); // Créer un nouvel animal

    if (*liste_animal == NULL) {
        *liste_animal = na; // Si la liste est vide, le nouvel animal devient le premier
    } else {
        na->suivant = *liste_animal; // Sinon, le nouvel animal pointe vers l'ancien premier
        *liste_animal = na; // Le nouvel animal devient le premier
    }
}

/* A Faire. Part 1, exercice 6, question 7 */
void enlever_animal(Animal **liste, Animal *animal) {
  /*A Completer*/
  assert(liste);
  assert(animal);

  if (*liste == NULL || animal == NULL)
    return;

  Animal *prev = NULL;
  Animal *current = *liste;

  while (current != NULL && current != animal) {
    prev = current;
    current = current->suivant;
  }

  if (current == NULL) {
    printf("L'animal n'a pas été trouvé dans la liste.\n");
    return;
  }

  if (prev == NULL) {
    *liste = current->suivant; // Si l'animal à enlever est le premier de la liste
  } else {
    prev->suivant = current->suivant;
  }

  free(current); // Libérer la mémoire de l'animal enlevé
}


/* A Faire. Part 1, exercice 6, question 4 */
void liberer_liste_animaux(Animal *liste) {
  /*A Completer*/
  // Vérifier si la liste est vide
  if(liste == NULL) 
  {
    printf("La liste est vide\n");
    return;
  }
  // Pointeur temporaire pour stocker l'élément en cours
  Animal* tmp = liste;
  // Pointeur pour stocker l'élément suivant
  Animal* suivant;
  // Parcourir la liste
  while (tmp != NULL) {
    // Sauvegarder le pointeur vers l'élément suivant
    suivant = tmp->suivant;
    // Libérer la mémoire de l'élément en cours
    free(tmp);
    // Passer à l'élément suivant
    tmp = suivant;
  }
}

/* Fourni: part 1, exercice 4, question 4 */
unsigned int compte_animal_rec(Animal *la) {
  if (!la) return 0;
  return 1 + compte_animal_rec(la->suivant);
}

/* Fourni: part 1, exercice 4, question 4 */
unsigned int compte_animal_it(Animal *la) {
  int cpt = 0;
  while (la) {
    ++cpt;
    la=la->suivant;
  }
  return cpt;
}

/* Part 1. Exercice 5, question 1, ATTENTION, ce code est susceptible de contenir des erreurs... */
void afficher_ecosys(Animal *liste_proie, Animal *liste_predateur) {
  unsigned int i, j;
  char ecosys[SIZE_X][SIZE_Y];
  Animal *pa=NULL;

  /* on initialise le tableau */
  for (i = 0; i < SIZE_X; ++i) {
    for (j = 0; j < SIZE_Y; ++j) {
      ecosys[i][j]=' ';
    }
  }

  /* on ajoute les proies */
  pa = liste_proie;
  while (pa) {
    if (pa->x >= 0 && pa->x < SIZE_X && pa->y >= 0 && pa->y < SIZE_Y) {
      ecosys[pa->x][pa->y] = '*';
    }
    pa = pa->suivant;
  }

  /* on ajoute les predateurs */
  pa = liste_predateur;
  while (pa) {
    if (pa->x >= 0 && pa->x < SIZE_X && pa->y >= 0 && pa->y < SIZE_Y) {
      if ((ecosys[pa->x][pa->y] == '@') || (ecosys[pa->x][pa->y] == '*')) { /* proies aussi present */
        ecosys[pa->x][pa->y] = '@';
      } else {
        ecosys[pa->x][pa->y] = 'O';
      }
    }
    pa = pa->suivant;
  }

  /* on affiche le tableau */
  printf("+");
  for (i = 0; i < SIZE_X; ++i) {
    printf("-");
  }  
  printf("+\n");
  for (j = 0; j < SIZE_Y; ++j) {
    printf("|");
    for (i = 0; i < SIZE_X; ++i) {
      putchar(ecosys[i][j]);
    }
    printf("|\n");
  }
  printf("+");
  for (i = 0; i < SIZE_X; ++i) {
    printf("-");
  }
  printf("+\n");
  int nbproie = compte_animal_it(liste_proie);
  int nbpred = compte_animal_it(liste_predateur);
  
  printf("Nb proies (*): %5d\tNb predateurs (O): %5d\n", nbproie, nbpred);

}

void clear_screen() {
  printf("\x1b[2J\x1b[1;1H");  /* code ANSI X3.4 pour effacer l'ecran */
}

/* PARTIE 2*/

/* Part 2. Exercice 3*/
void ecrire_ecosys(const char* nom_fichier, Animal* liste_predateur, Animal* liste_proie) {
  //on le fait pendant TD
  FILE* f = fopen(nom_fichier, "w");
  if(f == NULL) {
    printf("Erreur lors de l'ouverture de %s\n", nom_fichier);
    return;
  }
  //ecrire la liste_proie
  fprintf(f, "<proies>\n");
  Animal* tmp = liste_proie;
  while(tmp) {
    fprintf(f, "x=%d y=%d dir=[%d %d] e=%f\n", tmp->x, tmp->y, tmp->dir[0], tmp->dir[1], tmp->energie);
    tmp = tmp->suivant;
  }
  fprintf(f, "</proies>\n");
  //ecrire la liste_predateur
  fprintf(f, "<predateurs>\n");
  tmp = liste_predateur;
  while(tmp) {
    fprintf(f, "x=%d y=%d dir=[%d %d] e=%f\n", tmp->x, tmp->y, tmp->dir[0], tmp->dir[1], tmp->energie);
    tmp = tmp->suivant;
  }
  fprintf(f, "</predateurs>\n");
  fclose(f);
}

void lire_ecosys(const char* nom_fichier, Animal** liste_predateur, Animal** liste_proie){
    //on le fait pendant TD
    FILE* f = fopen(nom_fichier, "r");
    if(f == NULL) {
        printf("Erreur lors de l'ouverture de %s\n", nom_fichier);
        return;
    }
    char buffer[256];
    fgets(buffer, 256, f);
    assert(strncmp(buffer, "<proies>", 8) == 0);
    printf("<proies>\n");
    fgets(buffer, 256, f);

    int x_lu, y_lu, dir_lu[2];
    float e_lu;

    while(strncmp(buffer, "</proies>", 9) != 0){
        sscanf(buffer, "x=%d y=%d dir=[%d %d] e=%f\n", &x_lu, &y_lu, &dir_lu[0], &dir_lu[1], &e_lu);
        Animal* a_lu = creer_animal(x_lu, y_lu, e_lu);
        a_lu->dir[0] = dir_lu[0];
        a_lu->dir[1] = dir_lu[1];
        // insertion en tete
        a_lu->suivant = *liste_proie;
        *liste_proie = a_lu;

        printf("x=%d y=%d dir=[%d %d] e=%f\n", x_lu, y_lu, dir_lu[0], dir_lu[1], e_lu);

        fgets(buffer, 256, f);
    }
    printf("</proies>\n");
    fgets(buffer, 256, f);
    assert(strncmp(buffer, "<predateurs>", 12) == 0);
    printf("<predateurs>\n");
    fgets(buffer, 256, f);
    
    while(strncmp(buffer, "</predateurs>", 13) != 0){
        sscanf(buffer, "x=%d y=%d dir=[%d %d] e=%f\n", &x_lu, &y_lu, &dir_lu[0], &dir_lu[1], &e_lu);
        Animal *a_lu = creer_animal(x_lu, y_lu, e_lu);
        a_lu->dir[0] = dir_lu[0];
        a_lu->dir[1] = dir_lu[1];

        // insertion en tete
        a_lu->suivant = *liste_predateur;
        *liste_predateur = a_lu;


        printf("x=%d y=%d dir=[%d %d] e=%f\n", x_lu, y_lu, dir_lu[0], dir_lu[1], e_lu);

        fgets(buffer, 256, f);
    }
    printf("</predateurs>\n");
    fclose(f);
}


/* Part 2. Exercice 4, question 1 */
void bouger_animaux(Animal *la) {
    /*A Completer*/
    Animal *ap = la; // Pointeur vers le premier animal de la liste
    while (ap) { // Tant qu'il y a un animal à traiter
        if (rand() / (float)RAND_MAX <= p_ch_dir) { // Vérifie la probabilité de changer de direction
            ap->dir[0] = rand() % 3 - 1; // Change la direction en x : -1, 0 ou 1
            ap->dir[1] = rand() % 3 - 1; // Change la direction en y : -1, 0 ou 1
        }

        // Effectue le déplacement en tenant compte de la toricité
        ap->x = (ap->x + ap->dir[0] + SIZE_X) % SIZE_X;
        ap->y = (ap->y + ap->dir[1] + SIZE_Y) % SIZE_Y;

        ap = ap->suivant; // Passe à l'animal suivant dans la liste
    }
}


/* Part 2. Exercice 4, question 3 */
void reproduce(Animal **liste_animal, float p_reproduce) {
   /*A Completer*/
   Animal *ani = liste_animal ? *liste_animal : NULL;
   while(ani){
      if(rand() / (float)RAND_MAX <= p_reproduce){
        ajouter_animal(ani->x, ani->y, ani->energie/2, liste_animal);
        ani -> energie /= 2;
    }
    ani = ani -> suivant;
  }
}


/* Part 2. Exercice 6, question 1 */
void rafraichir_proies(Animal **liste_proie, int monde[SIZE_X][SIZE_Y]) {
    /*A Completer*/
    Animal *tmp = *liste_proie;
    bouger_animaux(tmp);
    while (tmp) {
        Animal *next = tmp->suivant;
        
        // Baisser l'énergie de la proie
        tmp->energie-=1;
        
        // Gestion de l'herbe
        if (monde[tmp->x][tmp->y] >= 0) {
            tmp->energie += monde[tmp->x][tmp->y];
            monde[tmp->x][tmp->y] = temps_repousse_herbe;
        }
        
        // Vérifier si la proie est morte
        if (tmp->energie <= 0) {
            enlever_animal(liste_proie, tmp);
        }
        tmp = next;
    }
    // Appeler la fonction de reproduction
    reproduce(liste_proie, p_reproduce_proie);
}


/* Part 2. Exercice 7, question 1 */
Animal *animal_en_XY(Animal *l, int x, int y) {
  /*A Completer*/
  Animal *tmp = l;
  while(tmp){
    if(tmp->x == x && tmp->y == y){ // On trouve l'animal à cette position
      return tmp;
    }
    tmp = tmp->suivant;
  }
  // On n'a pas trouver l'animal ici
  return NULL;
} 

/* Part 2. Exercice 7, question 2 */
void rafraichir_predateurs(Animal **liste_predateur, Animal **liste_proie) {
    /*A Completer*/
    Animal *tmp = *liste_predateur;
    bouger_animaux(tmp);
    while (tmp) {
    	Animal *next = tmp->suivant;
    	
        // Baisser l'énergie du prédateur
        tmp->energie-=1;

        // Vérifier s'il y a une proie sur la même case
        Animal *proie = animal_en_XY(*liste_proie, tmp->x, tmp->y);

        if (proie != NULL) {
            // Si une proie est présente, "manger" la proie et augmenter l'énergie du prédateur
            tmp->energie += proie->energie;
            enlever_animal(liste_proie, proie);
        }

        // Vérifier si le prédateur est mort
        if (tmp->energie <= 0) {
            enlever_animal(liste_predateur, tmp);
        }
        tmp = next;
    }

    // Appeler la fonction de reproduction
    reproduce(liste_predateur,p_reproduce_predateur);
}


/* Part 2. Exercice 5, question 2 */
void rafraichir_monde(int monde[SIZE_X][SIZE_Y]) {
    /*A Completer*/
    for (int i = 0; i < SIZE_X; i++) {
        for (int j = 0; j < SIZE_Y; j++) {
            monde[i][j]++;
        }
    }
}

