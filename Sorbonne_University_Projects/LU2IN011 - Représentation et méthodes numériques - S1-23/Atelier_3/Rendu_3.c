#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

uint32_t add(uint32_t a, uint32_t b, uint32_t p) {
    return (a + b) % p;
}

uint32_t sub(uint32_t a, uint32_t b, uint32_t p) {
    return (a - b + p) % p;
}

uint32_t mul(uint32_t a, uint32_t b) {
    uint32_t *produit_ab = malloc(sizeof(uint32_t)*a*b);
    *produit_ab = a * b;
    return *produit_ab;
}


uint32_t mul_mod(uint32_t a, uint32_t b, uint32_t p) {
    return mul(a, b) % p;
}

uint32_t inv(uint32_t a, uint32_t p) {
    for (uint32_t u = 0; u < p; u++) {
        if ((a * u) % p == 1) {
            return u;
        }
    }
    return 0;
}

void split_64(uint64_t a, uint32_t *a1, uint32_t *a0) {
    *a1 = (uint32_t)a;
    *a0 = (uint32_t)(a >> 31);
}

void mul_naive_128(uint64_t a, uint64_t b, uint64_t *ab2, uint64_t *ab1, uint64_t *ab0) {
    uint32_t a0, a1, b0, b1;
    split_64(a, &a1, &a0);
    split_64(b, &b1, &b0);
    *ab2 = (uint64_t)a1 * b1;
    *ab1 = (uint64_t)a1 * b0 + (uint64_t)a0 * b1;
    *ab0 = (uint64_t)a0 * b0;
}

void mul_karatsuba_128(uint64_t a, uint64_t b, uint64_t *ab2, uint64_t *ab1, uint64_t *ab0) {
    uint32_t a0, a1, b0, b1;
    split_64(a, &a1, &a0);
    split_64(b, &b1, &b0);
    *ab2 = (uint64_t)a1 * b1;
    *ab0 = (uint64_t)a0 * b0;
    *ab1 = ((uint64_t)(a1 + a0) * (b1 + b0)) - *ab2 - *ab0;
}

int main(void) {
    uint32_t a = 5;
    uint32_t b = 7;
    uint32_t p_values[] = {2, 101, 65521, 1073741827};

    for(int i = 0; i < 4; i++) {
        uint32_t p = p_values[i];
        printf("p = %u\n", p);
        printf("add(%u, %u, %u) = %u\n", a, b, p, add(a, b, p));
        printf("sub(%u, %u, %u) = %u\n", a, b, p, sub(a, b, p));
        printf("mul(%u, %u) = %u\n", a, b, mul(a, b));
        printf("mul_mod(%u, %u, %u) = %u\n", a, b, p, mul_mod(a, b, p));

        uint32_t inverse = inv(a, p);
        if (inverse != 0) {
            printf("inv(%u, %u) = %u\n", a, p, inverse);
        } else {
            printf("inv(%u, %u) n'existe pas\n", a, p);
        }

        printf("\n");
    }



    return 0;
}