# LAB 3 - Parameter Tampering

Ứng dụng Flask/SQLite chạy độc lập tại `http://127.0.0.1:5003`, minh họa ba lỗi logic bằng dữ liệu giả lập: sửa giá checkout, IDOR hóa đơn và mass assignment `role=admin`. Mỗi tình huống có bản vulnerable, bản secure, audit log, trace thật, inspector, code comparison và Final Security Verdict.

**Nhóm sinh viên thực hiện:** Lê Minh — 21127645 và Nguyễn Vũ Bách — 21127224. Nguồn yêu cầu: `../BaiTapTopic04.docx`, slide 14-18 của `../Topic04_Lo-Hong-Bao-Mat-Ung-Dung-Web.pptx` và đặc tả Lab03 đính kèm.

## Phạm vi an toàn

- Khi chạy trực tiếp, Flask chỉ bind `127.0.0.1`. Trong Docker, Flask nghe interface container để bridge hoạt động, còn Compose chỉ publish `127.0.0.1:5003`, nên dịch vụ vẫn không lộ ra mạng ngoài host.
- Không gọi Internet, không nhận host/URL tùy ý, không quét ID ngoài dữ liệu mẫu.
- Không thanh toán, chuyển tiền, gửi email, thu thập tài khoản hay dữ liệu thật.
- Bản vulnerable chỉ dùng trong Lab03. Mọi SQL vẫn parameterized để không tạo SQL Injection ngoài mục tiêu bài.

## Kiến trúc

`Browser/Jinja -> Flask route -> Session authentication -> Validation -> Business logic -> Object authorization -> SQLite transaction -> Audit + Trace -> Response`

- `app.py`: route, security headers và bind local.
- `services.py`: cart và ba cặp vulnerable/secure.
- `database.py`, `schema.sql`, `seed.py`: SQLite và dữ liệu cố định.
- `authorization.py`, `validators.py`: owner-or-admin, field allowlist và validation.
- `audit_service.py`, `trace_service.py`: log bất thường và timeline/inspector.
- `templates/`, `static/`: UI, Request Tampering Console và Presentation Mode.
- `scripts/`: reset, fixed-scenario client, demo/evidence, screenshot checker, report generator.

## Tài khoản demo

| ID | Username | Password | Email | Role |
|---:|---|---|---|---|
| 12 | `user_a` | `UserA123!` | `usera@lab.local` | user |
| 13 | `user_b` | `UserB123!` | `userb@lab.local` | user |
| 1 | `admin` | `Admin123!` | `admin@lab.local` | admin |

Password chỉ xuất hiện trong README/login để phục vụ lab; database lưu hash Werkzeug, không lưu plaintext.

## Dữ liệu mẫu

| Product | Giá | Stock |
|---|---:|---:|
| 5 - USB Security Key | 100000 VND | 20 |
| 6 - Wireless Mouse | 250000 VND | 15 |
| 7 - Mechanical Keyboard | 1200000 VND | 10 |
| 8 - Lab Laptop | 15000000 VND | 5 |

Invoice 1001 và 1003 thuộc User A; invoice 1002 thuộc User B.

## Chạy ứng dụng

Python 3.11 trở lên:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python app.py
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

Hoặc dùng `scripts/run_lab.ps1`, `scripts/run_lab.bat`, `scripts/run_lab.sh`. Docker dùng `docker compose up --build`; compose chỉ publish `127.0.0.1:5003:5003`, chạy non-root, drop capability và không dùng host network/privileged. `LAB03_SECRET_KEY` có giá trị demo ổn định để session không mất sau restart; khi dùng ngoài lab local phải override biến này.

## URL demo

- `/login`, `/products`, `/products/5`, `/cart`
- `/vulnerable/checkout`, `/secure/checkout`
- `/vulnerable/invoice?id=1001`, `/secure/invoice?id=1001`
- `/vulnerable/profile`, `/secure/profile`
- `/comparison`, `/security-controls`, `/audit-logs`, `/health`
- `/api/trace/<trace_id>` và `POST /api/trace/clear`

Mọi route thực hành yêu cầu đăng nhập. Admin có policy xem invoice bất kỳ; user thường chỉ xem invoice của mình trong secure mode.

## Ba luồng thực hành

### 1. Checkout price tampering

1. Đăng nhập User A, thêm product 5 số lượng 1.
2. Mở `/vulnerable/checkout`; giá hidden gốc là `100000`.
3. Dùng Parameter Diff/DevTools sửa `price=1`, gửi request. Bản vulnerable tạo invoice `total=1`, `unit_price=1`.
4. Gửi cùng dữ liệu tới `/secure/checkout`. Server bỏ qua giá client, lấy `products.price_vnd=100000`, tạo invoice đúng và ghi `checkout_price_mismatch`.

### 2. Invoice IDOR

1. User A mở `/vulnerable/invoice?id=1001`, sau đó đổi thành `id=1002`.
2. Bản vulnerable chỉ query theo id nên trả invoice User B.
3. Mở `/secure/invoice?id=1002`. Policy owner-or-admin trả HTTP 403, không render nội dung invoice và ghi `invoice_access_denied`.

### 3. Role tampering

1. Mở `/vulnerable/profile`; sửa hidden `role=user` thành `role=admin`.
2. Bản vulnerable mass-assign email/role/user_id, đổi database và session thành admin.
3. Reset lab, rồi thêm `role=admin` vào POST secure. Server lấy user_id từ session, chỉ allowlist `email`, giữ role=user và ghi `sensitive_field_submitted`.

## Request Tampering Console và Inspector

Console chỉ có ba scenario và route cố định; không có ô host, URL hay header tùy ý. Parameter Diff đặt giá trị gốc cạnh giá trị gửi. Sau mỗi request:

- Request Inspector: method, path, query/form, handler, parameter trust; cookie bị che.
- Session Inspector: user_id/username/role và cờ cookie; không lộ secret/cookie đầy đủ.
- Server Decision/Database Inspector: dữ liệu server, dữ liệu client, query và database write.
- Authorization Inspector: subject, action, object, owner, policy, decision, reason.
- Audit Inspector: event, parameter, original/submitted value và trace ID.
- Code Comparison và Final Security Verdict: code đang chạy, kiểm tra thiếu/bản vá và tác động.

Timeline dùng màu cho normal, untrusted, vulnerable và blocked. Có prev/next, copy/export JSON, replay, mở inspector và so sánh mode.

## Presentation Mode

Nhấn **Presentation Mode** trong trace. Chế độ này phóng to chữ, chỉ hiển thị bước hiện tại, thanh tiến trình, nút trước/sau, autoplay/pause và các inspector. Autoplay chỉ chuyển bước của trace đã có, không tự gửi request hay thay đổi database.

## Audit log

Mở `/audit-logs`; lọc theo user, action, mode, decision hoặc trace ID. Log không chứa password, secret hay cookie đầy đủ. Audit giúp phát hiện tampering nhưng không thay server-side authorization.

## Reset, demo và evidence

```powershell
python scripts/reset_database.py
python scripts/run_demo_flows.py
python scripts/export_evidence.py
```

`run_demo_flows.py` dùng Flask test client, chạy đủ chín flow thật và ghi JSON vào `evidence/traces`, `requests`, `responses`, `audit`, `database`. Nó không mở browser, không tạo ảnh và không gọi Internet.

Client qua HTTP chỉ cho scenario cố định:

```powershell
python scripts/send_request.py --scenario checkout-price-1-vulnerable
python scripts/send_request.py --scenario invoice-1002-secure
python scripts/send_request.py --scenario profile-admin-secure
```

## Ảnh thủ công

Đọc [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md), chụp 41 ảnh PNG vào `evidence/screenshots/`, rồi chạy:

```powershell
python scripts/check_screenshots.py
```

Checker chỉ kiểm tra tên, PNG, file rỗng, kích thước, ảnh thiếu/thừa và hash trùng; không OCR, không phân tích nội dung và không tạo ảnh.

## Báo cáo DOCX

```powershell
python scripts/generate_report.py
```

Output:

- `report/21127645_LeMinh_21127224_NguyenVuBach_Lab03_ParameterTampering.docx`

Nếu thiếu ảnh, report vẫn được tạo và placeholder ghi tên ảnh, tài khoản, URL, dữ liệu cần sửa, panel và nội dung bắt buộc. Khi ảnh thật có mặt, chạy lại để thay placeholder mà giữ tỷ lệ.

## Kiểm thử

```powershell
pytest
```

Lưu kết quả thật bằng PowerShell:

```powershell
pytest 2>&1 | Tee-Object evidence/logs/pytest.txt
```

## Lỗi thường gặp

- Redirect về login: đăng nhập lại đúng tài khoản demo.
- Port 5003 bận: dừng process lab cũ. Không publish Compose ra địa chỉ host khác `127.0.0.1`.
- State không đúng: chạy `python scripts/reset_database.py`, rồi chỉ chạy một flow.
- Secure invoice 1002 trả 403: đây là kết quả đúng với User A; admin được phép theo policy.
- Report thiếu ảnh: xem danh sách cuối output, chụp thủ công đúng tên và chạy lại generator.
- Cookie `Secure=False`: đúng cho local HTTP; đặt `SESSION_COOKIE_SECURE=true` khi triển khai HTTPS.

Parameterized SQL chống SQL Injection, nhưng không tự vá sai logic giá, IDOR hoặc mass assignment. CSP/CSRF cũng không thay thế authorization.


## Chế độ báo cáo DOCX-only

`scripts/generate_report.py` chỉ tạo lại file DOCX đúng tên hiện có. Script không gọi ReportLab, LibreOffice/soffice, không chuyển đổi hoặc cập nhật PDF, không render DOCX và không chạy test/smoke test/ứng dụng. Các log cũ chỉ được đọc như evidence; ảnh chưa có được biểu diễn bằng placeholder chi tiết và không bị tuyên bố là đã chụp.
