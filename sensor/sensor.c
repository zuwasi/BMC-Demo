#include <stdio.h>

/* The sensor should emit one line per sample, for the full sample set. */
#define MAX_NUMBER_OF_SAMPLES 30

int main(void)
{
    /* BUG: the loop is capped at 20 instead of MAX_NUMBER_OF_SAMPLES (30),
       so only 20 samples are ever printed. */
    int limit = 20;

    for (int i = 1; i <= limit; i++) {
        printf("Sample %d: sensor reading OK\n", i);
    }

    return 0;
}
