CC := gcc
BUILD := build
NATIVE := native
WARN := -Wall -Wextra -Wpedantic -Wformat=2 -Werror=format-security
DEBUG := -O0 -g -fno-omit-frame-pointer
HARDEN := -O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack
REPRO := -ffile-prefix-map=$(CURDIR)=. -fdebug-prefix-map=$(CURDIR)=.

.PHONY: all clean vulnerable_debug vulnerable_asan secure_length secure_snprintf secure_hardened

all: vulnerable_debug vulnerable_asan secure_length secure_snprintf secure_hardened

$(BUILD):
	mkdir -p $(BUILD)

vulnerable_debug: $(BUILD)/vulnerable_debug

vulnerable_asan: $(BUILD)/vulnerable_asan

secure_length: $(BUILD)/secure_length

secure_snprintf: $(BUILD)/secure_snprintf

secure_hardened: $(BUILD)/secure_hardened

$(BUILD)/vulnerable_debug: $(NATIVE)/vulnerable_processor.c $(NATIVE)/processor_common.h | $(BUILD)
	$(CC) $(WARN) $(DEBUG) -fno-stack-protector $< -o $@

$(BUILD)/vulnerable_asan: $(NATIVE)/vulnerable_processor.c $(NATIVE)/processor_common.h | $(BUILD)
	$(CC) $(WARN) $(DEBUG) $(REPRO) -fsanitize=address,undefined $< -o $@

$(BUILD)/secure_length: $(NATIVE)/secure_length_processor.c $(NATIVE)/processor_common.h | $(BUILD)
	$(CC) $(WARN) $(HARDEN) $(REPRO) $< -o $@

$(BUILD)/secure_snprintf: $(NATIVE)/secure_snprintf_processor.c $(NATIVE)/processor_common.h | $(BUILD)
	$(CC) $(WARN) $(HARDEN) $(REPRO) $< -o $@

$(BUILD)/secure_hardened: $(NATIVE)/secure_snprintf_processor.c $(NATIVE)/processor_common.h | $(BUILD)
	$(CC) $(WARN) $(HARDEN) $(REPRO) -DPROFILE_HARDENED=1 $< -o $@

clean:
	rm -f $(BUILD)/vulnerable_debug $(BUILD)/vulnerable_asan $(BUILD)/secure_length $(BUILD)/secure_snprintf $(BUILD)/secure_hardened
