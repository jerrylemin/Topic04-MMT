# LAB 6 - COOKIE POISONING

**Nhóm sinh viên thực hiện:**  
1. Lê Minh — 21127645  
2. Nguyễn Vũ Bách — 21127224  
**Địa chỉ duy nhất của lab:** `http://127.0.0.1:5006`

Lab06 là ứng dụng học tập local, dùng tài khoản và dữ liệu giả lập để giải thích vì sao server không được tin dữ liệu phân quyền nằm trong cookie phía client. Lab so sánh năm mô hình: Plain Cookie, Base64 Cookie, Signed Cookie, Encrypted Cookie và Server-side Session.

> Trạng thái tài liệu: README này mô tả hợp đồng vận hành và cách kiểm chứng. Nó không xác nhận rằng test, coverage, smoke test, evidence, DOCX hay Docker đã chạy. Chỉ xem một kết quả là đạt sau khi lệnh tương ứng chạy thành công và artifact thật đã được kiểm tra.

## Phạm vi an toàn

Chỉ dùng Lab06 trên máy local:

- URL cố định: `http://127.0.0.1:5006`.
- Khi chạy trực tiếp trên host, Flask phải bind `127.0.0.1`, không bind toàn mạng.
- Không thử trên website thật và không dùng dữ liệu/tài khoản thật.
- Không có kết nối Internet trong lúc ứng dụng chạy.
- Không đọc cookie của website khác; không gửi cookie ra ngoài Lab06.
- Không có proxy, browser extension, replay tool, cookie editor tổng quát hay input tùy ý cho domain/host/URL/port/cookie name/target route.
- Không có `document.cookie`; JavaScript không đọc, ghi hoặc gửi cookie.
- Không có XSS, Session Hijacking, đánh cắp Session ID hay flow Session Fixation thực thi. Các thuật ngữ này chỉ được so sánh lý thuyết.
- Không dùng Playwright, Selenium, tự động DevTools, tự động chụp ảnh hoặc tạo ảnh giả.
- Việc sửa cookie chỉ làm thủ công bằng Browser DevTools, với cookie, route và giá trị demo cố định của Lab06.
- Không hiển thị secret key, password hash, full session token, full signed cookie hoặc full encrypted cookie trong UI/log/evidence.

## Mục tiêu học tập

Sau khi hoàn thành lab, người học có thể:

1. Giải thích Cookie Poisoning là sửa nội dung cookie để lừa server xử lý sai.
2. Giải thích cookie là dữ liệu client-controlled và phải được coi là không đáng tin cậy.
3. Quan sát Name, Value, Domain, Path, HttpOnly, Secure và SameSite.
4. Minh họa broken access control khi server tin `role` trong Plain Cookie hoặc Base64 Cookie.
5. Giải thích Base64 là encoding, không phải encryption.
6. Quan sát signed cookie phát hiện sửa đổi và hiểu rằng signing không che payload.
7. Phân biệt encoding, signing, encryption và authenticated encryption.
8. Giải thích vì sao role phải được kiểm tra server-side trên mỗi request.
9. Kiểm chứng session rotation, server-side logout invalidation và từ chối token cũ.
10. Phân biệt Cookie Poisoning, Cookie Stealing/Session Hijacking và Session Fixation.

## Năm mô hình

| Mode | Cookie cố định | Dữ liệu phân quyền | Tính chất | Kết luận |
|---|---|---|---|---|
| Plain Cookie Demo | `lab06_username`, `lab06_role` | `role` nằm ở client | Đọc/sửa trực tiếp, không integrity | Cố ý dễ bị Cookie Poisoning |
| Base64 Cookie Demo | `lab06_profile_b64` | `role` nằm trong JSON Base64 | Encoding, không signing/encryption | Cố ý dễ bị Cookie Poisoning |
| Signed Cookie Demo | `lab06_signed_profile` | Payload demo có chữ ký | Phát hiện sửa đổi; nội dung có thể đọc được | Integrity/authenticity, không thay authorization |
| Encrypted Cookie Demo | token demo read-only | Không dùng role để phân quyền | Fernet authenticated encryption | Confidentiality + integrity, không thay authorization |
| Server-side Session Demo | `lab06_session` | Role nằm trong database | Cookie chỉ có Session ID ngẫu nhiên; DB chỉ lưu hash | Mô hình phân quyền an toàn chính |

## Kiến trúc bảo mật

Luồng chung dự kiến:

```text
Browser local
  -> Flask route cố định
  -> cookie parser/verification theo mode
  -> authorization policy
  -> SQLite server-side state
  -> audit event + trace timeline + evidence đã che dữ liệu nhạy cảm
  -> HTML Inspector/Final Verdict
```

Ranh giới tin cậy:

- Mọi header, cookie, form field và URL request từ browser đều không đáng tin cậy.
- Plain/Base64 cố ý vi phạm ranh giới này để minh họa lỗi.
- Signed mode xác minh chữ ký trước khi dùng payload.
- Encrypted mode chỉ giải mã trên server và không dùng dữ liệu động trong token làm quyền.
- Server-side Session hash token nhận được, kiểm tra active/expiry/revocation, rồi lấy user/role mới nhất từ database cho từng request.

## Database dự kiến

SQLite dùng truy vấn có tham số và năm bảng:

- `users`: hồ sơ, password hash, role, active và timestamps.
- `server_sessions`: chỉ lưu SHA-256 của Session ID cùng user, expiry, active/revoked state và rotation reason.
- `audit_logs`: ai, hành động, route, mode, cookie status, submitted/database role, quyết định và trace ID.
- `cookie_events`: operation, fingerprint, signature/encryption status, decision và trace ID.
- `session_events`: rotation/revocation event, fingerprint cũ/mới, reason và trace ID.

Không lưu plaintext password hoặc raw Session ID. Inspector database không được lộ password hash.

## Tài khoản demo cố định

| Vai trò | Username | Password | ID | Email |
|---|---|---|---:|---|
| Student | `student` | `Student123!` | 10 | `student@lab.local` |
| Admin | `admin_lab` | `AdminLab123!` | 1 | `admin@lab.local` |

Các mật khẩu trên chỉ dành cho dữ liệu giả lập local và phải được lưu bằng:

```python
generate_password_hash(password, method="pbkdf2:sha256:600000")
```

Xác minh bằng `check_password_hash`; không ghi plaintext password vào database, log, trace hoặc evidence.

## URL cố định

### Chung

| Method | URL | Mục đích |
|---|---|---|
| GET | `/` | Tổng quan Lab06 |
| GET, POST | `/login` | Chọn một trong bốn mode đăng nhập cố định |
| POST | `/logout` | Logout theo mode hiện tại |
| GET | `/dashboard` | Dashboard và điều hướng flow |
| POST | `/reset-lab` | Reset dữ liệu demo local |
| GET | `/comparison` | So sánh năm mô hình và code |
| GET | `/security-controls` | Cấu hình/kiểm soát bảo mật thực tế |
| GET | `/audit-logs` | Audit events đã che dữ liệu nhạy cảm |
| GET | `/api/trace/<trace_id>` | Trace JSON theo ID do app tạo |
| POST | `/api/trace/clear` | Xóa trace demo local |
| GET | `/health` | Health check local |

### Theo mode

| Mode | Profile/demo | Admin |
|---|---|---|
| Plain | `/vulnerable/plain/profile` | `/vulnerable/plain/admin` |
| Base64 | `/vulnerable/base64/profile` | `/vulnerable/base64/admin` |
| Signed | `/secure/signed/profile` | `/secure/signed/admin` |
| Encrypted | `/secure/encrypted-demo` | Không có authorization bằng encrypted token |
| Server session | `/secure/session/profile` | `/secure/session/admin` |

Server-session logout dùng `POST /secure/session/logout`.

## Cài đặt

Yêu cầu Python 3.11 trở lên. Dependency installation cần Internet ở bước thiết lập nếu máy chưa có package; ứng dụng đã chạy thì không được gọi Internet.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python seed.py
python app.py
```

### Windows Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python seed.py
python app.py
```

### Linux/macOS shell

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python seed.py
python app.py
```

Sau khi console xác nhận bind local, mở `http://127.0.0.1:5006`. Dừng bằng `Ctrl+C`.

## Script chạy nhanh

Các entry point dự kiến:

```powershell
.\scripts\run_lab.ps1
```

```bat
scripts\run_lab.bat
```

```bash
bash scripts/run_lab.sh
```

Script chỉ được tạo virtual environment, cài dependency, seed khi cần và chạy app tại local. Không chạy quyền admin và không bind toàn mạng.

## Chạy Plain Cookie flow

1. Mở `/login`, chọn **Plain Cookie Demo**, đăng nhập `student`.
2. Mở DevTools > Application/Storage > Cookies > `http://127.0.0.1:5006`.
3. Quan sát `lab06_username=student` và `lab06_role=user`, cùng Domain/Path/HttpOnly/Secure/SameSite.
4. Mở `/vulnerable/plain/admin`: trạng thái `user` phải bị từ chối.
5. Chỉ trong DevTools, sửa `lab06_role` từ `user` thành `admin`.
6. Reload đúng `/vulnerable/plain/admin`: vulnerable route được thiết kế để cho phép và cảnh báo rằng quyền được cấp vì server tin cookie client.
7. Mở Authorization Inspector, Timeline, Final Verdict và Audit Log để xem dữ liệu thực của request.
8. Reset bằng `POST /reset-lab`, nút reset của UI (nếu có), hoặc xóa riêng cookie Lab06 rồi đăng nhập lại. Không sửa cookie bằng script.

`HttpOnly=False` ở hai plain cookie chỉ phục vụ quan sát trong lab. HttpOnly không ngăn người dùng sửa cookie bằng DevTools và không phải bản vá Cookie Poisoning.

## Chạy Base64 Cookie flow

1. Chọn **Base64 Cookie Demo**, đăng nhập `student`.
2. Quan sát cookie cố định `lab06_profile_b64`.
3. Base64 Inspector phải hiển thị chuỗi rút gọn, JSON decode thực, thuật toán URL-safe Base64, role được trích xuất và quyết định.
4. Dùng duy nhất hai trạng thái cố định hiển thị trong UI: JSON `role=user` và JSON demo `role=admin`, cùng Base64 tương ứng. Không nhập JSON tùy ý.
5. Copy giá trị demo cố định `role=admin` từ phần hướng dẫn read-only, sửa cookie thủ công trong DevTools rồi reload `/vulnerable/base64/admin`.
6. Quan sát route cho phép vì không có signature; xem Inspector/Timeline/Verdict.
7. Reset Lab06 trước khi chuyển mode.

Base64 chỉ biểu diễn bytes thành text. Nó không tạo confidentiality hoặc integrity.

## Chạy Signed Cookie flow

1. Chọn **Signed Cookie Demo**, đăng nhập `student`.
2. Mở `/secure/signed/profile` và Signature Inspector; xác nhận cookie có mặt và chữ ký hợp lệ. Chỉ payload/signature đã che được hiển thị.
3. Mở `/secure/signed/admin` để quan sát quyết định của mode.
4. Trong DevTools, sửa đúng một ký tự của `lab06_signed_profile`; không dán cookie từ nguồn khác.
5. Reload route signed: request phải bị từ chối trước khi payload không hợp lệ được dùng cho authorization.
6. Inspector phải cho biết verification result, deserialization/authorization có chạy hay không và quyết định; không được hiển thị secret key.

Signed cookie bảo vệ integrity/authenticity. Nó không tự mã hóa payload, không có khả năng revoke tức thời tốt như server-side session và không thay server-side authorization.

## Xem Encrypted Cookie demo

1. Mở `/secure/encrypted-demo`.
2. Quan sát plain JSON demo không nhạy cảm, token Fernet đã che, kết quả decrypt server-side, tamper detection, confidentiality và integrity.
3. Xem bảng phân biệt Base64 encoding, signing, encryption và authenticated encryption.
4. Không có role trong payload và không có nút/ô nhập token tùy ý.

Fernet dùng authenticated encryption; key chỉ ở server environment. Encryption không thay authorization và không phù hợp để mang role động cần revoke/cập nhật ngay.

## Chạy Server-side Session flow

### Student bị từ chối

1. Chọn **Server-side Session Demo**, đăng nhập `student`.
2. Quan sát `lab06_session`: cookie không chứa role hoặc user ID; UI/log chỉ hiển thị fingerprint.
3. Mở `/secure/session/admin`; server hash token, tìm session active/unexpired, lấy role từ database và từ chối student.
4. Xem Server Session, Authorization và Database Inspector.

### Admin được phép

1. Logout/reset, đăng nhập `admin_lab` bằng cùng mode.
2. Mở `/secure/session/admin`; server phải lấy role admin từ database trên request hiện tại rồi mới cho phép.
3. Không suy luận quyền từ nội dung cookie.

### Rotation và logout invalidation

1. Ghi fingerprint phiên trước/sau login; login phải tạo Session ID mới và revoke/replace phiên cũ theo chính sách.
2. Dùng Inspector/Audit/Timeline để xác nhận rotation reason; không hiển thị token thô.
3. Gửi `POST /secure/session/logout`; record server-side phải inactive/revoked và browser cookie phải hết hạn.
4. Việc kiểm thử token cũ chỉ làm bằng Flask test client hoặc script demo cố định của Lab06, không tạo replay tool UI.
5. Request dùng token cũ sau rotation/logout phải bị từ chối.

## Timeline, Inspector và Final Verdict

- **Action Timeline** trình bày các bước thực đã ghi với layer, technique, input/output đã che, code reference, status và security meaning.
- **Cookie Inspector** chỉ hiển thị cookie Lab06 cố định; không đọc toàn bộ cookie trình duyệt.
- **Attribute Inspector** lấy Path/HttpOnly/Secure/SameSite từ response/config thực.
- **Base64/Signature/Encryption Inspector** dùng kết quả encode/decode/verify/decrypt thực.
- **Server Session Inspector** dùng record/fingerprint thực, không token thô.
- **Authorization Inspector** hiển thị subject, action, policy, role source, database role, decision và reason.
- **Database Inspector** chỉ hiển thị trường an toàn; không password hash hoặc raw session token.
- **Code Comparison** phải được tạo từ source thật, không dùng snippet lệch implementation.
- **Security Control Panel** phản ánh cấu hình thực, không hard-code trạng thái đạt.
- **Final Security Verdict** tách rõ vulnerable demonstration với secure control.

## Presentation Mode

Mở một flow rồi bật **Presentation Mode** từ control của trang. Dùng Previous/Next hoặc phím điều hướng được UI ghi rõ. Progress, active timeline step, explanation, code highlight và Inspector phải đồng bộ với cùng trace. Presentation Mode không tự chạy DevTools và không tự sửa cookie.

## Audit Log và evidence

Mở `/audit-logs` để xem audit event đã che dữ liệu nhạy cảm. Trace JSON dùng `/api/trace/<trace_id>` với ID do flow thật tạo.

Chỉ xuất evidence sau khi app và flow đã chạy:

```powershell
python scripts/run_demo_flows.py
python scripts/export_evidence.py
```

Các thư mục evidence dự kiến gồm `traces`, `requests`, `responses`, `cookies`, `sessions`, `audit`, `database`, `logs` và `snippets`. Không chỉnh tay để tạo kết quả giả.

## Kiểm thử

Chạy từ thư mục `Lab06`:

```powershell
pytest
pytest --cov=. --cov-report=term-missing
python scripts/run_runtime_smoke_test.py
```

Sau khi chạy thật, log dự kiến:

- `evidence/logs/pytest.txt`
- `evidence/logs/coverage.txt`
- `evidence/logs/runtime_smoke.txt`

Mục tiêu là tối thiểu 80 test có ý nghĩa và coverage tối thiểu 90% cho các module lõi được nêu trong `requirements_review.txt`. README này không tuyên bố đã đạt các ngưỡng đó.

## Tạo báo cáo

Chỉ chạy sau khi có source và evidence thật:

```powershell
python scripts/generate_report.py
```

Đầu ra yêu cầu:

- `report/21127645_LeMinh_21127224_NguyenVuBach_Lab06_CookiePoisoning.docx`

Script phải báo lỗi rõ nếu không tạo được DOCX; không được báo hoàn thành khi artifact chưa tồn tại. Các ảnh còn thiếu phải được ghi rõ và không được thay bằng ảnh dựng.

## Chụp ảnh thủ công

Đọc [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md). Người học tự chụp 48 ảnh bằng browser/DevTools. Không dùng automation. Chỉ ảnh thật được kiểm tra thủ công mới được dùng làm bằng chứng.

Kiểm tra file ảnh sau khi người học đã chụp:

```powershell
python scripts/check_screenshots.py
```

Script chỉ kiểm tên, PNG, kích thước, file rỗng/thiếu/thừa và hash trùng; không OCR và không tạo ảnh.

## Reset và dọn bài nộp

Reset dữ liệu demo bằng UI hoặc:

```powershell
python scripts/reset_database.py
python seed.py
```

Dọn cache/tệp tạm trước khi nộp:

```powershell
python scripts/clean_submission.py
```

Cleanup phải giữ source, database demo cần thiết, evidence cuối, tests, report, README và hướng dẫn ảnh. Sau cleanup cần chạy lại test phù hợp trước khi công bố trạng thái cuối.

## Docker và mâu thuẫn binding

Yêu cầu có hai điều không thể đồng thời thỏa theo nghĩa đen trong Docker thông thường:

1. Process ứng dụng chỉ bind `127.0.0.1`, tuyệt đối không bind `0.0.0.0`.
2. Compose publish `127.0.0.1:5006:5006` và host truy cập được container.

Process bind `127.0.0.1` **bên trong container** chỉ nghe loopback của chính container nên Docker port forwarding thường không tới được. Cách Docker thông thường là app nghe `0.0.0.0:5006` trong container, còn Compose publish `127.0.0.1:5006:5006` để không lộ ra mạng ngoài; cách này an toàn ở host nhưng vi phạm câu chữ “không bind 0.0.0.0”.

Vì vậy:

- Cách chạy chuẩn, không mơ hồ của lab là chạy trực tiếp trên host với bind `127.0.0.1:5006`.
- Không tuyên bố Docker hoạt động và đồng thời tuân thủ literal no-`0.0.0.0` cho đến khi người dùng chấp nhận một cách diễn giải.
- Không tự ý nới ràng buộc. Dockerfile vẫn phải dùng non-root user, không privileged, không chứa secret, không cài browser automation/proxy; Compose chỉ được publish host `127.0.0.1`.

## Cookie flags khi chạy HTTP local

`Secure` cookie thường không được browser gửi qua `http://127.0.0.1`. Vì lab dùng HTTP local, cấu hình development thường cần `COOKIE_SECURE=false`. UI phải hiển thị giá trị config thực; không được ghi “Secure đang bật” nếu response thực không có flag này. Khi triển khai HTTPS, đặt secret qua environment và bật Secure.

## Giới hạn

- Đây là mô phỏng giáo dục, không phải pentest tool.
- Dữ liệu và quyết định chỉ áp dụng cho route/cookie cố định của Lab06.
- Plain/Base64 route cố ý không an toàn; không tái sử dụng mẫu đó trong hệ thống thật.
- Signed/encrypted token không thay database-backed authorization và revocation.
- SQLite/in-memory local store không đại diện cho kiến trúc phân tán production.
- Chưa có tuyên bố test pass, coverage, smoke, evidence, report, page count, screenshot hay Docker pass trong README này.


## Chế độ báo cáo DOCX-only

`scripts/generate_report.py` chỉ tạo lại file DOCX đúng tên hiện có. Script không gọi ReportLab, LibreOffice/soffice, không chuyển đổi hoặc cập nhật PDF, không render DOCX và không chạy test/smoke test/ứng dụng. Các log cũ chỉ được đọc như evidence; ảnh chưa có được biểu diễn bằng placeholder chi tiết và không bị tuyên bố là đã chụp.
