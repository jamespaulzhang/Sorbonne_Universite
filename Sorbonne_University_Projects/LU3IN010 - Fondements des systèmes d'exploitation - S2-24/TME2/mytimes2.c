#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/times.h>  // Pour times()
#include <unistd.h>  // Pour sysconf et _SC_CLK_TCK

void lance_commande(char *commande) {
    struct tms start_time, end_time;
    clock_t start_clock, end_clock;
    long ticks_per_sec = sysconf(_SC_CLK_TCK);  // Récupération des ticks par seconde

    // Récupérer l'heure avant l'exécution de la commande
    start_clock = times(&start_time);

    // Exécution de la commande avec system()
    int resultat = system(commande);

    // Récupérer l'heure après l'exécution de la commande
    end_clock = times(&end_time);

    if (resultat == -1) {
        // Si system() échoue
        printf("Erreur lors de l'exécution de la commande : %s\n", commande);
    }

    // Calcul des temps d'exécution
    double total_time_sec = (double)(end_clock - start_clock) / ticks_per_sec;
    double user_time_sec = (double)(end_time.tms_utime - start_time.tms_utime) / ticks_per_sec;
    double system_time_sec = (double)(end_time.tms_stime - start_time.tms_stime) / ticks_per_sec;
    double child_user_time_sec = (double)(end_time.tms_cutime - start_time.tms_cutime) / ticks_per_sec;
    double child_system_time_sec = (double)(end_time.tms_cstime - start_time.tms_cstime) / ticks_per_sec;

    // Affichage des statistiques
    printf("Statistiques de \"%s\" :\n", commande);
    printf("Temps total : %.6f\n", total_time_sec);
    printf("Temps utilisateur : %.6f\n", user_time_sec);
    printf("Temps systeme : %.6f\n", system_time_sec);
    printf("Temps utilisateur fils : %.6f\n", child_user_time_sec);
    printf("Temps systeme fils : %.6f\n", child_system_time_sec);
    printf("\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Aucune commande n'a été fournie.\n");
        return 1;
    }

    // Parcourir tous les arguments (à partir de argv[1] jusqu'à argv[argc-1])
    for (int i = 1; i < argc; i++) {
        printf("Exécution de la commande : %s\n", argv[i]);
        lance_commande(argv[i]);
    }

    return 0;
}
