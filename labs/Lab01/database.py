import sqlite3
from pathlib import Path
from flask import current_app, g
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(Path(current_app.root_path) / current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None: db.close()
def init_db():
    db = get_db(); db.executescript((Path(current_app.root_path) / "schema.sql").read_text(encoding="utf-8")); db.commit()
def reset_db():
    db = get_db(); db.execute("DROP TABLE IF EXISTS comments"); init_db()
    db.executemany("INSERT INTO comments(post_id,author,body) VALUES(1,?,?)", [("An","Bài viết rất dễ hiểu."),("Bình","Ví dụ local giúp phân biệt ba loại XSS.")]); db.commit()
