from trace_models import TraceStep
from validation import input_signals


def inspectors(*, feature: str, mode: str, raw_input: str, normalized_input: str,
               query: dict, rows: list, error_info: dict | None, decision: str,
               expected_count: int | None = None, session_created: bool = False) -> dict:
    result_ids = [row["id"] for row in rows]
    result_names = [row["name"] for row in rows if "name" in row.keys()]
    prepared = bool(query.get("prepared"))
    return {
        "input_inspector": {
            "raw_input": raw_input, "normalized_input": normalized_input,
            "source": "request.form" if feature == "login" else "request.args",
            "validation_result": "accepted", **input_signals(raw_input),
        },
        "query_inspector": {
            **{key: value for key, value in query.items() if key != "error"},
            "raw_input": raw_input, "normalized_input": normalized_input,
            "input_interpreted_as": "data" if prepared else "syntax-capable text",
            "operation": "SELECT", "read_only": True,
        },
        "execution_inspector": {
            "operation": "SELECT", "prepared_statement": prepared,
            "parameters_bound": query.get("placeholder_count", 0), "rows_returned": len(rows),
            "rows_changed": 0, "error_category": (error_info or {}).get("category"),
            "transaction_status": "read_only", "rollback_status": "not_needed",
            "database_label": "Lab05 local SQLite",
        },
        "decision_inspector": {
            "mode": mode, "rows_returned": len(rows), "session_created": session_created,
            "final_decision": decision, "password_verification_executed": mode == "secure" and feature == "login",
        },
        "database_inspector": {
            "table": "users" if feature in {"login", "user_detail"} else "products",
            "operation": "SELECT", "rows_returned": len(rows), "rows_changed": 0,
            "read_only": True, "result_ids": result_ids,
        },
        "result_set_inspector": {
            "expected_filter": normalized_input, "rows_expected": expected_count,
            "rows_returned": len(rows), "result_ids": result_ids, "result_names": result_names,
            "unexpected_data": expected_count is not None and len(rows) > expected_count,
            "other_table_accessed": False, "database_modified": False, "final_decision": decision,
        },
    }


def timeline(*, feature: str, mode: str, raw_input: str, query: dict, rows: list,
             decision: str, error_info: dict | None) -> list[TraceStep]:
    vulnerable = mode == "vulnerable"
    if feature == "login" and vulnerable:
        definitions = [
            ("Browser UI", "Credentials submitted", "Browser captured username and password length", "form submission"),
            ("HTTP Request", "POST created", "Browser sent the real local POST request", "HTTP form encoding"),
            ("Flask Router", "Form read", "Flask read request.form at the login route", "request parsing"),
            ("Input Validation", "Length checked", "Fixed scenario and length policy applied", "trust-boundary validation"),
            ("Password Processing", "Legacy digest created", "Unsalted SHA-256 digest created only for the intentionally weak legacy flow", "legacy digest"),
            ("Query Construction", "SQL concatenated", "Username and masked digest were concatenated into SQL text", "string concatenation"),
            ("Query Construction", "SQL structure evaluated", "Fixed input may change the WHERE condition", "SQL structure change"),
            ("SQLite Parser", "Final SQL parsed", "SQLite parsed the final SQL text", "SQL parsing"),
            ("SQLite Execution", "Result set returned", f"Read-only SELECT returned {len(rows)} row(s)", "local SQLite SELECT"),
            ("Authentication Decision", "First row evaluated", "Server selected a matched demo user when present", "legacy authentication decision"),
            ("Session Management", "Session decision", f"Session outcome: {decision}", "local demo session"),
            ("Final Result", "Security verdict", decision, "security verdict"),
        ]
    elif feature == "login":
        definitions = [
            ("Browser UI", "Credentials submitted", "Browser sent username and password length", "form submission"),
            ("Input Validation", "Length checked", "Server validated username and password length", "trust-boundary validation"),
            ("Query Construction", "Template selected", "Server selected SQL with a placeholder", "prepared statement"),
            ("Query Construction", "Username bound", "Username was bound as a value", "parameter binding"),
            ("SQLite Execution", "Exact user lookup", f"SQLite returned {len(rows)} candidate row(s)", "parameterized SELECT"),
            ("Password Processing", "PBKDF2 verified", "Werkzeug check_password_hash handled verification", "PBKDF2 verification"),
            ("Authentication Decision", "Decision made", decision, "generic authentication decision"),
            ("Session Management", "Session decision", f"Session outcome: {decision}", "session rotation"),
            ("Audit Logging", "Event recorded", "Structured event linked to this trace", "redacted audit logging"),
            ("Final Result", "Security verdict", decision, "security verdict"),
        ]
    elif feature == "search" and vulnerable:
        definitions = [
            ("Browser UI", "Keyword submitted", "Browser sent the local search keyword", "query string submission"),
            ("Flask Router", "Query string read", "Flask read request.args", "request parsing"),
            ("Query Construction", "Keyword concatenated", "Keyword was inserted into LIKE SQL text", "string concatenation"),
            ("Query Construction", "Final SQL created", "SQL structure may be changed by the fixed scenario", "SQL structure change"),
            ("SQLite Parser", "Final SQL parsed", "SQLite interpreted the final SQL text", "SQL parsing"),
            ("SQLite Execution", "Read-only SELECT", f"SQLite returned {len(rows)} product row(s)", "local SQLite SELECT"),
            ("Result Set", "Condition compared", "Actual rows were compared with the intended filter", "result comparison"),
            ("HTTP Response", "Results rendered", "Only product fields were sent to the template", "safe rendering"),
            ("Final Result", "Security verdict", decision, "security verdict"),
        ]
    elif feature == "search":
        definitions = [
            ("Browser UI", "Keyword submitted", "Browser sent the local search keyword", "query string submission"),
            ("Input Validation", "Keyword validated", "Server normalized whitespace and enforced the length limit", "trust-boundary validation"),
            ("Query Construction", "LIKE parameter created", "Server created a percent-wrapped Python value", "value transformation"),
            ("Query Construction", "Parameter bound", "SQLite received SQL template and value separately", "parameter binding"),
            ("SQLite Execution", "Structure preserved", f"Parameterized SELECT returned {len(rows)} row(s)", "parameterized SELECT"),
            ("Result Set", "Expected rows retained", "Rows follow the intended visible-name filter", "result comparison"),
            ("Final Result", "Security verdict", decision, "security verdict"),
        ]
    else:
        definitions = [
            ("HTTP Request", "Request received", "Flask received the real request", "HTTP parsing"),
            ("Input Validation", "Boundary checked", "Input type and range policy applied", "trust-boundary validation"),
            ("Query Construction", "Query prepared", query.get("construction_method", "none"), "query construction"),
            ("SQLite Execution", "Read-only flow", f"Returned {len(rows)} row(s)", "local SQLite SELECT"),
            ("Result Set", "Decision made", decision, "result evaluation"),
            ("Audit Logging", "Evidence linked", "Audit event shares this trace", "structured logging"),
            ("Final Result", "Security verdict", decision, "security verdict"),
        ]
    return [
        TraceStep(
            step_number=index, layer=layer, title=title, description=description,
            technique=technique,
            input_data={"value": raw_input if index in {1, 3, 4} else "[observed]"},
            output_data={"decision": decision, "error_category": (error_info or {}).get("category")},
            code_reference=("vulnerable_queries.py" if vulnerable else "secure_queries.py"),
            security_meaning=("SQL structure is not isolated from data" if vulnerable else "Input remains data"),
            status="error" if error_info and index >= 5 else "observed",
        )
        for index, (layer, title, description, technique) in enumerate(definitions, 1)
    ]
