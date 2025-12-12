#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sys/resource.h>

#define MAXFILS 1  // Nombre maximum de processus fils simultanés

void afficher_statistiques(pid_t pid, struct rusage *usage) {
    printf("Statistiques pour le processus fils %d :\n", pid);
    printf("  Temps CPU utilisateur : %ld.%06ld secondes\n", usage->ru_utime.tv_sec, usage->ru_utime.tv_usec);
    printf("  Temps CPU système   : %ld.%06ld secondes\n", usage->ru_stime.tv_sec, usage->ru_stime.tv_usec);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <motif> <fichier1> [fichier2 ...]\n", argv[0]);
        exit(1);
    }

    char *pattern = argv[1];
    int nb_fichiers = argc - 2;
    int fichiers_analyses = 0;
    int processus_actifs = 0;
    int prochain_fichier = 2;

    while (fichiers_analyses < nb_fichiers || processus_actifs > 0) {
        // Création de nouveaux processus si le nombre MAXFILS n'est pas atteint
        while (processus_actifs < MAXFILS && prochain_fichier < argc) {
            pid_t pid = fork();

            if (pid < 0) {
                fprintf(stderr, "Échec de la création du processus.\n");
                exit(1);
            } else if (pid == 0) {
                // Rediriger une nouvelle fois stdout vers /dev/null pour ne rien afficher comme dans l'exercice précédent
                close(STDOUT_FILENO);
                if (open("/dev/null", O_WRONLY) == -1) {
                    perror("Erreur lors de l'ouverture de /dev/null");
                    exit(1);
                }

                execl("/bin/grep", "grep", pattern, argv[prochain_fichier], (char *)NULL);
                fprintf(stderr, "Impossible d'exécuter grep sur le fichier %s.\n", argv[prochain_fichier]);
                exit(1);
            } else {
                processus_actifs++;
                prochain_fichier++;
            }
        }

        // Attente de la fin d'un processus fils
        int status;
        struct rusage usage;
        pid_t pid_termine = wait3(&status, 0, &usage);
        if (pid_termine == -1) {
            perror("wait3");
        } else {
            processus_actifs--;
            fichiers_analyses++;
            if (WIFEXITED(status)) {
                printf("Processus fils %d terminé avec le code %d\n", pid_termine, WEXITSTATUS(status));
            } else {
                printf("Processus fils %d terminé de manière inattendue.\n", pid_termine);
            }
            afficher_statistiques(pid_termine, &usage);
        }
    }

    return 0;
}
