# LAB04 - CROSS-SITE REQUEST FORGERY (CSRF)

Sinh viên: **21127645 - Lê Minh**.

Lab04 là hai ứng dụng Flask local minh họa đúng một hành vi vulnerable (đổi email thiếu CSRF token) và bản secure dùng Synchronizer Token Pattern, exact Origin/Referer validation, audit và trace từ SQLite thật.

## Phạm vi an toàn

- Victim Application: `http://127.0.0.1:5004`.
- Demo Page: `http://127.0.0.1:9004` hoặc `http://localhost:9004`.
- Chỉ bind loopback; runtime không gọi Internet và không nhận URL/host/port/route tùy ý.
- Demo Page chỉ có form local cố định; form chỉ gửi khi người dùng bấm và xác nhận.
- Không auto-submit, fetch/XHR cross-origin, iframe, `document.cookie`, browser automation hoặc ảnh giả.
- Đổi mật khẩu và chuyển số dư chỉ tồn tại dưới dạng chức năng phòng thủ trong Victim Application.

## Kiến trúc và cấu trúc

```text
Browser
├─ Victim Application :5004
│  └─ Flask session → Origin/Referer → CSRF → validation → SQLite → audit/trace
└─ Demo Page :9004
   └─ fixed HTML forms → Victim email routes
```

- `victim_app.py`, `attacker_app.py`, `run_both.py`: entry points.
- `auth.py`, `csrf_service.py`, `origin_service.py`, `security_utils.py`: kiểm soát bảo mật.
- `database.py`, `schema.sql`, `seed.py`: SQLite và dữ liệu demo.
- `audit_service.py`, `trace_models.py`, `trace_service.py`: audit/trace có redaction.
- `victim_templates/`, `attacker_templates/`, `static/`: UI, inspectors, timeline, Presentation Mode.
- `scripts/`: evidence, smoke test, report và cleanup.
- `tests/`: kiểm thử hành vi và acceptance.
- `evidence/`: trace/request/response/audit/state/log thật.
- `report/`: DOCX/PDF hoàn chỉnh không phụ thuộc ảnh.

## Tài khoản demo

| Username | Password | Email ban đầu | Balance |
|---|---|---|---:|
| `victim` | `Victim123!` | `victim_old@lab.local` | 1,000,000 |
| `receiver` | `Receiver123!` | `receiver@lab.local` | 500,000 |

Password được hash bằng Werkzeug; token, cookie và password không được ghi đầy đủ vào audit/evidence.

## Cài đặt và chạy

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python run_both.py
```

Reset từ command line: `python scripts/reset_database.py`. Trên UI, login rồi bấm Reset; route yêu cầu Origin/Referer và CSRF token.

## Chạy các flow

1. Mở `/login`, dùng tài khoản `victim`.
2. Vulnerable: mở Demo Page `/attack/vulnerable-email`, bấm gửi và xác nhận. Form POST cố định gửi `demo_changed@lab.local`; route không token/Origin check.
3. Secure missing token: `/attack/secure-email`; server trả 403 và state không đổi.
4. Secure invalid token: `/attack/bad-token`; server trả 403.
5. Secure success: mở Victim `/secure/change-email`; hidden token hợp lệ, Origin/Referer hợp lệ, token rotate sau UPDATE.
6. Logout/reset: chỉ thành công khi form chứa token hợp lệ; denial giữ session/database và tạo audit + trace.

## Đọc timeline, inspectors và audit

- Timeline hiển thị từng bước với timestamp, layer, technique, input/output, code reference, security meaning và status.
- Request Inspector lấy URL/header/form đã che từ request trace.
- Cookie Inspector lấy flags từ `app.config` và host/cookie presence từ request.
- Token Inspector mask ở server; Origin Inspector dùng exact validation result.
- State Inspector đọc `state_history`; Code Comparison trích source thật bằng AST.
- Presentation Mode chỉ trình bày trace đã có; Auto Play không gửi request hay đổi database.
- `/audit-logs` lọc theo action, decision, mode, username và trace ID.

## SameSite, SOP và CORS

- `127.0.0.1:9004 → 127.0.0.1:5004`: cross-origin, same-site.
- `localhost:9004 → 127.0.0.1:5004`: cross-origin, cross-site.
- `Expected` là suy luận từ policy; `Observed` phải lấy từ request/browser thật; `Not observed` nghĩa là chưa xác minh bằng browser.
- SOP kiểm soát script đọc response, không ngăn form gửi. Phần này chỉ giải thích lý thuyết; dự án không tự động điều khiển browser.
- SameSite là lớp bổ sung; token server-side vẫn là lớp chính. CORS không phải bản vá CSRF vì HTML form không cần CORS để submit.

## Kiểm thử, evidence, report và cleanup

```powershell
python -m pytest -q
python -m pytest -q --cov=csrf_service --cov=origin_service --cov=audit_service --cov=trace_service --cov=database --cov=auth --cov-report=term-missing
python scripts/export_evidence.py
python scripts/run_runtime_smoke_test.py
python scripts/generate_report.py
python scripts/clean_submission.py
```

`run_runtime_smoke_test.py` chỉ gọi hai endpoint loopback cố định và không tuyên bố kiểm tra SameSite/SOP của browser. `generate_report.py` đọc evidence/source thật và tạo lại cùng một nội dung dưới DOCX/PDF. `clean_submission.py` xóa cache/file tạm nhưng giữ source, database demo, evidence, tests, README và report.

## Quyết định tối giản

Lab dùng Flask session, Python stdlib (`secrets`, `hmac`, `urllib.parse`, `ast`) và SQLite trực tiếp. Không thêm framework frontend, CSRF framework, browser driver hay dịch vụ ngoài.
