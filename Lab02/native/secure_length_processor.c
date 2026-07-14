#include "processor_common.h"

enum { EXIT_INPUT_TOO_LONG = 65 };

int process_name(const char *user_input) {
    char name[NAME_BUFFER_SIZE];
    print_metadata(user_input);
    const size_t length = strnlen(user_input, NAME_BUFFER_SIZE + 1U);

    if (length > NAME_SAFE_CAPACITY) {
        fprintf(stderr, "Rejected: input exceeds 31 bytes (received at least %zu).\n", length);
        return EXIT_INPUT_TOO_LONG;
    }

    memcpy(name, user_input, length);
    name[length] = '\0';
    printf("Processed name: %s\n", name);
    return 0;
}

int main(int argc, char **argv) {
    if (!require_single_argument(argc)) {
        return 64;
    }
    return process_name(argv[1]);
}

