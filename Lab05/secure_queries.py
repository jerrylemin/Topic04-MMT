from time import perf_counter

from database import execute_read_only


LOGIN_SQL = (
    "SELECT id, username, display_name, role, password_hash FROM users "
    "WHERE username = ? AND active = 1 LIMIT 1"
)
SEARCH_SQL = (
    "SELECT id, name, category, price_vnd, stock FROM products "
    "WHERE visible = 1 AND name LIKE ? LIMIT 50"
)
USER_SQL = "SELECT id, username, display_name, role, active FROM users WHERE id = ? LIMIT 1"


def _run(feature: str, sql: str, parameters: tuple) -> tuple[list, dict]:
    started = perf_counter()
    rows = execute_read_only(sql, parameters)
    return rows, {
        "feature": feature, "mode": "secure", "query_template": sql,
        "construction_method": "parameter_binding", "final_query_masked": sql,
        "placeholder_count": sql.count("?"), "parameters_masked": ["[BOUND VALUE]" for _ in parameters],
        "prepared": True, "duration_ms": round((perf_counter() - started) * 1000, 3), "error": None,
    }


def secure_login_lookup(username: str) -> tuple[list, dict]:
    return _run("login", LOGIN_SQL, (username,))


def secure_search(keyword: str) -> tuple[list, dict]:
    return _run("search", SEARCH_SQL, (f"%{keyword}%",))


def secure_user_detail(user_id: int) -> tuple[list, dict]:
    return _run("user_detail", USER_SQL, (user_id,))

