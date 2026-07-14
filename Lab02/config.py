from pathlib import Path


ROOT = Path(__file__).resolve().parent


class Config:
    HOST = "127.0.0.1"
    PORT = 5002
    MAX_CONTENT_LENGTH = 4096
    MAX_NAME_BYTES = 256
    SUBPROCESS_TIMEOUT = 2.0
    TRACE_DIR = ROOT / "evidence" / "traces"
    BUILD_DIR = ROOT / "build"
    LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost"})
    MODES = {
        "vulnerable_debug": {
            "binary": "vulnerable_debug",
            "profile": "Vulnerable debug",
            "flags": "-Wall -Wextra -Wpedantic -Wformat=2 -Werror=format-security -O0 -g -fno-omit-frame-pointer -fno-stack-protector",
        },
        "vulnerable_asan": {
            "binary": "vulnerable_asan",
            "profile": "Vulnerable AddressSanitizer",
            "flags": "-Wall -Wextra -Wpedantic -Wformat=2 -Werror=format-security -O0 -g -fno-omit-frame-pointer -ffile-prefix-map=$PWD=. -fdebug-prefix-map=$PWD=. -fsanitize=address,undefined",
        },
        "secure_length": {
            "binary": "secure_length",
            "profile": "Secure length check",
            "flags": "-Wall -Wextra -Wpedantic -Wformat=2 -Werror=format-security -O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack -ffile-prefix-map=$PWD=. -fdebug-prefix-map=$PWD=.",
        },
        "secure_snprintf": {
            "binary": "secure_snprintf",
            "profile": "Secure snprintf",
            "flags": "-Wall -Wextra -Wpedantic -Wformat=2 -Werror=format-security -O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack -ffile-prefix-map=$PWD=. -fdebug-prefix-map=$PWD=.",
        },
        "secure_hardened": {
            "binary": "secure_hardened",
            "profile": "Secure hardened",
            "flags": "-Wall -Wextra -Wpedantic -Wformat=2 -Werror=format-security -O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack -ffile-prefix-map=$PWD=. -fdebug-prefix-map=$PWD=. -DPROFILE_HARDENED=1",
        },
    }
