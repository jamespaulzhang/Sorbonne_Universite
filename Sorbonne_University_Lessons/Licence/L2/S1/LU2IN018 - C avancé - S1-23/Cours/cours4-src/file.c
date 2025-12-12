#include <stdlib.h>
#include "file.h"

T_file push_f(T_file p, P_un_noeud d) {
  return insertion_queue(p,creer_elem(d));
}

T_file pop_f(T_file p, P_un_noeud *pd) {
  P_un_elem tmp=NULL;
  p=extraction_tete(p,&tmp);
  *pd=tmp->data;
  detruire_elem(tmp);
  return p;
}
