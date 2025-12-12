#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int compte_mots_chaine(char *chaine){
  int nb_mots =0;
  while (*chaine){
        if (*chaine == ' '){
                chaine++;
                continue;
        }
        nb_mots++;
        while (*chaine != ' ' && *chaine != '\0'){
                chaine++;
        }
  }
  return nb_mots;
}

char **decompose_chaine(char *chaine){

  char *pc= chaine;
  int nb_mots=0;
  char **ptab;
  char *psrc_mot;
  int ind_mot=0;

  //comptages des mots
  nb_mots=compte_mots_chaine(chaine);

  if (nb_mots == 0)
    return NULL;
  // allocation du tableau

  ptab = malloc((nb_mots + 1) * sizeof(char *));
  ptab[nb_mots] = NULL;

  // copie des mots

  pc=chaine;
  while (*pc)
    {
      if(*pc == ' ')
        {
          pc++;
          continue;
 }

      psrc_mot = pc;

      while((*pc != ' ') && (*pc)) pc++;

      //allocation du mot
      ptab[ind_mot] = malloc((pc - psrc_mot + 1)* sizeof(char));
      //copie du mot
      memcpy(ptab[ind_mot], psrc_mot, pc - psrc_mot);
      //insertion du marqueur de fin de chaine
      *(ptab[ind_mot] + (pc - psrc_mot)) = '\0';

      ind_mot++;
    }


  return ptab;
}

char *compose_chaine(char **ptab_mots){
        char** chnrec = malloc(compte_mots(ptab_mots)*sizeof(char*));
        for (int i=0; i<compte_mots(ptab_mots); i++){
                if (ptab_mots[i]==ptab_mots[i+1]==' '){
                        continue;
                }
                else{
                        chnrec[i] = ptab_mots[i];
                }
        }
        return chnrec[0];
}

void detruit_tab_mots(char **ptab_mots)
{

  /* Fonction vue en TD, exercice 2, question 5 */

  int i=0;

  if (ptab_mots)
    while(ptab_mots[i])
 free(ptab_mots[i++]);

  free(ptab_mots);
}

int compte_mots(char **ptab_mots){
        int nb_mots = 0;
        while (ptab_mots[nb_mots]){
                nb_mots++;
        }
        return nb_mots;
}

void affiche_tab_mots(char **ptab_mots){
        int nb_mots = 0;
        while (ptab_mots[nb_mots]){
                printf("mot d'indice %d : %s\n", nb_mots, ptab_mots[nb_mots]);
                nb_mots++;
        }
}

char **reduit_tab_mots(char **ptab_mots)
{
  /* a completer exercice 4, question 1 */
}

int main() {
        char* chn = "je suis Antoine";
        printf("nombre de mots dans la chaîne : %d\n", compte_mots_chaine(chn));

        char* tab[6] = {"mot1", "et", "mot2", "et", "mot3", NULL};
        printf("nombre de mots dans le tableau : %d\n", compte_mots(tab));

        affiche_tab_mots(tab);

        printf("%s\n", compose_chaine(tab));

  /* a completer:
   * exercice 3, question 3, 5
   * exercice 4, question 1
   */
    return 1;
}