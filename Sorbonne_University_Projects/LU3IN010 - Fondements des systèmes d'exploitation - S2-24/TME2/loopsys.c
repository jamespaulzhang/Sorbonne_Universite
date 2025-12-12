#include <stdio.h>
#include <unistd.h>  // Pour getpid()

int main() {
    unsigned long long i;
    unsigned long long max_iter = 50000000ULL; // 5 x 10^7

    for (i = 0; i < max_iter; i++) {
        volatile pid_t pid = getpid();
    }

    return 0;
}
