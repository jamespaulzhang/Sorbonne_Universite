

#include <stdio.h>
#include "arbre.h"

int main(void) {
  P_un_noeud p5=creer_noeud(5);
  P_un_noeud p3=creer_noeud(3);
  P_un_noeud p1=creer_noeud(1);
  P_un_noeud p4=creer_noeud(4);
  P_un_noeud p7=creer_noeud(7);
  P_un_noeud p8=creer_noeud(8);
  P_un_noeud p9=creer_noeud(9);

  p5->gauche=p3;
  p5->droit=p8;

  p3->gauche=p1;
  p3->droit=p4;

  p8->gauche=p7;
  p8->droit=p9;

  printf("Affichage profondeur prefixe: ");
  aff_prof_prefixe(p5);
  printf("\n");

  printf("Affichage profondeur infixe: ");
  aff_prof_infixe(p5);
  printf("\n");

  printf("Affichage profondeur postfixe: ");
  aff_prof_postfixe(p5);
  printf("\n");

  printf("Affichage profondeur prefixe iteratif: ");
  aff_prof_prefixe_iteratif(p5);
  printf("\n");

  printf("Affichage largeur iteratif: ");
  aff_largeur_iteratif(p5);
  printf("\n");

  detruire_arbre(p5);

  return 0;
}
