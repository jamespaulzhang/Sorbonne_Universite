#include <stdio.h>
#include <math.h>

int bitcommun(double x, double y) {
    double diff = fabs(x - y);
    double common_digits = -log(diff / fmax(fabs(x), fabs(y))) / log(2.0);
    
    return common_digits;
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
    double x = -2.69998756;
    double y = -2.70001234;
    
    int bits_communs = bitcommun(x, y);
    int common_bits_opt = bitcommun_opt(x, y);
    printf("Nombre de bits communs : %d\n", bits_communs);
    printf("Nombre de bits communs : %d\n", common_bits_opt);
    return 0;
}
