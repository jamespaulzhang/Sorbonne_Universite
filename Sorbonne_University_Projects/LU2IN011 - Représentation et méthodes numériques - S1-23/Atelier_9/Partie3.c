#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


void gauss(double *a, double *b, int n) {
    int i, j, k, il;
    double aux, aux2;

    for (i = 0; i < n - 1; i++) {
        aux = a[i * n + i];
        for (k = i + 1; k < n; k++)
            a[i * n + k] /= aux;
        b[i] /= aux;

        for (k = i + 1; k < n; k++) {
            aux2 = a[k * n + i];
            for (j = i + 1; j < n; j++)
                a[k * n + j] -= aux2 * a[i * n + j];
            b[k] -= aux2 * b[i];
        }
    }

    // Rétro-substitution
    for (i = n - 1; i >= 0; i--) {
        for (il = i - 1; il >= 0; il--) {
            b[il] -= b[i] * a[il * n + i];
        }
    }
}


void interpol_linalg(double *a, double *f_a, int n, double *coeff_f) {
    // Vérifier si les pointeurs sont valides
    if (a == NULL || coeff_f == NULL) {
        printf("Erreur : pointeurs invalides\n");
        return;
    }

    // Vérifier si n est valide
    if (n < 0) {
        printf("Erreur : degré invalide\n");
        return;
    }

    // Construire la matrice du système linéaire
    int m = n + 1; // Nombre d'équations
    double *matrix_A = (double *)malloc(m * (n + 1) * sizeof(double));
    for (int i = 0; i < m; i++) {
        double current_a = 1.0;
        for (int j = 0; j <= n; j++) {
            matrix_A[i * (n + 1) + j] = current_a;
            current_a *= a[i];
        }
    }

    // Construire le vecteur colonne B
    double *vector_B = (double *)malloc(m * sizeof(double));
    for (int i = 0; i < m; i++) {
        vector_B[i] = f_a[i];
    }

    // Appliquer la méthode de Gauss pour résoudre le système linéaire
    gauss(matrix_A, vector_B, m);

    // Copier les coefficients résultants dans le tableau coeff_f
    for (int i = 0; i <= n; i++) {
        coeff_f[i] = vector_B[i];
    }

    // Libérer la mémoire allouée
    free(matrix_A);
    free(vector_B);
}

void interpol_Lagrange(double *a, double *f_a, int n, double *coeff_f) {
    // Vérifier si les pointeurs sont valides
    if (a == NULL || coeff_f == NULL) {
        printf("Erreur : pointeurs invalides\n");
        return;
    }

    // Vérifier si n est valide
    if (n < 0) {
        printf("Erreur : degré invalide\n");
        return;
    }

    // Initialiser les coefficients à zéro
    for (int i = 0; i <= n; i++) {
        coeff_f[i] = 0.0;
    }

    // Calculer les coefficients du polynôme interpolateur de Lagrange
    for (int i = 0; i <= n; i++) {
        double term = f_a[i];

        for (int j = 0; j <= n; j++) {
            if (j != i) {
                term *= 1.0 / (a[i] - a[j]);
            }
        }

        coeff_f[i] = term;
    }
}

int main() {
    const int max_degree = 16;
    srand(time(NULL));

    for (int i = 0; i <= max_degree; i++) {
        int n = 2 * i;

        // Générer des entrées aléatoires dans [−1, 1]
        double a[n + 1];
        double f_a[n + 1];

        for (int j = 0; j <= n; j++) {
            a[j] = (double)rand() / RAND_MAX * 2.0 - 1.0;
            f_a[j] = (double)rand() / RAND_MAX * 2.0 - 1.0;
        }

        // Mesurer le temps d'exécution pour interpol_linalg
        clock_t start_time_linalg = clock();
        double coeff_f_linalg[n + 1];
        interpol_linalg(a, f_a, n, coeff_f_linalg);
        clock_t end_time_linalg = clock();

        // Mesurer le temps d'exécution pour interpol_Lagrange
        clock_t start_time_Lagrange = clock();
        double coeff_f_Lagrange[n + 1];
        interpol_Lagrange(a, f_a, n, coeff_f_Lagrange);
        clock_t end_time_Lagrange = clock();

        // Afficher les résultats
        printf("Degré %d:\n", n);

        printf("interpol_linalg : ");
        for (int j = 0; j <= n; j++) {
            printf("%.2f ", coeff_f_linalg[j]);
        }
        printf("\n");

        printf("interpol_Lagrange : ");
        for (int j = 0; j <= n; j++) {
            printf("%.2f ", coeff_f_Lagrange[j]);
        }
        printf("\n");

        // Calculer les temps d'exécution en secondes
        double time_linalg = ((double)(end_time_linalg - start_time_linalg)) / CLOCKS_PER_SEC;
        double time_Lagrange = ((double)(end_time_Lagrange - start_time_Lagrange)) / CLOCKS_PER_SEC;

        printf("Temps d'exécution interpol_linalg : %.10lf secondes\n", time_linalg);
        printf("Temps d'exécution interpol_Lagrange : %.10lf secondes\n", time_Lagrange);

        printf("\n");
    }

    return 0;
}

/* 

En conclusion, les différences observées entre `interpol_linalg` et `interpol_Lagrange` en termes de précision et de rapidité peuvent être expliquées par les méthodes numériques spécifiques utilisées dans chaque fonction.

1. **Précision :**
   - **`interpol_linalg` (Gauss/Moindres carrés) :** La méthode des moindres carrés peut être sensible aux erreurs numériques, en particulier pour des polynômes de degrés élevés. La construction de la matrice du système linéaire et la résolution du système peuvent introduire des erreurs d'approximation.
   - **`interpol_Lagrange` (Méthode de Lagrange) :** En utilisant directement la formule mathématique du polynôme interpolateur de Lagrange, cette méthode évite la résolution d'un système linéaire, réduisant ainsi les erreurs numériques potentielles.

2. **Rapidité :**
   - **`interpol_linalg` :** La méthode des moindres carrés implique la construction d'une matrice et la résolution d'un système linéaire, opérations potentiellement coûteuses en termes de temps de calcul, surtout pour des polynômes de degrés élevés.
   - **`interpol_Lagrange` :** En effectuant des calculs directs sans la nécessité de résoudre un système linéaire, la méthode de Lagrange peut être plus rapide, nécessitant moins d'itérations.

Bien que la méthode de Lagrange puisse offrir une précision supérieure et une exécution plus rapide dans certains cas, le choix entre les deux dépend des exigences spécifiques du problème, de la nature des données d'entrée, et des compromis entre précision et rapidité. La méthode de Lagrange est souvent préférable dans des contextes où la stabilité numérique est cruciale, tandis que la méthode des moindres carrés peut être utilisée efficacement dans d'autres situations.

*/
