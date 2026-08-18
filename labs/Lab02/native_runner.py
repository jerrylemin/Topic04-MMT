import re
import subprocess
from pathlib import Path
from time import perf_counter

from config import Config, ROOT
from security_utils import parse_asan, redact_text, signal_name, utf8_length, validate_name

try:
    import resource
except ImportError:  # Windows only orchestrates the Linux lab.
    resource = None


def restricted_environment() -> dict[str, str]:
    return {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "ASAN_OPTIONS": "abort_on_error=1:detect_leaks=0:color=never:symbolize=1",
        "UBSAN_OPTIONS": "halt_on_error=1:print_stacktrace=1",
    }


def disable_core_dumps() -> None:
    if resource is not None:
        _soft, hard = resource.getrlimit(resource.RLIMIT_CORE)
        resource.setrlimit(resource.RLIMIT_CORE, (0, hard))


def _base_result(mode: str, mode_info: dict, timeout: float) -> dict:
    return {
        "binary": mode_info["binary"],
        "build_profile": mode_info["profile"],
        "pid": None,
        "timeout": False,
        "timeout_seconds": timeout,
        "exit_code": None,
        "signal": None,
        "stdout": "",
        "stderr": "",
        "asan": {"detected": False},
        "crash_detected": False,
        "duration_ms": 0.0,
        "status": "error",
        "mode": mode,
    }


def run_native(
    mode: str,
    name: str,
    *,
    modes: dict | None = None,
    root: Path = ROOT,
    timeout: float = Config.SUBPROCESS_TIMEOUT,
    max_name_bytes: int = Config.MAX_NAME_BYTES,
) -> dict:
    modes = modes or Config.MODES
    if mode not in modes:
        raise ValueError("Mode không được phép.")
    validate_name(name, max_name_bytes)
    mode_info = modes[mode]
    result = _base_result(mode, mode_info, timeout)
    build_dir = (Path(root) / "build").resolve()
    binary = (build_dir / mode_info["binary"]).resolve()
    if binary.parent != build_dir:
        raise ValueError("Binary không hợp lệ.")
    if not binary.is_file():
        result.update(status="unavailable", stderr="Binary chưa được build.")
        return result

    disable_core_dumps()
    started = perf_counter()
    try:
        completed = subprocess.run(
            [str(binary), name],
            cwd=str(Path(root).resolve()),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=restricted_environment(),
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        result.update(
            timeout=True,
            status="timeout",
            stdout=redact_text(exc.stdout, Path(root)),
            stderr=redact_text(exc.stderr, Path(root)),
        )
    except OSError:
        result.update(status="unavailable", stderr="Không thể chạy binary trong môi trường hiện tại.")
    else:
        stdout = redact_text(completed.stdout, Path(root))
        stderr = redact_text(completed.stderr, Path(root))
        native_signal = signal_name(completed.returncode)
        asan = parse_asan(completed.stderr, Path(root), utf8_length(name))
        asan.update(exit_code=completed.returncode, raw=stderr)
        pid = re.search(r"^PID:\s*(\d+)\s*$", stdout, re.MULTILINE)
        result.update(
            pid=int(pid.group(1)) if pid else None,
            exit_code=completed.returncode,
            signal=native_signal,
            stdout=stdout,
            stderr=stderr,
            asan=asan,
            crash_detected=bool(native_signal or asan["detected"]),
            status="completed",
        )
    result["duration_ms"] = round((perf_counter() - started) * 1000, 3)
    return result
