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

- Nhấn `F12` hoặc `Ctrl+Shift+I`; bấm `Network`, bật `Preserve log` và `Disable cache`, rồi bấm thùng rác `Clear` trước mỗi mode.
- Để sửa cookie thủ công, bấm `Application` → bên trái mở `Storage` → `Cookies` → bấm đúng `http://127.0.0.1:5006` (không chọn host/port khác) → click đúng row cookie được ghi trong bước đó. Bấm đúp cột `Value`, sửa đúng cookie demo, nhấn `Enter`; nếu không thấy row, reload trang rồi mở lại đúng host, không tạo cookie mới bằng Console.
- Để chứng minh request, bấm `Network` → ô `Filter` gõ route như `/plain/admin`, `/base64/admin` hoặc `/signed/profile` → bấm dòng vừa phát sinh. Trong pane phải bấm `Headers` → `General` để kiểm tra `Request URL`, `Request Method` và status; mở `Request Headers`/`Response` chỉ vào header hoặc decision được ghi rõ ở bước tương ứng.
- Trace panel là panel ứng dụng trên trang, không phải F12. Sau khi xem Network quay lại trang, cuộn xuống và bấm đúng tab `Cookie`, `Base64`, `Signature`, `Encryption`, `Session`, `Authorization`, `Database`, `Audit` hoặc `Verdict`.
- Không dùng `document.cookie` và không copy credential. Nếu cần show cookie, chỉ vào Name/Path/flags hoặc giá trị đã được che.


## Kịch bản trình bày

*Quy ước: đọc từng mục theo thứ tự **Thao tác → Nói khi demo → F12 show → Quan sát**. Cookie chỉ kiểm tra tên/flags hoặc giá trị đã che; không dùng Console để đọc hay tự tạo cookie.*

### Bước 1 — Plain cookie tin trực tiếp role

1. **Thao tác:** Mở `http://127.0.0.1:5006`, vào menu `Đăng nhập demo` và chọn flow `Plain Cookie Demo`.
   - **Nói khi demo:** “Tôi bắt đầu với plain cookie để cho thấy role nằm trong dữ liệu do browser gửi lại.”
   - **F12 show:** Nhấn `F12` → `Network` → bấm `Clear`; tích `Preserve log` và `Disable cache`. Trong ô `Filter` nhập `/login`. Chưa mở Console và không chạy JavaScript đọc cookie.
   - **Quan sát:** Đúng form Plain Cookie xuất hiện; Network chờ request login mới.
2. **Thao tác:** Nhập `student` / `Student123!`, chọn `Plain Cookie Demo` nếu form yêu cầu, rồi bấm `Đăng nhập và tạo flow`.
   - **Nói khi demo:** “Tôi đăng nhập student để tạo cookie role=user ban đầu.”
   - **F12 show:** Chọn request mới nhất có tên/URL `/login` → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` chỉ vào username `student`; che password. Nếu URL có mode, xác nhận đúng plain, không chọn request của mode khác.
   - **Quan sát:** Ghi status/redirect thật và chờ trang kết quả; login thành công mới tiếp tục.
3. **Thao tác:** Trên trang kết quả bấm `Mở profile`, sau đó bấm `Mở trang admin` hoặc `Kiểm tra admin` để có request kiểm tra quyền ban đầu.
   - **Nói khi demo:** “Trước khi sửa cookie, student phải bị từ chối ở admin route.”
   - **F12 show:** Đổi Network Filter thành `/vulnerable/plain/admin` → chọn request GET mới nhất → `Headers` → `General` kiểm tra URL/status → `Request Headers` nếu cần chỉ tên cookie, không đọc value → `Response` → `Ctrl+F` tìm `decision` hoặc `admin`.
   - **Quan sát:** Ghi decision/status ban đầu; nếu nhiều chữ admin, chọn object/message kết quả request, không chọn link menu.
4. **Thao tác:** Trong DevTools bấm `Application` → cây bên trái mở `Storage` → `Cookies` → chọn đúng `http://127.0.0.1:5006`, tìm hàng `Name=lab06_role`.
   - **Nói khi demo:** “Tôi sửa đúng cookie demo, không sửa username hay tạo cookie mới.”
   - **F12 show:** Trong bảng cookie chọn row có chính xác `Name = lab06_role`; nếu có nhiều host, chỉ chọn host `http://127.0.0.1:5006`. Chỉ vào `Path`/flags và value hiện tại nếu cần; không mở các cookie khác.
   - **Quan sát:** Value ban đầu là role user theo UI/runtime; nếu không thấy row, reload đúng host rồi mở lại Application.
5. **Thao tác:** Bấm đúp cột `Value` của đúng row `lab06_role` → nhấn `Ctrl+A` → nhập `admin` → nhấn `Enter`, rồi reload và bấm lại `Mở trang admin`.
   - **Nói khi demo:** “Tôi chỉ đổi claim role trong cookie; nếu route vulnerable tin cookie, quyết định sẽ thay đổi.”
   - **F12 show:** Application → nhìn lại đúng row để xác nhận Value đã lưu, sau đó bấm `Network` → Filter `/vulnerable/plain/admin` → chọn request mới nhất sau reload → `Headers` → `General` kiểm tra `GET`/URL/status → `Request Headers` chỉ tên `Cookie`, che full value → `Response` tìm `decision` hoặc `admin` nếu có.
   - **Quan sát:** So sánh status/decision trước và sau sửa cookie; chỉ kết luận nếu request sau reload thật sự dùng đúng route.
**Kết luận:** Plain cookie không có integrity; server không được dùng role do client kiểm soát làm nguồn authorization.

### Bước 2 — Base64 chỉ là encoding

1. **Thao tác:** Trong Application → Cookies, chọn đúng host `http://127.0.0.1:5006`, xóa cookie demo cũ nếu còn bằng nút xóa của DevTools, rồi quay lại menu `Đăng nhập demo`.
   - **Nói khi demo:** “Tôi dọn cookie mode trước để Base64 flow không bị lẫn với plain cookie.”
   - **F12 show:** Application → Storage → Cookies → đúng host → xóa đúng row được ghi trong UI; không dùng Console để set/delete hàng loạt. Sau đó Network → `Clear` → Filter `/login`.
   - **Quan sát:** Cookie cũ biến mất hoặc trạng thái sạch được hiển thị; nếu chưa sạch, reload đúng host trước khi login.
2. **Thao tác:** Nhập `student` / `Student123!`, chọn `Base64 Cookie Demo` và bấm `Đăng nhập và tạo flow`.
   - **Nói khi demo:** “Base64 chỉ encode JSON; nó không tạo chữ ký hay bí mật.”
   - **F12 show:** Network → chọn request login mới nhất → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` xác nhận username/mode, che password. Không tìm chuỗi Base64 trong request login nếu endpoint không gửi nó ở đó.
   - **Quan sát:** Ghi status/redirect và chờ trang Base64 profile.
3. **Thao tác:** Bấm `Mở profile`; sau đó mở F12 → `Application` → `Storage` → `Cookies` → `http://127.0.0.1:5006` và tìm `Name=lab06_profile_b64`.
   - **Nói khi demo:** “Cookie profile chứa payload đã encode; tôi chọn đúng row bằng Name, không chọn lab06_role.”
   - **F12 show:** Trong bảng cookie bấm row có chính xác `Name = lab06_profile_b64`; chỉ value hiện tại nếu cần và che phần không liên quan. Nếu có nhiều row, không chọn `lab06_role` hoặc `lab06_signed_profile`.
   - **Quan sát:** Xác nhận row Base64 tồn tại; nếu value UI hiện `—`, ghi rõ đó không phải chuỗi source-observed.
4. **Thao tác:** Bấm đúp cột `Value` của `lab06_profile_b64` → `Ctrl+A` → nhập chuỗi source-derived `eyJ1c2VybmFtZSI6InN0dWRlbnQiLCJyb2xlIjoiYWRtaW4ifQ==` → nhấn `Enter`.
   - **Nói khi demo:** “JSON gốc role=user được đổi thành role=admin rồi encode lại; không cần secret vì Base64 không có integrity.”
   - **F12 show:** Vẫn ở Application, nhìn lại đúng row `lab06_profile_b64` để xác nhận value đã lưu. Không dùng Console để tạo cookie; không sửa username cookie.
   - **Quan sát:** Giá trị admin là source-derived; nếu UI không hiển thị chuỗi đó, không nói rằng đã copy từ UI.
5. **Thao tác:** Nhấn `Ctrl+R` rồi bấm `Mở trang admin`/card admin.
   - **Nói khi demo:** “Tôi reload để request mới gửi cookie Base64 đã sửa.”
   - **F12 show:** Bấm `Network` → Filter `/vulnerable/base64/admin` → chọn request mới nhất sau reload → `Headers` → `General` xác nhận `GET`, URL và status → `Request Headers` chỉ tên cookie/status, che full value → `Response` nhấn `Ctrl+F` tìm `allow` hoặc `deny` nếu body có.
   - **Quan sát:** Ghi decision live và đối chiếu với tab `Trace Panel → Base64`/`Authorization`.
**Kết luận:** Base64 có thể decode và sửa công khai; nó không cung cấp confidentiality hoặc integrity.

### Bước 3 — Signed cookie từ chối tamper

1. **Thao tác:** Quay menu `Đăng nhập demo`, chọn `Signed Cookie Demo`, đăng nhập `student` / `Student123!` rồi bấm `Mở profile`.
   - **Nói khi demo:** “Signed cookie vẫn có payload ở client nhưng server sẽ kiểm tra chữ ký trước khi dùng.”
   - **F12 show:** Network → `Clear` → Filter `/secure/signed/profile`. Chọn request profile mới nhất → `Headers` → `General` kiểm tra GET/status; không đọc full cookie value.
   - **Quan sát:** Profile signed tải được với cookie nguyên vẹn; ghi status baseline.
2. **Thao tác:** Mở `Application` → `Storage` → `Cookies` → đúng host `http://127.0.0.1:5006` → tìm `lab06_signed_profile`, bấm đúp Value và đổi một ký tự duy nhất, rồi nhấn `Enter`.
   - **Nói khi demo:** “Tôi tamper một ký tự để chữ ký không còn khớp; không thay toàn bộ cookie bằng chuỗi tự đoán.”
   - **F12 show:** Chọn đúng row có `Name = lab06_signed_profile`; xác nhận host đúng, chỉ sửa cột Value của row đó. Sau Enter, nhìn lại cùng row để chắc thay đổi đã lưu; không sửa `lab06_session` hoặc cookie khác.
   - **Quan sát:** Cookie vẫn tồn tại nhưng nội dung đã bị đổi; đây chưa phải kết quả authorization cho đến khi reload.
3. **Thao tác:** Nhấn `Ctrl+R` hoặc bấm lại `Mở profile` để tạo request signed profile mới.
   - **Nói khi demo:** “Server bây giờ phải reject trước khi dùng payload signed đã bị sửa.”
   - **F12 show:** Network → chọn request mới nhất có URL `/secure/signed/profile` → `Headers` → `General` kiểm tra status → `Response` → `Ctrl+F` tìm chính xác `invalid signature`; nếu không có, tìm `signature_rejected`. Nếu nhiều occurrence, chọn message/object kết quả profile, không chọn chữ trong hướng dẫn.
   - **Quan sát:** Ghi status/body thực tế; không gọi là signature invalid chỉ vì profile UI cũ còn đang nhìn thấy.
4. **Thao tác:** Cuộn `Trace Panel` và bấm tab `Signature`.
   - **Nói khi demo:** “Trace cho thấy chữ ký bị từ chối trước khi payload được dùng cho quyền.”
   - **F12 show:** Request signed profile → `Response` → tìm `trace_id` hoặc `signature`, chọn occurrence trong response mới nhất rồi đối chiếu với tab Signature. Không dùng Elements để xác nhận cryptographic signature.
   - **Quan sát:** Chỉ vào trạng thái invalid/rejected thật sự và trường payload_used nếu inspector có hiển thị.
**Kết luận:** Signed cookie phát hiện tamper, nhưng authorization vẫn phải dựa trên policy/server state.

### Bước 4 — Signed admin và role trong database

1. **Thao tác:** Với session student signed hiện tại, bấm `Kiểm tra admin`.
   - **Nói khi demo:** “Tôi kiểm tra quyền student trước, không sửa signed cookie để nâng role.”
   - **F12 show:** Network → bấm `Clear` → Filter `/secure/signed/admin` → chọn request mới nhất → `Headers` → `General` xác nhận URL có `/secure/signed/admin`, method GET và status → `Response` tìm `decision` hoặc `authorization` nếu body có.
   - **Quan sát:** Ghi status/decision student theo runtime.
2. **Thao tác:** Quay menu `Đăng nhập demo`, nhập `admin_lab` / `AdminLab123!`, chọn lại `Signed Cookie Demo`, bấm `Đăng nhập và tạo flow` rồi `Kiểm tra admin`.
   - **Nói khi demo:** “Tôi đổi session hợp lệ sang admin để so sánh database role, không sửa claim bằng tay.”
   - **F12 show:** Giữ `Preserve log`; chọn request mới nhất cùng route `/secure/signed/admin` sau login admin → `Headers` → `General` kiểm tra status → `Response` đọc decision. Dùng thời điểm request và `Request URL` để không nhầm request student cũ.
   - **Quan sát:** Ghi riêng status/decision của admin; không gộp hai request cùng URL.
3. **Thao tác:** Mở `Trace Panel` → bấm `Authorization` và `Database` để so sánh hai lần kiểm tra.
   - **Nói khi demo:** “Signed cookie bảo vệ integrity của claim, nhưng server vẫn phải kiểm tra role database/policy.”
   - **F12 show:** Chọn từng request → `Response` → `Ctrl+F` tìm `trace_id` hoặc `role`; nếu nhiều occurrence, chọn object authorization của request tương ứng rồi đối chiếu trace. Không suy ra quyền chỉ từ payload signed.
   - **Quan sát:** Chỉ ra role/policy quyết định allow/deny thật sự của student và admin.
**Kết luận:** Chữ ký chống sửa payload, nhưng nguồn authorization cuối cùng vẫn phải là server policy/database.

### Bước 5 — Encrypted cookie: bảo mật nội dung không đồng nghĩa nguồn quyền

1. **Thao tác:** Nhấn `Ctrl+L`, nhập chính xác `http://127.0.0.1:5006/secure/encrypted-demo` và nhấn `Enter`. Không bấm link stale `/secure/encrypted/demo` nếu giao diện còn hiển thị.
   - **Nói khi demo:** “Tôi vào đúng route encrypted-demo; route cũ có thể chỉ là link stale và không được dùng làm bằng chứng.”
   - **F12 show:** F12 → `Network` → bấm `Clear` → ô `Filter` nhập `/secure/encrypted-demo`. Chỉ chọn request mới nhất có URL chính xác route này.
   - **Quan sát:** Đúng trang encrypted demo tải được; nếu Network chỉ có route stale, quay lại nhập URL chính xác.
2. **Thao tác:** Trong Network, bấm request encrypted-demo mới nhất → `Headers` → `General`; kéo xuống `Response Headers`.
   - **Nói khi demo:** “Tôi kiểm tra header server trả về để biết decrypt/authorization status thật.”
   - **F12 show:** Ở `General` chỉ vào `Request URL` và status. Trong `Response Headers` dùng cuộn hoặc `Ctrl+F` trong pane để tìm lần lượt `X-Lab-Encryption-Status`, `X-Lab-Authorization-Used` và `X-Lab-Trace-ID`. Nếu header nào không có, nói đúng “không thấy header live”, không tự điền giá trị.
   - **Quan sát:** Ghi đúng status/header đang hiển thị; không copy token Fernet đầy đủ ra ngoài.
3. **Thao tác:** Quay trang, cuộn `Trace Panel` và bấm `Encryption`; mở các dòng `valid`/`tampered` nếu có.
   - **Nói khi demo:** “Trace tách decrypt thành công, decrypt bị từ chối và việc authorization có dùng payload hay không.”
   - **F12 show:** Quay lại request encrypted-demo → `Response` nếu cần xem body read-only → nhấn `Ctrl+F` tìm `trace_id` hoặc `authorization_used`; chọn occurrence trong response của route chính xác, rồi đối chiếu tab Encryption.
   - **Quan sát:** Chỉ trình bày valid/tampered và authorization_used đúng như trace/header; encryption không tự chứng minh role là authoritative.
**Kết luận:** Encryption bảo vệ nội dung token, nhưng quyền vẫn phải được quyết định bằng server-side authorization.

### Bước 6 — Server-side session và rotation/logout

1. **Thao tác:** Trong Application → Cookies → đúng host `http://127.0.0.1:5006`, xóa cookie demo cũ nếu còn rồi quay menu `Đăng nhập demo`.
   - **Nói khi demo:** “Tôi dọn cookie cũ để session student bắt đầu từ trạng thái xác định.”
   - **F12 show:** Application → Storage → Cookies → đúng host → xóa đúng các row demo cần dọn; không dùng Console và không xóa host khác. Sau đó Network → `Clear` → Filter `/login`.
   - **Quan sát:** Cookie mode cũ đã biến mất; nếu không thấy row sau login, reload đúng host rồi mở lại Application.
2. **Thao tác:** Nhập `student` / `Student123!`, chọn `Server-side Session` và bấm `Đăng nhập và tạo flow`.
   - **Nói khi demo:** “Cookie bây giờ chỉ mang opaque session ID; identity và role nằm ở server.”
   - **F12 show:** Chọn request login mới nhất → `Headers` → `General` kiểm tra POST/status → `Payload` → `Form Data` chỉ username/mode, che password. Sau khi login, Application → Cookies → đúng host → tìm `Name=lab06_session`, chỉ Name/Path/flags hoặc fingerprint đã che, không đọc raw Value.
   - **Quan sát:** Xác nhận cookie session tồn tại và không có role/user ID rõ trong value hiển thị.
3. **Thao tác:** Bấm `Mở profile` rồi bấm `Kiểm tra admin` trong session student.
   - **Nói khi demo:** “Tôi kiểm tra hai route: profile phải đọc được, còn admin phải dùng role server và từ chối student.”
   - **F12 show:** Network → Filter `/secure/session/profile` → chọn GET mới nhất → `Headers` → `General` kiểm tra status → đổi Filter thành `/secure/session/admin` → chọn request mới nhất → `Headers` → `General` kiểm tra status → `Response` nếu cần tìm `decision`. Dùng URL đầy đủ để không nhầm hai route.
   - **Quan sát:** Ghi riêng profile và admin status của student; không kết luận role từ cookie.
4. **Thao tác:** Quay menu `Đăng nhập demo`, nhập `admin_lab` / `AdminLab123!`, giữ `Server-side Session`, bấm `Đăng nhập và tạo flow` rồi bấm `Kiểm tra admin`.
   - **Nói khi demo:** “Tôi tạo session admin mới và kiểm tra cùng route để đối chiếu database role.”
   - **F12 show:** Network → Filter `/secure/session/admin` → chọn request mới nhất sau login admin → `Headers` → `General` kiểm tra URL/status → `Response` đọc decision nếu có. Nếu có nhiều request, chọn theo timestamp sau login admin, không chọn request student.
   - **Quan sát:** Ghi status/decision admin riêng với student; Application chỉ hiển thị opaque session cookie.
5. **Thao tác:** Trên đúng origin, mở tab `Console` trong DevTools và chạy chính xác `fetch("/secure/session/logout",{method:"POST",credentials:"same-origin"}).then(r=>r.status)` rồi nhấn `Enter`.
   - **Nói khi demo:** “Flow không có nút logout riêng, nên tôi gọi đúng POST logout trên cùng origin; lệnh chỉ trả status và không đọc cookie.”
   - **F12 show:** Bấm tab `Console` ở hàng tab DevTools, click vùng nhập lệnh, gõ hoặc dán chính xác lệnh trên rồi nhấn `Enter`. Nếu Chrome hiện cảnh báo không cho dán, tự gõ `allow pasting` theo hướng dẫn của Chrome rồi gõ lại lệnh logout; không chạy lệnh khác và không dùng `document.cookie`.
   - **Quan sát:** Console trả status thật của POST logout; nếu có lỗi, ghi lỗi thay vì coi logout đã thành công.
6. **Thao tác:** Quay `Network`, kiểm tra logout rồi reload profile/admin sau logout.
   - **Nói khi demo:** “Tôi xác nhận cả cookie expiry và việc session cũ không còn được dùng sau logout.”
   - **F12 show:** Network → Filter `/secure/session/logout` → chọn request mới nhất → `Headers` → `General` xác nhận `POST`/status → kéo đến `Response Headers` → tìm `Set-Cookie` và chỉ expiry/status. Sau đó Filter `/secure/session/admin`, chọn request sau logout → `Headers` → `General` ghi status. Application → Cookies chỉ xem hàng `lab06_session` đã hết hạn/xóa hoặc fingerprint che.
   - **Quan sát:** Đối chiếu status admin sau logout và trace `Session`/`Authorization`; session cũ phải bị revoke/expire theo runtime.
**Kết luận:** Server-side session đưa identity/authorization về trusted server state và hỗ trợ rotate, revoke, expiry và logout invalidation.

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
