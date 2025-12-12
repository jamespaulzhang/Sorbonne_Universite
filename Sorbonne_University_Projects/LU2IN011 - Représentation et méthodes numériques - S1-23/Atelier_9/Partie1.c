#include<stdio.h>
#include<stdlib.h>
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

int main() {
    const int max_degree = 16;
    const int repetitions = 100000; // Nombre de répétitions pour chaque mesure

    // Initialiser le générateur de nombres aléatoires
    srand(time(NULL));

    double result_1, result_2, result_minus_2; // Déclarer les variables à l'extérieur de la boucle

    for (int i = 0; i <= max_degree; i++) {
        int degree = 2 * i;
        double coefficients[degree + 1];

        // Générer des coefficients aléatoires dans l'intervalle [-1, 1]
        for (int j = 0; j <= degree; j++) {
            coefficients[j] = (double)rand() / RAND_MAX * 2.0 - 1.0;
        }

        // Mesurer le temps d'évaluation pour eval_Horner_1
        clock_t start_time_1 = clock();
        for (int rep = 0; rep < repetitions; rep++) {
            eval_Horner_1(2.0, coefficients, degree, &result_1);
        }
        clock_t end_time_1 = clock();

        // Mesurer le temps d'évaluation pour eval_Horner_2
        clock_t start_time_2 = clock();
        for (int rep = 0; rep < repetitions; rep++) {
            eval_Horner_2(2.0, coefficients, degree, &result_2, &result_minus_2);
        }
        clock_t end_time_2 = clock();

        // Calculer les temps d'exécution moyens en secondes
        double time_1 = ((double)(end_time_1 - start_time_1)) / CLOCKS_PER_SEC / repetitions;
        double time_2 = ((double)(end_time_2 - start_time_2)) / CLOCKS_PER_SEC / repetitions;

        printf("Degré %d:\n", degree);
        printf("eval_Horner_1 : %.10lf secondes\n", time_1);
        printf("eval_Horner_2 : %.10lf secondes\n", time_2);

        printf("Résultat(Horner_1): %f\n", result_1);
        printf("Résultat(Horner_2): %f\n", result_2);
        printf("Résultat(Horner_2(minus_a_2): %f\n", result_minus_2);

        printf("\n");
    }

    return 0;
}

/* 

On a fait les tests et on a trouvé les résultat suivants:

Degré 0:
eval_Horner_1 : 0.0000000226 secondes
eval_Horner_2 : 0.0000000225 secondes
Résultat(Horner_1): -0.268114
Résultat(Horner_2): -0.268114
Résultat(Horner_2(minus_a_2): -0.268114

Degré 2:
eval_Horner_1 : 0.0000000096 secondes
eval_Horner_2 : 0.0000000164 secondes
Résultat(Horner_1): 0.331642
Résultat(Horner_2): 0.331642
Résultat(Horner_2(minus_a_2): 3.407597

Degré 4:
eval_Horner_1 : 0.0000000137 secondes
eval_Horner_2 : 0.0000000268 secondes
Résultat(Horner_1): -8.779283
Résultat(Horner_2): -8.779283
Résultat(Horner_2(minus_a_2): 3.138385

Degré 6:
eval_Horner_1 : 0.0000000195 secondes
eval_Horner_2 : 0.0000000276 secondes
Résultat(Horner_1): -17.798754
Résultat(Horner_2): -17.798754
Résultat(Horner_2(minus_a_2): -86.790309

Degré 8:
eval_Horner_1 : 0.0000000252 secondes
eval_Horner_2 : 0.0000000337 secondes
Résultat(Horner_1): 272.544204
Résultat(Horner_2): 272.544204
Résultat(Horner_2(minus_a_2): 68.334216

Degré 10:
eval_Horner_1 : 0.0000000309 secondes
eval_Horner_2 : 0.0000000419 secondes
Résultat(Horner_1): 886.770179
Résultat(Horner_2): 886.770179
Résultat(Horner_2(minus_a_2): -126.963875

Degré 12:
eval_Horner_1 : 0.0000000351 secondes
eval_Horner_2 : 0.0000000486 secondes
Résultat(Horner_1): 324.644963
Résultat(Horner_2): 324.644963
Résultat(Horner_2(minus_a_2): -271.782374

Degré 14:
eval_Horner_1 : 0.0000000455 secondes
eval_Horner_2 : 0.0000000514 secondes
Résultat(Horner_1): 4141.086539
Résultat(Horner_2): 4141.086539
Résultat(Horner_2(minus_a_2): -5919.312661

Degré 16:
eval_Horner_1 : 0.0000000444 secondes
eval_Horner_2 : 0.0000000596 secondes
Résultat(Horner_1): 10577.378387
Résultat(Horner_2): 10577.378387
Résultat(Horner_2(minus_a_2): 24676.128818

Degré 18:
eval_Horner_1 : 0.0000000502 secondes
eval_Horner_2 : 0.0000000621 secondes
Résultat(Horner_1): 200198.367819
Résultat(Horner_2): 200198.367819
Résultat(Horner_2(minus_a_2): 213061.904262

Degré 20:
eval_Horner_1 : 0.0000000559 secondes
eval_Horner_2 : 0.0000000688 secondes
Résultat(Horner_1): -637844.317591
Résultat(Horner_2): -637844.317591
Résultat(Horner_2(minus_a_2): -447698.703095

Degré 22:
eval_Horner_1 : 0.0000000673 secondes
eval_Horner_2 : 0.0000000743 secondes
Résultat(Horner_1): 439264.303713
Résultat(Horner_2): 439264.303713
Résultat(Horner_2(minus_a_2): 3490530.724774

Degré 24:
eval_Horner_1 : 0.0000000712 secondes
eval_Horner_2 : 0.0000000807 secondes
Résultat(Horner_1): -3431337.212383
Résultat(Horner_2): -3431337.212383
Résultat(Horner_2(minus_a_2): 9858260.846539

Degré 26:
eval_Horner_1 : 0.0000000800 secondes
eval_Horner_2 : 0.0000000863 secondes
Résultat(Horner_1): 14887787.261187
Résultat(Horner_2): 14887787.261187
Résultat(Horner_2(minus_a_2): 44229972.613893

Degré 28:
eval_Horner_1 : 0.0000000843 secondes
eval_Horner_2 : 0.0000000931 secondes
Résultat(Horner_1): 245239972.832049
Résultat(Horner_2): 245239972.832049
Résultat(Horner_2(minus_a_2): 209983461.932048

Degré 30:
eval_Horner_1 : 0.0000000948 secondes
eval_Horner_2 : 0.0000001000 secondes
Résultat(Horner_1): -1181033521.506705
Résultat(Horner_2): -1181033521.506705
Résultat(Horner_2(minus_a_2): -390928452.713832

Degré 32:
eval_Horner_1 : 0.0000001023 secondes
eval_Horner_2 : 0.0000001098 secondes
Résultat(Horner_1): -3904375733.249982
Résultat(Horner_2): -3904375733.249982
Résultat(Horner_2(minus_a_2): -1038674418.801278

Conclusion: En mesurant le temps d'exécution des deux fonctions sur une seule exécution, il est difficle de comparer leur efficacité.
Ainsi, si on fait un grand nombre d'appels sur ces deux fonctions, (100000 ici) on commence à voir une différence et la première fonction de Horner semble être plus rapide pour effectuer les calculs selon les conditions de l'exercice.

*/