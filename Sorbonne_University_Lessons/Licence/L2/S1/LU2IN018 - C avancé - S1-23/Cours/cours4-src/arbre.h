#ifndef _ARBRE_H_
#define _ARBRE_H_

typedef struct _un_noeud *P_un_noeud;
typedef struct _un_noeud {
  int data;
  P_un_noeud gauche;
  P_un_noeud droit;
} Un_noeud;

P_un_noeud creer_noeud(int data);
P_un_noeud ajouter_racine(int data, P_un_noeud abg, P_un_noeud abd);
void detruire_noeud(P_un_noeud p);
void detruire_arbre(P_un_noeud a);
void afficher_arbre(P_un_noeud a);


void aff_prof_prefixe(P_un_noeud a);
void aff_prof_infixe(P_un_noeud a);
void aff_prof_postfixe(P_un_noeud a);

void aff_prof_prefixe_iteratif(P_un_noeud a);
void aff_largeur_iteratif(P_un_noeud a);

#endif
