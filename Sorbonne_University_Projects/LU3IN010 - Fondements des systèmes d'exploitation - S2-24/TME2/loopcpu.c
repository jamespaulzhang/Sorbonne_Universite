#include <stdio.h>

int main() {
    volatile unsigned long long i;
    unsigned long long max_iter = 5000000000ULL; // 5 x 10^9

    for (i = 0; i < max_iter; i++);

    return 0;
}
