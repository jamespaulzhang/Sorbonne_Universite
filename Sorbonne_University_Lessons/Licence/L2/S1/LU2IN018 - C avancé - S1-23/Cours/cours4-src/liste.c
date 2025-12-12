#include <stdio.h>
#include <stdlib.h>

#include "liste.h"


P_un_elem creer_elem(P_un_noeud d) {
  P_un_elem pe=(P_un_elem) malloc(sizeof(Un_elem));
  if (pe ==NULL) {
    fprintf(stderr,"Erreur lors de l'allocation d'un element de liste.\n");
    return NULL;
  }
  pe->data=d;
  pe->suivant=NULL;
  return pe;
}

void detruire_elem(P_un_elem p) {
  free(p);
}

P_un_elem insertion_tete(P_un_elem liste,P_un_elem elt) {
  elt->suivant=liste;
  return elt;
}

P_un_elem insertion_queue(P_un_elem liste, P_un_elem elt) {
  if (liste==NULL) {
    return elt;
  }

  P_un_elem tmp=liste;
  
  while(tmp->suivant!=NULL) {
    tmp=tmp->suivant;
  }
  tmp->suivant=elt;
  return liste;
}

P_un_elem extraction_tete(P_un_elem liste, P_un_elem *pelt) {
  /* on ne libere pas la memoire, ce sera a l'appelant de le faire si besoin */
  *pelt=liste;
  if (liste==NULL) {
    return NULL;
  }
  return liste->suivant;
}

P_un_elem extraction_queue(P_un_elem liste, P_un_elem *pelt) {
  /* on ne libere pas la memoire, ce sera a l'appelant de le faire si besoin */

  if (liste==NULL) {
    *pelt=NULL;
    return NULL;
  }

  P_un_elem tmp=liste;

  if(tmp->suivant==NULL) {
    *pelt=tmp;
    return NULL;
  }

  while(tmp->suivant->suivant) {
    tmp=tmp->suivant;
  }
  
  *pelt=tmp->suivant;
  tmp->suivant=NULL;

  return liste;

}
