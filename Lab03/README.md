# Lab03 - Parameter Tampering

Ứng dụng Flask/SQLite local minh họa ba lỗi: sửa giá checkout, IDOR hóa đơn và mass assignment `role`. Mỗi luồng có bản vulnerable/secure, trace, inspector và audit thật.

## Phạm vi an toàn

- Chỉ chạy tại `http://127.0.0.1:5003` với dữ liệu giả lập.
- Không gọi Internet, không nhận host/URL tùy ý, không có thanh toán hoặc email thật.
- Không dùng Playwright/Selenium; ảnh được chụp thủ công.

## Chạy ứng dụng

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/reset_database.py
python app.py
```

Tài khoản: `user_a / UserA123!`, `user_b / UserB123!`, `admin / Admin123!`.

Route chính: `/login`, `/products`, `/cart`, `/vulnerable/checkout`, `/secure/checkout`, `/vulnerable/invoice?id=1001`, `/secure/invoice?id=1001`, `/vulnerable/profile`, `/secure/profile`, `/audit-logs`.

Giao diện hiện có vẫn giữ Request Tampering Console, Presentation Mode, Authorization Inspector và Database Inspector để đọc trace; các thành phần này không làm tăng số ảnh bắt buộc.

## Evidence và báo cáo

Lab03 yêu cầu **8 ảnh** theo [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md). Danh sách cũ được lưu tại [LEGACY_SCREENSHOTS.md](LEGACY_SCREENSHOTS.md).

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/run_demo_flows.py
python scripts/generate_report.py
```

Report:

- `report/21127645_LeMinh_Lab03_ParameterTampering.docx`
- `report/21127645_LeMinh_Lab03_ParameterTampering.pdf`

Thiếu ảnh thì report vẫn có placeholder chi tiết tại đúng phần. Đặt PNG hợp lệ đúng tên vào `evidence/screenshots/` và chạy lại generator để tự chèn ảnh thật.

## Kiểm thử

```powershell
python -m compileall .
python -m pytest -q
```

Không sửa hoặc xóa source vulnerable/secure, trace, inspector, audit, database demo và Docker configuration.
