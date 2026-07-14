PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'admin')),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS server_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_token_hash TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    revoked_at TEXT,
    rotation_reason TEXT
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    username TEXT,
    action TEXT NOT NULL,
    route TEXT NOT NULL,
    mode TEXT NOT NULL,
    cookie_name TEXT,
    cookie_status TEXT,
    submitted_role TEXT,
    database_role TEXT,
    authorization_decision TEXT,
    reason TEXT NOT NULL,
    trace_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cookie_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    mode TEXT NOT NULL,
    cookie_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    value_fingerprint TEXT,
    signature_status TEXT,
    encryption_status TEXT,
    decision TEXT,
    trace_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS session_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,
    old_session_fingerprint TEXT,
    new_session_fingerprint TEXT,
    reason TEXT NOT NULL,
    trace_id TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_sessions_hash ON server_sessions(session_token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_user_active ON server_sessions(user_id, active);
CREATE INDEX IF NOT EXISTS idx_audit_trace ON audit_logs(trace_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_cookie_events_trace ON cookie_events(trace_id);
CREATE INDEX IF NOT EXISTS idx_session_events_trace ON session_events(trace_id);
