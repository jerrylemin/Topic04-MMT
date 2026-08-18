#ifndef PROCESSOR_COMMON_H
#define PROCESSOR_COMMON_H

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define NAME_BUFFER_SIZE 32U
#define NAME_SAFE_CAPACITY (NAME_BUFFER_SIZE - 1U)

static inline int require_single_argument(int argc) {
    if (argc == 2) {
        return 1;
    }
    fprintf(stderr, "Usage: processor <name>\n");
    return 0;
}

static inline void print_metadata(const char *input) {
    printf("PID: %ld\n", (long)getpid());
    printf("Input bytes: %zu\n", strlen(input));
    printf("Buffer bytes: %u\n", NAME_BUFFER_SIZE);
    fflush(stdout);
}

#endif

