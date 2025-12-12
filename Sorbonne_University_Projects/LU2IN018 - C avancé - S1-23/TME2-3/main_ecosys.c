#include <assert.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <strings.h>
#include "ecosys.h"


#define NB_PROIES 20
#define NB_PREDATEURS 20
#define T_WAIT 40000

#define iteration_max 200

/* Parametres globaux de l'ecosysteme (externes dans le ecosys.h)*/
//J'ai declare dans le ecosys.h avec 
	/*extern double p_ch_dir;
	extern float p_reproduce_proie;
	extern float p_reproduce_predateur;
	extern int temps_repousse_herbe;*/
//Et j'ai initialiser les variables suivants dans le ecosys.c,et donc on peut modifier les variables globaux dans le ecosys.c
	/*double p_ch_dir=0.01;
	float p_reproduce_proie=0.4;
	float p_reproduce_predateur=0.5;
	int temps_repousse_herbe=-15; */

int main(void) {
    // Initialiation du generateurs de nombre aleatoires
    srand(time(NULL));
    
  /* A completer. Part 2: exercice 4, questions 1 et 2*/
    // Test de la fonction de déplacement
    Animal *animal = creer_animal(3, 4, 10); // Crée un animal à la position (3, 4) avec 10 d'énergie
    printf("Position initiale de l'animal : (%d, %d)\n", animal->x, animal->y);
    afficher_ecosys(animal, NULL);
    // Déplace l'animal
    bouger_animaux(animal);
    
    printf("Position après déplacement : (%d, %d)\n", animal->x, animal->y);
    afficher_ecosys(animal, NULL);

    // Test de la fonction de reproduction
    printf("\nTest de la reproduction :\n");
    printf("Nombre d'animaux avant la reproduction : %d\n", compte_animal_it(animal));

    reproduce(&animal, 1); // Taux de reproduction de 1 (tous les animaux se reproduisent)

    printf("Nombre d'animaux après la reproduction : %d\n", compte_animal_it(animal));

    // Libération de la mémoire
    liberer_liste_animaux(animal);
    
    printf("\n");
    printf("===========================================================================\n");
    printf("\n");
		
    /* exercice 5, question 2 & exercice 6, question 3 */
    int energie=10;
    Animal *liste_proies = NULL;
    Animal *liste_predateurs = NULL;
    /* exercice 7, question 1 */
    int monde[SIZE_X][SIZE_Y] = {0};// Déclarer et initialiser le tableau monde
    
    // Création de NB_PROIES proies
    for (int i = 0; i < NB_PROIES; i++) {
      ajouter_animal(rand() % SIZE_X, rand() % SIZE_Y, 10, &liste_proies);
    }
	
    // Création de NB_PREDATEURS prédateurs
    for (int i = 0; i < NB_PREDATEURS; i++) {
      ajouter_animal(rand() % SIZE_X, rand() % SIZE_Y, 10, &liste_predateurs);
    }
    
    /* exercice 8, question 1 */
    FILE *file = fopen("Evol_Pop.txt", "w"); // Ouvrir un ficher pour ecrire
    int iteration = 0;
    fprintf(file, "%d %d %d\n", iteration, compte_animal_rec(liste_proies), compte_animal_rec(liste_predateurs));
    iteration += 1;
    
    // Boucle while termine quand il y a pas les proies ou quand le fois d'iteration arrvier a 200
    while (liste_proies && iteration < iteration_max) {
    	
    	printf("Numero d'iteration %d\n",iteration);
    	// Afficher l'écosystème
    	afficher_ecosys(liste_proies, liste_predateurs);
    	
        // Mettre à jour le monde
        rafraichir_monde(monde);
    	
        // Mettre à jour les proies
        rafraichir_proies(&liste_proies, monde);

        // Mettre à jour les prédateurs (à implémenter)
        rafraichir_predateurs(&liste_predateurs, &liste_proies);

        // Ecrire la nombre de population dans le fichier
        fprintf(file, "%d %d %d\n", iteration, compte_animal_rec(liste_proies), compte_animal_rec(liste_predateurs));
        iteration++;

        // Pause de T_WAIT microseconds
        usleep(T_WAIT);
    }

    fclose(file); // Fermeture du fichier

    // Free le mémoire si besion
    liberer_liste_animaux(liste_proies);
    liberer_liste_animaux(liste_predateurs);

  return 0;
}

