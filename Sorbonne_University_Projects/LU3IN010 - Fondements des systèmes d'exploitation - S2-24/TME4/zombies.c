#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid1, pid2;

    // Création du premier processus fils
    pid1 = fork();
    if (pid1 < 0) {
        perror("Erreur lors de la création du premier processus fils");
        exit(1);
    }
    if (pid1 == 0) {
        // Code du premier processus fils
        printf("Premier processus fils (PID: %d) en cours de terminaison.\n", getpid());
        exit(0);  // Le fils se termine immédiatement
    }

    // Création du second processus fils
    pid2 = fork();
    if (pid2 < 0) {
        perror("Erreur lors de la création du second processus fils");
        exit(1);
    }
    if (pid2 == 0) {
        // Code du second processus fils
        printf("Second processus fils (PID: %d) en cours de terminaison.\n", getpid());
        exit(0);  // Le fils se termine immédiatement
    }

    // Le processus parent dort pendant 10 secondes pour laisser les fils en état zombie
    printf("Les processus fils sont maintenant des zombies pendant 10 secondes.\n");
    sleep(10);

    int status;
    pid_t finished_pid = wait(&status);  // Récupère le premier fils terminé

    // Identifier quel fils s'est terminé en premier
    if (finished_pid == pid1) {
        printf("Le premier processus terminé est le FILS 1 (PID %d)\n", finished_pid);
    } else if (finished_pid == pid2) {
        printf("Le premier processus terminé est le FILS 2 (PID %d)\n", finished_pid);
    } else {
        printf("Un processus inconnu s'est terminé (PID %d)\n", finished_pid);
    }

    // Attendre le deuxième fils
    finished_pid = wait(&status);
    if (finished_pid == pid1) {
        printf("Le second processus terminé est le FILS 1 (PID %d)\n", finished_pid);
    } else if (finished_pid == pid2) {
        printf("Le second processus terminé est le FILS 2 (PID %d)\n", finished_pid);
    }

    printf("Tous les processus fils sont terminés.\n");

    return 0;
}
