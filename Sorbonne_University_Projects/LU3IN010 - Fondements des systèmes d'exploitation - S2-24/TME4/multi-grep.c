#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>  // Pour open()

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <motif> <fichier1> [fichier2 ...]\n", argv[0]);
        exit(1);
    }

    char *pattern = argv[1];
    int nb_fichiers = argc - 2;
    pid_t pids[nb_fichiers];

    for (int i = 0; i < nb_fichiers; i++) {
        pid_t pid = fork();

        if (pid < 0) {
            fprintf(stderr, "Échec de la création du processus.\n");
            exit(1);
        } else if (pid == 0) {
            close(STDOUT_FILENO);

            //pour seulement afficher dans la stdout l'état des processus terminés (redirection de la sortie standard)
            if (open("/dev/null", O_WRONLY) == -1) {
                perror("Erreur lors de l'ouverture de /dev/null");
                exit(1);
            }
            execl("/bin/grep", "grep", pattern, argv[i + 2], (char *)NULL);
            fprintf(stderr, "Impossible d'exécuter grep sur le fichier %s.\n", argv[i + 2]);
            exit(1);
        } else {
            pids[i] = pid;
        }
    }

    for (int i = 0; i < nb_fichiers; i++) {
        int status;
        if (waitpid(pids[i], &status, 0) == -1) {
            fprintf(stderr, "Problème lors de l'attente du processus %d.\n", pids[i]);
        } else {
            if (WIFEXITED(status)) {
                printf("Processus fils %d terminé avec le code %d\n", pids[i], WEXITSTATUS(status));
            } else {
                printf("Processus fils %d terminé de manière inattendue.\n", pids[i]);
            }
        }
    }

    return 0;
}
