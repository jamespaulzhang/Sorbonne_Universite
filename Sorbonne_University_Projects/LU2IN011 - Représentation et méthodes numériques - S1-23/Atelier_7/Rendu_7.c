#include<stdio.h>
#include<math.h>

// Fonction pour compter les bits communs (méthode 1)
int bitcommun(double x, double y) {
    // Conversion des doubles en unsigned long long (pour manipuler les bits)
    unsigned long long x_bits = *(unsigned long long*)&x;
    unsigned long long y_bits = *(unsigned long long*)&y;

    // Variable pour stocker le nombre de bits communs
    int common_bits = 0;

    // Masque pour extraire chaque bit
    unsigned long long mask = 1ULL;

    // Boucle à travers les 64 bits
    for (int i = 0; i < 64; i++) {
        // Comparaison bit à bit et incrémentation si les bits sont égaux
        if ((x_bits & mask) != (y_bits & mask)) {
            common_bits++;
        }
        mask <<= 1; // Décalage du masque pour passer au bit suivant
    }

    return common_bits; // Retourne le nombre de bits communs
}

// Fonction pour compter les bits communs (méthode 2, optimisée)
int bitcommun_opt(double x, double y) {
    // Conversion des doubles en unsigned long long (pour manipuler les bits)
    unsigned long long x_bits = *(unsigned long long*)&x;
    unsigned long long y_bits = *(unsigned long long*)&y;

    // Calcul de la différence entre les bits
    unsigned long long diff = x_bits ^ y_bits;

    // Variable pour stocker le nombre de bits communs
    int common_bits = 0;

    // Boucle tant qu'il y a encore des bits à vérifier
    while (diff > 0) {
        // Vérifie le bit de poids faible et incrémente si c'est 1
        if (diff & 1) {
            common_bits++;
        }
        diff >>= 1; // Décalage pour passer au bit suivant
    }

    return common_bits; // Retourne le nombre de bits communs
}

int main() {
    double x = -2.69998756;
    double y = -2.70001234;

    // Appel de la fonction pour compter les bits communs (méthode 1)
    int common_bits = bitcommun(x, y);

    // Appel de la fonction pour compter les bits communs (méthode 2, optimisée)
    int common_bits_opt = bitcommun_opt(x, y);

    // Affichage du résultat
    printf("Number of common bits between %f and %f is %d\n", x, y, common_bits);
    printf("Number of common bits between %f and %f is %d (optimized)\n", x, y, common_bits_opt);

    return 0;
}
