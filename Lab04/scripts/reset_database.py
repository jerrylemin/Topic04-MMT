"""Reset only the local Lab04 SQLite database to the documented demo state."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seed import main  # noqa: E402


if __name__ == "__main__":
    main()
