# Demo script Lab04 — CSRF

## Mục tiêu demo

- Chứng minh request đổi email vulnerable không có CSRF token/origin check.
- So sánh cùng hành động qua attacker page và secure route.
- Quan sát cookie, Origin/Referer, token, before/after và status response.
- Phân biệt CSRF với XSS và giới hạn “không đọc được response” của cross-origin attacker.

## Chuẩn bị

- Thư mục làm việc: `cd Lab04`
- Khởi động: `scripts\run_lab.bat` (chạy Victim `:5004` và Demo Page `:9004`)
- Victim URL: `http://127.0.0.1:5004`; attacker same-site: `http://127.0.0.1:9004`; control cross-site: `http://localhost:9004`
- Reset khi cần: `python seed.py` tại `Lab04`
- Tài khoản: `victim / Victim123!`, `receiver / Receiver123!`; email ban đầu `victim_old@lab.local`
- Cần click và xác nhận trên attacker page vì implementation hiện tại không auto-submit.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`, mở `Network`, bật `Preserve log`/`Disable cache` và lọc `change-email`; trước mỗi flow bấm `Clear`.
- `Network → Headers`: show Request URL/method, `Origin`, `Referer`, `Cookie` và status; `Payload/Form Data` chỉ ra `email` và sự có mặt/vắng mặt của `csrf_token`, không đọc full session/token ra trước lớp.
- `Application → Storage → Cookies → http://127.0.0.1:5004`: show tên `lab04_session` và flags `HttpOnly/SameSite/Path`; không copy hoặc phát tán giá trị cookie.
- Sau request, show `Response/Preview` và quay lại `/profile` để chứng minh before/after; trace/audit của Lab04 là panel ứng dụng, không phải tab F12.

## Kịch bản trình bày

*Quy ước bằng chứng: cookie/header/status/email dưới đây phải được xác nhận trong browser live; “same-site” của `127.0.0.1:9004` và `127.0.0.1:5004` không được đồng nhất với “same-origin”.*

**Bước 1 — Đăng nhập victim và ghi before state**

* Thao tác:
  1. Mở `http://127.0.0.1:5004/login`. Bấm ô `Username`, nhập `victim`; bấm ô `Password`, nhập `Victim123!`; bấm `Đăng nhập`.
  2. Ở dashboard, nhìn card email để ghi lại giá trị ban đầu; bấm `Mở form` trong card `Đổi email vulnerable` hoặc nhấn `Ctrl+L` mở `http://127.0.0.1:5004/profile`.
  3. Giữ tab Victim này mở. Nhấn `F12`, chọn `Application → Storage → Cookies → http://127.0.0.1:5004`, tìm cookie `lab04_session` và chỉ vào flags; không copy giá trị cookie ra màn hình.
* Nói: “Victim đã có session cookie. Attacker không cần biết mật khẩu nếu browser tự gửi cookie phù hợp với request.”
* Quan sát: profile hiển thị email ban đầu; cookie có tên `lab04_session`, `HttpOnly`, `SameSite=Lax` theo cấu hình local; ghi flags thực tế của browser.
* F12 show: `Network → POST /login` và `GET /profile` chỉ ra status; `Application → Cookies` show tên/flags của `lab04_session`, che value khi trình bày.
* Kết luận: cookie là credential tự động đi theo policy trình duyệt, không phải bằng chứng attacker biết password.

**Bước 2 — Vulnerable cross-origin email change**

* Thao tác:
  1. Mở tab mới tới `http://127.0.0.1:9004`. Trên trang attacker, bấm trực tiếp vào card `Đổi email vulnerable` để mở attack page.
  2. Trên attack page bấm nút `Gửi form`; khi browser hiện hộp xác nhận, bấm `OK`.
  3. Chuyển ngay sang F12 của tab attacker, chọn `Network`, bấm request POST tới Victim; mở `Headers` và `Payload`.
  4. Quay lại tab Victim, nhấn `Ctrl+L` mở `http://127.0.0.1:5004/profile`, nhấn `Enter`, rồi chỉ vào email before/after.
* Nói: “Demo page khác origin nhưng cùng site theo hostname này. Form hiện tại yêu cầu người trình bày click và xác nhận; source vulnerable không gọi `_secure_checks`.”
* Quan sát: kết quả kỳ vọng theo source là POST tới `http://127.0.0.1:5004/vulnerable/change-email` với email `demo_changed@lab.local`; nếu browser gửi session cookie, email before/after đổi và server ghi trace/audit. Chỉ gọi cookie đã được gửi khi Network live hiển thị nó.
* F12 show: chọn request `POST /vulnerable/change-email`; `Headers` show Origin/Referer/Cookie, `Payload` show email, `Response` show status; nếu Cookie không có thì chỉ ghi nhận browser policy chưa cho flow thành công.
* Kết luận: thiếu CSRF token và origin validation cho phép cross-origin form kích hoạt mutation khi cookie được browser đính kèm.

**Bước 3 — Secure attacker page thiếu token bị từ chối**

* Thao tác:
  1. Quay về trang attacker `http://127.0.0.1:9004`, bấm card `Secure thiếu token`.
  2. Bấm `Gửi form`, rồi bấm `OK` trong hộp xác nhận.
  3. Trong Network chọn POST tới `/secure/change-email`, mở `Response` để chỉ status/lý do thiếu token.
  4. Chuyển sang tab Victim, nhấn `Ctrl+R` hoặc mở lại `/profile` và xác nhận email không đổi.
* Nói: “Payload nghiệp vụ vẫn là đổi email, nhưng request không có token hợp lệ. Secure kiểm tra trước khi update database.”
* Quan sát: kỳ vọng status `403`, trace reason missing CSRF token và email không đổi; xác nhận status/body live, không suy ra từ màu giao diện.
* F12 show: chọn `POST /secure/change-email`; `Payload` show không có hoặc không có token hợp lệ, `Headers` show Origin/Referer, `Response` show `403`; reload `/profile` để show email không đổi.
* Kết luận: token server-side là điều kiện bắt buộc trước state change.

**Bước 4 — Secure attacker page có token giả vẫn bị từ chối**

* Thao tác:
  1. Ở trang attacker, quay về home nếu cần, bấm card `Secure token giả`.
  2. Bấm `Gửi form`, rồi bấm `OK` trong confirm.
  3. Mở F12 → `Network`, chọn POST tới `/secure/change-email`, bấm `Payload` để chỉ field token giả và bấm `Response` để chỉ 403/invalid token.
  4. Quay lại Victim và tải lại profile để chứng minh database không bị mutation.
* Nói: “Biết tên field chưa đủ; token phải gắn với session victim và còn hợp lệ. Tôi dùng đúng payload cố định `fake_token_for_local_lab` để chứng minh token giả không được chấp nhận.”
* Quan sát: kỳ vọng status `403`, response ghi bad/invalid token và email vẫn giữ before state; xem trace/audit để phân biệt reject trước mutation.
* F12 show: `Payload/Form Data` show field `csrf_token` với giá trị giả (không đọc token thật), `Response` show `403`/reason; `Network` không có request update thứ hai.
* Kết luận: CSRF defense không chỉ kiểm tra token có tồn tại mà phải xác minh giá trị server-issued.

**Bước 5 — Secure same-origin submission với token thật**

* Thao tác:
  1. Trong tab Victim, quay về dashboard bằng `Ctrl+L` mở `http://127.0.0.1:5004/dashboard` nếu chưa thấy dashboard.
  2. Trong card `Đổi email secure`, bấm `Mở form`.
  3. Bấm ô `Email mới`, nhấn `Ctrl+A`, nhập `victim_secure@lab.local`, rồi bấm `Đổi email an toàn`.
  4. Mở F12 → `Network`, chọn POST secure vừa gửi, mở `Headers` để chỉ Origin/Referer và mở `Payload` chỉ để xác nhận có field token; không đọc nguyên token ra khi trình bày.
* Nói: “Đây là request same-origin có token thật. Secure yêu cầu exact allowed Origin/Referer, update trong transaction rồi rotate token.”
* Quan sát: kỳ vọng response thành công, before `victim_old@lab.local` hoặc state hiện tại → `victim_secure@lab.local`; trace cho thấy token valid, Origin/Referer hợp lệ và token mới sau mutation.
* F12 show: `Network → POST /secure/change-email → Headers` show exact Origin/Referer; `Payload` show email và sự có mặt của `csrf_token` (che giá trị); `Response` show success, rồi `GET /profile` show email after.
* Kết luận: primary fix là token gắn session kết hợp kiểm tra Origin/Referer trước thao tác đổi trạng thái.

**Bước 6 — Chốt SameSite và giới hạn của CSRF**

* Thao tác:
  1. Trong F12 của từng tab, bấm `Network`; nếu log cũ không còn, bật `Preserve log` rồi bấm biểu tượng xóa log.
  2. Lần lượt bấm request của Bước 2, 3, 4 và 5; trong mỗi request mở `Headers`, cuộn tới `Request Headers`, chỉ vào `Origin`, `Referer`, `Cookie` và status.
  3. Với Bước 2–4 bấm thêm `Response` để đối chiếu reject/allow; với Bước 5 bấm `Payload` để chỉ token tồn tại, không dùng Console đọc response cross-origin.
* Nói: “SameSite là lớp giảm rủi ro theo browser policy; Origin/Referer và CSRF token là kiểm tra server. CSRF không tự cho attacker đọc response cross-origin.”
* Quan sát: ghi header/status thực tế của từng request; current attacker page chỉ có manual click/confirm, không auto-submit.
* F12 show: đặt hai request vulnerable/secure cạnh nhau trong Network, so sánh Cookie/token/Origin/Referer/status; Application Cookies show flags, còn trace/audit show mutation decision.
* Kết luận: phải tách fact live của browser khỏi expected cookie policy; authorization/mutation vẫn phải được bảo vệ ở server.

## Demo Vulnerable → Secure

| Cùng hành động | Vulnerable → nguyên nhân | Secure → primary fix |
|---|---|---|
| POST đổi email thành `demo_changed@lab.local` từ `http://127.0.0.1:9004` | `/vulnerable/change-email` dùng session nhưng không `_secure_checks` | `/secure/change-email` yêu cầu CSRF token + exact Origin/Referer |
| POST thiếu token | Có thể mutate nếu cookie được browser gửi | `/attack/secure-email` kỳ vọng 403, không đổi email |
| Token `fake_token_for_local_lab` | Không có kiểm tra token ở route vulnerable | `/attack/bad-token` kỳ vọng 403 trước mutation |
| Form Victim có token thật | Không áp dụng | Same-origin valid submit, update + rotate token |

## Câu hỏi trong BaiTapTopic04.docx

**Câu 27. Vì sao trình duyệt tự động gửi cookie?**  
**Trả lời khi demo:** Browser tự gắn cookie phù hợp domain, path và SameSite policy vào request, vì cookie là cơ chế duy trì session. Việc có thực sự gửi hay không phải xem header Network live, không suy ra chỉ từ HTML form.

**Câu 28. Vì sao CSRF vẫn xảy ra dù attacker không biết mật khẩu victim?**  
**Trả lời khi demo:** Attacker lợi dụng session đã đăng nhập trong browser của victim; browser có thể tự gửi cookie cùng request forged. CSRF nhắm vào hành động được server xác thực bằng cookie, không cần đọc password.

**Câu 29. CSRF có đọc được response của victim không?**  
**Trả lời khi demo:** Thông thường cross-origin policy chặn attacker đọc response, nhưng request state-changing vẫn có thể được gửi. CSRF vì vậy vẫn nguy hiểm cho mutation dù không đọc được dữ liệu trả về.

**Câu 30. CSRF khác XSS như thế nào?**  
**Trả lời khi demo:** CSRF gửi hành động từ origin khác bằng credential tự động của victim; XSS chạy script trong origin/trang đáng tin vì input lọt vào HTML/DOM sink. Lab04 sửa token/origin, còn Lab01 sửa output sink.

**Câu 31. Vì sao request thay đổi trạng thái không nên dùng GET?**  
**Trả lời khi demo:** GET dễ bị preload, link, crawler hoặc hình ảnh kích hoạt ngoài ý muốn và không thể hiện rõ mutation. Đổi email nên dùng POST/động từ mutation kèm CSRF và Origin/Referer checks.

## Nếu demo lỗi

- Nếu hai port không lên, dừng tiến trình cũ và chạy lại `scripts\run_lab.bat`; kiểm tra lần lượt `:5004` và `:9004`.
- Nếu email đã đổi từ lần trước, chạy `python seed.py` trong `Lab04`, đăng nhập lại victim và ghi before state mới.
- Nếu attacker page không gửi request, bấm nút rồi xác nhận `OK`; implementation hiện tại cố ý không auto-submit.
- Nếu Cookie header không xuất hiện, giữ Network evidence và nói rõ browser policy chưa cho thấy flow; không tuyên bố CSRF thành công.

## Chốt lab

Root cause: state-changing route tin session cookie nhưng thiếu token/origin validation.
Primary fix: POST + CSRF token gắn session + kiểm tra Origin/Referer trước mutation.
Defense in depth: SameSite, secure cookie flags, re-authentication và audit before/after.
