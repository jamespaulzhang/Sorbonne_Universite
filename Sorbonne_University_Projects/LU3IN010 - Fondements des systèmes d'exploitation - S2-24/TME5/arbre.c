#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

void creer_arbre(int niveau) {
    if (niveau == 0) {
        sleep(30);
        return;
    }

    pid_t gauche, droit;

    gauche = fork();
    if (gauche == 0) {
        creer_arbre(niveau - 1);
        sleep(30);
        exit(0);
    }

    droit = fork();
    if (droit == 0) {
        creer_arbre(niveau - 1);
        sleep(30);
        exit(0);
    }

    wait(NULL);
    wait(NULL);
}


int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <niveau>\n", argv[0]);
        return 1;
    }

    int L = atoi(argv[1]);
    if (L < 0) {
        fprintf(stderr, "Le niveau doit être un entier positif.\n");
        return 1;
    }

    creer_arbre(L);
    sleep(30);
    return 0;
}
