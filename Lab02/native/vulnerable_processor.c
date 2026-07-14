#include "processor_common.h"

int process_name(const char *user_input) {
    char name[32];
    print_metadata(user_input);
    /* CỐ Ý CÓ LỖ HỔNG: strcpy không biết kích thước buffer đích. */
    strcpy(name, user_input);
    printf("Processed name: %s\n", name);
    return 0;
}

int main(int argc, char **argv) {
    if (!require_single_argument(argc)) {
        return 64;
    }
    return process_name(argv[1]);
}
