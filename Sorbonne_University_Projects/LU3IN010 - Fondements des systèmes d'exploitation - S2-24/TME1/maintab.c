#include <stdio.h>
#include <stdlib.h>
#include "tab.h"
#include <sys/resource.h>

void PrintMem() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    printf("Memory usage: %ld kilobytes\n", usage.ru_maxrss);
}

int main() {
    PrintMem(); // Memory usage: 1179648 kilobytes
    
    int tab[NMAX];
    PrintMem(); // Memory usage: 1196032 kilobytes
    
    int *heapTab = malloc(NMAX * sizeof(int));
    PrintMem(); // Memory usage: 1228800 kilobytes

    if (heapTab == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Initialisation et affichage du tableau sur la pile

    // Afficher la mémoire avant et après l'allocation (tests effectués avec NMAX=1000000)
    PrintMem();     // Memory usage: 1228800 kilobytes
    InitTab(tab, NMAX);
    PrintMem();     // Memory usage: 5128192 kilobytes

    PrintTab(tab, NMAX);

    // Initialisation et affichage du tableau sur le tas

    // Afficher la mémoire avant et après l'allocation
    PrintMem();     // Memory usage: 5128192 kilobytes
    InitTab(heapTab, NMAX);
    PrintMem();     // Memory usage: 9142272 kilobytes

    PrintTab(heapTab, NMAX);

    /* Question 2.9
    Ce qu'on peut constater :
    Mémoire allouée sur la pile : La mémoire pour le tableau tab est allouée dès sa déclaration dans la pile.
    Mémoire allouée sur le tas : La mémoire pour le tableau heapTab est allouée uniquement lors de l'appel à malloc. 
    Cependant, l'utilisation effective de cette mémoire augmente lors de l'appel à InitTab, où les données sont remplies, 
    ce qui entraîne une utilisation plus importante de la mémoire.
    
    Ainsi, l'allocation de mémoire effective pour tab (sur la pile) se produit dès sa déclaration, 
    tandis que pour heapTab (sur le tas), elle a lieu lors de l'appel à malloc.

    La mémoire est allouée à plusieurs moments :
    Lors de la déclaration de tab dans la pile et de l'appel à malloc pour heapTab au début du main.
    Lors des appels à InitTab, qui remplissent les tableaux avec des données, 
    augmentant ainsi l'utilisation effective de la mémoire.
    */

    // Tester les fonctions SumTab et MinSumTab
    int min;
    int sum = SumTab(tab, NMAX);
    printf("Sum of elements: %d\n", sum);

    int minSum = MinSumTab(&min, tab, NMAX);
    printf("Sum: %d, Min: %d\n", minSum, min);

    free(heapTab); // Libérer la mémoire allouée

    return 0;
}
