#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "tab.h"

void InitTab(int *tab, int size) {
    srand(time(NULL));  // Initialiser le générateur de nombres aléatoires
    for (int i = 0; i < size; i++) {
        tab[i] = rand() % 10;  // Valeurs aléatoires entre 0 et 9
    }
}

void PrintTab(int *tab, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", tab[i]);
    }
    printf("\n");
}

int SumTab(int *tab, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += tab[i];
    }
    return sum;
}

int MinSumTab(int *min, int *tab, int size) {
    int sum = 0;
    *min = tab[0];  // Initialiser min avec le premier élément
    for (int i = 0; i < size; i++) {
        sum += tab[i];
        if (tab[i] < *min) {
            *min = tab[i];
        }
    }
    return sum;
}
