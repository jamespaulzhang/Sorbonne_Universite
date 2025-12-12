#include <stdio.h>
#include <stdlib.h>

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

int main() {
    // Exemple d'utilisation
    int degre_f = 2;
    double coefficients_f[] = {1.0, 2.0, 3.0}; // f(x) = 1 + 2x + 3x^2

    int degre_g = 1;
    double coefficients_g[] = {4.0, 5.0}; // g(x) = 4 + 5x

    int degre_h; // Le degré du polynôme résultant
    double coefficients_h[degre_f + degre_g + 1]; // Le tableau des coefficients du polynôme résultant

    // Appel de la fonction mulpol
    mulpol(coefficients_f, degre_f, coefficients_g, degre_g, coefficients_h, &degre_h);

    // Affichage du polynôme résultant
    printf("Le produit h(x) : ");
    for (int i = degre_h; i >= 0; i--) {
        printf("%.2f", coefficients_h[i]);
        if (i > 0) {
            printf("x^%d + ", i);
        }
    }
    printf("\n");

    return 0;
}
