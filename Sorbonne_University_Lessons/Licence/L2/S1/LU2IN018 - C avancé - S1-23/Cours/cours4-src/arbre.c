#include <stdio.h>
#include <stdlib.h>

#include "arbre.h"
#include "pile.h"
#include "file.h"

P_un_noeud creer_noeud(int data) {
  P_un_noeud p=(P_un_noeud)malloc(sizeof(Un_noeud));
  if (p==NULL) {
    fprintf(stderr,"Erreur lors de l'allocation d'un noeud\n");
    return NULL;
  }
  p->data=data;
  p->gauche=NULL;
  p->droit=NULL;
  return p;
}

P_un_noeud ajouter_racine(int data, P_un_noeud abg, P_un_noeud abd) {
  P_un_noeud r=creer_noeud(data);
  r->gauche=abg;
  r->droit=abd;
  return r;
}


void detruire_noeud(P_un_noeud p) {
  free(p);
}

void detruire_arbre(P_un_noeud a) {
  if (a!=NULL) {
    detruire_arbre(a->gauche);
    detruire_arbre(a->droit);
    detruire_noeud(a);
  }
}

void afficher_arbre(P_un_noeud a) {
  if (a) {
    printf("( %d ",a->data);
    afficher_arbre(a->gauche);
    afficher_arbre(a->droit);
    printf(")");
  }
}

void aff_prof_prefixe(P_un_noeud a) {

  if (a) {
    printf(" %d",a->data);
    aff_prof_prefixe(a->gauche);
    aff_prof_prefixe(a->droit);
  }
}

void aff_prof_infixe(P_un_noeud a) {

  if (a) {
    aff_prof_infixe(a->gauche);
    printf(" %d",a->data);
    aff_prof_infixe(a->droit);
  }
}

void aff_prof_postfixe(P_un_noeud a) {

  if (a) {
    aff_prof_postfixe(a->gauche);
    aff_prof_postfixe(a->droit);
    printf(" %d",a->data);
  }
}

void aff_prof_prefixe_iteratif(P_un_noeud a) {
  P_un_noeud p = a; 
  T_pile pile = NULL;
  if (p) {
    pile=push_p(pile, p);
    do
      {
        pile=pop_p(pile , &p); 
        printf("%d ", p->data); 
        if(p->droit) {
          pile=push_p(pile, p->droit);
        }
        if(p->gauche){
          pile=push_p(pile, p->gauche);
        }
      }
    while(pile); 
  }
}

void aff_largeur_iteratif(P_un_noeud a) 
{
  P_un_noeud p = a; 
  T_file fifo = NULL;
  if (p) {
    fifo=push_f( fifo , p);
    do
      {
        fifo=pop_f(fifo , &p); 
        printf("%d ", p->data); 
        if(p->gauche) {
          fifo=push_f(fifo , p->gauche);
        }
        if(p->droit) {
          fifo=push_f(fifo, p->droit);
        }
      }
    while(fifo); 
  }
}

