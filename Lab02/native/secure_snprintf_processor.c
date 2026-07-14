#include "processor_common.h"

enum { EXIT_FORMAT_ERROR = 66, EXIT_TRUNCATED = 67 };

int process_name(const char *user_input) {
    char name[NAME_BUFFER_SIZE];
    print_metadata(user_input);
    const int written = snprintf(name, sizeof(name), "%s", user_input);

    if (written < 0) {
        fprintf(stderr, "Rejected: snprintf encoding error.\n");
        return EXIT_FORMAT_ERROR;
    }
    if ((size_t)written >= sizeof(name)) {
        fprintf(stderr, "Rejected: snprintf would truncate input to 31 bytes.\n");
        return EXIT_TRUNCATED;
    }

    printf("Processed name: %s\n", name);
    return 0;
}

int main(int argc, char **argv) {
    if (!require_single_argument(argc)) {
        return 64;
    }
    return process_name(argv[1]);
}

