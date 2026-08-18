CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    legacy_password_digest TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    price_vnd INTEGER NOT NULL CHECK (price_vnd >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    visible INTEGER NOT NULL DEFAULT 1 CHECK (visible IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    action TEXT NOT NULL,
    route TEXT NOT NULL,
    mode TEXT NOT NULL,
    username_submitted TEXT,
    input_summary TEXT NOT NULL,
    query_template TEXT,
    parameter_count INTEGER NOT NULL DEFAULT 0,
    decision TEXT NOT NULL,
    reason TEXT NOT NULL,
    result_count INTEGER NOT NULL DEFAULT 0,
    error_category TEXT,
    trace_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    mode TEXT NOT NULL,
    username_submitted TEXT,
    success INTEGER NOT NULL,
    matched_user_id INTEGER,
    reason TEXT NOT NULL,
    trace_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS query_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    mode TEXT NOT NULL,
    feature TEXT NOT NULL,
    query_template TEXT NOT NULL,
    final_query_masked TEXT NOT NULL,
    parameters_json TEXT NOT NULL,
    result_count INTEGER NOT NULL DEFAULT 0,
    error_category TEXT,
    trace_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trace_records (
    trace_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    payload TEXT NOT NULL
);

