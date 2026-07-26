# Báo cáo đánh giá `Topic04_6Labs_short.html`

Ngày kiểm tra: 26/07/2026  
Phạm vi: `BaiTapTopic04.docx`, toàn bộ nội dung có ý nghĩa của `Lab01` đến `Lab06`, và `presentation/Topic04_6Labs_short.html` (HTML, CSS, JavaScript, DOM sau khi chạy).

## Phương pháp và quy ước

- Đề bài được trích xuất bằng `python-docx`: 536 paragraph, 1 bảng, 1 section. Nội dung dưới đây chỉ lấy từ file, không bổ sung yêu cầu suy đoán.
- Đã đọc 832 file có ý nghĩa trong sáu Lab, gồm source, template, JavaScript/CSS, cấu hình, README, DOCX/PDF, JSON, log, request/response, trace, SQLite và binary. Các thư mục môi trường/phụ thuộc sinh tự động như `.venv`, cache bytecode và `__pycache__` không được dùng làm bằng chứng nghiệp vụ.
- Tất cả 203 file JSON đều parse được. Các database SQLite đã được mở read-only và kiểm tra bảng/số record.
- Không có ảnh `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp` hoặc `.svg` trong sáu Lab. Các thư mục screenshot hiện có chứa 0 ảnh (Lab04 chỉ có `.gitkeep`). Sáu DOCX báo cáo mới có 0 media nhúng; sáu PDF có 0 image object.
- HTML dài 1.459 dòng, chứa 18 slide và không tải tài nguyên ngoài. Chạy bằng Chromium headless ở viewport 1920×1080 xác nhận: 18 slide, điều hướng đến slide 18 hoạt động, counter/progress/hash cập nhật đúng, 61 vùng chỉnh sửa được bật bằng phím `E`, không có page error hoặc console warning/error.
- JavaScript không sinh thêm nội dung Lab mới; nó chỉ điều khiển slide, khôi phục nội dung chỉnh sửa từ `localStorage`, bật chỉnh sửa và export HTML. Browser context sạch không có dữ liệu `localStorage`.
- Tổng số mục chấm: 6 Lab × 15 tiêu chí = 90. Phần trăm hoàn thành dùng thang minh bạch: `Đầy đủ = 1`, `Thiếu một phần = 0,5`, `Thiếu nhiều = 0,25`, `Không tìm thấy = 0`, `Sai hoặc không khớp = 0`.

## Chỉ mục bằng chứng

Mỗi nhận xét trong bảng dùng mã dưới đây; mã trỏ đến đường dẫn tuyệt đối hoặc vị trí chính xác trong file.

| Mã | Bằng chứng |
|---|---|
| D-REQ | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\BaiTapTopic04.docx` |
| D-HTML | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\presentation\Topic04_6Labs_short.html` |
| L1-SRC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab01\app.py` (dòng 46-112), `Lab01\static\js\dom_vulnerable.js` và `dom_secure.js` |
| L1-EV | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab01\evidence\traces\reflected_vulnerable.json`, `stored_vulnerable.json`, `dom_vulnerable.json`; `Lab01\evidence\logs\pytest.txt` |
| L1-DOC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab01\README.md`, `Lab01\report\21127645_LeMinh_21127224_NguyenVuBach_Lab01_XSS.docx` |
| L2-SRC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab02\native\vulnerable_processor.c`, `secure_length_processor.c`, `secure_snprintf_processor.c`; `Lab02\app.py`, `config.py`, `native_runner.py`, `Makefile` |
| L2-EV | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab02\evidence\traces\aece51864ec14840a288a2ba64e49544.json`; `Lab02\evidence\logs\pytest.txt` |
| L2-DOC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab02\README.md`, `Lab02\gdb\README_GDB.md`, `Lab02\report\21127645_LeMinh_21127224_NguyenVuBach_Lab02_BufferOverflow.docx` |
| L3-SRC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab03\app.py`, `services.py`, `authorization.py`, `validators.py`, `config.py` |
| L3-EV | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab03\evidence\requests\`, `responses\`, `traces\`, `audit\audit_logs.json`, `database\snapshot.json`, `logs\pytest.txt` |
| L3-DOC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab03\README.md`, `Lab03\report\21127645_LeMinh_21127224_NguyenVuBach_Lab03_ParameterTampering.docx` |
| L4-SRC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab04\victim_app.py`, `attacker_app.py`, `csrf_service.py`, `origin_service.py`, `attacker_templates\attack_page.html`, `config.py` |
| L4-EV | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab04\evidence\requests\`, `responses\`, `state\state_transitions.json`, `traces\`, `logs\pytest.txt`, `logs\runtime_smoke_test.txt` |
| L4-DOC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab04\README.md`, `Lab04\report\21127645_LeMinh_21127224_NguyenVuBach_Lab04_CSRF.docx` |
| L5-SRC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab05\config.py`, `vulnerable_queries.py`, `secure_queries.py`, `auth_service.py`, `app.py` |
| L5-EV | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab05\evidence\requests\`, `responses\`, `queries\`, `traces\`, `results\flow_results.json`, `logs\pytest.txt`, `logs\runtime_smoke_test.txt` |
| L5-DOC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab05\README.md`, `Lab05\report\21127645_LeMinh_21127224_NguyenVuBach_Lab05_SQLInjection.docx` |
| L6-SRC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab06\cookie_service.py`, `base64_cookie_service.py`, `signed_cookie_service.py`, `encrypted_cookie_service.py`, `server_session_service.py`, `authorization_service.py`, `app.py`, `config.py` |
| L6-EV | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab06\evidence\cookies\`, `sessions\`, `requests\`, `responses\`, `traces\`, `results\flow_results.json`, `logs\pytest.txt`, `logs\runtime_smoke_test.txt` |
| L6-DOC | `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab06\README.md`, `Lab06\report\21127645_LeMinh_21127224_NguyenVuBach_Lab06_CookiePoisoning.docx` |

# Phần 1. Tóm tắt yêu cầu của `BaiTapTopic04.docx`

## 1.1. Yêu cầu chung

Nguồn: D-REQ, paragraph 4-22 và 514-535.

- Chỉ thực hành trên máy ảo local, Docker local, ứng dụng cố tình có lỗ hổng hoặc nền tảng học tập hợp pháp (DVWA, OWASP Juice Shop, WebGoat, PortSwigger Web Security Academy).
- Không thử payload trên website thật; không tấn công hệ thống trường/doanh nghiệp/cá nhân; không lấy cookie, tài khoản hoặc dữ liệu thật; không viết mã chiếm quyền hệ thống thật; không tạo reverse shell, malware, persistence, botnet hoặc keylogger.
- Mỗi Lab phải nộp báo cáo PDF, ảnh chụp từng bước, mô tả nguyên nhân kỹ thuật, mức độ ảnh hưởng, cách phòng chống, và bản vá/đoạn mã khắc phục.
- Cấu trúc báo cáo gợi ý gồm: tên Lab, mục tiêu, môi trường, bước thực hiện, kết quả quan sát, nguyên nhân, ảnh hưởng, phòng chống, bản vá, bài học, phụ lục ảnh/log/request-response.
- Chu trình cần thể hiện: nhận diện → khai thác trong lab → phân tích nguyên nhân → đánh giá rủi ro → phòng chống → vá lỗi.

## 1.2. Lab01 — Cross-Site Scripting

Nguồn: D-REQ, paragraph 25-109 và bảng kịch bản XSS.

- Phân biệt và thực hành Reflected XSS, Stored XSS, DOM-based XSS.
- Môi trường đề xuất: Chrome/Firefox, Burp/ZAP, ứng dụng local có search, comment, profile, DOM search.
- Reflected: dùng `/search?q=keyword`, thử input thường và payload JavaScript an toàn, xác định vị trí phản chiếu, kiểm tra escaping, phân tích việc nạn nhân mở URL.
- Stored: dùng `/post/1/comments`, đăng comment thường và payload an toàn, reload/đổi tài khoản, xác định nơi lưu, phân tích phạm vi mọi viewer và rủi ro cookie không `HttpOnly`.
- DOM: dùng `/dom-search#keyword`, kiểm tra JavaScript đọc `location.hash`, `location.search` hoặc `document.URL`; tìm `innerHTML`, `document.write`, `eval`, `setTimeout` chuỗi; thử fragment an toàn; giải thích lỗi phía browser.
- Phải đề xuất ít nhất 5 biện pháp: encoding theo context, `textContent`, sanitization tin cậy, CSP, cookie `HttpOnly/Secure/SameSite`, validation server, không tin URL/form/cookie/localStorage.
- Báo cáo phải trả lời 5 câu: so sánh ba loại XSS; vì sao validation chưa đủ; vì sao cần output encoding; CSP có thay sửa code không; cách vá từng lỗi.

## 1.3. Lab02 — Buffer Overflow trong ứng dụng web local

Nguồn: D-REQ, paragraph 112-188.

- Hiểu ghi vượt vùng nhớ, gây crash có kiểm soát, nguy cơ của hàm chuỗi không an toàn và cách phòng chống.
- Không yêu cầu shellcode, ROP hoặc chiếm quyền.
- Môi trường đề xuất: Linux VM local, GCC, GDB, chương trình C backend, Python gửi request local.
- Kịch bản `POST /submit`, dữ liệu đi vào `char name[32]; strcpy(name, user_input);`.
- Thử input ngắn/dài; quan sát crash; dùng GDB xác định vị trí crash, stack overwrite và ngưỡng input; lưu crash log; sửa code.
- Phân tích stack, hành vi khi vượt buffer, nguy hiểm của `strcpy/gets/sprintf`, memory corruption, ASLR, DEP/NX và Stack Canary.
- Sửa ít nhất 2 cách: kiểm tra chiều dài; `fgets/snprintf/strncpy` cẩn thận; request limit; compiler hardening (stack protector, PIE, RELRO, NX); cân nhắc thư viện/ngôn ngữ memory-safe.
- Trả lời 5 câu: khác Injection; vì sao HTTP kích hoạt native bug; firewall không đủ; bản vá hiệu quả; ít nhất 3 cơ chế hardening.

## 1.4. Lab03 — Parameter Tampering

Nguồn: D-REQ, paragraph 191-264.

- Hiểu thao túng tham số, ranh giới client/server, dữ liệu từ form/URL/hidden field/cookie và server-side validation/authorization.
- Môi trường: mini e-commerce có login, sản phẩm, cart, checkout, invoice; dùng DevTools/Burp/ZAP.
- Thay đổi giá: chặn `POST /checkout`, sửa `price`, kiểm tra server có chấp nhận, giải thích vì sao giá phải lấy từ server.
- IDOR: user A mở `/invoice?id=1001`, đổi `id=1002`, kiểm tra truy cập invoice người khác và phân tích IDOR.
- Role tampering: `POST /profile/update`, thêm/sửa `role=admin`, kiểm tra cập nhật quyền và phân tích phân quyền.
- Phòng chống: không tin client storage/parameter; giá từ DB; owner check; session access control; không nhận field nhạy cảm; logging; object-level authorization.
- Trả lời 5 câu: khác SQL Injection; hidden field không phải bảo mật; IDOR thuộc nhóm nào; kiểm tra trước khi trả invoice; vì sao không truyền giá authoritative từ client.

## 1.5. Lab04 — Cross-Site Request Forgery

Nguồn: D-REQ, paragraph 267-330.

- Hiểu browser bị ép gửi request ngoài ý muốn, khác XSS, cookie tự gắn, và phòng chống bằng token/SameSite/Origin/Referer.
- Môi trường: ứng dụng local có login, đổi email, đổi mật khẩu giả lập, chuyển tiền giả lập; phiên bản lỗi không token; trang attacker local.
- Kịch bản đề mô tả target `http://localhost:8080`, attacker ví dụ `http://localhost:9000/fake-page.html`, `POST /change-email`.
- Đăng nhập victim; xem request; tạo trang attacker có form **tự gửi** đến `/change-email`; xác nhận cookie đi kèm và email bị đổi; bật CSRF token; thử lại và chứng minh thất bại.
- Phân tích cookie tự gửi, attacker không cần mật khẩu, SOP/response, khác XSS, và không dùng GET cho state change.
- Phòng chống: token ngẫu nhiên theo session và kiểm tra server; SameSite Lax/Strict; Origin/Referer; POST cho mutation; re-authentication; CAPTCHA không phải biện pháp chính.
- Bài nộp phải có request hợp lệ, mã HTML attacker, ảnh trước/sau email bị đổi, ảnh sau bản vá, giải thích bản vá.

## 1.6. Lab05 — SQL Injection

Nguồn: D-REQ, paragraph 332-416.

- Hiểu SQL Injection, lỗi nối chuỗi, authentication bypass, data extraction/error-based cơ bản, prepared statement/parameterized query/ORM.
- Môi trường: app local có login, search, user detail; SQLite/MySQL/PostgreSQL; browser, Burp/ZAP, DB Browser nếu dùng SQLite.
- Phát hiện bằng input thường và dấu nháy đơn; quan sát lỗi/hành vi bất thường; xác định input có nguy cơ.
- Authentication bypass: thay logic `WHERE`, chứng minh login không biết password, ghi query biến đổi và phân tích nối chuỗi.
- Search injection: làm đổi điều kiện, trả dữ liệu ngoài dự kiến, phân tích rò rỉ.
- Vá bằng prepared statement; không concat SQL; không password plaintext; dùng hashing; không lộ database error.
- Trả lời 5 câu: tầng lỗi; escaping thủ công; prepared statement; giới hạn của ORM; không lộ lỗi SQL.
- Phòng chống: parameterization, ORM đúng, bcrypt/Argon2/PBKDF2, generic errors, least privilege, type validation, logging/monitoring; WAF chỉ hỗ trợ.

## 1.7. Lab06 — Cookie Poisoning

Nguồn: D-REQ, paragraph 419-512.

- Hiểu sửa cookie để đổi hành vi; rủi ro lưu state nhạy cảm client-side; phân biệt plain, signed, encrypted cookie; server session/chữ ký/mã hóa/toàn vẹn.
- Môi trường: app local login user/admin, cookie lưu role, admin page; dùng DevTools/Burp/ZAP.
- Quan sát tên, value, Domain, Path, HttpOnly, Secure, SameSite.
- Sửa `role=user` thành `role=admin`, reload `/admin`, kiểm tra quyền và phân tích access control.
- Với Base64: decode JSON, sửa role, encode lại, kiểm tra server; giải thích Base64 không phải encryption.
- Vá bằng server-side session; role ở server/DB; ký dữ liệu client nếu bắt buộc; mã hóa và kiểm tra toàn vẹn với dữ liệu nhạy cảm.
- Trả lời 5 câu: cookie không đáng tin; poisoning khác hijacking; Base64; signed cookie; server-side authorization.
- Phòng chống: không lưu role/is_admin/balance/permission trực tiếp; cookie flags; authorization mỗi request; signed cookie; rotate login; logout hủy session server-side.

# Phần 2. Bảng kiểm tra chi tiết

## Lab01

| Lab | Yêu cầu trong đề bài | Nội dung tìm thấy trong thư mục Lab | Nội dung đã có trong HTML | Trạng thái | Nội dung còn thiếu | Đề xuất bổ sung |
|---|---|---|---|---|---|---|
| Lab01-01 | Tên và mục tiêu đúng | Ba dạng XSS, source→sink và bản vá có trong L1-SRC/L1-DOC | Slide 3-4, D-HTML:801-864 | Đầy đủ | Không | Giữ nguyên |
| Lab01-02 | Mô tả đúng lỗ hổng | `Markup`, SQLite, `location.hash/innerHTML` khớp L1-SRC | D-HTML:804-831 | Đầy đủ | Không | Giữ nguyên |
| Lab01-03 | Nguyên nhân/bản chất | Bypass autoescape, stored taint, DOM sink được chứng minh trong L1-SRC/L1-EV | D-HTML:809-831, 841-855 | Đầy đủ | Không | Giữ nguyên |
| Lab01-04 | Cơ chế/quy trình khai thác | Trace Reflected/Stored và source DOM có trong L1-EV | Ba flow source→sink ở slide 3 | Đầy đủ | Chưa gắn trace ID | Thêm một trace ID/case thực |
| Lab01-05 | Môi trường | Flask/SQLite, `127.0.0.1:5000`, browser, route ở L1-DOC/L1-SRC | Chỉ ghi “local” chung ở slide 2 | Không tìm thấy | Stack, port, tool, route | Thêm hộp môi trường |
| Lab01-06 | Các bước thực hiện | README và hướng dẫn ảnh có quy trình; L1-DOC | Không có bước thao tác cụ thể | Thiếu nhiều | Input thường, payload, reload, secure retest | Thêm checklist ngắn |
| Lab01-07 | Giải thích source/code quan trọng | `app.py:59,86,88`; hai file DOM JS; L1-SRC | Có tên API/primitive nhưng không có code thật đầy đủ | Thiếu một phần | Route/hàm/dòng và before-after cụ thể | Chèn 3 snippet ngắn |
| Lab01-08 | Kết quả chạy thực tế | Reflected/Stored trace 200; pytest 13 pass trong L1-EV | Không có status, output hoặc test result | Không tìm thấy | Kết quả từng flow | Thêm bảng observed result |
| Lab01-09 | Ảnh/log/request/response/terminal | Có JSON trace và pytest; không có ảnh; L1-EV | Không nhúng bất kỳ evidence nào | Không tìm thấy | Request/response/log/ảnh | Chèn trace/request thật; ghi rõ chưa có ảnh |
| Lab01-10 | Tác động | Trace ghi người mở URL/mọi viewer; L1-EV | Chỉ nêu nạn nhân, mọi viewer, cookie risk | Thiếu một phần | Session action, defacement, phạm vi/điều kiện | Thêm 2-3 tác động có điều kiện |
| Lab01-11 | Phòng chống/khắc phục | Autoescape, Bleach, `textContent`, CSP/cookie flags; L1-SRC | Slide 4 nêu đủ hơn 5 lớp | Đầy đủ | Không | Giữ nguyên |
| Lab01-12 | HTML khớp source | `Markup(q)`, `Markup(row["body"])`, Bleach, `innerHTML/textContent` đều khớp L1-SRC | D-HTML:846-855 | Đầy đủ | `Markup(body)` là tên rút gọn | Đổi thành `Markup(row["body"])` nếu cần chính xác tuyệt đối |
| Lab01-13 | Không thêm claim thiếu bằng chứng | Reflected/Stored có trace; DOM JSON tĩnh chưa phải browser proof và có `final_result` mâu thuẫn trong L1-EV | Slide mô tả “event handler thực thi”, “reload chạy lại” | Thiếu một phần | Browser evidence cho DOM | Ghi “có thể thực thi” hoặc chèn capture runtime thật |
| Lab01-14 | Bao phủ mọi yêu cầu đề | Đề yêu cầu route, thao tác, câu hỏi báo cáo, evidence; D-REQ | Deck chỉ giữ lý thuyết + phòng thủ | Thiếu nhiều | Môi trường, bước, kết quả, 5 câu trả lời tường minh | Bổ sung 1 slide evidence hoặc speaker notes có nguồn |
| Lab01-15 | Đủ độ sâu | Folder Lab chi tiết; deck chỉ 2 slide | 2 slide, không kết quả | Thiếu nhiều | Phần thực hành/evidence | Ưu tiên thêm slide kết quả |

## Lab02

| Lab | Yêu cầu trong đề bài | Nội dung tìm thấy trong thư mục Lab | Nội dung đã có trong HTML | Trạng thái | Nội dung còn thiếu | Đề xuất bổ sung |
|---|---|---|---|---|---|---|
| Lab02-01 | Tên và mục tiêu đúng | Buffer Overflow local qua HTTP→C; L2-SRC/L2-DOC | Slide 5-6 | Đầy đủ | Không | Giữ nguyên |
| Lab02-02 | Mô tả đúng kỹ thuật | `name[32]`, `strcpy`, stack overflow; L2-SRC | D-HTML:872-900 | Đầy đủ | Không | Giữ nguyên |
| Lab02-03 | Nguyên nhân/bản chất | Copy không biết capacity, 31 byte + null; L2-SRC | D-HTML:886, 896, 918-930 | Đầy đủ | Không | Giữ nguyên |
| Lab02-04 | Cơ chế/quy trình | Browser→POST→Flask→subprocess→C; L2-SRC | D-HTML:874-879 | Đầy đủ | Không | Giữ nguyên |
| Lab02-05 | Môi trường | Linux/WSL/Docker, GCC/GDB, port 5002; L2-DOC | Có kiến trúc nhưng không nêu OS/GCC/GDB/port | Thiếu một phần | Công cụ và port | Thêm dòng môi trường |
| Lab02-06 | Các bước | README/GDB guide có lệnh và input 31/32/64; L2-DOC | Không có lệnh hay sequence thao tác/retest | Thiếu nhiều | Build, request, GDB/ASan, vá, retest | Thêm 5 bước |
| Lab02-07 | Giải thích source | Ba C source và flags rõ; L2-SRC | Có snippet nhưng là pseudocode (`reject()`) | Thiếu một phần | Tên hằng, return code, file/dòng thật | Gắn nhãn pseudocode hoặc thay bằng code thật |
| Lab02-08 | Kết quả thực tế | ASan: input 64, write 65, `SIGABRT`, exit `-6`, line 7; L2-EV | Không hiển thị số liệu này | Không tìm thấy | Crash/ASan/GDB output | Chèn 4 dòng evidence |
| Lab02-09 | Evidence | Có ASan trace và pytest 14 pass; chưa có GDB log/ảnh; L2-EV/L2-DOC | Không có log/terminal/debugger | Không tìm thấy | Evidence thực nghiệm | Chèn ASan trace; ghi GDB chưa thu thập |
| Lab02-10 | Tác động | Trace ghi crash/DoS local; đề yêu cầu memory corruption | Có crash, control data có thể ảnh hưởng | Thiếu một phần | DoS, data/control-flow risk, điều kiện | Thêm impact box ngắn |
| Lab02-11 | Phòng chống | 2 code fix + request limit + hardening; L2-SRC | Slide 6 nêu đầy đủ | Đầy đủ | Không | Giữ nguyên |
| Lab02-12 | HTML khớp source | Logic đúng nhưng snippet rút gọn so với `user_input`, hằng và `return 65/67`; L2-SRC | D-HTML:926-930 | Thiếu một phần | Độ chính xác literal | Gắn “pseudocode” |
| Lab02-13 | Claim có bằng chứng | Stack diagram là mô hình; canary/return address chưa có GDB measurement; L2-EV không có GDB log | D-HTML:888-899 | Thiếu một phần | Phân biệt sơ đồ khái niệm với quan sát | Ghi “mô hình, không phải layout đo được” |
| Lab02-14 | Bao phủ đề | D-REQ yêu cầu GDB, ngưỡng crash, log, 5 câu | Deck thiếu toàn bộ evidence/GDB/câu trả lời tường minh | Thiếu nhiều | GDB/ASan result, threshold, questions | Thêm slide evidence |
| Lab02-15 | Đủ độ sâu | Lab có nhiều evidence; deck 2 slide | Không có kết quả | Thiếu nhiều | Thực nghiệm | Bổ sung trước nộp |

## Lab03

| Lab | Yêu cầu trong đề bài | Nội dung tìm thấy trong thư mục Lab | Nội dung đã có trong HTML | Trạng thái | Nội dung còn thiếu | Đề xuất bổ sung |
|---|---|---|---|---|---|---|
| Lab03-01 | Tên và mục tiêu đúng | Ba scenario đúng đề; L3-SRC/L3-DOC | Slide 7-8 | Đầy đủ | Không | Giữ nguyên |
| Lab03-02 | Mô tả đúng kỹ thuật | Price, IDOR, mass assignment; L3-SRC | D-HTML:958-966 | Đầy đủ | Không | Giữ nguyên |
| Lab03-03 | Nguyên nhân | Tin client, thiếu owner check/allowlist | D-HTML:958-990 | Đầy đủ | Không | Giữ nguyên |
| Lab03-04 | Cơ chế/quy trình | Request/response/traces 9 flow; L3-EV | Client sửa → server decision được mô tả | Đầy đủ | Chưa gắn request thật | Thêm evidence ID |
| Lab03-05 | Môi trường | Flask/SQLite, `127.0.0.1:5003`, DevTools/proxy; L3-DOC | Không có | Không tìm thấy | Stack/port/tool/accounts | Thêm hộp môi trường |
| Lab03-06 | Các bước | README có ba flow chi tiết; L3-DOC | Chỉ nêu tình huống, không có login/intercept/retest | Thiếu nhiều | Các bước thao tác | Thêm 3×3 bước rút gọn |
| Lab03-07 | Giải thích source | Hàm vulnerable/secure ở `services.py:106-321`; policy ở `authorization.py`; L3-SRC | Không có snippet source | Thiếu một phần | Hàm/query/update thật | Chèn before-after code |
| Lab03-08 | Kết quả thực tế | Price vulnerable 200/sai giá; IDOR 200 vs 403; role escalation 200 vs blocked; L3-EV | Bảng có “403”, “tính lại đúng”, “giữ role” nhưng không có trace/status đầy đủ | Thiếu một phần | Actual value, trace ID, response status | Chèn bảng observed |
| Lab03-09 | Evidence | Có request/response/trace/audit/DB và pytest 105 pass; không có ảnh; L3-EV | Không hiển thị evidence | Không tìm thấy | Request/response/log/DB diff | Chèn 3 evidence cards |
| Lab03-10 | Tác động | Evidence ghi invoice sai, disclosure, privilege escalation | Deck chỉ hàm ý qua result | Thiếu một phần | Tác động kinh doanh/quyền | Thêm cột Impact |
| Lab03-11 | Phòng chống | DB price, session, object authz, allowlist; L3-SRC | Slide 7-8 đầy đủ | Đầy đủ | Không | Giữ nguyên |
| Lab03-12 | HTML khớp source | `price=1`, `id=1002`, `role=admin`, `products.price_vnd`, 403 đều khớp L3-EV/L3-SRC | D-HTML:958-984 | Đầy đủ | Không | Giữ nguyên |
| Lab03-13 | Không thêm claim thiếu bằng chứng | Các kết quả chính đều có response/trace | Không thấy claim sai | Đầy đủ | Chỉ thiếu cách dẫn nguồn | Gắn file/trace |
| Lab03-14 | Bao phủ đề | D-REQ yêu cầu môi trường, thao tác và 5 câu | Deck trả lời một phần nhưng thiếu thực hành/evidence | Thiếu nhiều | Môi trường, steps, request, impact | Thêm slide evidence |
| Lab03-15 | Đủ độ sâu | Lab đầy đủ; deck 2 slide | Thiếu source/evidence | Thiếu nhiều | Kết quả | Bổ sung |

## Lab04

| Lab | Yêu cầu trong đề bài | Nội dung tìm thấy trong thư mục Lab | Nội dung đã có trong HTML | Trạng thái | Nội dung còn thiếu | Đề xuất bổ sung |
|---|---|---|---|---|---|---|
| Lab04-01 | Tên và mục tiêu đúng | CSRF đổi email + token/origin; L4-SRC/L4-DOC | Slide 9-10 | Đầy đủ | Không | Giữ nguyên |
| Lab04-02 | Mô tả đúng kỹ thuật | Cookie tự gắn, thiếu intent, SOP/CORS; L4-SRC/L4-DOC | D-HTML:1001-1010 | Đầy đủ | Không | Giữ nguyên |
| Lab04-03 | Nguyên nhân | Chỉ session, không token/origin | D-HTML:1001, 1007-1010 | Đầy đủ | Không | Giữ nguyên |
| Lab04-04 | Cơ chế/quy trình | Hai app local, request/state trace; L4-SRC/L4-EV | Sequence diagram rõ | Đầy đủ | Không | Giữ nguyên |
| Lab04-05 | Môi trường | Victim `5004`, attacker `9004`, Flask/SQLite; L4-DOC | Chỉ nói trang local/victim/target | Thiếu một phần | Port, account, tool | Thêm dòng môi trường |
| Lab04-06 | Các bước | README: login, mở attacker, bấm/xác nhận, secure retest; L4-DOC | Có 4 bước logic nhưng thiếu setup/login/retest | Thiếu một phần | Trước/sau state và thao tác | Thêm steps |
| Lab04-07 | Giải thích source | Route `victim_app.py:354/376`, token/origin modules, attacker form; L4-SRC | Chỉ policy field, không code HTML/server | Thiếu một phần | Attacker form + handler | Chèn 2 snippet |
| Lab04-08 | Kết quả thực tế | Vulnerable 200/email đổi; missing/invalid token 403; state transition; smoke 12/12; L4-EV | Có “email bị đổi”, “403/state giữ nguyên” nhưng không dẫn evidence | Thiếu một phần | Giá trị email, trace/status | Chèn actual result |
| Lab04-09 | Evidence | Request/response/state/log rất đầy đủ; không ảnh; L4-EV | Không nhúng evidence | Không tìm thấy | Request/response/before-after | Chèn evidence |
| Lab04-10 | Tác động | State email đổi ngoài ý muốn; L4-EV | Có mutation nhưng chưa nêu hệ quả account/security | Thiếu một phần | Hậu quả cụ thể | Thêm 2 dòng impact |
| Lab04-11 | Phòng chống | Token, Origin/Referer, SameSite, POST, re-auth; L4-SRC | Slide 10 đầy đủ | Đầy đủ | Không | Giữ nguyên |
| Lab04-12 | HTML khớp source | Source thực tế yêu cầu bấm/xác nhận; slide 9 cũng ghi “mở trang + bấm gửi form” | Khớp implementation | Đầy đủ | Route bị rút gọn | Ghi route đầy đủ |
| Lab04-13 | Không thêm claim thiếu bằng chứng | SOP/CORS được trình bày như lý thuyết; README nói browser behavior chưa đo | HTML dùng “SOP thường…” chứ không tuyên bố đã đo | Đầy đủ | Không | Giữ cách diễn đạt có điều kiện |
| Lab04-14 | Bao phủ đề | D-REQ yêu cầu form tự gửi và ảnh trước/sau; source thực tế cố ý không auto-submit, không có ảnh | Deck không nêu sự lệch này | Thiếu nhiều | Auto-submit theo đề, mã attacker, ảnh | Quyết định sửa Lab hoặc giải trình rõ; ưu tiên cao |
| Lab04-15 | Đủ độ sâu | Lab/evidence tốt; deck 2 slide | Thiếu evidence/source | Thiếu nhiều | Kết quả thực nghiệm | Bổ sung |

## Lab05

| Lab | Yêu cầu trong đề bài | Nội dung tìm thấy trong thư mục Lab | Nội dung đã có trong HTML | Trạng thái | Nội dung còn thiếu | Đề xuất bổ sung |
|---|---|---|---|---|---|---|
| Lab05-01 | Tên và mục tiêu đúng | SQLi login/search + fix; L5-SRC/L5-DOC | Slide 11-12 | Đầy đủ | Không | Giữ nguyên |
| Lab05-02 | Mô tả đúng kỹ thuật | Concat làm input thành SQL syntax | D-HTML:1060-1078 | Đầy đủ | Không | Giữ nguyên |
| Lab05-03 | Nguyên nhân | String interpolation/concat | D-HTML:1062-1067 | Đầy đủ | Không | Giữ nguyên |
| Lab05-04 | Cơ chế/quy trình | Auth bypass và expanded search có trace; L5-EV | Hai nhánh rõ | Đầy đủ | Không | Giữ nguyên |
| Lab05-05 | Môi trường | Flask/SQLite, `127.0.0.1:5005`, SELECT-only; L5-DOC | Chỉ footer “SQLite local/SELECT-only” | Thiếu một phần | Port/tool/database view | Thêm dòng môi trường |
| Lab05-06 | Các bước | README có normal, quote, bypass, search, secure retest | Deck chỉ có payload/flow | Thiếu một phần | Dấu nháy phát hiện, thao tác/retest | Thêm 5 bước |
| Lab05-07 | Giải thích source | Query thật ở L5-SRC | Có snippet concat/bind nhưng giản lược login/password flow | Thiếu một phần | `legacy_password_digest`, `check_password_hash` | Sửa và mở rộng snippet |
| Lab05-08 | Kết quả thực tế | Bypass vulnerable: 1 row; secure: 0; search vulnerable: 8; secure: 0; L5-EV | Chỉ ghi “bypass/expanded”, không số liệu | Thiếu một phần | Status/count/decision/trace ID | Chèn bảng 4 kết quả |
| Lab05-09 | Evidence | Có request/response/query/trace/log; không ảnh; L5-EV | Không nhúng evidence | Không tìm thấy | Request/query/response | Chèn evidence |
| Lab05-10 | Tác động | Auth bypass/data exposure có trong evidence | Deck chỉ nói auth/rows bị đổi | Thiếu một phần | Confidentiality/authentication impact | Thêm impact |
| Lab05-11 | Phòng chống | Parameter binding, PBKDF2, generic errors, least privilege, validation/logging; L5-SRC | Slide 12 đầy đủ | Đầy đủ | Không | Giữ nguyên |
| Lab05-12 | HTML khớp source | Source dùng cột `legacy_password_digest`; L5-SRC | D-HTML:1072 ghi `password_digest` | Sai hoặc không khớp | Sai tên cột; secure snippet bỏ bước verify password hash | Sửa chính xác |
| Lab05-13 | Không thêm claim thiếu bằng chứng | Payload và result chính có evidence, nhưng tên cột HTML không tồn tại trong source | D-HTML:1072 | Sai hoặc không khớp | Claim code sai literal | Sửa trước nộp |
| Lab05-14 | Bao phủ đề | D-REQ còn yêu cầu quote/error detection, môi trường, bước, evidence, câu hỏi | Deck thiếu các phần đó | Thiếu nhiều | Error-based basic, steps, result | Thêm slide evidence |
| Lab05-15 | Đủ độ sâu | Folder nhiều bằng chứng; deck 2 slide | Không kết quả thực | Thiếu nhiều | Evidence | Bổ sung |

## Lab06

| Lab | Yêu cầu trong đề bài | Nội dung tìm thấy trong thư mục Lab | Nội dung đã có trong HTML | Trạng thái | Nội dung còn thiếu | Đề xuất bổ sung |
|---|---|---|---|---|---|---|
| Lab06-01 | Tên và mục tiêu đúng | Plain/Base64/signed/encrypted/server session; L6-SRC/L6-DOC | Slide 13-14 | Đầy đủ | Không | Giữ nguyên |
| Lab06-02 | Mô tả đúng kỹ thuật | Sửa role plain/Base64; L6-EV | D-HTML:1133-1148 | Đầy đủ | Không | Giữ nguyên |
| Lab06-03 | Nguyên nhân | Tin state do client kiểm soát | D-HTML:1133-1151 | Đầy đủ | Không | Giữ nguyên |
| Lab06-04 | Cơ chế/quy trình | Encode/decode/modify/authorize có trace | Cycle và Base64 flow rõ | Đầy đủ | Chưa có DevTools steps | Thêm evidence |
| Lab06-05 | Môi trường | `127.0.0.1:5006`, Flask/SQLite/DevTools; L6-DOC | Không nêu port/tool/account | Thiếu một phần | Môi trường | Thêm dòng |
| Lab06-06 | Các bước | README có plain/Base64/signed/encrypted/session lifecycle | Deck chỉ nêu flow khái niệm | Thiếu một phần | Login, DevTools edit, reload, retest | Thêm 5 bước |
| Lab06-07 | Giải thích source | Nhiều service/policy rõ; L6-SRC | Không có snippet hoặc tên cookie thật | Thiếu một phần | `lab06_role`, `lab06_profile_b64`, policy functions | Chèn code ngắn |
| Lab06-08 | Kết quả thực tế | Smoke 20/20; plain/base64 allow after modify; signed tamper 400; session 403/200/401; L6-EV | Bảng chỉ mô tả thuộc tính, không status/output | Thiếu một phần | Actual result/status | Chèn bảng runtime |
| Lab06-09 | Evidence | 101 JSON + request/response/session/log; không ảnh; L6-EV | Không nhúng evidence | Không tìm thấy | Cookie diff, status, session event | Chèn evidence |
| Lab06-10 | Tác động | Access control bypass trong plain/Base64 | Deck có “allow sai” nhưng chưa nêu privilege/data risk | Thiếu một phần | Impact cụ thể | Thêm impact |
| Lab06-11 | Phòng chống | Signed/encrypted/session, DB role, rotate/revoke/flags; L6-SRC | Slide 14 và tổng hợp nêu đủ | Đầy đủ | Không | Giữ nguyên |
| Lab06-12 | HTML khớp source | Signed flow thực tế verify signature **và dùng current database role**; `authorization_service.py:61-85` | D-HTML:1166 ghi nguồn role “Payload đã ký” | Sai hoặc không khớp | Nguồn quyết định bị ghi sai | Đổi thành DB role hiện tại sau verify |
| Lab06-13 | Không thêm claim thiếu bằng chứng | Dòng signed role source trái source/test; L6-SRC | D-HTML:1166 | Sai hoặc không khớp | Claim sai | Sửa trước nộp |
| Lab06-14 | Bao phủ đề | D-REQ yêu cầu quan sát toàn bộ cookie attributes, bước sửa, câu hỏi, evidence | Deck thiếu giá trị cookie thật, flags thực và kết quả | Thiếu nhiều | Observation table/steps/result | Thêm slide evidence |
| Lab06-15 | Đủ độ sâu | Lab06 có evidence nhiều nhất; deck 2 slide | Không sử dụng evidence | Thiếu nhiều | Kết quả | Bổ sung |

## Thống kê 90 tiêu chí

| Trạng thái | Số lượng |
|---|---:|
| Đầy đủ | 35 |
| Thiếu một phần | 26 |
| Thiếu nhiều | 15 |
| Không tìm thấy | 10 |
| Sai hoặc không khớp | 4 |
| **Tổng** | **90** |

Điểm quy đổi: `(35×1 + 26×0,5 + 15×0,25) / 90 = 57,5%`, làm tròn **58%**.

# Phần 3. Kiểm tra tính chính xác

## 3.1. Nội dung sai hoặc không khớp trực tiếp

1. **Lab05 — sai tên cột trong query authentication bypass**
   - Vị trí cần sửa: D-HTML, slide 11 “Authentication bypass”, dòng 1072.
   - HTML hiện ghi: `password_digest`.
   - Source thực tế: `legacy_password_digest` tại `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab05\vulnerable_queries.py:9` và `:22`.
   - Payload thực tế đúng là `admin_lab' -- ` tại `Lab05\config.py:8`; response thật là `local_demo_bypass`, 1 row tại `Lab05\evidence\responses\auth_logic_vulnerable.txt`.
   - Sửa thành: `AND legacy_password_digest='…'` hoặc hiển thị nguyên query masked từ evidence.

2. **Lab06 — sai nguồn role của signed-cookie authorization**
   - Vị trí cần sửa: D-HTML, slide 14, dòng 1166, cột “Nguồn role”.
   - HTML hiện ghi: `Payload đã ký`.
   - Source thực tế: signed payload được verify, sau đó `authorize_signed_admin()` kiểm tra identity và **current database role**; xem `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab06\authorization_service.py:61-85` và `Lab06\app.py:658-741`.
   - Test còn chứng minh payload role `admin` nhưng DB role `user` vẫn bị từ chối: `Lab06\tests\test_authorization.py:48-56`.
   - Sửa thành: `Payload đã verify + role hiện tại trong DB (DB quyết định)`.

## 3.2. Nội dung rút gọn, chưa phải lỗi logic nhưng cần gắn nhãn

- **Lab01 slide 4, dòng 847:** `Markup(body)` là ký hiệu rút gọn; code thật là `Markup(row["body"])` tại `Lab01\app.py:88`.
- **Lab02 slide 6, dòng 926-930:** `strnlen(input, 33)`, `reject()`, `snprintf(name, 32,...)` là pseudocode. Code thật dùng `user_input`, `NAME_BUFFER_SIZE + 1U`, `memcpy`, `return 65`, và `sizeof(name)`; xem ba file C trong L2-SRC. Nên ghi “pseudocode” hoặc thay bằng code literal.
- **Lab04 slide 9, dòng 1007:** `POST change-email` thiếu route thật. Source có `/vulnerable/change-email` và `/secure/change-email` tại `Lab04\victim_app.py:354` và `:376`.
- **Lab06 slide 13:** tên cookie thật là `lab06_username`, `lab06_role`, `lab06_profile_b64`; xem `Lab06\cookie_service.py:11-12` và `base64_cookie_service.py:14`. Nội dung hiện không sai về khái niệm nhưng chưa đủ chính xác để đối chiếu DevTools.

## 3.3. Không khớp với yêu cầu đề bài

- **Lab04:** D-REQ yêu cầu attacker page có form tự gửi. Implementation thực tế ghi rõ “chỉ gửi sau khi bấm nút và xác nhận” tại `C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab04\attacker_templates\attack_page.html:5-8`; HTML cũng mô tả “mở trang + bấm gửi form” ở dòng 1006. Vì vậy HTML khớp source nhưng source/deck chưa hoàn thành đúng nhiệm vụ auto-submit trong đề.
- **Toàn bộ sáu Lab:** D-REQ yêu cầu ảnh chụp từng bước và báo cáo PDF. Sáu Lab hiện có 0 ảnh thật; DOCX mới dùng nội dung/placeholder và không nhúng media. HTML dòng 1239 lại nêu “Ảnh từng bước” như evidence tối thiểu nhưng chính deck không chứa ảnh hay ghi trạng thái “chưa có”.
- **Lab02:** đề yêu cầu log GDB xác định crash/stack/ngưỡng. Folder có GDB script/hướng dẫn nhưng không có GDB output thực; chỉ có ASan trace. HTML không được phép biến sơ đồ stack thành bằng chứng GDB.

## 3.4. Nội dung động khi chạy HTML

- `SlidePresentation` chỉ đổi `active/visible/aria-hidden`, counter, progress và hash; không tạo nội dung Lab.
- `InlineEditor.restore()` có thể thay 61 vùng `[data-editable]` từ `localStorage`. Browser context kiểm tra không có bản chỉnh sửa lưu trước; nội dung runtime khớp file tĩnh.
- Không có lỗi JavaScript/console khi load hoặc điều hướng.
- HTML không có `<img>`, SVG hoặc canvas trong 18 slide; tất cả hình minh họa hiện là CSS boxes/flow, không phải bằng chứng thực nghiệm.

# Phần 4. Danh sách nội dung cần bổ sung

## Ưu tiên cao

1. Sửa `password_digest` → `legacy_password_digest` ở Lab05 slide 11.
2. Sửa nguồn role của Signed Cookie ở Lab06 slide 14 thành “signature verified + current DB role”.
3. Thêm ít nhất một slide evidence dùng dữ liệu thật cho mỗi Lab:
   - Lab01: request/response Reflected, row SQLite Stored, DOM runtime.
   - Lab02: ASan input 64/write 65/SIGABRT/exit -6; ghi rõ chưa có GDB log.
   - Lab03: price 1 accepted vs recalculated; IDOR 200 vs 403; role escalation vs blocked.
   - Lab04: vulnerable 200 + state email đổi; secure missing/invalid token 403 + state giữ nguyên.
   - Lab05: bypass 1 vs 0 row; search 8 vs 0 row; query thật.
   - Lab06: plain/Base64 allow sau sửa; signed tamper 400; session 403/200/401.
4. Giải quyết yêu cầu auto-submit của Lab04 hoặc ghi rõ sai khác và xin chấp nhận; hiện chưa đúng câu chữ đề.
5. Bổ sung ảnh chụp thủ công thực tế. Không tuyên bố hoàn thành yêu cầu ảnh trước khi có file.
6. Với Lab02, thu thập GDB log thật cho vị trí crash, stack overwrite và ngưỡng; không dùng sơ đồ khái niệm thay bằng chứng.

## Ưu tiên trung bình

1. Thêm môi trường cho từng Lab: stack, URL/port, tài khoản/tool chính.
2. Thêm các bước thực hiện ngắn theo vulnerable → observed → patch → secure retest.
3. Gắn mỗi kết quả với file/trace ID/status cụ thể.
4. Thêm impact ngắn, tách “có thể” khỏi “đã quan sát”.
5. Đưa code thật hoặc ghi rõ “pseudocode” cho Lab02; đưa tên route/cookie thật cho Lab04/Lab06.
6. Bao phủ các câu hỏi báo cáo còn thiếu, ưu tiên câu nào chưa thể suy ra trực tiếp từ slide.

## Ưu tiên thấp

1. Thêm caption nguồn dưới evidence: file, timestamp, trace ID.
2. Dùng màu/nhãn riêng cho “Observed”, “Source-backed”, “Conceptual”.
3. Giữ slide tổng hợp 15-18 nhưng rút một phần trang chuyển chương để dành chỗ cho evidence.
4. Thêm số Lab và route đầy đủ ở footer để người nghe đối chiếu nhanh.

# Phần 5. Kết luận

- `Topic04_6Labs_short.html` **chưa trình bày đầy đủ** yêu cầu của `BaiTapTopic04.docx`.
- Điểm mạnh: tên Lab, bản chất lỗ hổng, trust boundary, root cause và biện pháp phòng chống nhìn chung đúng; HTML chạy ổn định và không phụ thuộc tài nguyên ngoài.
- Điểm thiếu có hệ thống: môi trường, bước thao tác, source literal, kết quả runtime, request/response/log/terminal, ảnh thực nghiệm và impact. Deck tự yêu cầu “evidence đi trước kết luận” nhưng không hiển thị evidence nào.
- **Lab đầy đủ nhất:** Lab04 theo thang 15 tiêu chí (10/15 điểm quy đổi, khoảng 66,7%), do flow và secure gate được mô tả rõ; tuy nhiên vẫn có lệch bắt buộc auto-submit so với đề.
- **Lab thiếu/sai nhiều nhất:** Lab05 và Lab06 đồng hạng thấp nhất (8/15 điểm quy đổi, khoảng 53,3%) vì ngoài thiếu evidence còn có một nội dung source không khớp trực tiếp ở mỗi Lab.
- Phần bắt buộc phải sửa trước khi nộp: hai lỗi chính xác Lab05/Lab06; evidence thực; ảnh từng bước; Lab04 auto-submit/giải trình; Lab02 GDB log; môi trường và steps cho sáu Lab.
- **Ước lượng hoàn thành toàn bộ deck: 58%.**

# Phần 6. Đề xuất chỉnh sửa HTML

## Lab01

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 3 “Ba luồng XSS” | Thêm route thật và 1 dòng observed result cho mỗi loại | `Lab01\app.py`, `Lab01\evidence\traces\*.json` | Dưới từng flow |
| Slide 4 “Vá XSS” | Đổi `Markup(body)` thành `Markup(row["body"])`; thêm code/file line | `Lab01\app.py:59,86,88`; hai DOM JS | Trong bảng comparison |
| Sau slide 4 | Thêm slide Evidence: request/response Reflected, SQLite Stored, DOM before/after; ghi “chưa có ảnh” nếu chưa chụp | L1-EV | Trước Lab02 |

## Lab02

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 5 “HTTP tới stack” | Ghi môi trường `Linux/WSL/Docker · GCC/GDB · 127.0.0.1:5002` | `Lab02\README.md`, `config.py` | Header phụ |
| Slide 6 “Vá Buffer Overflow” | Gắn nhãn pseudocode hoặc thay bằng code literal | Ba file C trong L2-SRC | Hai code box |
| Sau slide 6 | Thêm ASan result: 64-byte input, 65-byte write, line 7, SIGABRT, exit -6; ghi GDB log chưa có | `Lab02\evidence\traces\aece51864ec14840a288a2ba64e49544.json` | Trước Lab03 |

## Lab03

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 7 | Thêm route `/vulnerable/...` và `/secure/...` | `Lab03\app.py` | Dưới tên scenario |
| Slide 8 | Thêm status thực: checkout 200, IDOR secure 403, role secure giữ user | `Lab03\evidence\responses\*.json` | Cột “Secure result” |
| Sau slide 8 | Chèn request/response + DB diff/trace ID cho ba scenario | L3-EV | Trước Lab04 |

## Lab04

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 9 | Đổi `POST change-email` thành hai route thật; ghi port 5004/9004 | `Lab04\victim_app.py:354,376`, `attacker_app.py:79` | Sequence message/header |
| Slide 9 | Ghi rõ implementation hiện cần bấm/xác nhận và chưa thỏa yêu cầu auto-submit | `Lab04\attacker_templates\attack_page.html:5-8`, D-REQ | Sequence note |
| Slide 10 | Thêm actual result: vulnerable 200/email đổi; missing/invalid token 403/state giữ nguyên | L4-EV | Hai request card |
| Sau slide 10 | Chèn attacker form source và state transition trước/sau | L4-SRC/L4-EV | Trước Lab05 |

## Lab05

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 11 “Authentication bypass” | Sửa `password_digest` thành `legacy_password_digest` | `Lab05\vulnerable_queries.py:9,22` | Dòng query |
| Slide 11 | Thêm result count: vulnerable 1, secure 0; search vulnerable 8, secure 0 | `Lab05\evidence\responses\auth_logic_*.txt`, `expanded_search_*.txt` | Dưới từng branch |
| Slide 12 | Mở rộng secure login: lookup `username = ?`, sau đó `check_password_hash` | `Lab05\secure_queries.py`, `auth_service.py` | Secure code box |
| Sau slide 12 | Chèn quote detection/error category và query masked | L5-EV | Trước Lab06 |

## Lab06

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 13 | Ghi tên cookie thật `lab06_role`, `lab06_profile_b64` và status allow/deny | `Lab06\cookie_service.py`, `base64_cookie_service.py`, L6-EV | Các node |
| Slide 14 | Sửa hàng Signed: nguồn role là current DB role sau verify | `Lab06\authorization_service.py:61-85`, `app.py:658-741` | Cột “Nguồn role” |
| Slide 14 | Thêm runtime: signed tamper 400; session student 403/admin 200/old token 401 | `Lab06\evidence\logs\runtime_smoke_test.txt` | Dưới bảng |
| Sau slide 14 | Chèn cookie diff, signed verification, rotation/logout event | `Lab06\evidence\cookies\`, `sessions\` | Trước slide tổng hợp |

## Slide tổng hợp

| Section hiện tại | Nội dung cần thêm/sửa | File nguồn | Vị trí nên chèn |
|---|---|---|---|
| Slide 17 “Evidence tối thiểu” | Đổi từ lời khuyên chung thành bảng trạng thái thật: JSON/log có, ảnh chưa có, GDB Lab02 chưa có | Chỉ mục L1-EV đến L6-EV | Panel phải |
| Slide 18 | Giữ kết luận nhưng không dùng câu “chỉ kết luận điều đã quan sát” nếu các slide trước vẫn thiếu evidence | Toàn bộ báo cáo này | Trước khi nộp |

