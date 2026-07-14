# LAB 5 - SQL INJECTION

**Sinh viên:** 21127645 - Lê Minh  
**Ứng dụng:** Flask/SQLite local tại `http://127.0.0.1:5005`

Lab05 minh họa nguyên nhân SQL Injection bằng hai luồng `SELECT` cố tình nối
chuỗi và đối chiếu với bản vá dùng parameterized query, PBKDF2, kiểm tra đầu
vào, lỗi an toàn, audit và trace thật. Dữ liệu hoàn toàn giả lập; ứng dụng không
phải scanner và không nhận target, URL, connection string, đường dẫn database
hay câu SQL tùy ý.

## Phạm vi an toàn

- Flask chỉ bind `127.0.0.1:5005`; không bind toàn mạng.
- Runtime không gọi Internet và không kết nối database bên ngoài.
- Chỉ có ba chuỗi kiểm thử SQL cố định cho login/search local.
- Các flow vulnerable chỉ chạy `SELECT`; input không thể tạo thao tác ghi/DDL.
- Không UNION, blind/time-based/out-of-band, stacked query, schema enumeration,
  `sqlite_master`, `ATTACH DATABASE`, `load_extension`, dump hay đọc file.
- Không sqlmap, Burp API, proxy, host/URL input, request hàng loạt hoặc browser
  automation. Ảnh phải chụp thủ công.
- UI/evidence không hiển thị password, full hash/digest, session cookie,
  traceback hoặc đường dẫn database tuyệt đối.

Không dùng các chuỗi của lab trên hệ thống khác.

## Kiến trúc

```text
Browser/Jinja
  -> Flask route + validation/fixed-scenario gate
  -> vulnerable string concatenation | secure parameter binding
  -> SQLite parser/execution (read-only demo query)
  -> auth decision | product result set
  -> trace + audit + query event
  -> safe HTTP response + inspectors
```

- `app.py`: route, response headers, source-backed comparison và bind loopback.
- `database.py`, `schema.sql`, `seed.py`: SQLite local, schema và dữ liệu mẫu.
- `vulnerable_queries.py`: ba query nối chuỗi được giới hạn trong lab.
- `secure_queries.py`, `auth_service.py`: placeholder thật và PBKDF2 verification.
- `trace_service.py`, `query_trace.py`, `audit_service.py`: timeline, inspector,
  audit và query event cùng `trace_id`.
- `templates/`, `static/`: giao diện responsive, visualizer và Presentation Mode.
- `scripts/`: reset, demo/evidence, smoke, report, screenshot checker và cleanup.
- `evidence/`: trace/request/response/query/audit/log thật đã che dữ liệu nhạy cảm.
- `report/`: DOCX/PDF sinh từ evidence và source thật.

## Database và dữ liệu mẫu

Schema có các bảng `users`, `products`, `audit_logs`, `login_attempts`,
`query_events` và `trace_records`. `users` không có cột password plaintext.

| Username | Password demo | Tên | Role |
|---|---|---|---|
| `admin_lab` | `AdminLab123!` | Quản trị Lab | admin |
| `student_a` | `StudentA123!` | Sinh viên A | user |
| `student_b` | `StudentB123!` | Sinh viên B | user |

Secure authentication lưu `pbkdf2:sha256:600000` với salt riêng và kiểm tra bằng
`check_password_hash`. `legacy_password_digest` chỉ là SHA-256 không salt để
minh họa mô hình cũ cố tình yếu; secure route không dùng trường này. SHA-256
nhanh và không salt không phù hợp để lưu password thật.

Sản phẩm giả lập:

1. USB Security Key.
2. Wireless Mouse.
3. Mechanical Keyboard.
4. Lab Laptop.
5. Network Cable.
6. Web Security Book.
7. Linux Practice USB.
8. Local Test Router.

## Cài đặt và chạy

Yêu cầu Python 3.11 trở lên.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python app.py
```

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

Script nhanh:

```powershell
scripts\run_lab.bat
# hoặc
powershell -File scripts\run_lab.ps1
```

```bash
sh scripts/run_lab.sh
```

Dừng bằng `Ctrl+C`. Không chạy bằng quyền quản trị/root.

Reset database:

```powershell
python scripts/reset_database.py
```

## URL

| Route | Chức năng |
|---|---|
| `GET /` | Tổng quan và scenario cố định |
| `GET /dashboard` | Audit gần nhất và điều hướng |
| `POST /reset-lab` | Seed lại database local |
| `GET, POST /vulnerable/login` | Login nối chuỗi SQL |
| `GET, POST /secure/login` | Login placeholder + PBKDF2 |
| `POST /logout` | Xóa session |
| `GET /vulnerable/search` | Search nối chuỗi LIKE |
| `GET /secure/search` | Search `LIKE ?` + `LIMIT 50` |
| `GET /vulnerable/user?id=1` | Numeric concatenation local, không có payload tự động |
| `GET /secure/user?id=1` | Integer validation + `WHERE id = ?` |
| `GET /comparison` | Code Comparison từ source thật |
| `GET /security-controls` | Trạng thái control từ config/source thật |
| `GET /audit-logs` | Audit log đã redaction |
| `GET /api/trace/<trace_id>` | Trace JSON |
| `POST /api/trace/clear` | Xóa trace local |
| `GET /health` | Healthcheck |

## Chạy các flow login

### Normal vulnerable login

Mở `/vulnerable/login`, dùng `admin_lab` / `AdminLab123!`. Server tính legacy
digest, nối username/digest vào SQL và tạo session khi SQLite trả user.

### Quote detection

Nhấn nút **Dấu nháy đơn**. SQLite nhận SQL bị lỗi; Error Inspector chỉ hiển thị
category, exception class và thông điệp rút gọn, không có traceback/path. Cùng
input ở `/secure/login` là dữ liệu bind và không phá cú pháp.

### Authentication logic local

Nhấn nút scenario cố định có username `admin_lab' -- ` và password bất kỳ.
Trong vulnerable mode, phần comment làm điều kiện digest không còn tham gia và
session được gắn `authenticated_via=vulnerable_local_demo`. Cùng input tại
`/secure/login` chỉ là username literal, không match user và bị từ chối bằng
thông báo chung.

### Normal secure login

Mở `/secure/login`, dùng tài khoản demo. SQLite chỉ lookup `username = ?`, sau
đó Werkzeug kiểm tra PBKDF2; session được clear/rotate trước khi ghi các trường
`user_id`, `username`, `role`, `authenticated_via`, `login_time`.

## Chạy các flow search

- Normal: `/vulnerable/search?keyword=USB` chỉ trả tên chứa `USB`.
- Quote: nút dấu nháy đơn tạo lỗi query đã xử lý trong vulnerable mode.
- Expanded local search: scenario `%' OR 1=1 -- ` chỉ mở rộng result set trong
  bảng `products`; không đọc bảng khác và không sửa database.
- Secure comparison: cùng keyword được bind thành `%keyword%`; cấu trúc SQL giữ
  nguyên và chuỗi không match tên sản phẩm.
- Normal secure: `/secure/search?keyword=USB` trả đúng kết quả, tối đa 50 dòng.

## Đọc Timeline và Inspector

Sau mỗi request, Timeline chứa layer, timestamp, kỹ thuật, input/output, code
reference, security meaning và status. Chọn một bước để xem dữ liệu của bước.

- **Request Inspector:** method/URL/path/query/form thật; password là `[REDACTED]`.
- **Input Inspector:** độ dài, dấu nháy, marker/comment/boolean của scenario cố định.
- **Query Construction:** template, phương thức ghép/bind, final SQL masked,
  placeholder và parameter masked.
- **SQL Execution:** SELECT, prepared state, row count, error/transaction/read-only.
- **Authentication Decision:** match/verify/session/final decision, không password/hash.
- **Result Set:** expected/actual rows, IDs/names, other-table/write flags.
- **Database Inspector:** table/operation/count/changed rows và nhãn database local.
- **Error Inspector:** lỗi vulnerable rút gọn hoặc secure generic error ID.
- **Code Comparison:** AST đọc đúng hàm/source đang chạy.
- **Security Controls:** config/source/route/risk/limitation thật.
- **Final Verdict:** root cause, primary fix, defense in depth và remaining risk.

## Presentation Mode

Nhấn **Presentation Mode**, dùng Previous/Next hoặc Auto Play để trình bày từng
bước của trace hiện có. Auto Play chỉ thay bước đang nhìn; nó không gửi request,
không chạy scenario và không thay đổi database. Có thể mở trực tiếp Request,
Query, SQL Execution, Authentication, Result Set, Code Comparison và Verdict.

## Audit log và monitoring

Mở `/audit-logs`. Mỗi event có route, mode, action, input summary, query
construction, decision, reason, result count, error category và trace ID. Log
không chứa password, full hash/digest, session cookie hoặc secret. Logging giúp
phát hiện bất thường nhưng không thay parameterized query.

## Kiểm thử và coverage

```powershell
pytest
pytest --cov=. --cov-report=term-missing
```

Pipeline dự án lưu kết quả thật tại:

- `evidence/logs/pytest.txt`
- `evidence/logs/coverage.txt`

Các module lõi có ngưỡng mục tiêu 90%: `database.py`, `auth_service.py`,
`vulnerable_queries.py`, `secure_queries.py`, `trace_service.py`,
`audit_service.py`, `validation.py`, `error_service.py`.

## Demo, evidence và smoke test

Xuất lại toàn bộ 12 flow bằng Flask test client:

```powershell
python scripts/run_demo_flows.py
python scripts/export_evidence.py
```

Hai script không nhận URL/host/port/payload. Evidence được join bằng `trace_id`.

Khi app đang chạy tại cổng cố định:

```powershell
python scripts/run_runtime_smoke_test.py
```

Smoke test chỉ gọi `http://127.0.0.1:5005` và ghi
`evidence/logs/runtime_smoke_test.txt`.

## Báo cáo DOCX/PDF

Sau khi có evidence và ba log thật:

```powershell
python scripts/generate_report.py
```

Output:

- `report/21127645_LeMinh_Lab05_SQLInjection.docx`
- `report/21127645_LeMinh_Lab05_SQLInjection.pdf`

Generator đọc trace/request/response/query/audit/log/source thật, tạo 30 chương,
trace table, code comparison, sequence/data-flow diagram dạng vector Word, rồi
chuyển PDF bằng LibreOffice. Thiếu evidence/log/PDF converter sẽ trả lỗi rõ;
không tạo placeholder ảnh hoặc kết quả test/coverage giả.

## Ảnh thủ công

Không tự động chụp ảnh. Đọc [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md), lưu
đúng 36 PNG vào `evidence/screenshots/`, rồi chạy:

```powershell
python scripts/check_screenshots.py
```

Checker chỉ kiểm tra tên, PNG, file rỗng/hỏng, kích thước, thiếu/thừa và hash
trùng; không OCR, không phân tích nội dung và không tạo ảnh. Ảnh không phải tiêu
chí hoàn thành tự động của Codex.

## Docker

```powershell
docker compose up --build
```

Compose chỉ publish `127.0.0.1:5005:5005`, chạy user `labuser` không phải root,
drop capabilities, bật `no-new-privileges`, dùng volume cho database/evidence/
report và có healthcheck. Flask vẫn bind loopback trong container; `socat` chỉ
chuyển từ đúng IP nội bộ container sang `127.0.0.1:5005` để Docker port mapping
hoạt động mà không thêm bind toàn mạng.

## Dọn bài nộp

```powershell
python scripts/clean_submission.py
```

Script xóa cache, bytecode, coverage cache, `htmlcov`, `tmp`, `report/tmp`,
`evidence/tmp` và test database; giữ source, demo database, evidence cuối, tests,
report, README và hướng dẫn ảnh.

## Giới hạn và defense in depth

- SQLite không có database-user permission model như MySQL/PostgreSQL. Lab mô
  phỏng least privilege bằng file local, non-root Docker, query cố định,
  vulnerable `SELECT`-only, không raw SQL/write/schema/network.
- ORM không tự động an toàn nếu code dùng raw SQL sai; lab không thêm ORM vì
  `sqlite3` parameter binding đã minh họa đúng bản vá.
- Input validation không thay prepared statement. WAF không được cài và không
  thể thay sửa code. CSP, cookie flags, result limit, audit và monitoring chỉ là
  các lớp bổ sung.
- Secure cookie là `False` cho local HTTP; đặt `LAB05_COOKIE_SECURE=true` khi
  triển khai HTTPS thực tế. Lab này không phải sản phẩm production.
