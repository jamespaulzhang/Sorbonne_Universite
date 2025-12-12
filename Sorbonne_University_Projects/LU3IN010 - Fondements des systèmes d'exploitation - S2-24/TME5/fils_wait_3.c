#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/times.h>

#define MAX_CMD 100
#define MAX_ARGS 10

int main() {
    char commande[MAX_CMD];

    while (1) {
        printf("Entrez une commande : ");
        if (fgets(commande, MAX_CMD, stdin) == NULL) {
            perror("Erreur de lecture");
            continue;
        }

        // Supprimer le saut de ligne ajouté par fgets()
        commande[strcspn(commande, "\n")] = 0;

        if (strcmp(commande, "quit") == 0) {
            break;
        }

        int attendre = 1;
        int len = strlen(commande);
        if (len > 0 && commande[len - 1] == '&') {
            attendre = 0;
            commande[len - 1] = '\0'; // Supprimer le '&' de la commande
        }

        // Découper la commande et ses arguments
        char *args[MAX_ARGS];
        char *token = strtok(commande, " ");
        int i = 0;

        while (token != NULL && i < MAX_ARGS - 1) {
            args[i++] = token;
            token = strtok(NULL, " ");
        }
        args[i] = NULL; // Dernier élément NULL pour execvp

        struct tms start_time, end_time;
        clock_t start, end;

        start = times(&start_time);

        pid_t pid = fork();
        if (pid < 0) {
            perror("Erreur de fork");
            continue;
        }

        if (pid == 0) {
            execvp(args[0], args);
            perror("Erreur d'exécution");
            exit(1);
        }

        if (attendre) {
            waitpid(pid, NULL, 0);
            end = times(&end_time);

            double tps_utilisateur = (double)(end_time.tms_cutime - start_time.tms_cutime) / sysconf(_SC_CLK_TCK);
            double tps_systeme = (double)(end_time.tms_cstime - start_time.tms_cstime) / sysconf(_SC_CLK_TCK);

            printf("\nTemps utilisateur : %f s\n", tps_utilisateur);
            printf("Temps système : %f s\n\n", tps_systeme);
        }
    }

    return 0;
}
