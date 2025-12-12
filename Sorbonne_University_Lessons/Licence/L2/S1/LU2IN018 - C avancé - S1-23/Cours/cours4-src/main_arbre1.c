

#include <stdio.h>
#include "arbre.h"

int main(void) {
  P_un_noeud p1 = ajouter_racine(3, NULL, NULL);
  P_un_noeud p2 = ajouter_racine(4, NULL, NULL);
  P_un_noeud p3 = ajouter_racine(5, p1, p2);
  afficher_arbre(p3);
  printf("\n");
  detruire_arbre(p3);
  return 0;
}
