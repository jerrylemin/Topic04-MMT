import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from app import create_app
from database import reset_db
app=create_app()
with app.app_context(): reset_db()
print("Database đã reset.")
