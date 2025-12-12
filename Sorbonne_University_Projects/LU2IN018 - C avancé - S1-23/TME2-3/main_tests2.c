#include <assert.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "ecosys.h"

int main(void) {
  Animal *liste_proie = NULL;
  Animal *liste_predateur = NULL;
  int energie=10;
  
  srand(time(NULL));

  //créer 20 proies
  Animal *premier_proie = creer_animal(rand() % SIZE_X, rand() % SIZE_Y , energie);
  liste_proie = premier_proie;
  for(int i = 0; i < 19; i++){
    Animal *proie_suivant = creer_animal(rand() % SIZE_X, rand() % SIZE_Y , energie);
    liste_proie = ajouter_en_tete_animal(liste_proie, proie_suivant);
  }
  printf("Nombre de la liste_proie = %d\n", compte_animal_rec(liste_proie));

  ////créer 20 predateurs
  Animal *premier_predateur = creer_animal(rand() % SIZE_X, rand() % SIZE_Y , energie);
  liste_predateur = premier_predateur;
  for(int i = 0; i < 19; i++){
    Animal *predateur_suivant = creer_animal(rand() % SIZE_X, rand() % SIZE_Y , energie);
    liste_predateur = ajouter_en_tete_animal(liste_predateur, predateur_suivant);
  }
  printf("Nombre de la liste_predateur = %d\n", compte_animal_it(liste_predateur));
  afficher_ecosys(liste_proie,liste_predateur);  

  //enlever la dernière élément de liste_proie et liste_predateur
  enlever_animal(&liste_proie, premier_proie);
  enlever_animal(&liste_predateur, premier_predateur);
  printf("Nombre de la liste_proie = %d\n", compte_animal_rec(liste_proie));
  printf("Nombre de la liste_predateur = %d\n", compte_animal_it(liste_predateur));
  afficher_ecosys(liste_proie, liste_predateur);

  //test de l'écriture de fichier
  ecrire_ecosys("/home/laviestbelle/Desktop/c avance ZHANG/TME2-3/test.txt", liste_predateur, liste_proie);
  lire_ecosys("/home/laviestbelle/Desktop/c avance ZHANG/TME2-3/test.txt", &liste_predateur, &liste_proie);
  
  liberer_liste_animaux(liste_proie);
  liberer_liste_animaux(liste_predateur);
  return 0;
}
