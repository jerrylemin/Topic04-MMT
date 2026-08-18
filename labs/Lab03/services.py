from flask import session

from audit_service import log_event
from authorization import authorize_invoice, authorize_profile_fields
from database import get_db, query_all, query_one
from trace_service import new_trace, save_trace, step
from validators import ValidationError, email as validate_email, integer, role as validate_role


def get_user(user_id: int) -> dict | None:
    row = query_one("SELECT id, username, email, role, created_at, updated_at FROM users WHERE id = ?", (user_id,))
    return dict(row) if row else None


def list_products() -> list[dict]:
    return [dict(row) for row in query_all("SELECT * FROM products ORDER BY id")]


def get_product(product_id: int) -> dict | None:
    row = query_one("SELECT * FROM products WHERE id = ?", (product_id,))
    return dict(row) if row else None


def cart_for_user(user_id: int) -> list[dict]:
    return [dict(row) for row in query_all(
        """SELECT c.id, c.user_id, c.product_id, c.quantity, p.name, p.price_vnd,
                  c.quantity * p.price_vnd AS line_total
           FROM cart_items AS c JOIN products AS p ON p.id = c.product_id
           WHERE c.user_id = ? ORDER BY c.id""",
        (user_id,),
    )]


def add_to_cart(user_id: int, product_id_value, quantity_value) -> None:
    product_id = integer(product_id_value, "product_id")
    quantity = integer(quantity_value, "quantity", 1, 10)
    product = get_product(product_id)
    if not product:
        raise ValidationError("Sản phẩm không tồn tại.")
    if quantity > product["stock"]:
        raise ValidationError("Số lượng vượt tồn kho.")
    db = get_db()
    db.execute(
        """INSERT INTO cart_items(user_id, product_id, quantity) VALUES (?, ?, ?)
           ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = excluded.quantity""",
        (user_id, product_id, quantity),
    )
    db.commit()


def update_cart(user_id: int, product_id_value, quantity_value) -> None:
    product_id = integer(product_id_value, "product_id")
    quantity = integer(quantity_value, "quantity", 0, 10)
    db = get_db()
    if quantity == 0:
        db.execute("DELETE FROM cart_items WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    else:
        product = get_product(product_id)
        if not product or quantity > product["stock"]:
            raise ValidationError("Sản phẩm hoặc số lượng không hợp lệ.")
        db.execute(
            "UPDATE cart_items SET quantity = ? WHERE user_id = ? AND product_id = ?",
            (quantity, user_id, product_id),
        )
    db.commit()


def _create_invoice(user_id: int, product: dict, quantity: int, unit_price: int) -> dict:
    total = unit_price * quantity
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO invoices(user_id, status, total_amount) VALUES (?, 'demo_paid', ?)",
            (user_id, total),
        )
        invoice_id = cursor.lastrowid
        db.execute(
            """INSERT INTO invoice_items
               (invoice_id, product_id, product_name, unit_price, quantity, line_total)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (invoice_id, product["id"], product["name"], unit_price, quantity, total),
        )
    return get_invoice(invoice_id)


def _checkout_inputs(product_id_value, quantity_value, trace, mode: str) -> tuple[dict, int]:
    try:
        product_id = integer(product_id_value, "product_id")
        quantity = integer(quantity_value, "quantity", 1, 10)
    except ValidationError as exc:
        log_event("invalid_quantity", mode, "deny", str(exc), trace.trace_id,
                  "quantity", "1..10", quantity_value)
        raise
    product = get_product(product_id)
    if not product:
        log_event("invalid_product_id", mode, "deny", "Sản phẩm không tồn tại.", trace.trace_id,
                  "product_id", "existing product", product_id_value)
        raise ValidationError("Sản phẩm không tồn tại.")
    if quantity > product["stock"]:
        log_event("invalid_quantity", mode, "deny", "Số lượng vượt tồn kho.", trace.trace_id,
                  "quantity", product["stock"], quantity)
        raise ValidationError("Số lượng vượt tồn kho.")
    return product, quantity


def vulnerable_checkout(user_id: int, product_id_value, quantity_value, submitted_price_value) -> tuple[dict, dict]:
    trace = new_trace("checkout", "vulnerable")
    product, quantity = _checkout_inputs(product_id_value, quantity_value, trace, "vulnerable")
    submitted_price = integer(submitted_price_value, "price", 0)
    step(trace, "HTTP Request", "Đọc giá client", "Flask đọc price từ request.form.",
         technique="client-controlled hidden field", input_data=submitted_price_value,
         output_data=submitted_price, code_reference='request.form["price"]', status="warning")
    step(trace, "Business Logic", "Tin giá đã gửi", "Server không đối chiếu lại giá database.",
         input_data=submitted_price, output_data=submitted_price * quantity,
         code_reference="total = submitted_price * quantity", security_meaning="Parameter Tampering", status="danger")
    invoice = _create_invoice(user_id, product, quantity, submitted_price)
    mismatch = submitted_price != product["price_vnd"]
    trace.parameter_diff = [{"parameter": "price", "original_value": product["price_vnd"],
                             "submitted_value": submitted_price, "trusted_source": "database",
                             "status": "modified" if mismatch else "unchanged"}]
    trace.database_inspector = {"product_id": product["id"], "database_price": product["price_vnd"],
                                "submitted_price": submitted_price, "stored_unit_price": submitted_price,
                                "quantity": quantity, "stored_total": invoice["total_amount"]}
    trace.final_verdict = {"tampering_type": "checkout price", "success": mismatch,
                           "database_changed": True, "trusted_value": "products.price_vnd",
                           "missing_check": "server-side price lookup", "audit_event": "checkout_price_mismatch" if mismatch else "vulnerable_action_completed",
                           "impact": "Hóa đơn giả lập lưu sai giá." if mismatch else "Hóa đơn dùng giá client."}
    action = "checkout_price_mismatch" if mismatch else "vulnerable_action_completed"
    log_event(action, "vulnerable", "accepted", "Server vulnerable tin giá client.", trace.trace_id,
              "price", product["price_vnd"], submitted_price)
    step(trace, "Database Write", "Tạo invoice", "SQLite lưu unit_price do client gửi.",
         input_data=submitted_price, output_data=invoice["id"], code_reference="_create_invoice(...) ", status="danger" if mismatch else "normal")
    step(trace, "Final Result", "Kết luận", trace.final_verdict["impact"], status="danger")
    return invoice, save_trace(trace)


def secure_checkout(user_id: int, product_id_value, quantity_value, submitted_price_value=None) -> tuple[dict, dict]:
    trace = new_trace("checkout", "secure")
    product, quantity = _checkout_inputs(product_id_value, quantity_value, trace, "secure")
    submitted_price = None
    if submitted_price_value not in (None, ""):
        try:
            submitted_price = int(submitted_price_value)
        except (TypeError, ValueError):
            submitted_price = str(submitted_price_value)
    mismatch = submitted_price is not None and str(submitted_price) != str(product["price_vnd"])
    step(trace, "Authentication", "Lấy danh tính từ session", "Không nhận user_id từ form.",
         input_data=session.get("user_id"), output_data=user_id, code_reference='session["user_id"]', status="safe")
    step(trace, "Input Validation", "Validate product và quantity", "Quantity nằm trong 1..10 và không vượt stock.",
         input_data={"product_id": product_id_value, "quantity": quantity_value}, output_data="valid", status="safe")
    step(trace, "SQLite Query", "Lấy giá tin cậy", "Server truy vấn products.price_vnd bằng product_id.",
         technique="parameterized SQL", input_data=product["id"], output_data=product["price_vnd"],
         code_reference="SELECT * FROM products WHERE id = ?", status="safe")
    if mismatch:
        log_event("checkout_price_mismatch", "secure", "ignored", "Giá client khác giá database.", trace.trace_id,
                  "price", product["price_vnd"], submitted_price)
        step(trace, "Audit Logging", "Ghi price mismatch", "Giá client bị bỏ qua và sự kiện được ghi log.",
             input_data=submitted_price, output_data="checkout_price_mismatch", status="safe")
    invoice = _create_invoice(user_id, product, quantity, product["price_vnd"])
    trace.parameter_diff = [{"parameter": "price", "original_value": product["price_vnd"],
                             "submitted_value": submitted_price, "trusted_value": product["price_vnd"],
                             "status": "ignored" if submitted_price is not None else "not submitted"}]
    trace.database_inspector = {"product_id": product["id"], "database_price": product["price_vnd"],
                                "submitted_price": submitted_price, "stored_unit_price": product["price_vnd"],
                                "quantity": quantity, "stored_total": invoice["total_amount"]}
    trace.final_verdict = {"tampering_type": "checkout price", "success": False,
                           "database_changed": True, "trusted_value": "products.price_vnd",
                           "control": "server-side price lookup", "audit_event": "checkout_price_mismatch" if mismatch else "secure_action_completed",
                           "impact": "Giá client bị bỏ qua; invoice lưu giá database."}
    log_event("secure_action_completed", "secure", "allowed", "Invoice dùng giá database.", trace.trace_id,
              "price", product["price_vnd"], submitted_price)
    step(trace, "Database Write", "Tạo invoice đúng giá", "Transaction lưu giá lấy từ database.",
         input_data=product["price_vnd"], output_data=invoice["id"], status="safe")
    step(trace, "Final Result", "Kết luận", trace.final_verdict["impact"], status="safe")
    return invoice, save_trace(trace)


def get_invoice(invoice_id: int) -> dict | None:
    row = query_one("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    if not row:
        return None
    invoice = dict(row)
    invoice["items"] = [dict(item) for item in query_all(
        "SELECT * FROM invoice_items WHERE invoice_id = ? ORDER BY id", (invoice_id,)
    )]
    return invoice


def vulnerable_invoice(user_id: int, invoice_id_value) -> tuple[dict | None, dict]:
    invoice_id = integer(invoice_id_value, "invoice_id")
    trace = new_trace("invoice", "vulnerable")
    invoice = get_invoice(invoice_id)
    owner_id = invoice["user_id"] if invoice else None
    unauthorized = invoice is not None and owner_id != user_id and session.get("role") != "admin"
    step(trace, "SQLite Query", "Truy vấn chỉ theo ID", "Server không ràng buộc invoice với user trong session.",
         technique="parameterized SQL", input_data=invoice_id, output_data={"owner_id": owner_id},
         code_reference="SELECT * FROM invoices WHERE id = ?", status="danger" if unauthorized else "warning")
    trace.authorization_inspector = {"subject": f"user_id {user_id}", "action": "read invoice",
                                     "object": f"invoice {invoice_id}", "object_owner": owner_id,
                                     "policy": "none", "decision": "not checked", "reason": "Vulnerable route bỏ qua ownership."}
    trace.database_inspector = {"invoice_id": invoice_id, "owner_id": owner_id, "current_user_id": user_id,
                                "ownership_match": owner_id == user_id, "authorization_result": "not checked"}
    trace.final_verdict = {"tampering_type": "invoice ID / IDOR", "success": unauthorized,
                           "unauthorized_resource_disclosed": unauthorized, "database_changed": False,
                           "missing_check": "object-level authorization", "audit_event": "vulnerable_action_completed"}
    log_event("vulnerable_action_completed", "vulnerable", "accepted", "Không kiểm tra owner invoice.", trace.trace_id,
              "invoice_id", 1001 if user_id == 12 else "own invoice", invoice_id)
    step(trace, "HTTP Response", "Trả invoice", "Nội dung được trả trước khi kiểm tra ownership.",
         output_data={"invoice_id": invoice_id, "data_returned": bool(invoice)}, status="danger" if unauthorized else "normal")
    return invoice, save_trace(trace)


def secure_invoice(user_id: int, role: str, invoice_id_value) -> tuple[dict | None, dict, int]:
    invoice_id = integer(invoice_id_value, "invoice_id")
    trace = new_trace("invoice", "secure")
    owner_row = query_one("SELECT user_id FROM invoices WHERE id = ?", (invoice_id,))
    owner_id = owner_row["user_id"] if owner_row else None
    decision = authorize_invoice(user_id, role, invoice_id, owner_id)
    step(trace, "Authentication", "Lấy user từ session", "Danh tính không lấy từ query string.",
         input_data=session.get("user_id"), output_data=user_id, status="safe")
    step(trace, "Authorization", "Kiểm tra object-level authorization", decision.reason,
         input_data={"subject": user_id, "owner": owner_id}, output_data=decision.decision,
         code_reference="authorize_invoice(...) ", status="safe" if decision.decision == "allow" else "blocked")
    invoice = None
    status = 404 if owner_id is None else 200
    if decision.decision == "allow":
        if role == "admin":
            invoice = get_invoice(invoice_id)
        else:
            scoped = query_one("SELECT id FROM invoices WHERE id = ? AND user_id = ?", (invoice_id, user_id))
            invoice = get_invoice(scoped["id"]) if scoped else None
        log_event("secure_action_completed", "secure", "allowed", decision.reason, trace.trace_id,
                  "invoice_id", "owned invoice", invoice_id)
    elif owner_id is not None:
        status = 403
        log_event("invoice_access_denied", "secure", "denied", decision.reason, trace.trace_id,
                  "invoice_id", "owned invoice", invoice_id)
        log_event("authorization_denied", "secure", "denied", decision.reason, trace.trace_id,
                  "invoice_id", owner_id, invoice_id)
    trace.authorization_inspector = decision.to_dict()
    trace.database_inspector = {"invoice_id": invoice_id, "owner_id": owner_id, "current_user_id": user_id,
                                "ownership_match": owner_id == user_id, "authorization_result": decision.decision}
    trace.final_verdict = {"tampering_type": "invoice ID / IDOR", "success": False,
                           "unauthorized_resource_disclosed": False, "database_changed": False,
                           "control": "object-level authorization", "http_status": status,
                           "audit_event": "invoice_access_denied" if status == 403 else "secure_action_completed"}
    step(trace, "HTTP Response", "Trả kết quả", "Không trả nội dung invoice khi policy deny.",
         output_data={"status": status, "data_returned": invoice is not None}, status="blocked" if status == 403 else "safe")
    return invoice, save_trace(trace), status


def vulnerable_profile(current_user_id: int, submitted_user_id, submitted_email: str, submitted_role: str) -> tuple[dict, dict]:
    target_user_id = integer(submitted_user_id, "user_id")
    valid_email = validate_email(submitted_email)
    valid_role = validate_role(submitted_role)
    before = get_user(target_user_id)
    if not before:
        raise ValidationError("User mục tiêu không tồn tại.")
    trace = new_trace("profile", "vulnerable")
    db = get_db()
    db.execute("UPDATE users SET email = ?, role = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
               (valid_email, valid_role, target_user_id))
    db.commit()
    after = get_user(target_user_id)
    if target_user_id == current_user_id:
        session["role"] = after["role"]
    escalated = before["role"] != "admin" and after["role"] == "admin"
    trace.parameter_diff = [
        {"parameter": "user_id", "original_value": current_user_id, "submitted_value": target_user_id,
         "status": "modified" if target_user_id != current_user_id else "unchanged"},
        {"parameter": "role", "original_value": before["role"], "submitted_value": valid_role,
         "status": "sensitive field modified" if before["role"] != valid_role else "unchanged"},
    ]
    trace.database_inspector = {"target_user_id_from_form": target_user_id, "current_user_id_from_session": current_user_id,
                                "submitted_role": valid_role, "role_before": before["role"], "role_after": after["role"],
                                "accepted_fields": ["user_id", "email", "role"], "rejected_fields": []}
    trace.authorization_inspector = {"subject": f"user_id {current_user_id}", "action": "update role",
                                     "object": f"user {target_user_id}", "policy": "none", "decision": "not checked",
                                     "reason": "Mass assignment dùng trực tiếp user_id và role từ form."}
    trace.final_verdict = {"tampering_type": "role / mass assignment", "success": escalated,
                           "privilege_escalated": escalated, "database_changed": True,
                           "missing_check": "field allowlist and admin authorization", "audit_event": "vulnerable_action_completed"}
    log_event("vulnerable_action_completed", "vulnerable", "accepted", "Mass assignment chấp nhận role client.",
              trace.trace_id, "role", before["role"], valid_role)
    step(trace, "Database Write", "Mass assignment", "Email và role từ form được cập nhật trực tiếp.",
         input_data={"user_id": target_user_id, "role": valid_role}, output_data=after,
         code_reference="UPDATE users SET email = ?, role = ? WHERE id = ?", status="danger")
    step(trace, "Final Result", "Kết luận", "Role đã bị nâng trong phiên bản vulnerable." if escalated else "Form client quyết định role.", status="danger")
    return after, save_trace(trace)


def secure_profile(current_user_id: int, form) -> tuple[dict, dict]:
    trace = new_trace("profile", "secure")
    valid_email = validate_email(form.get("email", ""))
    submitted_fields = set(form.keys())
    rejected = sorted(submitted_fields - {"email"})
    before = get_user(current_user_id)
    decision = authorize_profile_fields(current_user_id, submitted_fields)
    if "user_id" in form and str(form.get("user_id")) != str(current_user_id):
        log_event("target_user_mismatch", "secure", "ignored", "user_id form không xác định danh tính.",
                  trace.trace_id, "user_id", current_user_id, form.get("user_id"))
    for name in rejected:
        action = "sensitive_field_submitted" if name in {"role", "is_admin", "balance", "user_id"} else "unknown_parameter"
        log_event(action, "secure", "ignored", "Trường không thuộc allowlist self-service.", trace.trace_id,
                  name, before.get(name, "not accepted"), form.get(name))
    db = get_db()
    db.execute("UPDATE users SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (valid_email, current_user_id))
    db.commit()
    after = get_user(current_user_id)
    trace.parameter_diff = [{"parameter": key, "submitted_value": form.get(key),
                             "status": "accepted" if key == "email" else "rejected"} for key in form.keys()]
    trace.database_inspector = {"target_user_id_from_form": form.get("user_id"), "current_user_id_from_session": current_user_id,
                                "submitted_role": form.get("role"), "role_before": before["role"], "role_after": after["role"],
                                "accepted_fields": ["email"], "rejected_fields": rejected}
    trace.authorization_inspector = decision.to_dict()
    trace.final_verdict = {"tampering_type": "role / mass assignment", "success": False,
                           "privilege_escalated": False, "database_changed": before["email"] != after["email"],
                           "control": "session identity and field allowlist",
                           "audit_event": "sensitive_field_submitted" if rejected else "secure_action_completed"}
    log_event("secure_action_completed", "secure", "allowed", "Chỉ email được cập nhật.", trace.trace_id,
              "email", before["email"], valid_email)
    step(trace, "Input Validation", "Áp dụng field allowlist", "Chỉ email được chấp nhận; role và user_id bị loại.",
         input_data=dict(form), output_data={"accepted": ["email"], "rejected": rejected}, status="safe")
    step(trace, "Database Write", "Cập nhật email của session user", "Role không xuất hiện trong UPDATE.",
         code_reference="UPDATE users SET email = ? WHERE id = ?", output_data=after, status="safe")
    return after, save_trace(trace)


CODE_COMPARISONS = {
    "checkout": {
        "vulnerable": 'submitted_price = int(request.form["price"])\ntotal = submitted_price * quantity',
        "secure": 'product = get_product(product_id)\nserver_price = product["price_vnd"]\ntotal = server_price * quantity',
    },
    "idor": {
        "vulnerable": "invoice = get_invoice(invoice_id)",
        "secure": "SELECT id FROM invoices WHERE id = ? AND user_id = ?",
    },
    "profile": {
        "vulnerable": "UPDATE users SET email = ?, role = ? WHERE id = ?",
        "secure": "UPDATE users SET email = ? WHERE id = ?",
    },
}
