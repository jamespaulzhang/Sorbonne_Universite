#include "LRU.h"

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int	initLRU(Swapper*);
void	referenceLRU(Swapper*,unsigned int frame);
unsigned int chooseLRU(Swapper*);
void	finalizeLRU(Swapper*);

typedef struct {
	unsigned int clock;
	unsigned int * age;
} InfoLRU;

int initLRUSwapper(Swapper*swap,unsigned int frames){
 return	initSwapper(swap,frames,initLRU,referenceLRU,chooseLRU,finalizeLRU);
}

int initLRU(Swapper* swap) {
    InfoLRU* info = (InfoLRU*)malloc(sizeof(InfoLRU));
    if (!info) return -1;

    info->clock = 0;

    // tableau pour stocker l'horloge de chaque page
    info->age = (unsigned int*)malloc(swap->frame_nb * sizeof(unsigned int));
    if (!info->age) {
        free(info);
        return -1;
    }

    // Init des âges (aucune page encore utilisée)
    for (unsigned int i = 0; i < swap->frame_nb; i++) {
        info->age[i] = 0;
    }

    swap->private_data = info;
    return 0;
}

void referenceLRU(Swapper* swap, unsigned int frame) {
    InfoLRU* info = (InfoLRU*)swap->private_data;

    // Maj horloge + enregistrer le dernier accès du frame
    info->clock++;
    info->age[frame] = info->clock;
}

unsigned int chooseLRU(Swapper* swap) {
    InfoLRU* info = (InfoLRU*)swap->private_data;

    // Trouver le frame le plus ancien
    unsigned int min_index = 0;
    unsigned int min_age = info->age[0];

    for (unsigned int i = 1; i < swap->frame_nb; i++) {
        if (info->age[i] < min_age) {
            min_index = i;
            min_age = info->age[i];
        }
    }

    return min_index;
}

void finalizeLRU(Swapper* swap) {
    InfoLRU* info = (InfoLRU*)swap->private_data;

    if (info) {
        free(info->age);
        free(info);
    }
}