#include <stdio.h>
#include <math.h>
int bitcommun(double x, double y) {
    double diff = fabs(x - y);
    int count = 0;

    while (diff < 1.0) {
        diff *= 10.0;
        count++;
    }

    int bits_communs = (int)(count * 3.32); // Convertir le nombre de chiffres en bits
    return bits_communs;
}

int bitcommun_opt(double x, double y) {
    unsigned long long int bx = *((unsigned long long int*)&x);
    unsigned long long int by = *((unsigned long long int*)&y);
    unsigned long long int diff = bx ^ by;
    int count = 0;

    while (diff) {
        count += diff & 1;
        diff >>= 1;
    }

    return count;
}


int main() {
    double x = 1.41421356;
    double y = 1.41427845;
    
    int bits_communs = bitcommun(x, y);
    int common_bits_opt = bitcommun_opt(x, y);
    printf("Nombre de bits communs : %d\n", bits_communs);
    printf("Nombre de bits communs : %d\n", common_bits_opt);
    return 0;
}
