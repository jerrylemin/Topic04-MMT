# Demo script Lab06 — Cookie Poisoning

## Mục tiêu demo

- Chứng minh plain và Base64 cookie không bảo vệ integrity của role.
- So sánh signed/encrypted cookie với server-side session.
- Quan sát cookie value/flags, signature/encryption trace và database authorization.
- Phân biệt cookie poisoning với session hijacking; luôn giữ authorization server-authoritative.

## Chuẩn bị

- Thư mục làm việc: `cd Lab06`
- Khởi động: `scripts\run_lab.bat`
- URL: `http://127.0.0.1:5006`
- Reset khi cần: `python seed.py` tại `Lab06`; để revoke session demo dùng nút `Reset Lab06` gửi `POST /reset-lab`.
- Tài khoản: `student / Student123!` (role `user`), `admin_lab / AdminLab123!` (role `admin`)
- Chỉ sửa cookie thủ công trên `127.0.0.1:5006`, không dùng JavaScript đọc cookie.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`, mở `Network`, bật `Preserve log`/`Disable cache` và bấm `Clear` trước mỗi mode.
- `Application → Storage → Cookies → http://127.0.0.1:5006`: show Name, Value cần tamper, Path, HttpOnly, SameSite, Secure; chỉ sửa đúng cookie demo, che session value khi trình bày.
- `Network → Headers`: show request URL/method, tên cookie trong `Cookie`, status và `Response`; không dùng `document.cookie` và không copy credential ra ngoài.
- Các inspector còn lại là panel ứng dụng: `Base64`/`Signature`/`Encryption`/`Session`/`Authorization`; dùng chúng để giải thích transform và decision sau khi F12 đã chứng minh request.

## Kịch bản trình bày

*Quy ước bằng chứng: cookie/status/trace dưới đây phải được xác nhận live. Giá trị Base64 là source-derived; nếu UI hiện `—`, không gọi đó là chuỗi đã copy từ UI.*

**Bước 1 — Plain cookie tin trực tiếp role**

* Thao tác:
  1. Mở `http://127.0.0.1:5006`, bấm `Bắt đầu flow cố định` hoặc menu `Đăng nhập demo`.
  2. Bấm ô `Tên đăng nhập`, nhập `student`; bấm ô `Mật khẩu`, nhập `Student123!`.
  3. Mở dropdown `Mô hình demo`, chọn `Plain Cookie Demo`, rồi bấm `Đăng nhập và tạo flow`.
  4. Ở trang kết quả bấm `Mở profile`, sau đó bấm `Thử trang admin`.
  5. Nhấn `F12`, chọn `Application → Storage → Cookies → http://127.0.0.1:5006`, tìm `lab06_role`, bấm đúp value `user`, sửa thành `admin`, giữ Path `/`, rồi nhấn `Ctrl+R`.
* Nói: “Role nằm trực tiếp trong cookie client-controlled. HttpOnly=False ở plain mode chỉ để quan sát thủ công, không phải cơ chế integrity.”
* Quan sát: trước sửa kỳ vọng `/vulnerable/plain/admin` là `403`; sau sửa cookie, kỳ vọng response cho phép/`200` vì route đọc `role=admin` từ request cookie; ghi status live.
* F12 show: `Application → Cookies` show row `lab06_role` trước/sau; `Network → GET /vulnerable/plain/admin` show request Cookie có role đã đổi và status `403`→`200` nếu live; không đọc session value.
* Kết luận: server không được dùng role do client gửi làm nguồn authorization.

**Bước 2 — Base64 chỉ là encoding**

* Thao tác:
  1. Trong Application → Cookies, chọn cookie `lab06_role`, bấm chuột phải/xóa rồi quay lại menu `Đăng nhập demo`.
  2. Nhập `student` / `Student123!`, chọn `Base64 Cookie Demo`, bấm `Đăng nhập và tạo flow`.
  3. Ở trang kết quả bấm `Mở profile`; mở lại F12 → Application → Cookies, tìm `lab06_profile_b64`.
  4. Sửa value thành `eyJ1c2VybmFtZSI6InN0dWRlbnQiLCJyb2xlIjoiYWRtaW4ifQ==`, nhấn `Ctrl+R`, rồi bấm `Mở trang admin` hoặc mở card admin trên profile.
* Nói: “JSON gốc `{"username":"student","role":"user"}` chỉ được Base64 encode. Tôi đổi role trong JSON rồi encode lại, không cần secret.”
* Quan sát: trước sửa kỳ vọng role decode là `user` và admin bị từ chối; sau sửa, source hiện tại decode role `admin` và route vulnerable kỳ vọng cho phép. Chuỗi admin là giá trị source-derived; route profile hiện tại không truyền `demo_values`, nên nếu phần fixed-value hiển thị `—` thì việc copy chuỗi từ UI là “Chưa có bằng chứng/không được implementation hiện tại hỗ trợ”; không gọi đó là UI-observed.
* F12 show: `Application → Cookies` show `lab06_profile_b64` trước/sau; `Network → GET /vulnerable/base64/admin` show Cookie field và status; panel `Base64 Inspector` show decoded role/integrity=false nếu runtime trả các trường đó.
* Kết luận: Base64 không tạo confidentiality hoặc integrity; bất kỳ ai sửa được cookie có thể sửa payload.

**Bước 3 — Signed cookie từ chối tamper**

* Thao tác:
  1. Xóa `lab06_profile_b64` trong Application → Cookies, rồi bấm menu `Đăng nhập demo`.
  2. Nhập `student` / `Student123!`, chọn `Signed Cookie Demo`, bấm `Đăng nhập và tạo flow`.
  3. Ở trang kết quả bấm `Mở signed profile`; trong Application → Cookies tìm `lab06_signed_profile`.
  4. Bấm đúp value, sửa đúng một ký tự, nhấn `Ctrl+R`; trong F12 → Network chọn request profile để xem status/response sau tamper.
* Nói: “Signed cookie không giấu payload nhưng chữ ký ràng buộc payload với secret server. Tôi chỉ đổi một ký tự để kiểm tra toàn vẹn.”
* Quan sát: token hợp lệ hiển thị profile; token bị đổi kỳ vọng trả `400`/invalid signature, `payload_used=false` và trace `signature_rejected`; chỉ báo số/status thật sau live.
* F12 show: `Application` show đổi một ký tự trong `lab06_signed_profile`; `Network → GET /secure/signed/profile` show status/Response invalid signature; panel `Signature Inspector` show rejected và `payload_used=false`.
* Kết luận: signing giải quyết integrity/authenticity của payload, không tự giải quyết authorization hoặc confidentiality.

**Bước 4 — Signed payload vẫn cần database authorization**

* Thao tác:
  1. Từ kết quả Signed Cookie, bấm `Kiểm tra admin` khi đang là `student`; ghi lại status/decision.
  2. Bấm menu `Đăng nhập demo`, nhập `admin_lab` / `AdminLab123!`, chọn lại `Signed Cookie Demo`, bấm `Đăng nhập và tạo flow`.
  3. Ở trang kết quả bấm `Kiểm tra admin` lần nữa, rồi mở trace/Authorization Inspector để so sánh student và admin.
* Nói: “Chữ ký chứng minh server đã phát hành payload, nhưng quyền admin vẫn phải kiểm tra role hiện tại ở database.”
* Quan sát: student kỳ vọng `403`; admin kỳ vọng `200` nếu database role là `admin`; trace chỉ ra `signature_verified_then_database_role_checked`.
* F12 show: chọn `Network → GET /secure/signed/admin` ở cả hai session, so sánh status/Response; panel `Authorization Inspector` show database role và decision, không chỉ dựa vào cookie value.
* Kết luận: signed cookie không phải giấy phép bỏ qua server-side authorization.

**Bước 5 — Encrypted cookie bảo mật nội dung nhưng không phải nguồn quyền**

* Thao tác:
  1. Nhấn `Ctrl+L`, nhập chính xác `http://127.0.0.1:5006/secure/encrypted-demo`, nhấn `Enter`. Không bấm link stale `/secure/encrypted/demo` nếu giao diện còn hiển thị link đó.
  2. Cuộn tới trace panel, bấm tab `Encryption`.
  3. Mở rộng các dòng valid/tampered trong trace để chỉ decrypt thành công, decrypt bị từ chối và `authorization_used=false`.
* Nói: “Route read-only tự tạo token Fernet, giải mã token hợp lệ và thử token bị tamper. Payload demo chỉ là preferences/issued_at, không quyết định admin.”
* Quan sát: trace kỳ vọng có `Fernet authenticated encryption`, valid decrypt và tampered decrypt bị từ chối; header/trace nêu `authorization_used=false`; xác nhận live.
* F12 show: `Network → GET /secure/encrypted-demo → Headers` show `X-Lab-Encryption-Status`, `X-Lab-Authorization-Used` và trace ID; panel `Encryption Inspector` show valid/tampered decrypt, không show token đầy đủ.
* Kết luận: encryption cung cấp bí mật + toàn vẹn, nhưng mọi quyết định quyền vẫn phải lấy từ policy/server state.

**Bước 6 — Server-side session và rotation/logout**

* Thao tác: xóa cookie cũ; tại `/login` chọn `Server-side Session`, đăng nhập `student`/`Student123!`; mở `/secure/session/profile`, `/secure/session/admin`; sau đó đăng nhập `admin_lab / AdminLab123!` cùng mode và mở `/secure/session/admin`; gọi logout bằng Console trên cùng origin: `fetch("/secure/session/logout",{method:"POST",credentials:"same-origin"}).then(r=>r.status)`.
* Thao tác chi tiết:
  1. Trong Application → Cookies xóa cookie demo cũ nếu còn, rồi bấm menu `Đăng nhập demo`.
  2. Nhập `student` / `Student123!`, chọn `Server-side Session`, bấm `Đăng nhập và tạo flow`.
  3. Ở trang kết quả bấm `Mở profile`, sau đó bấm `Kiểm tra admin` để ghi nhận student bị từ chối.
  4. Quay lại menu `Đăng nhập demo`, nhập `admin_lab` / `AdminLab123!`, giữ `Server-side Session`, bấm `Đăng nhập và tạo flow`; bấm `Kiểm tra admin` và ghi nhận kết quả admin.
  5. Không có nút logout riêng trong flow này: mở F12 → `Console` trên đúng origin và chạy `fetch("/secure/session/logout",{method:"POST",credentials:"same-origin"}).then(r=>r.status)`; sau đó quay lại profile/admin để kiểm tra session cũ bị revoke.
* Nói: “Cookie `lab06_session` chỉ là opaque ID; server hash/resolve nó rồi tải user và role từ SQLite. Logout revoke record và expire cookie, nên session cũ không còn dùng được.”
* Quan sát: student kỳ vọng `/secure/session/admin` bị 403, admin kỳ vọng được phép; Session Inspector không chứa role/user ID trong cookie; logout response có Set-Cookie expire và request sau đó bị từ chối theo status live.
* F12 show: `Application` show `lab06_session` là opaque ID; `Network` show `GET /secure/session/profile`, `GET /secure/session/admin` và `POST /secure/session/logout`; mở `Headers/Response` của logout để show `Set-Cookie` expire; panel `Session`/`Authorization` show role lấy từ database.
* Kết luận: server-side session đưa identity/authorization về trusted server state và hỗ trợ rotate, revoke, logout invalidation.

## Demo Vulnerable → Secure

| Mô hình | Cùng dữ liệu/tác vụ | Vulnerable → nguyên nhân | Secure → primary fix |
|---|---|---|---|
| Plain | `lab06_role=user` → `admin` | Route tin trực tiếp cookie role | Không dùng cookie role; dùng signed/session + server policy |
| Base64 | JSON `role=user` → `role=admin`, cookie `lab06_profile_b64` | Decode được nhưng không có integrity | Signing chống sửa; server session là nguồn role |
| Signed | Đổi một ký tự `lab06_signed_profile` | Không áp dụng quyền nếu signature invalid | Reject trước `payload_used`; vẫn check database role |
| Encrypted | Tamper token Fernet | Token bị sửa không decrypt được, nhưng encryption không authorize | Dùng mã hóa cho bí mật/toàn vẹn; authorization lấy từ server |
| Server session | student/admin cùng `/secure/session/admin` | Không tin role trong cookie | Resolve opaque ID, tải role DB, rotate/revoke/logout |

## Câu hỏi trong BaiTapTopic04.docx

**Câu 37. Vì sao cookie là dữ liệu không đáng tin cậy?**  
**Trả lời khi demo:** Cookie nằm ở browser và request gửi lại có thể bị người dùng sửa, copy hoặc replay trong phạm vi kiểm soát của họ. Bước plain/Base64 cho thấy server không được coi mọi field trong cookie là trusted authorization.

**Câu 38. Cookie Poisoning khác Session Hijacking như thế nào?**  
**Trả lời khi demo:** Cookie Poisoning là sửa nội dung/claim của cookie để server ra quyết định sai, như đổi role user thành admin. Session Hijacking là lấy và dùng session credential hợp lệ của người khác; signed/server session chống sửa nhưng vẫn cần bảo vệ việc lộ session ID.

**Câu 39. Base64 có phải là mã hóa không?**  
**Trả lời khi demo:** Không. Base64 chỉ là encoding có thể decode công khai, không tạo bí mật và không có chữ ký; chuỗi admin của Lab06 được tạo lại mà không cần key.

**Câu 40. Signed cookie giải quyết vấn đề gì?**  
**Trả lời khi demo:** Signed cookie giúp phát hiện payload bị sửa và xác minh nó do server phát hành nếu secret được bảo vệ. Nó không mã hóa nội dung và không thay thế kiểm tra role/authorization phía server.

**Câu 41. Vì sao server-side authorization vẫn là bắt buộc?**  
**Trả lời khi demo:** Cookie, kể cả signed hoặc encrypted, vẫn là dữ liệu mang claim và có thể cũ, bị replay hoặc không còn đúng trạng thái account. Server phải resolve identity, kiểm tra role/object/policy và quyết định allow/deny từ nguồn authoritative.

## Nếu demo lỗi

- Nếu cookie cũ làm lẫn mode, xóa đúng `lab06_username`, `lab06_role`, `lab06_profile_b64`, `lab06_signed_profile`, `lab06_encrypted_profile`, `lab06_session` rồi đăng nhập lại.
- Nếu cần làm sạch session server, mở Dashboard và bấm `Reset Lab06` (POST `/reset-lab`); `python seed.py` chỉ seed user, không tự revoke mọi session.
- Nếu Base64 profile hiện `—`, ghi rõ mismatch hiện tại: route profile không truyền `demo_values`; dùng chuỗi source-derived và trace/history, không gọi là UI-observed.
- Nếu signed/encrypted/session status khác expected, lưu trace/status thật và nói “chưa xác nhận theo expected”; không tự sửa cookie để tạo bằng chứng secure.

## Chốt lab

Root cause: server dùng dữ liệu client-controlled trong cookie làm nguồn role/authorization.
Primary fix: signature/server-side session và kiểm tra authorization từ database/policy.
Defense in depth: encryption khi cần bí mật, HttpOnly/SameSite/Secure, rotation, expiry, revoke và logout.
