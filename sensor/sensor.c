#include <stdio.h>

/* The sensor should emit one line per sample, for the full sample set. */
#define MAX_NUMBER_OF_SAMPLES 30

int main(void)
{
    /* Emit one line per sample across the full sample set. */
    int limit = MAX_NUMBER_OF_SAMPLES;

    for (int i = 1; i <= limit; i++) {
        printf("Sample %d: sensor reading OK\n", i);
    }

    return 0;
}
