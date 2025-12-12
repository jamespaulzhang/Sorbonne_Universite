#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_CMD 100

int main() {
    char commande[MAX_CMD];
    while (1) {
        printf("Entrez une commande : ");
        if (fgets(commande, MAX_CMD, stdin) == NULL) {
            perror("Erreur de lecture");
            continue;
        }
        
        // Supprimer le saut de ligne
        commande[strcspn(commande, "\n")] = 0;
        
        // Vérifier si on doit quitter
        if (strcmp(commande, "quit") == 0) {
            break;
        }
        
        int attendre = 1;
        int len = strlen(commande);
        if (len > 0 && commande[len - 1] == '&') {
            attendre = 0;
            commande[len - 1] = '\0'; // Supprimer le '&' de la commande
        }
        
        pid_t pid = fork();
        if (pid < 0) {
            perror("Erreur de fork");
            continue;
        }
        
        if (pid == 0) {
            execlp(commande, commande, NULL);
            perror("Erreur d'exécution");
            exit(1);
        }
        
        if (attendre) {
            waitpid(pid, NULL, 0);
        }
    }
    return 0;
}
