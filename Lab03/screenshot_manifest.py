"""Single source of truth for the manual screenshot guide and report."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent


def shot(filename, purpose, url, required, *, account="user_a", original="Không áp dụng", modified="Không sửa", button="Mở trang", panel="Không bắt buộc", step="Không bắt buộc", expected=None):
    return {
        "filename": filename,
        "purpose": purpose,
        "precondition": "Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.",
        "account": account,
        "url": url,
        "original": original,
        "modified": modified,
        "button": button,
        "panel": panel,
        "step": step,
        "required": required,
        "expected": expected or required,
        "caption": f"{purpose}. {required}",
        "errors": "Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.",
    }


SCREENSHOTS = [
    shot("01_home_overview.png", "Tổng quan Lab03", "/", "Ba bài thực hành checkout, IDOR và role tampering.", account="Chưa bắt buộc"),
    shot("02_login_user_a.png", "Tài khoản mẫu User A", "/login", "Thông tin user_a và cảnh báo chỉ dùng dữ liệu lab.", account="Chưa đăng nhập"),
    shot("03_products_database_price.png", "Giá tin cậy từ database", "/products", "Sản phẩm 5 có giá 100000 VND."),
    shot("04_cart_before_checkout.png", "Giỏ hàng trước checkout", "/cart", "User A có sản phẩm 5, số lượng 1.", button="Thêm vào giỏ"),
    shot("05_checkout_original_parameters.png", "Tham số checkout gốc", "/vulnerable/checkout", "product_id=5, quantity=1, price=100000.", original="price=100000", panel="Parameter Inspector"),
    shot("06_checkout_hidden_price_devtools.png", "Hidden field vẫn do client kiểm soát", "/vulnerable/checkout", "DevTools Elements hiển thị hidden price=100000.", original="price=100000", panel="DevTools Elements"),
    shot("07_checkout_price_modified.png", "So sánh giá trước và sau sửa", "/vulnerable/checkout", "Parameter Diff đánh dấu price modified.", original="price=100000", modified="price=1", panel="Parameter Diff"),
    shot("08_checkout_tampered_request.png", "Request checkout đã bị sửa", "/vulnerable/checkout", "Request Inspector hiển thị price=1.", original="price=100000", modified="price=1", button="Gửi vulnerable request", panel="Request Inspector", step="HTTP Request"),
    shot("09_checkout_vulnerable_server_logic.png", "Server lỗi tin submitted price", "/vulnerable/checkout", "Bước Business Logic dùng request.form['price'].", original="price=100000", modified="price=1", panel="Timeline", step="Business Logic"),
    shot("10_checkout_wrong_invoice.png", "Invoice sai giá", "/vulnerable/checkout", "Invoice mới có total 1 VND.", original="price=100000", modified="price=1", panel="Final Result"),
    shot("11_checkout_vulnerable_database.png", "Database lưu giá sai", "/vulnerable/checkout", "unit_price=1 và total=1.", original="price=100000", modified="price=1", panel="Database Inspector", step="Database Write"),
    shot("12_checkout_vulnerable_verdict.png", "Kết luận checkout vulnerable", "/vulnerable/checkout", "Parameter Tampering thành công.", original="price=100000", modified="price=1", panel="Final Security Verdict"),
    shot("13_checkout_secure_request.png", "Cùng request gửi vào route secure", "/secure/checkout", "Request vẫn có price=1 nhưng được đánh dấu untrusted.", original="price=100000", modified="price=1", button="Gửi secure request", panel="Request Inspector"),
    shot("14_checkout_secure_database_lookup.png", "Secure lookup giá server", "/secure/checkout", "SQLite Query lấy products.price_vnd=100000.", original="price=100000", modified="price=1", panel="Timeline", step="SQLite Query"),
    shot("15_checkout_price_mismatch.png", "Phát hiện price mismatch", "/secure/checkout", "submitted_price=1 khác database_price=100000.", original="price=100000", modified="price=1", panel="Parameter Diff"),
    shot("16_checkout_secure_invoice.png", "Invoice secure đúng giá", "/secure/checkout", "Invoice có total 100000 VND.", original="price=100000", modified="price=1", panel="Database Inspector"),
    shot("17_checkout_audit_log.png", "Audit checkout tampering", "/audit-logs", "Event checkout_price_mismatch cùng trace ID.", original="price=100000", modified="price=1", panel="Audit Inspector"),
    shot("18_invoice_user_a_1001.png", "Owner xem invoice của mình", "/vulnerable/invoice?id=1001", "Invoice 1001 thuộc user_id 12."),
    shot("19_invoice_id_changed.png", "Invoice ID bị đổi", "/vulnerable/invoice?id=1002", "Parameter Diff đánh dấu object reference changed.", original="id=1001", modified="id=1002", panel="Parameter Diff"),
    shot("20_invoice_idor_request.png", "Request IDOR", "/vulnerable/invoice?id=1002", "GET query id=1002.", original="id=1001", modified="id=1002", panel="Request Inspector", step="HTTP Request"),
    shot("21_invoice_idor_database.png", "Owner không khớp session", "/vulnerable/invoice?id=1002", "owner_id=13 và session user_id=12.", original="id=1001", modified="id=1002", panel="Database Inspector"),
    shot("22_invoice_idor_success.png", "IDOR vulnerable thành công", "/vulnerable/invoice?id=1002", "User A thấy invoice giả lập của User B.", original="id=1001", modified="id=1002", panel="Final Security Verdict"),
    shot("23_invoice_secure_authorization.png", "Object-level authorization", "/secure/invoice?id=1002", "Policy owner or admin đưa ra decision deny.", original="id=1001", modified="id=1002", panel="Authorization Inspector", step="Authorization"),
    shot("24_invoice_secure_403.png", "Secure IDOR bị chặn", "/secure/invoice?id=1002", "HTTP 403 và không có dòng hàng invoice 1002.", original="id=1001", modified="id=1002", panel="HTTP Response"),
    shot("25_invoice_access_denied_log.png", "Audit IDOR denied", "/audit-logs", "Event invoice_access_denied cùng trace ID.", original="id=1001", modified="id=1002", panel="Audit Inspector"),
    shot("26_profile_original_fields.png", "Các trường profile vulnerable", "/vulnerable/profile", "Form có user_id=12, email và role=user.", original="role=user", panel="Parameter Inspector"),
    shot("27_profile_role_modified.png", "Role bị sửa phía client", "/vulnerable/profile", "Parameter Diff đánh dấu role là sensitive field modified.", original="role=user", modified="role=admin", panel="Parameter Diff"),
    shot("28_profile_tampered_request.png", "Request profile bị sửa", "/vulnerable/profile", "POST chứa role=admin.", original="role=user", modified="role=admin", panel="Request Inspector", step="HTTP Request"),
    shot("29_profile_vulnerable_update.png", "Mass assignment đổi database", "/vulnerable/profile", "Role trước user, role sau admin.", original="role=user", modified="role=admin", panel="Database Inspector", step="Database Write"),
    shot("30_profile_privilege_escalation.png", "Nâng quyền vulnerable", "/vulnerable/profile", "UI và session hiển thị role admin.", original="role=user", modified="role=admin", panel="Final Security Verdict"),
    shot("31_profile_secure_field_allowlist.png", "Secure field allowlist", "/secure/profile", "accepted_fields=email; rejected_fields có role.", original="role=user", modified="role=admin", panel="Authorization Inspector", step="Input Validation"),
    shot("32_profile_secure_role_unchanged.png", "Role secure không đổi", "/secure/profile", "Database giữ role=user.", original="role=user", modified="role=admin", panel="Database Inspector"),
    shot("33_code_comparison_checkout.png", "So sánh code checkout", "/comparison", "Code chạy thật cho client price và database price.", panel="Code Comparison"),
    shot("34_code_comparison_idor.png", "So sánh code IDOR", "/comparison", "Query theo id so với query theo id và owner.", panel="Code Comparison"),
    shot("35_code_comparison_role.png", "So sánh mass assignment", "/comparison", "Submitted role so với allowlist email.", panel="Code Comparison"),
    shot("36_parameter_tampering_vs_sqli.png", "Phân biệt với SQL Injection", "/comparison", "Bảng nêu khác mục tiêu, kỹ thuật và bản vá.", panel="Comparison Table"),
    shot("37_security_controls.png", "Các lớp kiểm soát", "/security-controls", "Server price, session identity, authorization, allowlist và audit.", panel="Security Control Panel"),
    shot("38_audit_logs_overview.png", "Audit ba tình huống", "/audit-logs", "Có checkout mismatch, IDOR denied và sensitive field submitted.", panel="Audit Inspector"),
    shot("39_presentation_mode.png", "Trình chiếu trace", "/secure/invoice?id=1002", "Một bước Authorization ở cỡ chữ lớn và có thanh tiến trình.", panel="Presentation Mode", step="Authorization"),
    shot("40_pytest_passed.png", "Kết quả kiểm thử", "Terminal local", "Dòng tổng kết pytest đạt.", account="Không áp dụng", button="Chạy pytest"),
    shot("41_report_files.png", "Artifact báo cáo", "Thư mục report", "DOCX và PDF đúng tên.", account="Không áp dụng", button="Chạy scripts/generate_report.py"),
]


def write_guide(path: Path | None = None) -> Path:
    path = path or ROOT / "HUONG_DAN_CHUP_ANH.md"
    intro = """# Hướng dẫn chụp ảnh thủ công Lab03

Không dùng Playwright/Selenium và không tự động chụp ảnh. Chỉ chụp dữ liệu giả lập tại `http://127.0.0.1:5003`. Lưu PNG không dấu, không khoảng trắng trong `evidence/screenshots/`; không chụp tab cá nhân hay website thật.

## Chuẩn bị

1. Chạy `python app.py`, reset bằng `python scripts/reset_database.py`.
2. Đăng nhập User A bằng `user_a / UserA123!` hoặc User B bằng `user_b / UserB123!` khi mục ảnh yêu cầu.
3. Mở DevTools bằng F12; dùng Elements để sửa hidden field, Network để xem request, Application/Storage để xem cờ cookie.
4. Có thể dùng Request Tampering Console trong app, chỉ gọi route cố định localhost.
5. Mở Timeline, chọn inspector cần thiết; bật Presentation Mode khi chụp ảnh 39.
6. Xóa trace hoặc reset lab trước khi làm lại một luồng để bằng chứng không lẫn trạng thái.

"""
    fields = [("Mục đích", "purpose"), ("Điều kiện ban đầu", "precondition"), ("Tài khoản", "account"), ("URL", "url"), ("Dữ liệu gốc", "original"), ("Dữ liệu cần sửa", "modified"), ("Nút cần bấm", "button"), ("Panel cần mở", "panel"), ("Bước timeline", "step"), ("Nội dung bắt buộc", "required"), ("Kết quả mong đợi", "expected"), ("Caption báo cáo", "caption"), ("Lỗi thường gặp và cách làm lại", "errors")]
    sections = []
    for item in SCREENSHOTS:
        body = "\n".join(f"- **{label}:** {item[key]}" for label, key in fields)
        sections.append(f"## {item['filename']}\n\n{body}\n")
    path.write_text(intro + "\n".join(sections), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(write_guide())
