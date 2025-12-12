#include <stdlib.h>
#include "liste.h"
#include "pile.h"


T_pile push_p(T_pile p, P_un_noeud d) {
  return insertion_tete(p,creer_elem(d));
}

T_pile pop_p(T_pile p, P_un_noeud *pd) {
  P_un_elem pe=NULL;
  p=extraction_tete(p,&pe);
  *pd=pe->data;
  detruire_elem(pe);
  return p;
}
