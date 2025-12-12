#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double horner(double *a, double x, int n){
    double y;
    int i;
    y = a[n];
    for(i = n - 1; i >= 0; i--)
        y = y * x + a[i];
    return y;
}

void eval_Horner_1(double a, double* coeff_f, int n, double* f_a){
    // Vérifier si les coefficients sont valides
    if (coeff_f == NULL) {
        printf("Erreur : pointeur invalide\n");
        return;
    }

    // Vérifier si le degré du polynôme est valide
    if (n < 0) {
        printf("Erreur : degré du polynôme invalide\n");
        return;
    }

    // Utiliser la méthode de Horner pour évaluer le polynôme
    *f_a = horner(coeff_f, a, n);
}

double horner2(double *a, double x, int n)
{
    double yi, yp, x2;
    int i;
    x2 = x * x;
    if (n % 2 != 0){ // ou "if (n/2)" 
        yi = a[n]; yp = a[n - 1]; i = n - 2; 
    }else{ 
        yi = 0; yp = a[n]; i = n - 1; 
    }

    for(; i >= 0; i -= 2){
        yi = yi * x2 + a[i];
        yp = yp * x2 + a[i-1];
    }
    return yp + x * yi;
}

void eval_Horner_2(double a, double* coeff_f, int n, double* f_a, double* f_minus_a) {
    // Vérifier si les] coefficients sont valides
    if (coeff_f == NULL) {
        printf("Erreur : pointeur invalide\n");
        return;
    }

    // Vérifier si le degré du polynôme est valide
    if (n < 0) {
        printf("Erreur : degré du polynôme invalide\n");
        return;
    }

    // Utiliser la méthode de Horner2 pour évaluer le polynôme en a
    *f_a = horner2(coeff_f, a, n);

    // Utiliser la méthode de Horner2 pour évaluer le polynôme en -a
    *f_minus_a = horner2(coeff_f, -a, n);
}

void mulpol(double* coeff_f, int n, double* coeff_g, int p, double* coeff_h, int* q) {
    // Vérifier si les coefficients sont valides
    if (coeff_f == NULL || coeff_g == NULL || coeff_h == NULL || q == NULL) {
        printf("Erreur : pointeurs invalides\n");
        return;
    }

    // Vérifier si les degrés des polynômes sont valides
    if (n < 0 || p < 0) {
        printf("Erreur : degrés des polynômes invalides\n");
        return;
    }

    // Calculer le degré du polynôme résultant
    *q = n + p;

    // Initialiser le tableau des coefficients du polynôme résultant à zéro
    for (int i = 0; i <= *q; i++) {
        coeff_h[i] = 0.0;
    }

    // Calculer le produit des polynômes
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= p; j++) {
            coeff_h[i + j] += coeff_f[i] * coeff_g[j];
        }
    }
}

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

void multipointeval_Horner_1(double *a, double *coeff_f, int n, double *resultats, int m) {
    // Vérifier si les pointeurs sont valides
    if (a == NULL || coeff_f == NULL || resultats == NULL) {
        printf("Erreur : pointeurs invalides\n");
        return;
    }

    // Vérifier si n est valide
    if (n < 0) {
        printf("Erreur : degré invalide\n");
        return;
    }

    // Évaluer le polynôme aux points ±x1, …, ±xn en utilisant le schéma de Horner d'ordre 1
    for (int i = 0; i < m; i++) {
        eval_Horner_1(a[i], coeff_f, n, &resultats[i]);
    }
}

void multipointeval_Horner_2(double *a, double *coeff_f, int n, double *resultats, int m) {
    // Vérifier si les pointeurs sont valides
    if (a == NULL || coeff_f == NULL || resultats == NULL) {
        printf("Erreur : pointeurs invalides\n");
        return;
    }

    // Vérifier si n est valide
    if (n < 0) {
        printf("Erreur : degré invalide\n");
        return;
    }

    // Évaluer le polynôme aux points ±x1, …, ±xn en utilisant le schéma de Horner d'ordre 2
    for (int i = 0; i < m; i++) {
        double f_a, f_minus_a;
        eval_Horner_2(a[i], coeff_f, n, &f_a, &f_minus_a);
        resultats[i] = 0.5 * (f_a + f_minus_a);
    }
}

void multipointeval_linalg(double *a, double *coeff_f, int n, double *resultats, int m) {
    // Vérifier si les pointeurs sont valides
    if (a == NULL || coeff_f == NULL || resultats == NULL) {
        printf("Erreur : pointeurs invalides\n");
        return;
    }

    // Vérifier si n est valide
    if (n < 0) {
        printf("Erreur : degré invalide\n");
        return;
    }

    // Construire la matrice du système linéaire
    int system_size = n + 1;
    double *matrix_A = (double *)malloc(system_size * system_size * sizeof(double));
    for (int i = 0; i < system_size; i++) {
        double current_a = 1.0;
        for (int j = 0; j <= n; j++) {
            matrix_A[i * system_size + j] = current_a;
            current_a *= a[i];
        }
    }

    // Résoudre le système linéaire pour obtenir les coefficients du polynôme
    gauss(matrix_A, coeff_f, system_size);

    // Évaluer le polynôme aux points ±x1, …, ±xn en utilisant le produit de matrice vecteur
    for (int i = 0; i < m; i++) {
        double current_a = 1.0;
        resultats[i] = 0.0;

        for (int j = 0; j <= n; j++) {
            resultats[i] += current_a * coeff_f[j];
            current_a *= a[i];
        }
    }

    // Libérer la mémoire allouée
    free(matrix_A);
}

int main() {
    srand(time(NULL));  // Initialiser le générateur de nombres aléatoires

    for (int i = 0; i <= 16; i++) {
        int n = 2 * i;

        // Générer des entrées aléatoires pour a et coeff_f
        double *a = (double *)malloc((n + 1) * sizeof(double));
        double *coeff_f = (double *)malloc((n + 1) * sizeof(double));

        for (int j = 0; j <= n; j++) {
            a[j] = ((double)rand() / RAND_MAX) * 2.0 - 1.0;
            coeff_f[j] = ((double)rand() / RAND_MAX) * 2.0 - 1.0;
        }

        // Mesurer le temps d'exécution pour multipointeval_Horner_1
        clock_t start = clock();
        double *resultats1 = (double *)malloc((n + 1) * sizeof(double));
        multipointeval_Horner_1(a, coeff_f, n, resultats1, n + 1);
        clock_t end = clock();
        double time1 = ((double)(end - start)) / CLOCKS_PER_SEC;

        // Mesurer le temps d'exécution pour multipointeval_Horner_2
        start = clock();
        double *resultats2 = (double *)malloc((n + 1) * sizeof(double));
        multipointeval_Horner_2(a, coeff_f, n, resultats2, n + 1);
        end = clock();
        double time2 = ((double)(end - start)) / CLOCKS_PER_SEC;

        // Mesurer le temps d'exécution pour multipointeval_linalg
        start = clock();
        double *resultats3 = (double *)malloc((n + 1) * sizeof(double));
        multipointeval_linalg(a, coeff_f, n, resultats3, n + 1);
        end = clock();
        double time3 = ((double)(end - start)) / CLOCKS_PER_SEC;

        // Afficher les résultats
        printf("n = %d\tmultipointeval_Horner_1: %f s\tmultipointeval_Horner_2: %f s\tmultipointeval_linalg: %f s\n",n, time1, time2, time3);

        // Libérer la mémoire allouée
        free(a);
        free(coeff_f);
        free(resultats1);
        free(resultats2);
        free(resultats3);
    }

    return 0;
}

/* 

On a trouvé les résultat suivants:
n = 0	multipointeval_Horner_1: 0.000002 s	multipointeval_Horner_2: 0.000001 s	multipointeval_linalg: 0.000001 s
n = 2	multipointeval_Horner_1: 0.000001 s	multipointeval_Horner_2: 0.000001 s	multipointeval_linalg: 0.000002 s
n = 4	multipointeval_Horner_1: 0.000001 s	multipointeval_Horner_2: 0.000001 s	multipointeval_linalg: 0.000002 s
n = 6	multipointeval_Horner_1: 0.000001 s	multipointeval_Horner_2: 0.000002 s	multipointeval_linalg: 0.000002 s
n = 8	multipointeval_Horner_1: 0.000001 s	multipointeval_Horner_2: 0.000001 s	multipointeval_linalg: 0.000006 s
n = 10	multipointeval_Horner_1: 0.000002 s	multipointeval_Horner_2: 0.000002 s	multipointeval_linalg: 0.000005 s
n = 12	multipointeval_Horner_1: 0.000001 s	multipointeval_Horner_2: 0.000002 s	multipointeval_linalg: 0.000006 s
n = 14	multipointeval_Horner_1: 0.000002 s	multipointeval_Horner_2: 0.000003 s	multipointeval_linalg: 0.000013 s
n = 16	multipointeval_Horner_1: 0.000003 s	multipointeval_Horner_2: 0.000003 s	multipointeval_linalg: 0.000010 s
n = 18	multipointeval_Horner_1: 0.000003 s	multipointeval_Horner_2: 0.000003 s	multipointeval_linalg: 0.000014 s
n = 20	multipointeval_Horner_1: 0.000005 s	multipointeval_Horner_2: 0.000003 s	multipointeval_linalg: 0.000020 s
n = 22	multipointeval_Horner_1: 0.000004 s	multipointeval_Horner_2: 0.000004 s	multipointeval_linalg: 0.000022 s
n = 24	multipointeval_Horner_1: 0.000004 s	multipointeval_Horner_2: 0.000004 s	multipointeval_linalg: 0.000027 s
n = 26	multipointeval_Horner_1: 0.000004 s	multipointeval_Horner_2: 0.000004 s	multipointeval_linalg: 0.000038 s
n = 28	multipointeval_Horner_1: 0.000004 s	multipointeval_Horner_2: 0.000005 s	multipointeval_linalg: 0.000043 s
n = 30	multipointeval_Horner_1: 0.000006 s	multipointeval_Horner_2: 0.000005 s	multipointeval_linalg: 0.000052 s
n = 32	multipointeval_Horner_1: 0.000005 s	multipointeval_Horner_2: 0.000006 s	multipointeval_linalg: 0.000059 s

Conclusion :
En analysant les résultats fournis, nous pouvons tirer quelques conclusions :

1. **Complexité temporelle :**
   - Pour `multipointeval_Horner_1` et `multipointeval_Horner_2`, les temps d'exécution restent relativement constants avec une légère augmentation à mesure que `n` augmente. Cela suggère une complexité temporelle linéaire ou presque linéaire.
   - En revanche, pour `multipointeval_linalg`, le temps d'exécution augmente de manière plus significative avec `n`. Cela pourrait indiquer une complexité temporelle légèrement supérieure, en particulier en raison de la résolution d'un système linéaire.

2. **Comparaison des méthodes de Horner :**
   - Les deux méthodes de Horner (`multipointeval_Horner_1` et `multipointeval_Horner_2`) montrent des performances similaires avec des temps d'exécution généralement très bas. Cependant, `multipointeval_Horner_2` utilise une version optimisée de la méthode de Horner, ce qui pourrait expliquer sa légère amélioration par rapport à `multipointeval_Horner_1`.

3. **Méthode de résolution de système linéaire :**
   - La méthode `multipointeval_linalg`, qui résout un système linéaire, montre une augmentation significative des temps d'exécution à mesure que `n` augmente. Résoudre un système linéaire a une complexité temporelle plus élevée que l'évaluation directe par la méthode de Horner.

4. **Optimisations possibles :**
   - Les performances pour `n = 8` semblent être une exception, où `multipointeval_linalg` prend plus de temps que prévu. Cela pourrait être dû à des facteurs aléatoires dans les données d'entrée ou à d'autres considérations spécifiques.

5. **Choix de la méthode en fonction des besoins :**
   - Si la résolution d'un système linéaire n'est pas nécessaire, les méthodes de Horner (`multipointeval_Horner_1` et `multipointeval_Horner_2`) semblent être des choix plus efficaces.
   - Si la résolution d'un système linéaire est nécessaire, `multipointeval_linalg` peut toujours être une option valable pour des tailles de problèmes raisonnables.

*/