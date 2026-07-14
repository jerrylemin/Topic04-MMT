# HƯỚNG DẪN CHỤP ẢNH THỦ CÔNG - LAB 6 COOKIE POISONING

**Sinh viên:** Lê Minh - **MSSV:** 21127645  
**Base URL duy nhất:** `http://127.0.0.1:5006`  
**Thư mục ảnh:** `evidence/screenshots/`

## Quy tắc an toàn và tính trung thực

- Người học tự mở browser, DevTools và tự chụp từng ảnh. Không dùng Playwright, Selenium, extension, macro, script tự điều khiển DevTools, tự động chụp hoặc ảnh giả.
- Chỉ thao tác cookie thuộc `127.0.0.1:5006` và chỉ các tên cố định của Lab06. Không mở website thật, không đọc/copy toàn bộ cookie trình duyệt, không nhập domain/host/URL/port/cookie name tùy ý.
- Không dùng Console và không chạy `document.cookie`. Không gửi cookie bằng JavaScript.
- Không chụp secret key, password hash, plaintext password ngoài ô login demo, full Session ID, full signed token hoặc full encrypted token. Nếu panel chưa mask, dừng và sửa ứng dụng trước khi chụp.
- 48 ảnh là evidence do sinh viên bổ sung. **Ảnh thủ công không phải completion gate của Codex** và thiếu ảnh không được dùng để tạo ảnh placeholder hay tuyên bố ảnh đã có.
- Chỉ chụp ảnh test/coverage/report sau khi lệnh thật đã chạy và màn hình hiển thị kết quả thật.

## Chuẩn bị chung

1. Chạy app trực tiếp trên host tại `http://127.0.0.1:5006`; xác minh address bar đúng `127.0.0.1:5006`.
2. Dùng một profile/browser riêng cho lab nếu có thể. Đóng các tab website thật trước khi mở DevTools.
3. Đặt zoom browser 100%, cửa sổ đủ rộng để thấy trang và panel. Không chỉnh HTML bằng DevTools.
4. Trong Chromium/Edge: `F12` > **Application** > **Storage** > **Cookies** > `http://127.0.0.1:5006`. Trong Firefox: `F12` > **Storage** > **Cookies**.
5. Khi cần Network evidence: mở **Network**, bật Preserve log nếu phải reload, chọn request Lab06 rồi xem Headers/Response. Không dùng “Copy all as HAR”.
6. Trước mỗi nhóm flow, dùng nút Reset Lab hoặc `POST /reset-lab`, xóa riêng cookie Lab06 nếu hướng dẫn yêu cầu, rồi đăng nhập lại. Không xóa cookie của site khác.
7. Lưu đúng tên PNG bên dưới. Không đổi thứ tự, không crop làm mất address bar/panel cần chứng minh.

## Tài khoản demo

- Student: `student` / `Student123!`.
- Admin: `admin_lab` / `AdminLab123!`.

## Danh sách 48 ảnh

### 01. `01_home_overview.png`

- **Mục đích / URL / Mode / Tài khoản:** tổng quan lab; `/`; common; chưa đăng nhập.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** app vừa chạy, Lab06 đã reset; không yêu cầu cookie; N/A.
- **Thao tác DevTools thủ công:** không sửa gì; giữ address bar trong ảnh để chứng minh host local.
- **Panel / Timeline step / Nội dung bắt buộc:** trang Overview; chưa có step; tiêu đề Lab 6, năm mô hình, cảnh báo local-only và link tới login/comparison.
- **Kết quả mong đợi / Caption:** HTTP 200 và trang tổng quan hiển thị; “Tổng quan năm mô hình Cookie Poisoning trong Lab06 local”.
- **Lỗi thường gặp / Reset:** sai port hoặc app chưa chạy; khởi động lại app tại `127.0.0.1:5006` rồi reload.

### 02. `02_login_accounts.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh bốn lựa chọn login và hai tài khoản demo; `/login`; common; chưa đăng nhập.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** reset xong; không yêu cầu cookie; N/A.
- **Thao tác DevTools thủ công:** không nhập secret/cookie name; chỉ mở trang.
- **Panel / Timeline step / Nội dung bắt buộc:** Login; chưa có step; Plain, Base64, Signed, Server-side Session và thông tin student/admin.
- **Kết quả mong đợi / Caption:** form chỉ có mode cố định; “Trang đăng nhập với tài khoản và mode demo cố định”.
- **Lỗi thường gặp / Reset:** session cũ làm redirect; logout hoặc reset rồi mở lại `/login`.

### 03. `03_plain_student_login.png`

- **Mục đích / URL / Mode / Tài khoản:** login Plain bằng student; `/login` rồi trang kết quả/dashboard; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** reset; chưa có plain cookie; N/A.
- **Thao tác DevTools thủ công:** chọn Plain Cookie Demo, nhập tài khoản demo và submit; không sửa cookie.
- **Panel / Timeline step / Nội dung bắt buộc:** login result/Timeline; bước xác minh password và tạo cookie; username student, mode Plain, không lộ password.
- **Kết quả mong đợi / Caption:** login thành công và server tạo cookie user; “Student đăng nhập ở Plain Cookie Demo”.
- **Lỗi thường gặp / Reset:** chọn nhầm mode hoặc mật khẩu; reset và đăng nhập lại đúng mode.

### 04. `04_plain_cookie_devtools.png`

- **Mục đích / URL / Mode / Tài khoản:** thấy hai plain cookie trong browser storage; `/vulnerable/plain/profile`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** đã hoàn tất ảnh 03; `lab06_username=student`, `lab06_role=user`.
- **Thao tác DevTools thủ công:** mở Application/Storage > Cookies > đúng local origin; chưa sửa giá trị.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools Cookies và profile; bước browser lưu cookie; đúng Name/Value, không thấy cookie site khác.
- **Kết quả mong đợi / Caption:** cả hai cookie hiện diện; “Plain Cookie lưu username và role phía client”.
- **Lỗi thường gặp / Reset:** chọn nhầm origin hoặc cookie cũ; xóa riêng cookie Lab06, reset, login lại.

### 05. `05_plain_cookie_attributes.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi thuộc tính plain cookie; `/vulnerable/plain/profile`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** plain login hợp lệ; hai cookie gốc như ảnh 04.
- **Thao tác DevTools thủ công:** mở rộng cột Domain, Path, HttpOnly, Secure, SameSite; không sửa.
- **Panel / Timeline step / Nội dung bắt buộc:** Cookie Attribute Inspector + DevTools; bước response Set-Cookie; Path `/`, SameSite `Lax`, HttpOnly false cho demo, Secure bằng config thực.
- **Kết quả mong đợi / Caption:** UI và browser thống nhất; “Thuộc tính thật của Plain Cookie quan sát trong DevTools”.
- **Lỗi thường gặp / Reset:** cột bị ẩn; kéo rộng DevTools hoặc bật lại cột, không thay config để làm đẹp ảnh.

### 06. `06_plain_admin_denied.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh role user bị từ chối; `/vulnerable/plain/admin`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** chưa sửa cookie; `lab06_role=user`.
- **Thao tác DevTools thủ công:** điều hướng/reload route, không sửa cookie.
- **Panel / Timeline step / Nội dung bắt buộc:** denied page; bước cookie role=user dẫn tới deny; status 403 hoặc denied rõ ràng.
- **Kết quả mong đợi / Caption:** không vào admin; “Plain role=user bị vulnerable admin route từ chối”.
- **Lỗi thường gặp / Reset:** cookie đang là admin từ lần trước; reset và login student lại.

### 07. `07_plain_role_before.png`

- **Mục đích / URL / Mode / Tài khoản:** lưu trạng thái trước poisoning; `/vulnerable/plain/admin`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** ảnh 06 đã xong; `lab06_role=user`.
- **Thao tác DevTools thủ công:** mở đúng hàng `lab06_role`, đặt con trỏ nhưng chưa thay đổi.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools Cookies + denied page; bước trước sửa thủ công; Name và `user` đọc rõ.
- **Kết quả mong đợi / Caption:** baseline rõ ràng; “Giá trị role=user trước khi sửa cookie”.
- **Lỗi thường gặp / Reset:** edit đã commit nhầm; nhập lại `user`, reload để xác nhận denied.

### 08. `08_plain_role_modified_devtools.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh thao tác poisoning thủ công local; `/vulnerable/plain/admin`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** baseline ảnh 07; `lab06_role=user`.
- **Thao tác DevTools thủ công:** chỉ sửa Value của `lab06_role` thành `admin`, nhấn Enter; không sửa domain/path/cookie khác, không dùng Console.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools Cookies; bước sinh viên sửa thủ công; hàng `lab06_role=admin` và local origin.
- **Kết quả mong đợi / Caption:** browser lưu giá trị sửa; “Sửa thủ công role=user thành role=admin trong DevTools local”.
- **Lỗi thường gặp / Reset:** sửa nhầm cookie/origin; reset ngay, login lại và chỉ sửa `lab06_role`.

### 09. `09_plain_admin_allowed.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh broken access control sau poisoning; `/vulnerable/plain/admin`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** ảnh 08 đã commit; gốc user, hiện tại `lab06_role=admin`.
- **Thao tác DevTools thủ công:** reload route bằng browser; không dùng endpoint/nút tự sửa.
- **Panel / Timeline step / Nội dung bắt buộc:** vulnerable admin page; bước server không phát hiện thay đổi và cho phép; cảnh báo server tin cookie client.
- **Kết quả mong đợi / Caption:** HTTP 200/admin demo; “Cookie Poisoning thành công vì server tin role phía client”.
- **Lỗi thường gặp / Reset:** vẫn denied do edit chưa Enter; kiểm tra cookie rồi reload; sau ảnh dùng Reset Lab.

### 10. `10_plain_authorization_inspector.png`

- **Mục đích / URL / Mode / Tài khoản:** thấy nguồn role và policy lỗi; `/vulnerable/plain/admin`; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** poisoned state; `lab06_role=admin` (gốc user).
- **Thao tác DevTools thủ công:** không sửa thêm; mở Authorization Inspector trên trang.
- **Panel / Timeline step / Nội dung bắt buộc:** Authorization Inspector; bước Flask đọc request.cookies/decision; subject, action, submitted role, database lookup = không, decision allow, reason.
- **Kết quả mong đợi / Caption:** inspector chỉ ra client cookie là authorization source; “Phân quyền lỗi dựa trực tiếp trên lab06_role”.
- **Lỗi thường gặp / Reset:** inspector không đồng bộ trace; reload flow, chọn trace mới nhất; reset sau ảnh.

### 11. `11_plain_timeline.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi toàn bộ 14 bước Plain; trang flow/dashboard; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** đã chạy cả deny và allow; gốc user, poisoned admin.
- **Thao tác DevTools thủ công:** đóng DevTools nếu che Timeline; không thay cookie.
- **Panel / Timeline step / Nội dung bắt buộc:** Action Timeline; chọn bước 10-14; step number, layer, technique, input/output đã che, code reference, status, security meaning.
- **Kết quả mong đợi / Caption:** timeline nối login, edit, request và allow; “Action Timeline của Plain Cookie Poisoning”.
- **Lỗi thường gặp / Reset:** thiếu bước vì reset sớm; chạy lại ảnh 03-09 rồi chụp trước reset.

### 12. `12_plain_final_verdict.png`

- **Mục đích / URL / Mode / Tài khoản:** kết luận flow Plain; trang flow/dashboard; Plain; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** trace có deny và poisoned allow; `lab06_role=admin` sau sửa.
- **Thao tác DevTools thủ công:** không sửa; mở Final Security Verdict.
- **Panel / Timeline step / Nội dung bắt buộc:** Final Verdict; bước 14; vulnerable, root cause client-controlled role, impact privilege escalation, fix server-side authorization.
- **Kết quả mong đợi / Caption:** verdict ghi Cookie Poisoning thành công trong local lab; “Kết luận bảo mật của Plain Cookie flow”.
- **Lỗi thường gặp / Reset:** verdict hard-code/không khớp trace; không chụp cho tới khi flow thật sinh verdict; reset sau ảnh.

### 13. `13_base64_login.png`

- **Mục đích / URL / Mode / Tài khoản:** bắt đầu Base64 flow; `/login`; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** reset Plain flow; chưa có `lab06_profile_b64`.
- **Thao tác DevTools thủ công:** chọn Base64 Cookie Demo và submit student.
- **Panel / Timeline step / Nội dung bắt buộc:** login result; bước server tạo JSON và encode; mode, user, không lộ password.
- **Kết quả mong đợi / Caption:** cookie Base64 được tạo; “Student đăng nhập ở Base64 Cookie Demo”.
- **Lỗi thường gặp / Reset:** còn plain cookie không ảnh hưởng nhưng gây rối ảnh; reset/xóa riêng cookie Lab06 rồi login lại.

### 14. `14_base64_cookie_devtools.png`

- **Mục đích / URL / Mode / Tài khoản:** thấy Base64 cookie trong storage; `/vulnerable/base64/profile`; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** login Base64; `lab06_profile_b64` chứa JSON user cố định đã encode.
- **Thao tác DevTools thủ công:** mở đúng local origin, chưa sửa value.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools Cookies + profile; bước browser lưu chuỗi Base64; tên cookie và encoded value.
- **Kết quả mong đợi / Caption:** cookie hiện diện; “Payload JSON được lưu dưới dạng Base64 phía client”.
- **Lỗi thường gặp / Reset:** value bị URL-escape hoặc cột hẹp; xem giá trị theo browser thực, không chỉnh tay ngoài flow.

### 15. `15_base64_original_value.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi encoded baseline; trang Base64 profile/guide; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** chưa poisoning; JSON cố định `username=student`, `role=user`.
- **Thao tác DevTools thủ công:** không sửa; mở phần Original Base64 và hàng cookie.
- **Panel / Timeline step / Nội dung bắt buộc:** Cookie Transformation/Base64 Inspector; bước encode; full demo value chỉ ở hướng dẫn an toàn, log/trace dùng bản rút gọn.
- **Kết quả mong đợi / Caption:** UI và cookie gốc khớp; “Giá trị Base64 gốc đại diện cho role=user”.
- **Lỗi thường gặp / Reset:** serializer tạo spacing khác; dùng đúng chuỗi do app hiện, không tự đoán; reset/login lại nếu lệch.

### 16. `16_base64_decoded_json.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh decode đọc được JSON; `/vulnerable/base64/profile`; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** cookie gốc; JSON có `username: student`, `role: user`.
- **Thao tác DevTools thủ công:** không dùng decoder online; mở Base64 Inspector local.
- **Panel / Timeline step / Nội dung bắt buộc:** Base64 Inspector; bước decode/parse; algorithm URL-safe Base64, confidentiality=false, integrity=false, parse result và extracted role.
- **Kết quả mong đợi / Caption:** JSON đọc rõ; “Base64 decode cho thấy role=user, không phải dữ liệu được mã hóa”.
- **Lỗi thường gặp / Reset:** dùng dịch vụ web ngoài; dừng, reset và chỉ dùng Inspector local.

### 17. `17_base64_modified_json.png`

- **Mục đích / URL / Mode / Tài khoản:** thấy trạng thái JSON demo cố định role admin; trang Base64 guide; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** baseline role user; cookie chưa cần sửa.
- **Thao tác DevTools thủ công:** chỉ xem read-only JSON demo `role=admin`; không nhập JSON tự do.
- **Panel / Timeline step / Nội dung bắt buộc:** Base64 Transformation Inspector; bước chuẩn bị chuỗi demo; JSON gốc và modified khác đúng trường role.
- **Kết quả mong đợi / Caption:** hai trạng thái cố định rõ ràng; “JSON demo thay role=user bằng role=admin”.
- **Lỗi thường gặp / Reset:** có textarea/editor hoặc nút set cookie; không chụp, vì UI đó vi phạm yêu cầu; sửa app trước.

### 18. `18_base64_reencoded_value.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi chuỗi Base64 admin cố định; trang Base64 guide + DevTools; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** original encodes role user; modified demo encodes role admin.
- **Thao tác DevTools thủ công:** copy chuỗi admin từ read-only guide, paste vào Value của `lab06_profile_b64`, Enter; không dùng editor online/Console.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools + Transformation Inspector; bước cookie được sửa thủ công; value mới và local origin.
- **Kết quả mong đợi / Caption:** cookie chứa chuỗi demo admin; “Re-encode Base64 cố định và sửa cookie thủ công”.
- **Lỗi thường gặp / Reset:** thiếu padding/ký tự bị đổi; copy lại đúng chuỗi app cung cấp; reset nếu sai format.

### 19. `19_base64_admin_allowed.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh Base64 không ngăn poisoning; `/vulnerable/base64/admin`; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** cookie hiện decode role admin, gốc role user.
- **Thao tác DevTools thủ công:** reload route sau ảnh 18; không dùng API setter.
- **Panel / Timeline step / Nội dung bắt buộc:** admin demo page; bước server decode admin, không có signature, allow.
- **Kết quả mong đợi / Caption:** HTTP 200/admin demo; “Base64 Cookie Poisoning thành công vì không có integrity”.
- **Lỗi thường gặp / Reset:** decode error do chuỗi sai; reset/login lại rồi copy đúng fixed value.

### 20. `20_base64_inspector.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi pipeline decode và authorization; `/vulnerable/base64/admin`; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** poisoned role admin; gốc role user.
- **Thao tác DevTools thủ công:** không sửa thêm; mở Base64 Inspector.
- **Panel / Timeline step / Nội dung bắt buộc:** Base64 Inspector; bước decode/parse/role extraction/allow; encoded masked, decoded JSON, no confidentiality/integrity/signature.
- **Kết quả mong đợi / Caption:** decision liên kết với role thật đã decode; “Inspector cho thấy Base64 chỉ encode, server vẫn tin role client”.
- **Lỗi thường gặp / Reset:** inspector dùng dữ liệu mẫu không khớp request; chạy lại flow thật trước khi chụp.

### 21. `21_base64_final_verdict.png`

- **Mục đích / URL / Mode / Tài khoản:** kết luận Base64 flow; trang flow/dashboard; Base64; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** trace có original deny và modified allow; role admin hiện tại.
- **Thao tác DevTools thủ công:** không sửa; mở Verdict.
- **Panel / Timeline step / Nội dung bắt buộc:** Final Verdict; bước cuối Base64; root cause, impact, “Base64 is not encryption”, fix signing/server-side role.
- **Kết quả mong đợi / Caption:** vulnerable verdict dựa trace; “Kết luận Base64 không bảo vệ tính toàn vẹn”.
- **Lỗi thường gặp / Reset:** thiếu original deny; reset và chạy cả hai trạng thái trước khi chụp; reset sau ảnh.

### 22. `22_signed_cookie_login.png`

- **Mục đích / URL / Mode / Tài khoản:** bắt đầu signed flow; `/login`; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** reset; chưa có signed cookie.
- **Thao tác DevTools thủ công:** chọn Signed Cookie Demo và submit student.
- **Panel / Timeline step / Nội dung bắt buộc:** signed login result; bước create/sign; algorithm được nêu, không secret/full token trong log.
- **Kết quả mong đợi / Caption:** signed cookie được tạo; “Student đăng nhập và nhận signed cookie”.
- **Lỗi thường gặp / Reset:** dùng nhầm Base64 mode; reset và chọn Signed.

### 23. `23_signed_cookie_attributes.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi flags signed cookie; `/secure/signed/profile`; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** valid `lab06_signed_profile`; value không được chụp đầy đủ nếu UI chưa mask.
- **Thao tác DevTools thủ công:** mở cookie row, kéo cột để thấy flags; không sửa.
- **Panel / Timeline step / Nội dung bắt buộc:** Attribute Inspector + DevTools; bước Set-Cookie; HttpOnly true, SameSite Lax, Path `/`, Secure theo config thực.
- **Kết quả mong đợi / Caption:** flags UI/browser khớp; “Thuộc tính signed cookie lấy từ cấu hình thực”.
- **Lỗi thường gặp / Reset:** Secure false trên HTTP local là bình thường; không giả bật flag, ghi đúng config.

### 24. `24_signed_cookie_valid.png`

- **Mục đích / URL / Mode / Tài khoản:** signed cookie hợp lệ được xác minh; `/secure/signed/profile`; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** signed cookie nguyên vẹn; masked token.
- **Thao tác DevTools thủ công:** reload profile, không sửa cookie.
- **Panel / Timeline step / Nội dung bắt buộc:** profile/result; bước verify thành công rồi deserialize; signature valid và request accepted.
- **Kết quả mong đợi / Caption:** profile HTTP 200; “Signed cookie hợp lệ vượt qua kiểm tra toàn vẹn”.
- **Lỗi thường gặp / Reset:** secret thay đổi sau restart làm token cũ invalid; reset/login lại để tạo token mới.

### 25. `25_signature_inspector_valid.png`

- **Mục đích / URL / Mode / Tài khoản:** chi tiết verification hợp lệ; `/secure/signed/profile`; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** token nguyên vẹn; payload/signature đã che.
- **Thao tác DevTools thủ công:** không sửa; mở Signature Inspector.
- **Panel / Timeline step / Nội dung bắt buộc:** Signature Inspector; verify step; present=true, algorithm, valid=true, deserialization=true, authorization status/decision, không key.
- **Kết quả mong đợi / Caption:** integrity/authenticity được chứng minh; “Signature Inspector - chữ ký hợp lệ”.
- **Lỗi thường gặp / Reset:** full token/secret xuất hiện; không chụp, sửa masking rồi login lại.

### 26. `26_signed_cookie_modified_devtools.png`

- **Mục đích / URL / Mode / Tài khoản:** tamper signed cookie thủ công; `/secure/signed/profile`; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** valid `lab06_signed_profile`; chỉ ghi phần rút gọn/fingerprint trong tài liệu.
- **Thao tác DevTools thủ công:** sửa đúng một ký tự trong Value, Enter; không thay cookie name/flags, không dùng tool tùy ý.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools local cookie; bước tamper; thể hiện origin và giá trị đã thay nhưng crop/mask tránh lộ full token nếu cần.
- **Kết quả mong đợi / Caption:** browser lưu token bị sửa; “Sửa một ký tự của signed cookie bằng DevTools local”.
- **Lỗi thường gặp / Reset:** sửa ở đầu làm malformed thay vì signature mismatch vẫn là negative hợp lệ nhưng không đúng kịch bản; reset/login và sửa ký tự phần phù hợp.

### 27. `27_signed_cookie_rejected.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh tamper bị từ chối; `/secure/signed/profile` hoặc `/secure/signed/admin`; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** token đã đổi một ký tự, gốc valid.
- **Thao tác DevTools thủ công:** reload route; không thử brute force hoặc nhập secret.
- **Panel / Timeline step / Nội dung bắt buộc:** signed invalid page; bước verify fail trước deserialize/authorization; status từ chối rõ.
- **Kết quả mong đợi / Caption:** request bị reject; “Signed cookie bị sửa được server phát hiện và từ chối”.
- **Lỗi thường gặp / Reset:** route redirect login không nêu lý do; mở trace/inspector để có evidence; reset sau ảnh 28.

### 28. `28_signature_inspector_invalid.png`

- **Mục đích / URL / Mode / Tài khoản:** chi tiết negative path; signed invalid result; Signed; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** tampered token; gốc valid.
- **Thao tác DevTools thủ công:** không sửa thêm; mở Signature Inspector.
- **Panel / Timeline step / Nội dung bắt buộc:** Signature Inspector; verify failure step; valid=false, deserialization=false, authorization=false, decision reject, masked sections.
- **Kết quả mong đợi / Caption:** không dùng payload trước verification; “Signature Inspector - token bị sửa không được deserialize”.
- **Lỗi thường gặp / Reset:** inspector nói authorization executed; đó là lỗi implementation, không chụp cho tới khi sửa; reset Signed flow.

### 29. `29_encrypted_cookie_demo.png`

- **Mục đích / URL / Mode / Tài khoản:** xem Fernet demo read-only; `/secure/encrypted-demo`; Encrypted; không cần login hoặc tài khoản theo UI.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** reset signed flow; token demo do server tạo, payload không có role/password/session ID.
- **Thao tác DevTools thủ công:** không edit token, không nhập key; chỉ mở trang.
- **Panel / Timeline step / Nội dung bắt buộc:** Encryption Inspector; encrypt/decrypt step; plain JSON demo, masked token, decrypt result, key location “Server environment only”.
- **Kết quả mong đợi / Caption:** valid decrypt và confidentiality/integrity true; “Fernet authenticated encryption demo không dùng cho authorization”.
- **Lỗi thường gặp / Reset:** key hoặc full token lộ; không chụp, sửa masking/config; reload để tạo demo mới.

### 30. `30_encoding_signing_encryption.png`

- **Mục đích / URL / Mode / Tài khoản:** so sánh bốn khái niệm; `/secure/encrypted-demo` hoặc `/comparison`; Encrypted/comparison; N/A.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** encrypted demo đã chạy; token chỉ masked.
- **Thao tác DevTools thủ công:** không sửa; mở comparison panel.
- **Panel / Timeline step / Nội dung bắt buộc:** Encryption/Comparison Inspector; comparison step; Base64 encoding, signing, encryption, authenticated encryption với confidentiality/integrity chính xác.
- **Kết quả mong đợi / Caption:** bảng nêu encryption không thay authorization; “Phân biệt encoding, signing, encryption và authenticated encryption”.
- **Lỗi thường gặp / Reset:** gọi Base64 là encryption hoặc signing là confidentiality; sửa nội dung trước khi chụp.

### 31. `31_server_session_student_login.png`

- **Mục đích / URL / Mode / Tài khoản:** student login bằng server session; `/login`; Server-side Session; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** reset; chưa có `lab06_session`.
- **Thao tác DevTools thủ công:** chọn Server-side Session Demo và submit student.
- **Panel / Timeline step / Nội dung bắt buộc:** session login result; create/rotate step; user student, session fingerprint, expiry, không raw token.
- **Kết quả mong đợi / Caption:** session mới được tạo; “Student đăng nhập với Server-side Session”.
- **Lỗi thường gặp / Reset:** signed cookie còn nhưng không liên quan; reset để ảnh sạch rồi login lại.

### 32. `32_server_session_cookie.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh cookie chỉ chứa opaque Session ID; `/secure/session/profile`; Server-side Session; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** active `lab06_session`; token ngẫu nhiên, không ghi lại đầy đủ.
- **Thao tác DevTools thủ công:** mở cookie row, không copy/paste hoặc sửa.
- **Panel / Timeline step / Nội dung bắt buộc:** DevTools + Cookie Inspector; browser send step; cookie name/flags, masked value/fingerprint, không role/user_id.
- **Kết quả mong đợi / Caption:** cookie opaque; “Server-side session cookie không chứa role hoặc user ID”.
- **Lỗi thường gặp / Reset:** ảnh lộ full token; che/crop cột Value nhưng vẫn giữ Name/flags, hoặc dùng Inspector masked.

### 33. `33_server_session_inspector.png`

- **Mục đích / URL / Mode / Tài khoản:** thấy lookup bằng token hash; `/secure/session/profile`; Server-side Session; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** active session; raw token chỉ ở browser cookie, database có SHA-256.
- **Thao tác DevTools thủ công:** không sửa; mở Server Session Inspector.
- **Panel / Timeline step / Nội dung bắt buộc:** Server Session Inspector; hash/lookup/active/expiry step; fingerprints, active, expiry, user lookup, rotation reason, không raw token.
- **Kết quả mong đợi / Caption:** record thật khớp request; “Server hash Session ID và tra trạng thái phía server”.
- **Lỗi thường gặp / Reset:** DB hiển thị raw token; dừng và sửa schema/inspector trước khi chụp.

### 34. `34_student_admin_denied.png`

- **Mục đích / URL / Mode / Tài khoản:** server-side authorization từ chối student; `/secure/session/admin`; Server-side Session; `student`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** active student session; cookie không có role.
- **Thao tác DevTools thủ công:** điều hướng route, không sửa token.
- **Panel / Timeline step / Nội dung bắt buộc:** denied + Authorization Inspector; database role lookup/decision step; submitted role N/A, database role user, deny reason.
- **Kết quả mong đợi / Caption:** HTTP 403/denied; “Student bị từ chối sau khi server lấy role=user từ database”.
- **Lỗi thường gặp / Reset:** trang cho phép do seed sai; reset database/seed và login student lại.

### 35. `35_admin_server_session_login.png`

- **Mục đích / URL / Mode / Tài khoản:** tạo admin server session mới; `/login`; Server-side Session; `admin_lab`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** logout/reset student session; không reuse token cũ.
- **Thao tác DevTools thủ công:** chọn Server-side Session, nhập admin demo và submit.
- **Panel / Timeline step / Nội dung bắt buộc:** session login result; create/rotate step; admin username, new fingerprint, không password/token.
- **Kết quả mong đợi / Caption:** admin login thành công với session mới; “Admin đăng nhập bằng Server-side Session”.
- **Lỗi thường gặp / Reset:** browser vẫn dùng student cookie do logout lỗi; POST logout/reset rồi login lại.

### 36. `36_admin_access_allowed.png`

- **Mục đích / URL / Mode / Tài khoản:** admin được phép bằng database role; `/secure/session/admin`; Server-side Session; `admin_lab`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** active admin session; opaque token.
- **Thao tác DevTools thủ công:** mở route, không sửa cookie.
- **Panel / Timeline step / Nội dung bắt buộc:** secure admin page + Authorization Inspector; DB lookup/allow step; database role admin và allow reason.
- **Kết quả mong đợi / Caption:** HTTP 200/admin; “Admin được phép sau kiểm tra role phía server”.
- **Lỗi thường gặp / Reset:** token expired; logout/login admin lại để tạo session mới.

### 37. `37_database_role_lookup.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh nguồn quyền là database; `/secure/session/admin`; Server-side Session; `admin_lab`.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** active admin session; cookie không chứa role.
- **Thao tác DevTools thủ công:** không sửa; mở Database + Authorization Inspector.
- **Panel / Timeline step / Nội dung bắt buộc:** Database Inspector; user lookup step; safe user fields, role admin, parameterized lookup indication, không password hash.
- **Kết quả mong đợi / Caption:** role source = database; “Secure authorization đọc role mới nhất từ database”.
- **Lỗi thường gặp / Reset:** password_hash xuất hiện; không chụp, sửa redaction; login lại nếu trace stale.

### 38. `38_session_rotation.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh rotate sau login; session flow/dashboard; Server-side Session; `admin_lab` hoặc `student` theo trace.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** flow có old/new session events; chỉ fingerprints.
- **Thao tác DevTools thủ công:** không copy/replay token; mở Session Inspector/Audit sau login.
- **Panel / Timeline step / Nội dung bắt buộc:** Session Inspector + session_events; rotation step; old fingerprint, new fingerprint, reason, old active=false/new active=true.
- **Kết quả mong đợi / Caption:** fingerprint thay đổi và phiên cũ revoked; “Session rotation sau đăng nhập”.
- **Lỗi thường gặp / Reset:** không có old event ở fresh browser; dùng fixed demo flow/test evidence do app tạo, không tạo replay UI; reset và chạy lại.

### 39. `39_logout_invalidation.png`

- **Mục đích / URL / Mode / Tài khoản:** logout hủy server session; `/secure/session/logout` rồi trang kết quả/audit; Server-side Session; account đang login.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** active session fingerprint đã biết; raw token không ghi.
- **Thao tác DevTools thủ công:** dùng nút/form POST Logout; sau response mở Cookies để thấy expired/removed, không tự xóa trước.
- **Panel / Timeline step / Nội dung bắt buộc:** Session Inspector/Audit; revoke/logout step; active false, revoked_at/reason, expired Set-Cookie.
- **Kết quả mong đợi / Caption:** server record bị revoke và browser cookie hết hạn; “Logout thực hiện server-side invalidation”.
- **Lỗi thường gặp / Reset:** chỉ mất cookie nhưng DB vẫn active; đó là lỗi, không chụp; login lại sau khi sửa.

### 40. `40_old_session_rejected.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh token cũ không dùng được; secure session result/audit; Server-side Session; account của phiên đã revoke.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** rotation/logout đã tạo old fingerprint inactive; không lấy raw token để replay thủ công.
- **Thao tác DevTools thủ công:** mở kết quả của fixed demo flow hoặc trace/test-client evidence trong UI; không tạo replay tool và không paste token cũ.
- **Panel / Timeline step / Nội dung bắt buộc:** Session Inspector/Audit/Timeline; old-session rejection step; fingerprint, inactive/revoked/expired reason, decision reject.
- **Kết quả mong đợi / Caption:** old session rejected; “Phiên cũ bị từ chối sau rotation/logout”.
- **Lỗi thường gặp / Reset:** không có event vì chưa chạy fixed demo; chạy `python scripts/run_demo_flows.py` rồi tự mở UI và chụp, không tự động chụp.

### 41. `41_code_comparison.png`

- **Mục đích / URL / Mode / Tài khoản:** so sánh code vulnerable/secure; `/comparison`; comparison; N/A.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** ít nhất một trace vulnerable và secure đã chạy; N/A.
- **Thao tác DevTools thủ công:** không sửa; mở Code Comparison.
- **Panel / Timeline step / Nội dung bắt buộc:** Code Comparison; comparison step; đọc cookie role vs verify signature vs DB role lookup, source references thật và bản vá.
- **Kết quả mong đợi / Caption:** snippet khớp source hiện hành; “So sánh nguồn quyết định phân quyền vulnerable và secure”.
- **Lỗi thường gặp / Reset:** snippet hard-code lệch source; sửa generator/metadata rồi reload.

### 42. `42_security_controls.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi control thực tế; `/security-controls`; common; N/A.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** app đang chạy config local; N/A.
- **Thao tác DevTools thủ công:** không sửa; có thể mở Network Headers cho cùng response.
- **Panel / Timeline step / Nội dung bắt buộc:** Security Control Panel; config step; bind host, debug false, cookie flags thực, CSP/nosniff/DENY/referrer/permissions/cache, request size, no wildcard CORS.
- **Kết quả mong đợi / Caption:** panel phản ánh response/config thật; “Security controls của Lab06 tại runtime local”.
- **Lỗi thường gặp / Reset:** ghi Secure=true trên HTTP nhưng header không có; chụp giá trị thật hoặc sửa config, không hard-code.

### 43. `43_audit_logs.png`

- **Mục đích / URL / Mode / Tài khoản:** tập hợp audit event; `/audit-logs`; common; account tùy flow đã chạy.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** đã chạy Plain/Base64/Signed/Session; chỉ cookie names/status/fingerprints an toàn.
- **Thao tác DevTools thủ công:** không sửa; mở audit page và lọc bằng control cố định nếu có.
- **Panel / Timeline step / Nội dung bắt buộc:** Audit Inspector; audit write steps; timestamp, actor, route, mode, decision, reason, trace ID; không password/secret/full cookie.
- **Kết quả mong đợi / Caption:** event thật liên kết trace; “Audit log đã che dữ liệu nhạy cảm của các flow”.
- **Lỗi thường gặp / Reset:** log chứa token/password; xóa evidence không an toàn, sửa logging, reset và chạy lại flow trước khi chụp.

### 44. `44_trace_timeline.png`

- **Mục đích / URL / Mode / Tài khoản:** minh họa trace chi tiết; dashboard/flow hoặc `/api/trace/<trace_id>` kèm UI; mode đã chọn; account của trace.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** có trace thật; chỉ masked/fingerprint.
- **Thao tác DevTools thủ công:** không chỉnh JSON/DOM; chọn một trace ID thật từ Audit/Timeline.
- **Panel / Timeline step / Nội dung bắt buộc:** Trace Panel + Action Timeline; một active step; step_number, timestamp, layer, technique, input/output, code reference, status, security meaning.
- **Kết quả mong đợi / Caption:** JSON/panel đồng bộ; “Trace JSON và Action Timeline của request thật”.
- **Lỗi thường gặp / Reset:** trace ID stale/404 sau clear; chạy flow mới và dùng ID mới.

### 45. `45_presentation_mode.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh Presentation Mode; trang flow có trace; mode/account của flow đã chọn.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** trace nhiều bước đã có; masked values.
- **Thao tác DevTools thủ công:** đóng DevTools, bật Presentation Mode bằng UI; nhấn Next/Previous hoặc phím được hỗ trợ; không automation.
- **Panel / Timeline step / Nội dung bắt buộc:** Presentation controls; active middle step; progress, current step, explanation, code highlight và Inspector đồng bộ.
- **Kết quả mong đợi / Caption:** điều hướng hoạt động thủ công; “Presentation Mode đồng bộ Timeline và Inspector”.
- **Lỗi thường gặp / Reset:** phím browser cuộn trang thay vì đổi step; focus presentation control hoặc dùng nút; thoát và bật lại mode.

### 46. `46_pytest_passed.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi kết quả pytest thật; terminal tại thư mục Lab06; test; N/A.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** source/test hoàn chỉnh; N/A.
- **Thao tác DevTools thủ công:** không cần DevTools; tự chạy `pytest`, chờ kết thúc rồi chụp terminal; không sửa output.
- **Panel / Timeline step / Nội dung bắt buộc:** terminal; N/A; command, số collected/passed/failed/skipped và exit summary thật, không secret/path nhạy cảm.
- **Kết quả mong đợi / Caption:** chỉ dùng caption “Pytest passed” nếu exit code 0; “Kết quả pytest thực tế của Lab06”.
- **Lỗi thường gặp / Reset:** test fail hoặc output cũ; sửa lỗi, chạy lại toàn bộ lệnh rồi chụp kết quả mới; không crop mất summary.

### 47. `47_coverage.png`

- **Mục đích / URL / Mode / Tài khoản:** ghi coverage thật; terminal tại Lab06; coverage; N/A.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** pytest-cov cài và test chạy được; N/A.
- **Thao tác DevTools thủ công:** tự chạy `pytest --cov=. --cov-report=term-missing`, chờ xong rồi chụp; không chỉnh log.
- **Panel / Timeline step / Nội dung bắt buộc:** terminal; N/A; từng module lõi, percent/missing lines và summary thật; không chỉ chụp total nếu module bị thiếu.
- **Kết quả mong đợi / Caption:** ghi đúng số đo, chỉ nói đạt 90% khi mọi module yêu cầu thật sự đạt; “Coverage thực tế của các module lõi”.
- **Lỗi thường gặp / Reset:** coverage thấp hoặc module omitted; bổ sung test có ý nghĩa, chạy lại; không sửa file coverage thủ công.

### 48. `48_report_files.png`

- **Mục đích / URL / Mode / Tài khoản:** chứng minh DOCX/PDF thật tồn tại; File Explorer và/hoặc viewer local; report; N/A.
- **Điều kiện ban đầu / Cookie / Giá trị gốc:** đã chạy `python scripts/generate_report.py` thành công; N/A.
- **Thao tác DevTools thủ công:** không cần DevTools; mở thư mục `report`, sau đó mở DOCX/PDF để xác nhận không hỏng; tự chụp màn hình.
- **Panel / Timeline step / Nội dung bắt buộc:** Explorer/viewer; N/A; đúng hai tên `21127645_LeMinh_Lab06_CookiePoisoning.docx/.pdf`, dung lượng khác 0, trang nội dung thật, không placeholder ảnh.
- **Kết quả mong đợi / Caption:** hai file mở được; ghi page count chỉ sau khi đo; “Báo cáo DOCX và PDF được tạo từ evidence thật”.
- **Lỗi thường gặp / Reset:** PDF thiếu/hỏng hoặc script báo lỗi; không chụp/tuyên bố hoàn thành, sửa generator rồi chạy lại.

## Kiểm tra ảnh sau khi chụp

Sau khi đã tự chụp và lưu đủ file:

```powershell
python scripts/check_screenshots.py
```

Script chỉ được kiểm tra tên, PNG, file rỗng, kích thước quá nhỏ, thiếu/thừa và hash trùng. Script không OCR, không phân tích nội dung, không chụp hoặc tạo ảnh. Người học vẫn phải tự mở từng ảnh để kiểm tra address bar, panel, dữ liệu che và caption.

## Reset toàn bộ để làm lại

1. Dùng UI Reset Lab hoặc gửi form `POST /reset-lab`.
2. Nếu cần, chạy `python scripts/reset_database.py` rồi `python seed.py`.
3. Trong DevTools, chỉ xóa năm cookie Lab06 cố định: `lab06_username`, `lab06_role`, `lab06_profile_b64`, `lab06_signed_profile`, `lab06_session` (nếu tồn tại). Không xóa/copy cookie của site khác.
4. Đóng DevTools, mở lại `/login`, chọn đúng mode và chạy lại nhóm ảnh.
5. Không giữ ảnh của flow lỗi rồi đổi tên thành ảnh đạt.
