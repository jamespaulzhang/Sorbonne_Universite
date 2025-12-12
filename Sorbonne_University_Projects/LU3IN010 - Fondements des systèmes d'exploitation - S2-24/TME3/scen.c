#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <malloc.h>
#include <sched.h>
#include <sys/time.h>

#define LONGTIME 8E8
void ProcLong(int *);
void ProcCourt(int *);

// Exemple de processus long (une simple bouble),
// Chaque processus long crée a son tour 4 processus courts
//
void ProcLong(int *pid) {
  long i;
  static int cpt = 0;

  for (i=0;i<LONGTIME;i++) {
    if (i%(long)(LONGTIME/4) == 0)  {
      int *tcpt = (int *) malloc(sizeof(int));
      *tcpt = cpt;
      CreateProc((function_t)ProcCourt,(void *)tcpt, 10);
      cpt++;
    }
    if (i%(long)(LONGTIME/100) == 0)
      printf("Proc. Long %d - %ld\n",*pid, i);
  }
  printf("############ FIN LONG %d\n\n", *pid );
}


// Processus court
void ProcCourt(int *pid) {
  long i;

  for (i=0;i<LONGTIME/10;i++)
    if (i%(long)(LONGTIME/100) == 0)
      printf("Proc. Court %d - %ld\n",*pid, i);
  printf("############ FIN COURT %d\n\n", *pid );
}




// Exemples de primitive d'election definie par l'utilisateur
// Remarques : les primitives d'election sont appelées directement
//             depuis la librairie. Elles ne sont appelées que si au
//             moins un processus est à l'etat pret (RUN)
//             Ces primitives manipulent la table globale des processus
//             définie dans sched.h


// Election aléatoire
int RandomElect(void) {
  int i;

  printf("RANDOM Election !\n");

  do {
    i = (int) ((float)MAXPROC*rand()/(RAND_MAX+1.0));
  } while (Tproc[i].flag != RUN);

  return i;
}


int SJFElect(void) {
  int i, p = -1;

  // Trouver le premier processus en état RUN
  for (i = 0; i < MAXPROC; i++) {
      if (Tproc[i].flag == RUN) {
          p = i;
          break;
      }
  }

  // Si aucun processus n'est en état RUN, retourner -1 (aucune élection possible)
  if (p == -1) {
      return -1;
  }

  // Parcourir les processus restants pour trouver celui avec la plus courte durée
  for (; i < MAXPROC; i++) {
      if (Tproc[i].flag == RUN && Tproc[i].duration < Tproc[p].duration) {
          p = i;
      }
  }

  return p;
}


// Approximation SJF
int ApproxSJF(void) {
    int i, p = -1;
    float priority, temp_priority;
    float coefficient = 1;  // Coefficient pour ajuster le vieillissement
    struct timeval current_time;  // Variable pour stocker l'heure actuelle

    // Obtenir l'heure actuelle
    gettimeofday(&current_time, NULL);

    priority = __FLT_MAX__;

    // Parcourir tous les processus
    for (i = 0; i < MAXPROC; i++) {
        if (Tproc[i].flag == RUN) {
            // Calcul du temps d'attente en utilisant la différence entre l'heure actuelle et le temps de début
            double waiting_time = (current_time.tv_sec - Tproc[i].realstart_time.tv_sec) +
                                  (current_time.tv_usec - Tproc[i].realstart_time.tv_usec) / 1000000.0;


            // Calcul de la priorité ajustée
            temp_priority = Tproc[i].ncpu - (coefficient * waiting_time);

            // Sélectionner le processus avec la plus petite priorité
            if (temp_priority < priority) {
                priority = temp_priority;
                p = i;
            }
        }
    }

    // Si aucun processus n'est trouvé, on retourne -1
    return p;
}


int main (int argc, char *argv[]) {
  int i;
  int *j;  

  // Créer les processus long
  for  (i = 0; i < 2; i++) {
    j = (int *) malloc(sizeof(int));
    *j= i;
    CreateProc((function_t)ProcLong,(void *)j, 80);
  }


  SchedParam(NEW, 0, SJFElect);

  // Lancer l'ordonnanceur en mode non "verbeux"
  sched(0);     

  // Imprimer les statistiques
  PrintStat();

  return EXIT_SUCCESS;

}
