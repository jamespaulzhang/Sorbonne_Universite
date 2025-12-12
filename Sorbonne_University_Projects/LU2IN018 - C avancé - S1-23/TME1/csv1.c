#include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* Exercice 1 */
/* Q1 */
int compte_mots_chaine(char *chaine){
    int nb_mots = 0;
    while(*chaine){
        if (*chaine == ' '){
            chaine ++;
            continue;
        }
        nb_mots ++;
        while(*chaine != ' ' && *chaine != '\0'){
            chaine++;
        }
    }
    return nb_mots;
}

/* Q2 */
int compte_mots(char **ptab_mots){
    int cpt = 0;
    while(ptab_mots[cpt]) {
        cpt++;
    }
    return cpt;
}

/* Q3 */
void affiche_tab_mots(char **ptab_mots)
{
  int nb_mots = 0;
  while(ptab_mots[nb_mots]) {
    printf("%s\t", ptab_mots[nb_mots]);
    nb_mots++;
  }
  printf("\n");
}

/* Q4 */
char *compose_chaine(char **ptab_mots)
{
  int ind_mot = 0;
  int taille = 1;
  char *pc, *tmp_pc, *pmot;

  for(ind_mot = 0; ptab_mots[ind_mot] != NULL; ind_mot++) {
    taille += strlen(ptab_mots[ind_mot]) + 1;
  }

  pc = (char *)malloc(taille * sizeof(char));
  pc[taille] = 0;

  ind_mot = 0;
  tmp_pc = pc;
  while(ptab_mots[ind_mot]) {
    pmot = ptab_mots[ind_mot];
    while(*pmot) {
      *(tmp_pc ++) = *(pmot ++);
    }
    *(tmp_pc++) = ' ';
    ind_mot ++;
  }
  return pc;
}

/* Q5 */
void detruit_tab_mots(char **ptab_mots)
{
  int i=0;
  if (ptab_mots){
    while(ptab_mots[i]){
       free(ptab_mots[i++]); 
    }
  }
  free(ptab_mots);
}

/* Exercice 2 */
/* Q1 */
char **reduit_tab_mots(char **ptab_mots)
{
  char **ptab;
  int nb_mots = compte_mots(ptab_mots);
  ptab = malloc((nb_mots + 1) * sizeof(char *));
  ptab[nb_mots] = NULL;
  for(int num_ptab_mots = 0; ptab_mots[num_ptab_mots] != NULL; num_ptab_mots++) {
    int repete = 0;
    int flag = 0;
    for(int num_ptab = 0; ptab[num_ptab] != NULL; num_ptab++) {
      if(ptab_mots[num_ptab_mots] == ptab[num_ptab]) {
        repete += 1;
        flag = num_ptab;
        break;
      }
    }
    if(repete == 0) {
      ptab[num_ptab_mots] = ptab_mots[num_ptab_mots];
    }else {
      ptab[num_ptab_mots] = ptab[flag];
    }
  }
  return ptab;
}

int main(void){
    char *chaine = {"  mot1  et mot2 et mot3"};
    char *ptabmots[] = {"mot1","et","mot2","et","mot3",NULL};
    printf("Il y a %d mots dans ce chaine de charactere\n",compte_mots_chaine(chaine));
    printf("Il y a %d mots dans ce tableau\n",compte_mots(ptabmots));
    //printf("Afficher les mots dans le tableau:  ");
    affiche_tab_mots(ptabmots);
    printf("%s",compose_chaine(ptabmots));
    return 0;
}