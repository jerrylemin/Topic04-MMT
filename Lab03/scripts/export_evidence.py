from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from database import query_all  # noqa: E402


def rows(sql):
    return [dict(row) for row in query_all(sql)]


def write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    app = create_app()
    with app.app_context():
        traces = rows("SELECT trace_id, payload_json FROM trace_records ORDER BY created_at")
        write(ROOT / "evidence" / "traces" / "all_traces.json", [{"trace_id": item["trace_id"], **json.loads(item["payload_json"])} for item in traces])
        write(ROOT / "evidence" / "audit" / "audit_logs.json", rows("SELECT * FROM audit_logs ORDER BY id"))
        write(ROOT / "evidence" / "database" / "snapshot.json", {
            "users": rows("SELECT id, username, email, role, created_at, updated_at FROM users ORDER BY id"),
            "products": rows("SELECT * FROM products ORDER BY id"),
            "cart_items": rows("SELECT * FROM cart_items ORDER BY id"),
            "invoices": rows("SELECT * FROM invoices ORDER BY id"),
            "invoice_items": rows("SELECT * FROM invoice_items ORDER BY id"),
        })
    print("Exported real traces, audit logs, and database snapshot.")


if __name__ == "__main__":
    main()
