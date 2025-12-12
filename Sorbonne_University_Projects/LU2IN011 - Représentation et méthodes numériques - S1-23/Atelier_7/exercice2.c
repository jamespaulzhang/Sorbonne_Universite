#include <stdio.h>
#include <math.h>

double horner(double *p, int deg, double val) {
    double result = p[0];
    for (int i = 1; i <= deg; i++) {
        result = result * val + p[i];
    }
    return result;
}

int main() {
    double x0, alpha, epsilon;
    printf("Entrez la valeur de x0 : ");
    scanf("%lf", &x0);
    printf("Entrez la valeur de alpha : ");
    scanf("%lf", &alpha);
    printf("Entrez la valeur de epsilon : ");
    scanf("%lf", &epsilon);
    // Coefficients du polynôme numerateur
    double numerateur[] = {4.0 , -(3.0 * alpha-2.0) , -alpha ,-2.0 * alpha};
    double denominateur[] = {5.0 , -(4.0 * alpha - 3.0) , -2.0 * alpha -2.0}; 
    int deg = 3; // Degré du polynôme
    double x1 = horner(numerateur, deg, x0) / horner(denominateur, deg - 1, x0);
    printf("x0 : %.15e\n",x0);
    printf("x0 : %.15e\n",x1);
    int n = 2;
    while(fabs(x1 - x0) > epsilon){
        x0 = x1;
        x1 = horner(numerateur, deg, x1) / horner(denominateur, deg - 1, x1);
        printf("x%d = %.15e\n",n++,x1);
    }
    return 0;
}

