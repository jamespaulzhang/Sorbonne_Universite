#include <stdio.h> 
#include <unistd.h> 
#include <stdlib.h> 
#include <signal.h> 
#include <libipc.h>

/************************************************************/

/* Definition des parametres */ 
#define NE 2     /* Nombre d'emetteurs */ 
#define NR 5     /* Nombre de recepteurs */ 

/************************************************************/

/* Definition des semaphores */ 
int EMET;
int RECEP[NR];
int MUTEX;
        
/************************************************************/

/* Definition de la memoire partagee */ 
struct {
    int message;
    int nb_recepteurs;
} *sp;

/************************************************************/

/* Variables globales */ 
int emet_pid[NE], recep_pid[NR]; 

/************************************************************/

/* Traitement de Ctrl-C */ 
void handle_sigint(int sig) { 
    int i;
    for (i = 0; i < NE; i++) kill(emet_pid[i], SIGKILL); 
    for (i = 0; i < NR; i++) kill(recep_pid[i], SIGKILL); 
    det_sem(); 
    det_shm((char *)sp);
    exit(0);
} 

/************************************************************/

/* Fonction EMETTEUR */ 
void emetteur() {
    while (1) {
        P(EMET);
        sp->message = rand() % 100;
        sp->nb_recepteurs = 0;  // Réinitialisation du compteur
        printf("Émetteur %d a envoyé %d\n", getpid(), sp->message);

        // Signale tous les récepteurs
        for (int i = 0; i < NR; i++) {
            V(RECEP[i]);
        }
    }
}

/************************************************************/

/* Fonction RECEPTEUR */ 
void recepteur(int id) {
    while (1) {
        P(RECEP[id]);
        printf("Récepteur %d a reçu %d\n", getpid(), sp->message);
        
        P(MUTEX);
        sp->nb_recepteurs++;
        if (sp->nb_recepteurs == NR) {
            V(EMET); // L'émetteur peut envoyer un nouveau message
        }
        V(MUTEX);
    }
}

/************************************************************/

int main() { 
    struct sigaction action;
    setbuf(stdout, NULL);

    /* Creation du segment de memoire partagee */
    sp = init_shm(sizeof(*sp));
    if (!sp) {
        perror("Erreur allocation mémoire partagée");
        exit(1);
    }
    sp->nb_recepteurs = 0;

    /* Création et initialisation des sémaphores */ 
    EMET = creer_sem(1);
    init_un_sem(EMET, 1);
    MUTEX = creer_sem(1);
    init_un_sem(MUTEX, 1);

    for (int i = 0; i < NR; i++) {
        RECEP[i] = creer_sem(1);
        init_un_sem(RECEP[i], 0);
    }

    /* Création des processus émetteurs */ 
    for (int i = 0; i < NE; i++) {
        if ((emet_pid[i] = fork()) == 0) {
            emetteur();
            exit(0);
        }
    }

    /* Création des processus récepteurs */ 
    for (int i = 0; i < NR; i++) {
        if ((recep_pid[i] = fork()) == 0) {
            recepteur(i);
            exit(0);
        }
    }

    /* Redéfinition du traitement de Ctrl-C */ 
    sigemptyset(&action.sa_mask);
    action.sa_flags = 0;
    action.sa_handler = handle_sigint;
    sigaction(SIGINT, &action, 0); 

    pause();   /* Attente du Ctrl-C */
    return 0;
}