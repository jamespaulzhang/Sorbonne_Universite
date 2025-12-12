#include "Fifo.h"

#include <stdlib.h>
#include <stdio.h>

int initFifo(Swapper*);
unsigned int fifoChoose(Swapper*);
void fifoReference(Swapper*, unsigned int frame);
void finalizeFifo(Swapper*);

int initFifoSwapper(Swapper* swap, unsigned int frames) {
    return initSwapper(swap, frames, initFifo, NULL, fifoChoose, finalizeFifo);
}

int initFifo(Swapper* swap) {
    // stocker l'index FIFO
    swap->private_data = malloc(sizeof(unsigned int));
    if (!swap->private_data) return -1;

    *(unsigned int*)swap->private_data = 0;
    return 0;
}

unsigned int fifoChoose(Swapper* swap) {
    unsigned int* index = (unsigned int*)swap->private_data;
	unsigned int frame = *index;

    // Avancer l’index
    *index = (*index + 1) % swap->frame_nb;

    return frame;
}

void finalizeFifo(Swapper* swap) {
    free(swap->private_data);
}
