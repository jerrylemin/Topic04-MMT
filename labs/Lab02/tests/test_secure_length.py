import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
BINARY = ROOT / "build" / "secure_length"


def run(value: str):
    return subprocess.run(
        [str(BINARY), value], cwd=ROOT, capture_output=True, text=True,
        timeout=2, check=False,
    )


def test_length_patch_accepts_31_bytes_and_rejects_32():
    accepted = run("A" * 31)
    rejected = run("A" * 32)

    assert accepted.returncode == 0
    assert "Processed name:" in accepted.stdout
    assert rejected.returncode == 65
    assert "exceeds 31 bytes" in rejected.stderr
    assert "Processed name:" not in rejected.stdout
