from time import perf_counter

from database import execute_read_only
from security_utils import legacy_digest, mask_query


LOGIN_TEMPLATE = (
    "SELECT id, username, display_name, role FROM users "
    "WHERE username = '<username_input>' AND legacy_password_digest = '<password_digest>'"
)
SEARCH_TEMPLATE = (
    "SELECT id, name, category, price_vnd, stock FROM products "
    "WHERE visible = 1 AND name LIKE '%<keyword>%'"
)
USER_TEMPLATE = "SELECT id, username, display_name, role, active FROM users WHERE id = <id> LIMIT 1"


def vulnerable_login(username: str, password: str) -> tuple[list, dict]:
    digest = legacy_digest(password)
    sql = (
        "SELECT id, username, display_name, role FROM users "
        f"WHERE username = '{username}' AND legacy_password_digest = '{digest}'"
    )
    started = perf_counter()
    try:
        rows = execute_read_only(sql)
        error = None
    except Exception as exc:
        rows, error = [], exc
    return rows, {
        "feature": "login", "mode": "vulnerable", "query_template": LOGIN_TEMPLATE,
        "construction_method": "string_concatenation", "final_query_masked": mask_query(sql, (digest,)),
        "placeholder_count": 0, "parameters_masked": [], "prepared": False,
        "duration_ms": round((perf_counter() - started) * 1000, 3), "error": error,
    }


def vulnerable_search(keyword: str) -> tuple[list, dict]:
    sql = (
        "SELECT id, name, category, price_vnd, stock FROM products "
        f"WHERE visible = 1 AND name LIKE '%{keyword}%'"
    )
    started = perf_counter()
    try:
        rows = execute_read_only(sql)
        error = None
    except Exception as exc:
        rows, error = [], exc
    return rows, {
        "feature": "search", "mode": "vulnerable", "query_template": SEARCH_TEMPLATE,
        "construction_method": "string_concatenation", "final_query_masked": sql,
        "placeholder_count": 0, "parameters_masked": [], "prepared": False,
        "duration_ms": round((perf_counter() - started) * 1000, 3), "error": error,
    }


def vulnerable_user_detail(user_id: int) -> tuple[list, dict]:
    sql = f"SELECT id, username, display_name, role, active FROM users WHERE id = {user_id} LIMIT 1"
    rows = execute_read_only(sql)
    return rows, {
        "feature": "user_detail", "mode": "vulnerable", "query_template": USER_TEMPLATE,
        "construction_method": "string_concatenation", "final_query_masked": sql,
        "placeholder_count": 0, "parameters_masked": [], "prepared": False,
        "duration_ms": 0.0, "error": None,
    }

