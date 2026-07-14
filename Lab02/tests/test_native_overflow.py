import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_asan_detects_stack_overflow_for_64_bytes():
    env = {**os.environ, "ASAN_OPTIONS": "abort_on_error=1:detect_leaks=0"}
    result = subprocess.run(
        [str(ROOT / "build" / "vulnerable_asan"), "A" * 64],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=2,
        env=env,
        check=False,
    )

    assert result.returncode != 0
    assert "stack-buffer-overflow" in result.stderr
    assert "vulnerable_processor.c" in result.stderr
