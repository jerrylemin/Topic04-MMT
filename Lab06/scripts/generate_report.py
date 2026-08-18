"""Generate the two-member Lab06 DOCX only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from topic04_reports import generate

if __name__ == "__main__":
    print(generate("Lab06"))
