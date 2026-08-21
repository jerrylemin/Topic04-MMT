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

- Mở F12 riêng ở tab Victim và tab Attacker: nhấn `F12`/`Ctrl+Shift+I` → bấm `Network` → bật `Preserve log` và `Disable cache` → bấm thùng rác `Clear`. Luôn kiểm tra đúng tab browser trước khi đọc request.
- Trong ô `Filter` gõ `change-email` hoặc `/profile`; bấm dòng vừa phát sinh sau click gửi. Trong pane phải bấm `Headers` → mở `General` để kiểm tra `Request Method`, URL và status; mở `Request Headers` rồi cuộn tới `Origin`, `Referer`, `Cookie` nếu các header đó có mặt; POST mới bấm `Payload` → `Form Data`; bấm `Response` để chỉ status/body.
- Để xem cookie, ở tab Victim bấm `Application` → bên trái mở `Storage` → `Cookies` → bấm đúng `http://127.0.0.1:5004` (không chọn `localhost` hoặc port khác) → click row `lab04_session`. Chỉ vào Name/Path/HttpOnly/SameSite/Secure và che Value.
- Trace/audit của Lab04 là panel ứng dụng trên trang, không phải F12: sau request cuộn xuống và bấm `Request`, `Cookie`, `CSRF`, `Origin`, `State`, `Audit` hoặc `Verdict`.


## Kịch bản trình bày

*Quy ước: mỗi bước đọc theo thứ tự **Thao tác → Nói khi demo → F12 show → Quan sát**. Cookie/token chỉ hiển thị tên, thuộc tính và trạng thái; không đọc nguyên giá trị trên màn hình.*

### Bước 1 — Login victim và xác lập cookie trước khi thử CSRF

1. **Thao tác:** Mở tab Victim tại `http://127.0.0.1:5004`.
   - **Nói khi demo:** “Tôi bắt đầu ở origin Victim để xác lập session trước khi mở origin Attacker.”
   - **F12 show:** Nhấn `F12` → bấm `Network` → `Clear`; tích `Preserve log` và `Disable cache`. Ở ô `Filter` nhập `/login`.
   - **Quan sát:** Đúng trang Lab04 Victim xuất hiện; Network chỉ chờ request login mới.
2. **Thao tác:** Nhập username `victim`, password `Victim123!` rồi bấm nút đăng nhập.
   - **Nói khi demo:** “Tôi đăng nhập tài khoản victim và không thay đổi origin.”
   - **F12 show:** Chọn dòng mới nhất có tên `login` → `Headers` → mở `General` → chỉ vào `Request Method: POST` và status. Bấm `Payload` → `Form Data`; chỉ vào username nếu cần, không trình bày password.
   - **Quan sát:** Ghi status/redirect thật. Nếu login thất bại, dừng để đăng nhập lại; không tiếp tục CSRF với session rỗng.
3. **Thao tác:** Bấm `Profile` hoặc mở trang profile của Victim.
   - **Nói khi demo:** “Tôi tải một trang cần session để xác nhận cookie đang được dùng.”
   - **F12 show:** Đổi Filter thành `/profile` → chọn request GET mới nhất → `Headers` → `General` kiểm tra URL/status → bấm `Response` và nhấn `Ctrl+F` tìm `victim` hoặc tiêu đề profile. Nếu nhiều kết quả, chọn đoạn nội dung profile, không chọn chữ trong menu.
   - **Quan sát:** Profile Victim hiển thị đúng trước khi gửi thay đổi email.
4. **Thao tác:** Trong DevTools, bấm tab `Application` → ở cây bên trái mở `Storage` → `Cookies` → bấm đúng host `http://127.0.0.1:5004`.
   - **Nói khi demo:** “Tôi kiểm tra thuộc tính bảo vệ của cookie, không cần đọc giá trị session.”
   - **F12 show:** Trong bảng cookie, tìm đúng hàng có cột `Name = lab04_session`. Chỉ vào các cột `Path`, `HttpOnly`, `SameSite` và `Secure`; nếu cần mở rộng bảng thì kéo ngang. Không bấm vào/không đọc cột Value.
   - **Quan sát:** Ghi tên cookie và các cờ đang hiển thị; đây là baseline trước khi so sánh vulnerable/secure.
**Kết luận:** Victim đã có session hợp lệ và ta biết thuộc tính cookie trước khi kiểm tra cross-origin request.

### Bước 2 — Vulnerable cross-origin change email

1. **Thao tác:** Giữ tab Victim không đăng xuất, mở tab mới tại `http://127.0.0.1:9004` và chọn flow vulnerable change-email.
   - **Nói khi demo:** “Tôi mở origin Attacker khác port nhưng giữ nguyên session ở tab Victim.”
   - **F12 show:** Trong tab Attacker nhấn `F12` → `Network` → `Clear`; tích `Preserve log`; ô `Filter` nhập `vulnerable/change-email`. DevTools của tab Attacker chỉ quan sát request do Attacker phát ra.
   - **Quan sát:** Attacker page hiển thị đúng flow vulnerable; không xóa cookie của tab Victim.
2. **Thao tác:** Trong form vulnerable, nhập email `demo_changed@lab.local` rồi bấm nút gửi/thay đổi email.
   - **Nói khi demo:** “Attacker cố tạo request thay đổi trạng thái mà không cung cấp CSRF token.”
   - **F12 show:** Ngay sau khi click, chọn dòng mới nhất có URL chứa `/vulnerable/change-email` → `Headers` → `General` kiểm tra method/status. Bấm `Payload` → `Form Data` và chỉ vào `email=demo_changed@lab.local`; kiểm tra không có `csrf_token`.
   - **Quan sát:** Nếu không có request, ghi rõ client không phát request; không tự gọi đó là server reject. Nếu có request, giữ lại status/URL để đối chiếu.
3. **Thao tác:** Nếu trang hiện hộp xác nhận, bấm đúng nút `Confirm`/`Xác nhận`; nếu không hiện, giữ nguyên kết quả click ở bước trước.
   - **Nói khi demo:** “Tôi xác nhận thao tác thủ công để loại bỏ nhầm lẫn giữa popup của demo và request thật.”
   - **F12 show:** Network → chọn request có timestamp mới nhất sau lần xác nhận → `Headers` → `General` → `Request URL` và status; `Request Headers` tìm `Origin`/`Referer`, chỉ vào tên header và che giá trị cookie nếu có. `Payload` vẫn phải kiểm tra email và sự vắng mặt của csrf_token.
   - **Quan sát:** Chỉ coi request sau Confirm là kết quả thử nghiệm; nếu có hai request, chọn request mới nhất và giải thích request nào là preflight hay submit.
4. **Thao tác:** Quay tab Victim, tải lại profile bằng `Ctrl+R` hoặc bấm lại `Profile`.
   - **Nói khi demo:** “Tôi kiểm tra tác động ở origin Victim, vì Attacker không cần đọc response để tạo thay đổi.”
   - **F12 show:** Mở DevTools của tab Victim → `Network` → Filter `/profile` → chọn GET mới nhất → `Headers` → `General` kiểm tra URL/status → `Response`/`Preview` nhấn `Ctrl+F` tìm `demo_changed@lab.local`. Nếu nhiều email, chọn field email trong object/profile.
   - **Quan sát:** Email Victim đổi hay không đổi theo response thực tế; không suy luận từ trang Attacker.
**Kết luận:** Vulnerable endpoint không yêu cầu token nên request cross-origin có thể gây thay đổi nếu browser gửi session phù hợp.

### Bước 3 — Secure attacker không có token

1. **Thao tác:** Ở tab Attacker, mở flow secure change-email và giữ email `demo_changed@lab.local` hoặc nhập lại email đó.
   - **Nói khi demo:** “Tôi giữ nguyên origin Attacker và payload để chỉ thay đổi endpoint vulnerable thành secure.”
   - **F12 show:** DevTools Attacker → `Network` → `Clear` → Filter `secure/change-email`. Nếu trang có hidden token nhưng Attacker form không điền, chưa submit vội; nhìn tên field, không đọc giá trị.
   - **Quan sát:** Đúng secure form xuất hiện và không có token hợp lệ do Victim cấp.
2. **Thao tác:** Bấm submit secure; nếu hiện confirm thì bấm `Confirm`.
   - **Nói khi demo:** “Request secure thiếu token phải bị chặn hoặc không được server chấp nhận.”
   - **F12 show:** Chọn request mới nhất chứa `/secure/change-email` → `Headers` → `General` xem status → `Request Headers` xem `Origin`/`Referer` nếu có → `Payload` → `Form Data` kiểm tra không có csrf_token hoặc token đang thiếu. Nếu không có request, giữ Network trống và mở `Console` để chỉ ra lỗi client-side, không bịa response.
   - **Quan sát:** Ghi status/message thực tế. Nếu có 403, chỉ vào status và response; nếu không phát request, nói đúng “client không gửi request”.
3. **Thao tác:** Quay tab Victim, reload profile và kiểm tra email vẫn ở trạng thái trước phép thử secure.
   - **Nói khi demo:** “Tôi xác nhận secure request không tạo thay đổi ngoài ý muốn.”
   - **F12 show:** Victim DevTools → `Network` → Filter `/profile` → chọn GET sau reload → `Response`/`Preview` → `Ctrl+F` tìm email hiện tại. Trong `Application` → Cookies chỉ kiểm tra hàng `lab04_session` còn tồn tại, không đọc Value.
   - **Quan sát:** Profile không đổi do request secure thiếu token; kết luận dựa vào GET profile mới.
**Kết luận:** Secure endpoint yêu cầu CSRF token; thiếu token dẫn đến reject hoặc không có request hợp lệ.

### Bước 4 — Secure attacker dùng token giả

1. **Thao tác:** Trên Attacker secure form, nhập email `fake_token_test@lab.local` và điền token giả `fake_token_for_local_lab` nếu form có ô token.
   - **Nói khi demo:** “Có một chuỗi tên giống token không có nghĩa là token được server cấp cho session này.”
   - **F12 show:** DevTools Attacker → `Network` → `Clear` → Filter `secure/change-email`. Trước khi submit, nếu cần dùng `Elements` → `Ctrl+F` tìm `csrf_token` để xác nhận đang sửa đúng ô token; không chọn hidden token trong phần mẫu.
   - **Quan sát:** Form có email và token giả, chưa có request mới.
2. **Thao tác:** Bấm submit và xác nhận popup nếu có.
   - **Nói khi demo:** “Tôi gửi token giả để kiểm tra server xác thực token với session và origin.”
   - **F12 show:** Network → chọn request mới nhất `/secure/change-email` → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` xác nhận email và `csrf_token=fake_token_for_local_lab`. Bấm `Response` → `Ctrl+F` tìm `invalid` hoặc `token`; nếu không có, đọc status 403 ở `General`.
   - **Quan sát:** Nếu nhiều chữ token, chọn occurrence trong message/JSON kết quả submit, không chọn label của input hay script mẫu.
3. **Thao tác:** Quay Victim và reload profile.
   - **Nói khi demo:** “Tôi kiểm tra token giả không tạo được thay đổi.”
   - **F12 show:** Victim → `Network` → Filter `/profile` → chọn GET mới nhất → `Response`/`Preview` → `Ctrl+F` tìm `fake_token_test@lab.local` và email hiện tại. Chỉ vào field email trong profile object.
   - **Quan sát:** Email vẫn không đổi sau request token giả; nếu có đổi, dừng và báo đó là kết quả trái với kỳ vọng của lab.
**Kết luận:** Token phải hợp lệ với session/flow; chỉ gửi một chuỗi có tên csrf_token không đủ để vượt kiểm tra.

### Bước 5 — Same-origin có token thật

1. **Thao tác:** Quay tab Victim, mở form secure change-email và nhập `victim_secure@lab.local`.
   - **Nói khi demo:** “Bây giờ tôi gửi từ đúng origin Victim với token do server cấp.”
   - **F12 show:** Victim DevTools → `Network` → `Clear` → Filter `secure/change-email`. Nếu muốn chỉ rõ token field, bấm `Elements` → `Ctrl+F` → `csrf_token`, chọn hidden input thuộc form secure Victim; không đọc giá trị token.
   - **Quan sát:** Đúng form secure và token thật của form đang tồn tại.
2. **Thao tác:** Bấm nút secure change-email và xác nhận nếu có.
   - **Nói khi demo:** “Request này cùng origin, có session và token thật nên là baseline hợp lệ của secure flow.”
   - **F12 show:** Chọn request mới nhất → `Headers` → `General` kiểm tra `POST` và status → mở `Request Headers`, tìm `Origin` và `Referer`, chỉ vào tên header → `Payload` → `Form Data` xác nhận có email và csrf_token nhưng che giá trị token.
   - **Quan sát:** Ghi status/response thật. Không trình bày nguyên token, kể cả trong screenshot.
3. **Thao tác:** Reload profile Victim để xác nhận email mới.
   - **Nói khi demo:** “Tôi dùng GET profile sau POST để chứng minh thay đổi hợp lệ đã được lưu.”
   - **F12 show:** Network → đổi Filter thành `/profile` → chọn GET mới nhất sau POST → `Headers` → `General` → `Response`/`Preview` → `Ctrl+F` tìm `victim_secure@lab.local`. Nếu nhiều occurrence, chọn field email trong object/profile.
   - **Quan sát:** Email mới xuất hiện trong response/profile; đây là kết quả same-origin có token thật.
4. **Thao tác:** Mở `Trace Panel` và lần lượt bấm tab `CSRF Token Inspector`, `CSRF` và `Origin` nếu có.
   - **Nói khi demo:** “Trace panel cho thấy server kiểm tra token và origin, còn F12 cho thấy request đã mang các thành phần đó.”
   - **F12 show:** Chọn lại POST secure → `Response` → `Ctrl+F` tìm `trace_id` hoặc `csrf`; chọn occurrence trong kết quả request rồi đối chiếu với các tab trace. Không chọn chữ csrf trong menu hướng dẫn.
   - **Quan sát:** Chỉ vào trạng thái token/origin được trace thật sự báo.
**Kết luận:** Cùng endpoint secure hoạt động khi request đi từ origin hợp lệ và mang token do server cấp.

### Bước 6 — So sánh SameSite và giới hạn bảo vệ

1. **Thao tác:** Mở song song tab Victim và Attacker, giữ nguyên session Victim, rồi chuẩn bị hai flow vulnerable/secure change-email.
   - **Nói khi demo:** “Tôi đặt hai origin cạnh nhau để so sánh request, cookie và token theo cùng một quy trình.”
   - **F12 show:** Ở từng tab bấm `Network` → `Clear` → Filter `change-email`. Trên Victim mở thêm `Application` → `Storage` → `Cookies` → `http://127.0.0.1:5004`; trên Attacker không chọn nhầm cookie của host Victim.
   - **Quan sát:** Hai tab có origin khác nhau; chỉ Victim mới là nơi xem cookie session của Lab04.
2. **Thao tác:** Thực hiện một lần vulnerable từ Attacker và một lần secure từ Attacker bằng payload khác nhau để nhận diện request.
   - **Nói khi demo:** “Tôi tạo hai request có thể phân biệt bằng endpoint và payload, không so sánh hai dòng chỉ dựa vào vị trí.”
   - **F12 show:** Mỗi tab Network → chọn row có Request URL tương ứng → `Headers` → `General` kiểm tra method/status → `Request Headers` tìm `Origin`, `Referer` và `Cookie` nếu browser hiển thị; chỉ đọc tên header, che giá trị. `Payload` kiểm tra email và sự có/không có csrf_token.
   - **Quan sát:** Có thể browser không gửi Cookie hoặc không cho response cross-origin đọc được; đó là kết quả cần ghi, không được tự khẳng định cookie đã gửi.
3. **Thao tác:** Trên Application → Cookies, chọn hàng `lab04_session` và đọc các cột bảo vệ; không sửa cookie.
   - **Nói khi demo:** “Cookie flags là một lớp kiểm soát, nhưng chúng không thay thế CSRF token và kiểm tra origin.”
   - **F12 show:** Application → Storage → Cookies → đúng host → hàng `lab04_session`; chỉ vào `Path`, `HttpOnly`, `SameSite`, `Secure`. Nếu không thấy cột do cửa sổ hẹp, kéo ngang bảng hoặc phóng to DevTools; không cần mở Value.
   - **Quan sát:** Ghi đúng giá trị cờ đang hiển thị và giới hạn của chúng trong flow này.
4. **Thao tác:** Mở `Trace Panel → State` và `Audit` để chốt kết quả của các request.
   - **Nói khi demo:** “Tôi dùng trace để tách rõ cookie/session, CSRF token và authorization thay vì gộp tất cả thành một nguyên nhân.”
   - **F12 show:** Chọn từng POST trong Network → `Response` → `Ctrl+F` tìm `trace_id` hoặc `status`; với nhiều occurrence, chọn object kết quả submit. Đối chiếu đúng trace ID với State/Audit.
   - **Quan sát:** Chỉ kết luận về tác động khi profile GET hoặc audit record xác nhận.
**Kết luận:** Cookie flags, same-origin và CSRF token là các lớp khác nhau; secure flow cần chứng minh đúng lớp đã chặn hoặc cho phép request.

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
