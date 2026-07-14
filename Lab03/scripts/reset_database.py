import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from seed import reset_database  # noqa: E402


app = create_app()
with app.app_context():
    reset_database()
print(f"Database reset: {app.config['DATABASE']}")
