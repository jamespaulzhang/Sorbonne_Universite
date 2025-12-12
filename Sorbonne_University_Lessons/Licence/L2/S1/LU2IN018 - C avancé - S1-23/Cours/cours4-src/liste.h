#ifndef _LISTE_H_
#define _LISTE_H_

#include "arbre.h"

typedef struct _un_elem * P_un_elem;
typedef struct _un_elem {
  P_un_noeud data;
  P_un_elem suivant;
} Un_elem;

P_un_elem creer_elem(P_un_noeud d);
void detruire_elem(P_un_elem p);

P_un_elem insertion_tete(P_un_elem liste,P_un_elem elt);

P_un_elem insertion_queue(P_un_elem liste, P_un_elem elt);

P_un_elem extraction_tete(P_un_elem liste, P_un_elem *pelt);

P_un_elem extraction_queue(P_un_elem liste, P_un_elem *pelt);

#endif
