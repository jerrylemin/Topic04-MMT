# Lab04 - Cross-Site Request Forgery (CSRF)

Hai ứng dụng Flask local minh họa đổi email thiếu CSRF token và bản secure dùng synchronizer token, exact Origin/Referer validation, audit và trace thật.

## Phạm vi an toàn

- Victim Application: `http://127.0.0.1:5004`.
- Demo Page cố định: `http://127.0.0.1:9004`.
- Chỉ bind loopback; không Internet, target tùy ý, auto-submit, browser automation hoặc ảnh giả.

## Chạy ứng dụng

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/reset_database.py
python run_both.py
```

Tài khoản: `victim / Victim123!` và `receiver / Receiver123!`.

Route chính: `/login`, `/dashboard`, `/vulnerable/change-email`, `/secure/change-email`, `/audit-logs`; Demo Page có `/attack/vulnerable-email`, `/attack/secure-email`, `/attack/bad-token`.

## Evidence và báo cáo

Lab04 yêu cầu **7 ảnh** theo [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md).

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/export_evidence.py
python scripts/generate_report.py
```

Report:

- `report/21127645_LeMinh_Lab04_CSRF.docx`
- `report/21127645_LeMinh_Lab04_CSRF.pdf`

Khi thiếu ảnh, DOCX/PDF vẫn có placeholder chi tiết đúng vị trí. Đặt PNG hợp lệ đúng tên vào `evidence/screenshots/`, rồi chạy lại generator để tự thay bằng ảnh thật.

## Kiểm thử

```powershell
python -m compileall .
python -m pytest -q
```

Không xóa source vulnerable/secure, trace, audit, inspector, database demo hoặc Docker configuration.
