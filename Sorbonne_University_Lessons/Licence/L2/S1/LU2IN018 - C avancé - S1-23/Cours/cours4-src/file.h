#ifndef _FILE_H_
#define _FILE_H_

#include "liste.h"
#include "arbre.h"

typedef P_un_elem T_file;

T_file push_f(T_file p, P_un_noeud d);
T_file pop_f(T_file p, P_un_noeud *pd);


#endif
