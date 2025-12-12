/* Diffusion tampon N case */

#include <stdio.h> 
#include <unistd.h> 
#include <signal.h> 
#include <libipc.h>

/************************************************************/

/* definition des parametres */ 

#define NE 2     /*  Nombre d'emetteurs         */ 
#define NR 5     /*  Nombre de recepteurs       */ 
#define NMAX 3     /*  Taille du tampon           */ 

/************************************************************/

/* definition des semaphores */ 

int mutex_e;      // Mutex pour synchroniser l'écriture
int mutex_r;      // Mutex pour synchroniser la lecture
int vide;         // Nombre de cases vides
int plein;        // Nombre de cases pleines


/************************************************************/

/* definition de la memoire partagee */ 

struct {
	int messages[NMAX];
    int nb_recepteurs[NMAX];
	int index_ecriture;
	int index_lecture;
}*sp;

/************************************************************/

/* variables globales */ 
int emet_pid[NE], recep_pid[NR]; 

/************************************************************/

/* traitement de Ctrl-C */ 

void handle_sigint(int sig) { 
	int i;
  	for (i = 0; i < NE; i++) kill(emet_pid[i], SIGKILL); 
	for (i = 0; i < NR; i++) kill(recep_pid[i], SIGKILL); 
	det_sem(); 
	det_shm((char *)sp); 
    exit(0);
} 

/************************************************************/

/* fonction EMETTEUR */ 

void emetteur() {
	while (1) {
		P(vide);       // Attente d'une case vide
		P(mutex_e);      // Accès exclusif à l'écriture
			
		sp->messages[sp->index_ecriture] = rand() % 100;
        sp->nb_recepteurs[sp->index_ecriture] = 0;
        printf("Émetteur %d a envoyé %d dans la case %d\n", getpid(), sp->messages[sp->index_ecriture], sp->index_ecriture);
		sp->index_ecriture = (sp->index_ecriture + 1) % NMAX;
			
		V(mutex_e);
		V(plein);      // Signal qu'une case est pleine
	}
}

/************************************************************/

/* fonction RECEPTEUR */ 

void recepteur(int id) {
    while (1) {
        P(plein);      // Attente d'une case pleine
        P(mutex_r);      // Accès exclusif à la lecture

        printf("Recepteur %d a reçu %d de la case %d\n", getpid(), sp->messages[sp->index_lecture], sp->index_lecture);
        sp->nb_recepteurs[sp->index_lecture]++;

        if (sp->nb_recepteurs[sp->index_lecture] == NR) {
            sp->nb_recepteurs[sp->index_lecture] = 0; // Réinitialisation du compteur
            sp->index_lecture = (sp->index_lecture + 1) % NMAX;
            V(vide);
        }
        V(mutex_r);       // Signal qu'une case est vide
    }
}

/************************************************************/

int main() { 
    struct sigaction action;
	/* autres variables (a completer) */
    
    setbuf(stdout, NULL);

/* Creation du segment de memoire partagee */

	sp = init_shm(sizeof(*sp));
    if (!sp) {
        perror("Erreur allocation mémoire partagée");
        exit(1);
    }

    sp->index_ecriture = 0;
    sp->index_lecture = 0;
    for (int i = 0; i < NMAX; i++) {
        sp->nb_recepteurs[i] = 0;
    }

/* creation des semaphores */ 

	mutex_e = creer_sem(1);
    mutex_r = creer_sem(1);
    vide = creer_sem(1);
    plein = creer_sem(1);

/* initialisation des semaphores */ 

    init_un_sem(mutex_e, 1);
    init_un_sem(mutex_r, 1);
    init_un_sem(vide, NMAX); // NMAX cases vides
    init_un_sem(plein, 0);   // Aucune case pleine au début
    
/* creation des processus emetteurs */ 

	for (int i = 0; i < NE; i++) {
        if ((emet_pid[i] = fork()) == 0) {
            emetteur();
            exit(0);
        }
    }

/* creation des processus recepteurs */ 

	for (int i = 0; i < NR; i++) {
    	if ((recep_pid[i] = fork()) == 0) {
            recepteur(i);
            exit(0);
        }
    }
    
/* redefinition du traitement de Ctrl-C pour arreter le programme */ 

    sigemptyset(&action.sa_mask);
    action.sa_flags = 0;
    action.sa_handler = handle_sigint;
    sigaction(SIGINT, &action, 0); 

    pause();                     /* attente du Ctrl-C */
    return EXIT_SUCCESS;
}