#ifndef _PILE_H_
#define _PILE_H_

#include "liste.h"

typedef P_un_elem T_pile;

T_pile push_p(T_pile p, P_un_noeud d);
T_pile pop_p(T_pile p, P_un_noeud *pd);

#endif
