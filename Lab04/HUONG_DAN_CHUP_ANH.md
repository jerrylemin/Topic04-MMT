# HƯỚNG DẪN CHỤP ẢNH THỦ CÔNG - LAB04 CSRF

## 1. Mục đích tài liệu

Tài liệu giúp sinh viên tự cài môi trường, tự chạy lab, tự thực hiện kịch bản và tự chụp bằng chứng thật. Chỉ thao tác trên localhost của repository; không thử trên website/hệ thống thật, không dùng ảnh dựng, Playwright, Selenium, extension/macro chụp tự động hoặc công cụ chỉnh DOM để giả kết quả. Đóng tab riêng tư, không để lộ cookie/token thật, dữ liệu cá nhân, password, session ID hay chữ ký dài.

## 2. Chuẩn bị môi trường từ đầu

Từ Command Prompt tại thư mục repository, vào `Topic04\Lab04`, rồi chạy `scripts\run_lab.bat`. Script tạo `.venv`, cài requirements, seed database khi thiếu và chạy `run_both.py`. Mở Victim tại `http://127.0.0.1:5004` và Demo Page tại `http://127.0.0.1:9004` (same-site cross-origin) hoặc `http://localhost:9004` (cross-site). Dừng cả hai server bằng `Ctrl+C`; reset bằng `.venv\Scripts\python scripts\reset_database.py`.

### Tài khoản và dữ liệu cố định

Victim: `victim` / `Victim123!`, email đầu `victim_old@lab.local`; receiver: `receiver` / `Receiver123!`.

## 3. Chuẩn bị trình duyệt và F12

1. Mở Chrome hoặc Microsoft Edge và truy cập đúng URL `127.0.0.1`/`localhost` nêu trong từng ảnh.
2. Nhấn `F12`, chọn menu DevTools > Dock side > Dock to right. Đặt browser zoom 80-100% và kéo vách ngăn để cùng thấy thanh địa chỉ, UI và DevTools.
3. Mở **Network**; bật **Preserve log** khi thao tác có redirect/reload; bật **Disable cache** trong lúc DevTools mở nếu cache làm sai nội dung.
4. Bấm Clear để xóa request cũ trước mỗi kịch bản. Lọc theo route như `login`, `search`, `checkout`, `invoice`, `change-email`, `admin` hoặc `submit`.
5. Chọn đúng request, lần lượt mở **Headers**, **Payload**, **Response** hoặc **Preview**. Mở **Cookies**, **Initiator** hay **Timing** chỉ khi mục ảnh yêu cầu.
6. Dùng **Application/Storage > Cookies** cho cookie; **Elements** cho DOM/form/hidden field; **Console** chỉ quan sát lỗi/trạng thái được yêu cầu, không chạy lệnh đọc cookie; **Sources** chỉ khi cần chứng minh JavaScript client-side.
7. Kéo rộng cột/khung chi tiết, thu gọn panel không liên quan và che value nhạy cảm; không cắt mất URL, status, tên request, tab đang mở hoặc kết quả UI.

## 4. Luồng thao tác theo kịch bản F12

Trước mỗi nhóm: reset đúng cách, đăng nhập đúng tài khoản, chụp trạng thái trước, thực hiện request vulnerable, chụp request/payload/response/trạng thái sau, rồi reset và chạy cùng dữ liệu ở bản secure. Không giả định bước trước còn hiệu lực; kiểm tra lại URL, account và cookie trước từng ảnh.

### F12-01. `01_victim_login_session.png`

- **Mục tiêu:** Thiết lập session victim
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/login`
- **Tài khoản:** victim / Victim123!
- **Dữ liệu nhập:** `username=victim; password che`
- **Thao tác/nút:** Đăng nhập
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Headers; Application Cookies
- **Request cần chọn:** `POST /login`
- **Trường cần mở:** Form Data; Set-Cookie
- **Nội dung bắt buộc:** Redirect thành công; `lab04_session` hiện diện với HttpOnly/SameSite/Path
- **Kết quả mong đợi:** Victim đã đăng nhập
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Đăng nhập victim và tạo session local
- **Mục báo cáo:** F12 / Session

### F12-02. `02_email_before.png`

- **Mục tiêu:** Ghi email trước thao tác
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/profile`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Không`
- **Thao tác/nút:** Mở profile
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /profile`
- **Trường cần mở:** Response/Preview
- **Nội dung bắt buộc:** Email `victim_old@lab.local` và session local
- **Kết quả mong đợi:** Baseline trước CSRF
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Email victim trước request CSRF
- **Mục báo cáo:** F12 / State before

### F12-03. `03_legitimate_email_request.png`

- **Mục tiêu:** Chứng minh request đổi email hợp lệ ở vulnerable route
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/vulnerable/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=demo_changed@lab.local`
- **Thao tác/nút:** Submit từ Victim UI
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Headers
- **Request cần chọn:** `POST /vulnerable/change-email`
- **Trường cần mở:** General, Request Headers, Form Data
- **Nội dung bắt buộc:** Method POST, route, form email và Cookie đã che
- **Kết quả mong đợi:** Email đổi thành công ở flow hợp lệ
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request đổi email hợp lệ
- **Mục báo cáo:** F12 / Legitimate request

### F12-04. `04_vulnerable_no_token_payload.png`

- **Mục tiêu:** Chứng minh vulnerable request không có CSRF token
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/vulnerable/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=demo_changed@lab.local`
- **Thao tác/nút:** Chọn POST
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/change-email`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** Chỉ có email; không có `csrf_token`
- **Kết quả mong đợi:** Route phụ thuộc session cookie
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Vulnerable Form Data thiếu CSRF token
- **Mục báo cáo:** F12 / Vulnerable / Token

### F12-05. `05_attacker_form_dom.png`

- **Mục tiêu:** Chứng minh form attacker local
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:9004/attack/vulnerable-email`
- **Tài khoản:** victim đang đăng nhập ở victim origin
- **Dữ liệu nhập:** `email=demo_changed@lab.local`
- **Thao tác/nút:** Mở trang, chưa submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Elements
- **Request cần chọn:** `N/A`
- **Trường cần mở:** Form action/method/hidden input
- **Nội dung bắt buộc:** action trỏ `http://127.0.0.1:5004/vulnerable/change-email`, method POST, email cố định
- **Kết quả mong đợi:** Form cross-origin có thể tạo request
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** DOM form của Demo Page local
- **Mục báo cáo:** F12 / Attacker form

### F12-06. `06_attacker_origin_request.png`

- **Mục tiêu:** Chứng minh request phát sinh từ Demo Page
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:9004/attack/vulnerable-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=demo_changed@lab.local`
- **Thao tác/nút:** Bấm gửi và xác nhận
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers/Payload
- **Request cần chọn:** `POST http://127.0.0.1:5004/vulnerable/change-email`
- **Trường cần mở:** Origin, Referer, Sec-Fetch-Site, Cookie, Form Data
- **Nội dung bắt buộc:** Origin/Referer là :9004; Sec-Fetch-Site nếu browser có; Cookie tự gửi nếu policy cho phép
- **Kết quả mong đợi:** Request cross-origin tới victim
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request CSRF từ Demo Page local
- **Mục báo cáo:** F12 / Vulnerable / Cross-origin request

### F12-07. `07_vulnerable_response_success.png`

- **Mục tiêu:** Chứng minh vulnerable response cho phép
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/vulnerable/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email demo_changed`
- **Thao tác/nút:** Chọn request attacker
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /vulnerable/change-email`
- **Trường cần mở:** Status và Response
- **Nội dung bắt buộc:** Status thành công/redirect và thông báo email đã đổi
- **Kết quả mong đợi:** State bị thay đổi do thiếu token
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response vulnerable đổi email thành công
- **Mục báo cáo:** F12 / Vulnerable / Response

### F12-08. `08_email_after_csrf.png`

- **Mục tiêu:** Ghi email sau CSRF
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/profile`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Không`
- **Thao tác/nút:** Mở profile sau attack
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `GET /profile`
- **Trường cần mở:** Response/UI
- **Nội dung bắt buộc:** Email `demo_changed@lab.local`
- **Kết quả mong đợi:** So sánh trước/sau rõ ràng
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Email victim sau request CSRF
- **Mục báo cáo:** F12 / State after

### F12-09. `09_secure_form_token.png`

- **Mục tiêu:** Chứng minh form secure có token
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/secure/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=secure_changed@lab.local`
- **Thao tác/nút:** Mở form, chưa submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Elements
- **Request cần chọn:** `GET /secure/change-email`
- **Trường cần mở:** hidden input
- **Nội dung bắt buộc:** Input hidden `csrf_token` có giá trị; che phần lớn token
- **Kết quả mong đợi:** Token gắn với session
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Form secure chứa CSRF token
- **Mục báo cáo:** F12 / Secure / Form

### F12-10. `10_secure_valid_request.png`

- **Mục tiêu:** Chứng minh request secure có token hợp lệ
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/secure/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=secure_changed@lab.local; csrf_token che`
- **Thao tác/nút:** Submit từ Victim UI
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Headers
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Form Data, Origin, Referer, Cookie
- **Nội dung bắt buộc:** Token hiện diện (che), Origin/Referer victim origin, cookie che
- **Kết quả mong đợi:** Request secure hợp lệ
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request secure có token hợp lệ
- **Mục báo cáo:** F12 / Secure / Valid request

### F12-11. `11_secure_valid_response.png`

- **Mục tiêu:** Chứng minh token hợp lệ cho phép update
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/secure/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=secure_changed@lab.local`
- **Thao tác/nút:** Chọn POST secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Status và Response
- **Nội dung bắt buộc:** Thành công; email mới; token rotate theo trace nếu hiển thị
- **Kết quả mong đợi:** Secure flow hoạt động bình thường
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure với token hợp lệ
- **Mục báo cáo:** F12 / Secure / Valid response

### F12-12. `12_secure_missing_token_request.png`

- **Mục tiêu:** Chứng minh request giả mạo thiếu token
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:9004/attack/secure-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email=demo_changed@lab.local; không token`
- **Thao tác/nút:** Bấm gửi và xác nhận
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Headers
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Form Data, Origin, Referer, Cookie
- **Nội dung bắt buộc:** Không có csrf_token; origin :9004; cookie nếu policy cho phép
- **Kết quả mong đợi:** Server nhận request không đủ bằng chứng
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request secure giả mạo thiếu token
- **Mục báo cáo:** F12 / Secure / Missing token

### F12-13. `13_secure_missing_token_403.png`

- **Mục tiêu:** Chứng minh secure từ chối thiếu token
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/secure/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Thiếu token`
- **Thao tác/nút:** Chọn request ảnh 12
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers/Response
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Status và Response
- **Nội dung bắt buộc:** HTTP 403 và thông báo token missing/denied; email không đổi
- **Kết quả mong đợi:** Bản vá chặn request
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response 403 khi thiếu CSRF token
- **Mục báo cáo:** F12 / Secure / Denied

### F12-14. `14_secure_bad_token_payload.png`

- **Mục tiêu:** Chứng minh token sai bị gửi
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:9004/attack/bad-token`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `csrf_token=giá trị giả cố định của trang`
- **Thao tác/nút:** Bấm gửi và xác nhận
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** Token giả hiện diện nhưng không khớp; che nếu dài
- **Kết quả mong đợi:** Server kiểm tra equality/timing-safe
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request secure với token sai
- **Mục báo cáo:** F12 / Secure / Bad token

### F12-15. `15_secure_bad_token_403.png`

- **Mục tiêu:** Chứng minh secure từ chối token sai
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/secure/change-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Token sai`
- **Thao tác/nút:** Chọn request ảnh 14
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Status/Response
- **Nội dung bắt buộc:** HTTP 403; reason token mismatch; state không đổi
- **Kết quả mong đợi:** Token validation hiệu quả
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response 403 khi CSRF token sai
- **Mục báo cáo:** F12 / Secure / Bad token response

### F12-16. `16_cookie_samesite_application.png`

- **Mục tiêu:** Chứng minh SameSite/HttpOnly/Secure
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/profile`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Không`
- **Thao tác/nút:** Mở cookie victim origin
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Application/Storage > Cookies
- **Request cần chọn:** `GET /profile`
- **Trường cần mở:** Name, Domain, Path, HttpOnly, Secure, SameSite
- **Nội dung bắt buộc:** `lab04_session`, Path=/, HttpOnly=true, SameSite theo config, Secure phản ánh HTTP local; che Value
- **Kết quả mong đợi:** Cookie flags là defense-in-depth
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Cookie SameSite của Victim Application
- **Mục báo cáo:** F12 / Cookie

### F12-17. `17_set_cookie_response_header.png`

- **Mục tiêu:** Chứng minh Set-Cookie từ response login
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5004/login`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Đăng nhập lại nếu cần`
- **Thao tác/nút:** Chọn POST login
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `POST /login`
- **Trường cần mở:** Response Headers
- **Nội dung bắt buộc:** Set-Cookie có HttpOnly, Path, SameSite; Secure chỉ khi config bật
- **Kết quả mong đợi:** Header khớp Application
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Set-Cookie của session victim
- **Mục báo cáo:** F12 / Cookie / Response

### F12-18. `18_origin_validation_denied.png`

- **Mục tiêu:** Chứng minh Origin/Referer validation nếu request tới bước này
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://localhost:9004/attack/secure-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Request cross-site thiếu token`
- **Thao tác/nút:** Submit từ localhost:9004
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers/Response
- **Request cần chọn:** `POST /secure/change-email`
- **Trường cần mở:** Origin, Referer, Response
- **Nội dung bắt buộc:** Origin/Referer localhost:9004 và decision denied theo source/trace
- **Kết quả mong đợi:** Exact origin là lớp bổ sung
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Origin validation từ chối cross-origin
- **Mục báo cáo:** F12 / Origin validation

### F12-19. `19_preserve_log_redirect_chain.png`

- **Mục tiêu:** Chứng minh redirect không làm mất request
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:9004/attack/vulnerable-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `email demo_changed`
- **Thao tác/nút:** Bật Preserve log trước submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network
- **Request cần chọn:** `POST và request tiếp theo`
- **Trường cần mở:** Status/Initiator
- **Nội dung bắt buộc:** Chuỗi request giữ lại, Initiator là form document
- **Kết quả mong đợi:** Nguồn request được truy vết
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Preserve log giữ chuỗi CSRF request
- **Mục báo cáo:** F12 / Network workflow

### F12-20. `20_cookie_auto_sent_header.png`

- **Mục tiêu:** Chứng minh browser tự gửi cookie
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:9004/attack/vulnerable-email`
- **Tài khoản:** victim
- **Dữ liệu nhập:** `Không biết cookie value`
- **Thao tác/nút:** Submit form
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `POST /vulnerable/change-email`
- **Trường cần mở:** Request Headers > Cookie
- **Nội dung bắt buộc:** Cookie header có tên session nhưng Value phải che; attacker form không chứa cookie field
- **Kết quả mong đợi:** Browser tự gắn credential theo policy
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Cookie tự gửi trong request CSRF
- **Mục báo cáo:** F12 / Cookie flow

## 5. Bảng mô tả ảnh F12

| STT | Tên file | Mục tiêu | Chuẩn bị | URL/lệnh | Dữ liệu và thao tác | F12 cần mở | Nội dung bắt buộc | Kết quả | Caption | Mục báo cáo |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `01_victim_login_session.png` | Thiết lập session victim | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/login` | username=victim; password che; Đăng nhập | Network > Payload/Headers; Application Cookies; Form Data; Set-Cookie | Redirect thành công; `lab04_session` hiện diện với HttpOnly/SameSite/Path | Victim đã đăng nhập | Đăng nhập victim và tạo session local | F12 / Session |
| 2 | `02_email_before.png` | Ghi email trước thao tác | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/profile` | Không; Mở profile | Network > Headers; Response/Preview | Email `victim_old@lab.local` và session local | Baseline trước CSRF | Email victim trước request CSRF | F12 / State before |
| 3 | `03_legitimate_email_request.png` | Chứng minh request đổi email hợp lệ ở vulnerable route | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/vulnerable/change-email` | email=demo_changed@lab.local; Submit từ Victim UI | Network > Payload/Headers; General, Request Headers, Form Data | Method POST, route, form email và Cookie đã che | Email đổi thành công ở flow hợp lệ | Request đổi email hợp lệ | F12 / Legitimate request |
| 4 | `04_vulnerable_no_token_payload.png` | Chứng minh vulnerable request không có CSRF token | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/vulnerable/change-email` | email=demo_changed@lab.local; Chọn POST | Network > Payload; Form Data | Chỉ có email; không có `csrf_token` | Route phụ thuộc session cookie | Vulnerable Form Data thiếu CSRF token | F12 / Vulnerable / Token |
| 5 | `05_attacker_form_dom.png` | Chứng minh form attacker local | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:9004/attack/vulnerable-email` | email=demo_changed@lab.local; Mở trang, chưa submit | Elements; Form action/method/hidden input | action trỏ `http://127.0.0.1:5004/vulnerable/change-email`, method POST, email cố định | Form cross-origin có thể tạo request | DOM form của Demo Page local | F12 / Attacker form |
| 6 | `06_attacker_origin_request.png` | Chứng minh request phát sinh từ Demo Page | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:9004/attack/vulnerable-email` | email=demo_changed@lab.local; Bấm gửi và xác nhận | Network > Headers/Payload; Origin, Referer, Sec-Fetch-Site, Cookie, Form Data | Origin/Referer là :9004; Sec-Fetch-Site nếu browser có; Cookie tự gửi nếu policy cho phép | Request cross-origin tới victim | Request CSRF từ Demo Page local | F12 / Vulnerable / Cross-origin request |
| 7 | `07_vulnerable_response_success.png` | Chứng minh vulnerable response cho phép | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/vulnerable/change-email` | email demo_changed; Chọn request attacker | Network > Response/Preview; Status và Response | Status thành công/redirect và thông báo email đã đổi | State bị thay đổi do thiếu token | Response vulnerable đổi email thành công | F12 / Vulnerable / Response |
| 8 | `08_email_after_csrf.png` | Ghi email sau CSRF | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/profile` | Không; Mở profile sau attack | Network > Response/Preview; Response/UI | Email `demo_changed@lab.local` | So sánh trước/sau rõ ràng | Email victim sau request CSRF | F12 / State after |
| 9 | `09_secure_form_token.png` | Chứng minh form secure có token | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/secure/change-email` | email=secure_changed@lab.local; Mở form, chưa submit | Elements; hidden input | Input hidden `csrf_token` có giá trị; che phần lớn token | Token gắn với session | Form secure chứa CSRF token | F12 / Secure / Form |
| 10 | `10_secure_valid_request.png` | Chứng minh request secure có token hợp lệ | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/secure/change-email` | email=secure_changed@lab.local; csrf_token che; Submit từ Victim UI | Network > Payload/Headers; Form Data, Origin, Referer, Cookie | Token hiện diện (che), Origin/Referer victim origin, cookie che | Request secure hợp lệ | Request secure có token hợp lệ | F12 / Secure / Valid request |
| 11 | `11_secure_valid_response.png` | Chứng minh token hợp lệ cho phép update | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/secure/change-email` | email=secure_changed@lab.local; Chọn POST secure | Network > Response/Preview; Status và Response | Thành công; email mới; token rotate theo trace nếu hiển thị | Secure flow hoạt động bình thường | Response secure với token hợp lệ | F12 / Secure / Valid response |
| 12 | `12_secure_missing_token_request.png` | Chứng minh request giả mạo thiếu token | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:9004/attack/secure-email` | email=demo_changed@lab.local; không token; Bấm gửi và xác nhận | Network > Payload/Headers; Form Data, Origin, Referer, Cookie | Không có csrf_token; origin :9004; cookie nếu policy cho phép | Server nhận request không đủ bằng chứng | Request secure giả mạo thiếu token | F12 / Secure / Missing token |
| 13 | `13_secure_missing_token_403.png` | Chứng minh secure từ chối thiếu token | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/secure/change-email` | Thiếu token; Chọn request ảnh 12 | Network > Headers/Response; Status và Response | HTTP 403 và thông báo token missing/denied; email không đổi | Bản vá chặn request | Response 403 khi thiếu CSRF token | F12 / Secure / Denied |
| 14 | `14_secure_bad_token_payload.png` | Chứng minh token sai bị gửi | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:9004/attack/bad-token` | csrf_token=giá trị giả cố định của trang; Bấm gửi và xác nhận | Network > Payload; Form Data | Token giả hiện diện nhưng không khớp; che nếu dài | Server kiểm tra equality/timing-safe | Request secure với token sai | F12 / Secure / Bad token |
| 15 | `15_secure_bad_token_403.png` | Chứng minh secure từ chối token sai | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/secure/change-email` | Token sai; Chọn request ảnh 14 | Network > Response; Status/Response | HTTP 403; reason token mismatch; state không đổi | Token validation hiệu quả | Response 403 khi CSRF token sai | F12 / Secure / Bad token response |
| 16 | `16_cookie_samesite_application.png` | Chứng minh SameSite/HttpOnly/Secure | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/profile` | Không; Mở cookie victim origin | Application/Storage > Cookies; Name, Domain, Path, HttpOnly, Secure, SameSite | `lab04_session`, Path=/, HttpOnly=true, SameSite theo config, Secure phản ánh HTTP local; che Value | Cookie flags là defense-in-depth | Cookie SameSite của Victim Application | F12 / Cookie |
| 17 | `17_set_cookie_response_header.png` | Chứng minh Set-Cookie từ response login | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5004/login` | Đăng nhập lại nếu cần; Chọn POST login | Network > Headers; Response Headers | Set-Cookie có HttpOnly, Path, SameSite; Secure chỉ khi config bật | Header khớp Application | Set-Cookie của session victim | F12 / Cookie / Response |
| 18 | `18_origin_validation_denied.png` | Chứng minh Origin/Referer validation nếu request tới bước này | Server local đang chạy; xóa request cũ trong Network. | `http://localhost:9004/attack/secure-email` | Request cross-site thiếu token; Submit từ localhost:9004 | Network > Headers/Response; Origin, Referer, Response | Origin/Referer localhost:9004 và decision denied theo source/trace | Exact origin là lớp bổ sung | Origin validation từ chối cross-origin | F12 / Origin validation |
| 19 | `19_preserve_log_redirect_chain.png` | Chứng minh redirect không làm mất request | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:9004/attack/vulnerable-email` | email demo_changed; Bật Preserve log trước submit | Network; Status/Initiator | Chuỗi request giữ lại, Initiator là form document | Nguồn request được truy vết | Preserve log giữ chuỗi CSRF request | F12 / Network workflow |
| 20 | `20_cookie_auto_sent_header.png` | Chứng minh browser tự gửi cookie | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:9004/attack/vulnerable-email` | Không biết cookie value; Submit form | Network > Headers; Request Headers > Cookie | Cookie header có tên session nhưng Value phải che; attacker form không chứa cookie field | Browser tự gắn credential theo policy | Cookie tự gửi trong request CSRF | F12 / Cookie flow |

## 6. Xử lý lỗi thường gặp

- **Port 5004 và 9004 bị chiếm:** dừng server lab cũ bằng `Ctrl+C`; dùng `Get-NetTCPConnection -LocalPort 5004 -ErrorAction SilentlyContinue` để xác định tiến trình, không tự đổi port tài liệu.
- **Virtual environment chưa kích hoạt/thiếu dependency:** dùng đúng Python trong `.venv\Scripts\python.exe` và chạy `-m pip install -r requirements.txt`.
- **Database chưa seed/state cũ:** chạy script reset nêu ở mục 2, restart server rồi đăng nhập lại.
- **Cookie/session cũ hoặc sai tài khoản:** logout/reset, chỉ xóa cookie của đúng origin local, mở cửa sổ mới rồi đăng nhập lại.
- **Network không thấy request/bị lọc mất:** bỏ filter, bật Preserve log, bấm Clear rồi thực hiện lại; lưu ý đổi `location.hash` không phát sinh request mới.
- **Payload chưa URL encode:** nhập payload qua form; kiểm tra Request URL encoded và Query String Parameters decoded, không sửa payload sang chuỗi khác.
- **Alert không xuất hiện/redirect làm mất request/cache cũ:** bật Preserve log và Disable cache, reload, reset state rồi lặp lại đúng mode.
- **Server chưa nhận biến môi trường mới:** dừng bằng `Ctrl+C`, chạy lại script; không sửa source để làm khớp ảnh.
- **Ảnh nhỏ/bị cắt:** dock phải, giảm zoom, mở rộng trường cần đọc; giữ URL, request, status và UI kết quả.

## 7. Checklist cuối lab

- [ ] Server chạy đúng localhost và port.
- [ ] Đúng tài khoản/dữ liệu local; đủ ảnh theo manifest và đúng tên file.
- [ ] Ảnh có URL/lệnh, kết quả UI và đúng request/tab/field F12.
- [ ] Cookie/token/session/chữ ký dài đã che; vulnerable và secure tách biệt.
- [ ] Caption khớp báo cáo; không có ảnh trùng/ảnh giả/ảnh chụp tự động.
- [ ] Không chạy lại pytest/smoke test/Docker để tạo ảnh; ảnh test cũ (nếu có) chỉ là bằng chứng tùy chọn.
- [ ] Chỉ tạo DOCX; không tạo, cập nhật, mở hoặc render PDF.
- [ ] Chạy `python scripts/check_screenshots.py` khi sinh viên đã tự chụp đủ ảnh, rồi `python scripts/generate_report.py` để tạo DOCX.
