"""Reset only the fixed local Lab05 SQLite database."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seed import main  # noqa: E402


if __name__ == "__main__":
    main()
