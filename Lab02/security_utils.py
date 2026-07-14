import re
import signal
from pathlib import Path
from urllib.parse import urlsplit


ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
HOME_PATH = re.compile(r"(?:[A-Za-z]:\\Users\\[^\\\s:]+|/home/[^/\s:]+)")


def is_local_host(host: str, allowed: set[str] | frozenset[str], port: int = 5002) -> bool:
    try:
        parsed = urlsplit(f"//{host}")
        return parsed.hostname in allowed and parsed.port in {None, port}
    except ValueError:
        return False


def is_local_origin(
    origin: str | None,
    allowed: set[str] | frozenset[str],
    port: int = 5002,
) -> bool:
    if not origin:
        return True
    try:
        parsed = urlsplit(origin)
    except ValueError:
        return False
    return parsed.scheme == "http" and parsed.hostname in allowed and parsed.port == port


def utf8_length(value: str) -> int:
    return len(value.encode("utf-8"))


def validate_name(value: str | None, maximum: int) -> str:
    if value is None:
        raise ValueError("Thiếu trường name.")
    if not value:
        raise ValueError("Trường name không được để trống.")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError("Name chứa ký tự điều khiển không hợp lệ.")
    if utf8_length(value) > maximum:
        raise ValueError(f"Name vượt giới hạn {maximum} byte UTF-8.")
    return value


def redact_text(value: object, root: Path, limit: int = 16_384) -> str:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    text = ANSI_ESCAPE.sub("", str(value or ""))
    for prefix in {str(root), root.as_posix()}:
        text = text.replace(prefix, ".")
    text = HOME_PATH.sub("<HOME>", text)
    text = "".join(char for char in text if char in "\n\t" or ord(char) >= 32)
    return text if len(text) <= limit else f"{text[:limit]}\n...[output truncated]"


def signal_name(return_code: int | None) -> str | None:
    if return_code is None or return_code >= 0:
        return None
    try:
        return signal.Signals(-return_code).name
    except ValueError:
        return f"SIGNAL_{-return_code}"


def parse_asan(stderr: str, root: Path, input_bytes: int) -> dict:
    cleaned = redact_text(stderr, root)
    error = re.search(r"AddressSanitizer:\s*([\w-]+)", cleaned)
    write = re.search(r"WRITE of size (\d+)", cleaned)
    source = re.search(
        r"(?P<file>[^\s:]*[\\/]?[^\s:]*\.c):(?P<line>\d+)(?::\d+)?(?:\s+in\s+(?P<function>[\w.]+))?",
        cleaned,
    )
    function = re.search(r"#\d+.*?\bin\s+([\w.]+)\s+.*?\.c:\d+", cleaned)
    frames = [line.strip() for line in cleaned.splitlines() if re.match(r"\s*#\d+", line)][:5]
    return {
        "detected": bool(error),
        "error_type": error.group(1) if error else None,
        "source_file": source.group("file") if source else None,
        "file": source.group("file") if source else None,
        "line": int(source.group("line")) if source else None,
        "function": (function.group(1) if function else None)
        or (source.group("function") if source else None),
        "write_size": int(write.group(1)) if write else None,
        "buffer_name": "name" if "'name'" in cleaned or "name[32]" in cleaned else None,
        "buffer_size": 32,
        "input_length": input_bytes,
        "stack_trace": frames,
    }
