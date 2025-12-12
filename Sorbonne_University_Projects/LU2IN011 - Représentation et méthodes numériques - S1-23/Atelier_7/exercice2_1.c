#include <stdio.h>
#include <math.h>

// Fonction pour évaluer le polynôme en utilisant l'algorithme de Horner
double horner(double *p, int deg, double val) {
    double result = p[0]; // Initialisation du résultat avec le premier coefficient
    for (int i = 1; i <= deg; i++) {
        result = result * val + p[i]; // Algorithme de Horner
    }
    return result; // Renvoie le résultat final
}

int main() {
    double x0, alpha, epsilon;

    // Demander à l'utilisateur d'entrer les valeurs x0,alpha et epsilon
    printf("Entrez la valeur de x0 : ");
    scanf("%lf", &x0);
    printf("Entrez la valeur de alpha : ");
    scanf("%lf", &alpha);
    printf("Entrez la valeur de epsilon : ");
    scanf("%lf", &epsilon);

    // Coefficients du polynôme numerateur
    double numerateur[] = {4.0 , -(3.0 * alpha-2.0) , -alpha ,-2.0 * alpha};
    // Coefficients du polynôme denominateur
    double denominateur[] = {5.0 , -(4.0 * alpha - 3.0) , -2.0 * alpha -2.0}; 
    
    int deg = 3; // Degré du polynôme
    
    double x1 = horner(numerateur, deg, x0) / horner(denominateur, deg - 1, x0); // Calcul de la première itération
    
    printf("x0 : %.15e\n",x0); // Affichage de x0
    
    int n = 1;
    while(fabs(x1 - x0) > epsilon){ //si epsilon est inferieur a la valeur absolue de (x1 - x0),on passe dans le boucle,sinon on s'arrete
        x0 = x1;
        x1 = horner(numerateur, deg, x1) / horner(denominateur, deg - 1, x1); // Calcul de la prochaine itération xn+1
        printf("x%d = %.15e\n",n++,x0); // Affichage du résultat de l'itération
    }
    printf("x%d = %.15e\n",n++,x1); // Affichage du résultat final
    
    return 0;
}