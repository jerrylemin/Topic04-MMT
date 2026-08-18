import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_vulnerable_processor_accepts_short_name():
    binary = ROOT / "build" / "vulnerable_debug"
    result = subprocess.run(
        [str(binary), "Le Minh"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=2,
        check=False,
    )

    assert result.returncode == 0
    assert "Processed name: Le Minh" in result.stdout
    assert "Input bytes: 7" in result.stdout
    assert "Buffer bytes: 32" in result.stdout
