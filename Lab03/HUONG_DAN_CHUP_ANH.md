# HƯỚNG DẪN CHỤP ẢNH THỦ CÔNG - LAB03 PARAMETER TAMPERING

## 1. Mục đích tài liệu

Tài liệu giúp sinh viên tự cài môi trường, tự chạy lab, tự thực hiện kịch bản và tự chụp bằng chứng thật. Chỉ thao tác trên localhost của repository; không thử trên website/hệ thống thật, không dùng ảnh dựng, Playwright, Selenium, extension/macro chụp tự động hoặc công cụ chỉnh DOM để giả kết quả. Đóng tab riêng tư, không để lộ cookie/token thật, dữ liệu cá nhân, password, session ID hay chữ ký dài.

## 2. Chuẩn bị môi trường từ đầu

Từ Command Prompt tại thư mục repository, vào `Topic04\Lab03`, rồi chạy `scripts\run_lab.bat`. Script tạo `.venv`, cài requirements, seed `lab03.db` khi thiếu và chạy `app.py`. Cách trực tiếp: `.venv\Scripts\python app.py`. Mở `http://127.0.0.1:5003`; dừng bằng `Ctrl+C`. Trước mỗi nhóm nên chạy `.venv\Scripts\python scripts\reset_database.py` để khôi phục giá, invoice và role.

### Tài khoản và dữ liệu cố định

User A: `user_a` / `UserA123!`; User B: `user_b` / `UserB123!`; admin: `admin` / `Admin123!`. Luồng chính dùng User A.

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

### F12-01. `42_login_user_a_network.png`

- **Mục tiêu:** Chứng minh phiên User A
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/login`
- **Tài khoản:** user_a / UserA123!
- **Dữ liệu nhập:** `username=user_a; password phải che`
- **Thao tác/nút:** Đăng nhập
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Headers; Application Cookies
- **Request cần chọn:** `POST /login`
- **Trường cần mở:** Form Data; Cookie
- **Nội dung bắt buộc:** username user_a, response redirect, cookie Value đã che
- **Kết quả mong đợi:** Session thuộc User A
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Đăng nhập User A và session local
- **Mục báo cáo:** F12 / Authentication

### F12-02. `43_cart_add_request.png`

- **Mục tiêu:** Chứng minh request thêm sản phẩm
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/products`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `product_id=5; quantity=1`
- **Thao tác/nút:** Bấm Thêm vào giỏ
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /cart/add`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** product_id 5, quantity 1
- **Kết quả mong đợi:** Giỏ có USB Security Key
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request thêm sản phẩm vào giỏ
- **Mục báo cáo:** F12 / Checkout / Cart

### F12-03. `44_checkout_original_payload.png`

- **Mục tiêu:** Ghi payload checkout ban đầu
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/checkout`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `product_id=5; quantity=1; price=100000`
- **Thao tác/nút:** Submit checkout chưa sửa
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/checkout`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** product_id, quantity, price và giá gốc 100000
- **Kết quả mong đợi:** Invoice dùng giá gốc
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload checkout ban đầu
- **Mục báo cáo:** F12 / Checkout / Original

### F12-04. `45_checkout_tampered_payload.png`

- **Mục tiêu:** Chứng minh price bị sửa
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/checkout`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `price đổi 100000 thành 1`
- **Thao tác/nút:** Sửa hidden field trong Elements hoặc dùng Request Tampering Console cố định; submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/checkout`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** price=1 cùng product_id=5, quantity=1
- **Kết quả mong đợi:** Request tampered tới server
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload checkout sau sửa giá
- **Mục báo cáo:** F12 / Checkout / Tampered

### F12-05. `46_checkout_vulnerable_response.png`

- **Mục tiêu:** Chứng minh vulnerable chấp nhận giá client
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/checkout`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `price=1`
- **Thao tác/nút:** Chọn request tampered
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /vulnerable/checkout`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Invoice/total 1 hoặc verdict cho thấy client price được dùng
- **Kết quả mong đợi:** Bản vulnerable sai logic
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response vulnerable chấp nhận giá sửa
- **Mục báo cáo:** F12 / Checkout / Vulnerable response

### F12-06. `47_checkout_secure_response.png`

- **Mục tiêu:** Chứng minh secure lấy giá database
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/secure/checkout`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `product_id=5; quantity=1; thêm price=1 nếu console hỗ trợ`
- **Thao tác/nút:** Submit secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Response
- **Request cần chọn:** `POST /secure/checkout`
- **Trường cần mở:** Form Data và Response
- **Nội dung bắt buộc:** Server dùng 100000 từ database; mismatch được ghi/price client bị bỏ qua
- **Kết quả mong đợi:** Bản secure giữ giá đúng
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure lấy giá database
- **Mục báo cáo:** F12 / Checkout / Secure

### F12-07. `48_invoice_owner_request.png`

- **Mục tiêu:** Ghi invoice hợp lệ của User A
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/invoice?id=1001`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `id=1001`
- **Thao tác/nút:** Mở invoice
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/invoice?id=1001`
- **Trường cần mở:** Query String Parameters
- **Nội dung bắt buộc:** id=1001, status 200, cookie che
- **Kết quả mong đợi:** User A xem invoice của mình
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request invoice sở hữu bởi User A
- **Mục báo cáo:** F12 / IDOR / Baseline

### F12-08. `49_invoice_idor_request.png`

- **Mục tiêu:** Chứng minh đổi id sang invoice User B
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/invoice?id=1002`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `id đổi 1001 → 1002`
- **Thao tác/nút:** Sửa URL hoặc Edit and Resend nếu DevTools hỗ trợ
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/invoice?id=1002`
- **Trường cần mở:** Query String Parameters
- **Nội dung bắt buộc:** id=1002, session vẫn User A
- **Kết quả mong đợi:** Request trái quyền được gửi
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request IDOR đổi invoice id
- **Mục báo cáo:** F12 / IDOR / Request

### F12-09. `50_invoice_vulnerable_response.png`

- **Mục tiêu:** Chứng minh dữ liệu User B bị trả về
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/invoice?id=1002`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `id=1002`
- **Thao tác/nút:** Mở Response
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `GET /vulnerable/invoice?id=1002`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Dữ liệu invoice 1002 không thuộc user_a
- **Kết quả mong đợi:** Vulnerable trả 200 và dữ liệu trái quyền
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response vulnerable lộ invoice khác user
- **Mục báo cáo:** F12 / IDOR / Vulnerable response

### F12-10. `51_invoice_secure_403_response.png`

- **Mục tiêu:** Chứng minh object authorization
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/secure/invoice?id=1002`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `id=1002`
- **Thao tác/nút:** Mở route secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers/Response
- **Request cần chọn:** `GET /secure/invoice?id=1002`
- **Trường cần mở:** Status và Response
- **Nội dung bắt buộc:** HTTP 403 hoặc thông báo từ chối; không có nội dung invoice 1002
- **Kết quả mong đợi:** Secure chặn IDOR
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure trả 403 cho invoice khác chủ
- **Mục báo cáo:** F12 / IDOR / Secure

### F12-11. `52_profile_role_user_payload.png`

- **Mục tiêu:** Ghi payload profile bình thường
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/profile`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `email=usera@lab.local; role=user; user_id=12`
- **Thao tác/nút:** Submit chưa sửa
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/profile/update`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** role=user và user_id=12
- **Kết quả mong đợi:** Profile vẫn user
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload profile ban đầu
- **Mục báo cáo:** F12 / Profile / Baseline

### F12-12. `53_profile_role_admin_payload.png`

- **Mục tiêu:** Chứng minh role bị sửa
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/profile`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `role đổi user → admin`
- **Thao tác/nút:** Sửa hidden field/Request Console rồi submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/profile/update`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** role=admin; cookie/session che
- **Kết quả mong đợi:** Tampered field tới server
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload mass assignment role=admin
- **Mục báo cáo:** F12 / Profile / Tampered

### F12-13. `54_profile_vulnerable_response.png`

- **Mục tiêu:** Chứng minh vulnerable cập nhật role
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/vulnerable/profile`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `role=admin`
- **Thao tác/nút:** Chọn POST tampered
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /vulnerable/profile/update`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Response/UI cho thấy role admin hoặc session/database đổi
- **Kết quả mong đợi:** Vulnerable mass-assign field nhạy cảm
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response vulnerable nâng role
- **Mục báo cáo:** F12 / Profile / Vulnerable response

### F12-14. `55_profile_secure_response.png`

- **Mục tiêu:** Chứng minh field allowlist secure
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/secure/profile`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `email hợp lệ; thêm role=admin`
- **Thao tác/nút:** Submit secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Response
- **Request cần chọn:** `POST /secure/profile/update`
- **Trường cần mở:** Form Data và Response
- **Nội dung bắt buộc:** Role bị bỏ qua/từ chối; role database vẫn user
- **Kết quả mong đợi:** Allowlist chỉ chấp nhận email
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure loại bỏ role
- **Mục báo cáo:** F12 / Profile / Secure

### F12-15. `56_session_cookie_masked.png`

- **Mục tiêu:** Chứng minh tài khoản được xác định bằng session
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5003/products`
- **Tài khoản:** user_a
- **Dữ liệu nhập:** `Không`
- **Thao tác/nút:** Reload sau đăng nhập
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Application/Storage > Cookies; Network Headers
- **Request cần chọn:** `GET /products`
- **Trường cần mở:** Cookie Request Header và flags
- **Nội dung bắt buộc:** Cookie hiện diện nhưng Value/session ID được che; UI ghi user_a/user
- **Kết quả mong đợi:** Session gắn request với User A
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Cookie/session xác định tài khoản (đã che)
- **Mục báo cáo:** F12 / Session

## 5. Bảng mô tả ảnh F12

| STT | Tên file | Mục tiêu | Chuẩn bị | URL/lệnh | Dữ liệu và thao tác | F12 cần mở | Nội dung bắt buộc | Kết quả | Caption | Mục báo cáo |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `42_login_user_a_network.png` | Chứng minh phiên User A | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/login` | username=user_a; password phải che; Đăng nhập | Network > Payload/Headers; Application Cookies; Form Data; Cookie | username user_a, response redirect, cookie Value đã che | Session thuộc User A | Đăng nhập User A và session local | F12 / Authentication |
| 2 | `43_cart_add_request.png` | Chứng minh request thêm sản phẩm | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/products` | product_id=5; quantity=1; Bấm Thêm vào giỏ | Network > Payload; Form Data | product_id 5, quantity 1 | Giỏ có USB Security Key | Request thêm sản phẩm vào giỏ | F12 / Checkout / Cart |
| 3 | `44_checkout_original_payload.png` | Ghi payload checkout ban đầu | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/checkout` | product_id=5; quantity=1; price=100000; Submit checkout chưa sửa | Network > Payload; Form Data | product_id, quantity, price và giá gốc 100000 | Invoice dùng giá gốc | Payload checkout ban đầu | F12 / Checkout / Original |
| 4 | `45_checkout_tampered_payload.png` | Chứng minh price bị sửa | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/checkout` | price đổi 100000 thành 1; Sửa hidden field trong Elements hoặc dùng Request Tampering Console cố định; submit | Network > Payload; Form Data | price=1 cùng product_id=5, quantity=1 | Request tampered tới server | Payload checkout sau sửa giá | F12 / Checkout / Tampered |
| 5 | `46_checkout_vulnerable_response.png` | Chứng minh vulnerable chấp nhận giá client | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/checkout` | price=1; Chọn request tampered | Network > Response/Preview; Response | Invoice/total 1 hoặc verdict cho thấy client price được dùng | Bản vulnerable sai logic | Response vulnerable chấp nhận giá sửa | F12 / Checkout / Vulnerable response |
| 6 | `47_checkout_secure_response.png` | Chứng minh secure lấy giá database | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/secure/checkout` | product_id=5; quantity=1; thêm price=1 nếu console hỗ trợ; Submit secure | Network > Payload/Response; Form Data và Response | Server dùng 100000 từ database; mismatch được ghi/price client bị bỏ qua | Bản secure giữ giá đúng | Response secure lấy giá database | F12 / Checkout / Secure |
| 7 | `48_invoice_owner_request.png` | Ghi invoice hợp lệ của User A | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/invoice?id=1001` | id=1001; Mở invoice | Network > Headers; Query String Parameters | id=1001, status 200, cookie che | User A xem invoice của mình | Request invoice sở hữu bởi User A | F12 / IDOR / Baseline |
| 8 | `49_invoice_idor_request.png` | Chứng minh đổi id sang invoice User B | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/invoice?id=1002` | id đổi 1001 → 1002; Sửa URL hoặc Edit and Resend nếu DevTools hỗ trợ | Network > Headers; Query String Parameters | id=1002, session vẫn User A | Request trái quyền được gửi | Request IDOR đổi invoice id | F12 / IDOR / Request |
| 9 | `50_invoice_vulnerable_response.png` | Chứng minh dữ liệu User B bị trả về | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/invoice?id=1002` | id=1002; Mở Response | Network > Response/Preview; Response | Dữ liệu invoice 1002 không thuộc user_a | Vulnerable trả 200 và dữ liệu trái quyền | Response vulnerable lộ invoice khác user | F12 / IDOR / Vulnerable response |
| 10 | `51_invoice_secure_403_response.png` | Chứng minh object authorization | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/secure/invoice?id=1002` | id=1002; Mở route secure | Network > Headers/Response; Status và Response | HTTP 403 hoặc thông báo từ chối; không có nội dung invoice 1002 | Secure chặn IDOR | Response secure trả 403 cho invoice khác chủ | F12 / IDOR / Secure |
| 11 | `52_profile_role_user_payload.png` | Ghi payload profile bình thường | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/profile` | email=usera@lab.local; role=user; user_id=12; Submit chưa sửa | Network > Payload; Form Data | role=user và user_id=12 | Profile vẫn user | Payload profile ban đầu | F12 / Profile / Baseline |
| 12 | `53_profile_role_admin_payload.png` | Chứng minh role bị sửa | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/profile` | role đổi user → admin; Sửa hidden field/Request Console rồi submit | Network > Payload; Form Data | role=admin; cookie/session che | Tampered field tới server | Payload mass assignment role=admin | F12 / Profile / Tampered |
| 13 | `54_profile_vulnerable_response.png` | Chứng minh vulnerable cập nhật role | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/vulnerable/profile` | role=admin; Chọn POST tampered | Network > Response/Preview; Response | Response/UI cho thấy role admin hoặc session/database đổi | Vulnerable mass-assign field nhạy cảm | Response vulnerable nâng role | F12 / Profile / Vulnerable response |
| 14 | `55_profile_secure_response.png` | Chứng minh field allowlist secure | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/secure/profile` | email hợp lệ; thêm role=admin; Submit secure | Network > Payload/Response; Form Data và Response | Role bị bỏ qua/từ chối; role database vẫn user | Allowlist chỉ chấp nhận email | Response secure loại bỏ role | F12 / Profile / Secure |
| 15 | `56_session_cookie_masked.png` | Chứng minh tài khoản được xác định bằng session | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5003/products` | Không; Reload sau đăng nhập | Application/Storage > Cookies; Network Headers; Cookie Request Header và flags | Cookie hiện diện nhưng Value/session ID được che; UI ghi user_a/user | Session gắn request với User A | Cookie/session xác định tài khoản (đã che) | F12 / Session |

## 6. Xử lý lỗi thường gặp

- **Port 5003 bị chiếm:** dừng server lab cũ bằng `Ctrl+C`; dùng `Get-NetTCPConnection -LocalPort 5003 -ErrorAction SilentlyContinue` để xác định tiến trình, không tự đổi port tài liệu.
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

## 8. Phụ lục hướng dẫn bộ ảnh hiện có

Các tên ảnh cũ được giữ để không phá vỡ quy trình hiện có. Thực hiện theo mô tả dưới đây; ảnh test cũ là tùy chọn và ảnh report chỉ cần chứng minh DOCX.

Không dùng Playwright/Selenium và không tự động chụp ảnh. Chỉ chụp dữ liệu giả lập tại `http://127.0.0.1:5003`. Lưu PNG không dấu, không khoảng trắng trong `evidence/screenshots/`; không chụp tab cá nhân hay website thật.

## Chuẩn bị

1. Chạy `python app.py`, reset bằng `python scripts/reset_database.py`.
2. Đăng nhập User A bằng `user_a / UserA123!` hoặc User B bằng `user_b / UserB123!` khi mục ảnh yêu cầu.
3. Mở DevTools bằng F12; dùng Elements để sửa hidden field, Network để xem request, Application/Storage để xem cờ cookie.
4. Có thể dùng Request Tampering Console trong app, chỉ gọi route cố định localhost.
5. Mở Timeline, chọn inspector cần thiết; bật Presentation Mode khi chụp ảnh 39.
6. Xóa trace hoặc reset lab trước khi làm lại một luồng để bằng chứng không lẫn trạng thái.

## 01_home_overview.png

- **Mục đích:** Tổng quan Lab03
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** Chưa bắt buộc
- **URL:** /
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Ba bài thực hành checkout, IDOR và role tampering.
- **Kết quả mong đợi:** Ba bài thực hành checkout, IDOR và role tampering.
- **Caption báo cáo:** Tổng quan Lab03. Ba bài thực hành checkout, IDOR và role tampering.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 02_login_user_a.png

- **Mục đích:** Tài khoản mẫu User A
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** Chưa đăng nhập
- **URL:** /login
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Thông tin user_a và cảnh báo chỉ dùng dữ liệu lab.
- **Kết quả mong đợi:** Thông tin user_a và cảnh báo chỉ dùng dữ liệu lab.
- **Caption báo cáo:** Tài khoản mẫu User A. Thông tin user_a và cảnh báo chỉ dùng dữ liệu lab.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 03_products_database_price.png

- **Mục đích:** Giá tin cậy từ database
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /products
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Sản phẩm 5 có giá 100000 VND.
- **Kết quả mong đợi:** Sản phẩm 5 có giá 100000 VND.
- **Caption báo cáo:** Giá tin cậy từ database. Sản phẩm 5 có giá 100000 VND.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 04_cart_before_checkout.png

- **Mục đích:** Giỏ hàng trước checkout
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /cart
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Thêm vào giỏ
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** User A có sản phẩm 5, số lượng 1.
- **Kết quả mong đợi:** User A có sản phẩm 5, số lượng 1.
- **Caption báo cáo:** Giỏ hàng trước checkout. User A có sản phẩm 5, số lượng 1.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 05_checkout_original_parameters.png

- **Mục đích:** Tham số checkout gốc
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Parameter Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** product_id=5, quantity=1, price=100000.
- **Kết quả mong đợi:** product_id=5, quantity=1, price=100000.
- **Caption báo cáo:** Tham số checkout gốc. product_id=5, quantity=1, price=100000.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 06_checkout_hidden_price_devtools.png

- **Mục đích:** Hidden field vẫn do client kiểm soát
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** DevTools Elements
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** DevTools Elements hiển thị hidden price=100000.
- **Kết quả mong đợi:** DevTools Elements hiển thị hidden price=100000.
- **Caption báo cáo:** Hidden field vẫn do client kiểm soát. DevTools Elements hiển thị hidden price=100000.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 07_checkout_price_modified.png

- **Mục đích:** So sánh giá trước và sau sửa
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Parameter Diff
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Parameter Diff đánh dấu price modified.
- **Kết quả mong đợi:** Parameter Diff đánh dấu price modified.
- **Caption báo cáo:** So sánh giá trước và sau sửa. Parameter Diff đánh dấu price modified.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 08_checkout_tampered_request.png

- **Mục đích:** Request checkout đã bị sửa
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Gửi vulnerable request
- **Panel cần mở:** Request Inspector
- **Bước timeline:** HTTP Request
- **Nội dung bắt buộc:** Request Inspector hiển thị price=1.
- **Kết quả mong đợi:** Request Inspector hiển thị price=1.
- **Caption báo cáo:** Request checkout đã bị sửa. Request Inspector hiển thị price=1.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 09_checkout_vulnerable_server_logic.png

- **Mục đích:** Server lỗi tin submitted price
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Timeline
- **Bước timeline:** Business Logic
- **Nội dung bắt buộc:** Bước Business Logic dùng request.form['price'].
- **Kết quả mong đợi:** Bước Business Logic dùng request.form['price'].
- **Caption báo cáo:** Server lỗi tin submitted price. Bước Business Logic dùng request.form['price'].
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 10_checkout_wrong_invoice.png

- **Mục đích:** Invoice sai giá
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Final Result
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Invoice mới có total 1 VND.
- **Kết quả mong đợi:** Invoice mới có total 1 VND.
- **Caption báo cáo:** Invoice sai giá. Invoice mới có total 1 VND.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 11_checkout_vulnerable_database.png

- **Mục đích:** Database lưu giá sai
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Database Inspector
- **Bước timeline:** Database Write
- **Nội dung bắt buộc:** unit_price=1 và total=1.
- **Kết quả mong đợi:** unit_price=1 và total=1.
- **Caption báo cáo:** Database lưu giá sai. unit_price=1 và total=1.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 12_checkout_vulnerable_verdict.png

- **Mục đích:** Kết luận checkout vulnerable
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Final Security Verdict
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Parameter Tampering thành công.
- **Kết quả mong đợi:** Parameter Tampering thành công.
- **Caption báo cáo:** Kết luận checkout vulnerable. Parameter Tampering thành công.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 13_checkout_secure_request.png

- **Mục đích:** Cùng request gửi vào route secure
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Gửi secure request
- **Panel cần mở:** Request Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Request vẫn có price=1 nhưng được đánh dấu untrusted.
- **Kết quả mong đợi:** Request vẫn có price=1 nhưng được đánh dấu untrusted.
- **Caption báo cáo:** Cùng request gửi vào route secure. Request vẫn có price=1 nhưng được đánh dấu untrusted.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 14_checkout_secure_database_lookup.png

- **Mục đích:** Secure lookup giá server
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Timeline
- **Bước timeline:** SQLite Query
- **Nội dung bắt buộc:** SQLite Query lấy products.price_vnd=100000.
- **Kết quả mong đợi:** SQLite Query lấy products.price_vnd=100000.
- **Caption báo cáo:** Secure lookup giá server. SQLite Query lấy products.price_vnd=100000.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 15_checkout_price_mismatch.png

- **Mục đích:** Phát hiện price mismatch
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Parameter Diff
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** submitted_price=1 khác database_price=100000.
- **Kết quả mong đợi:** submitted_price=1 khác database_price=100000.
- **Caption báo cáo:** Phát hiện price mismatch. submitted_price=1 khác database_price=100000.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 16_checkout_secure_invoice.png

- **Mục đích:** Invoice secure đúng giá
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/checkout
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Database Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Invoice có total 100000 VND.
- **Kết quả mong đợi:** Invoice có total 100000 VND.
- **Caption báo cáo:** Invoice secure đúng giá. Invoice có total 100000 VND.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 17_checkout_audit_log.png

- **Mục đích:** Audit checkout tampering
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /audit-logs
- **Dữ liệu gốc:** price=100000
- **Dữ liệu cần sửa:** price=1
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Audit Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Event checkout_price_mismatch cùng trace ID.
- **Kết quả mong đợi:** Event checkout_price_mismatch cùng trace ID.
- **Caption báo cáo:** Audit checkout tampering. Event checkout_price_mismatch cùng trace ID.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 18_invoice_user_a_1001.png

- **Mục đích:** Owner xem invoice của mình
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/invoice?id=1001
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Invoice 1001 thuộc user_id 12.
- **Kết quả mong đợi:** Invoice 1001 thuộc user_id 12.
- **Caption báo cáo:** Owner xem invoice của mình. Invoice 1001 thuộc user_id 12.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 19_invoice_id_changed.png

- **Mục đích:** Invoice ID bị đổi
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/invoice?id=1002
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Parameter Diff
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Parameter Diff đánh dấu object reference changed.
- **Kết quả mong đợi:** Parameter Diff đánh dấu object reference changed.
- **Caption báo cáo:** Invoice ID bị đổi. Parameter Diff đánh dấu object reference changed.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 20_invoice_idor_request.png

- **Mục đích:** Request IDOR
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/invoice?id=1002
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Request Inspector
- **Bước timeline:** HTTP Request
- **Nội dung bắt buộc:** GET query id=1002.
- **Kết quả mong đợi:** GET query id=1002.
- **Caption báo cáo:** Request IDOR. GET query id=1002.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 21_invoice_idor_database.png

- **Mục đích:** Owner không khớp session
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/invoice?id=1002
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Database Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** owner_id=13 và session user_id=12.
- **Kết quả mong đợi:** owner_id=13 và session user_id=12.
- **Caption báo cáo:** Owner không khớp session. owner_id=13 và session user_id=12.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 22_invoice_idor_success.png

- **Mục đích:** IDOR vulnerable thành công
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/invoice?id=1002
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Final Security Verdict
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** User A thấy invoice giả lập của User B.
- **Kết quả mong đợi:** User A thấy invoice giả lập của User B.
- **Caption báo cáo:** IDOR vulnerable thành công. User A thấy invoice giả lập của User B.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 23_invoice_secure_authorization.png

- **Mục đích:** Object-level authorization
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/invoice?id=1002
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Authorization Inspector
- **Bước timeline:** Authorization
- **Nội dung bắt buộc:** Policy owner or admin đưa ra decision deny.
- **Kết quả mong đợi:** Policy owner or admin đưa ra decision deny.
- **Caption báo cáo:** Object-level authorization. Policy owner or admin đưa ra decision deny.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 24_invoice_secure_403.png

- **Mục đích:** Secure IDOR bị chặn
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/invoice?id=1002
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** HTTP Response
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** HTTP 403 và không có dòng hàng invoice 1002.
- **Kết quả mong đợi:** HTTP 403 và không có dòng hàng invoice 1002.
- **Caption báo cáo:** Secure IDOR bị chặn. HTTP 403 và không có dòng hàng invoice 1002.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 25_invoice_access_denied_log.png

- **Mục đích:** Audit IDOR denied
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /audit-logs
- **Dữ liệu gốc:** id=1001
- **Dữ liệu cần sửa:** id=1002
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Audit Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Event invoice_access_denied cùng trace ID.
- **Kết quả mong đợi:** Event invoice_access_denied cùng trace ID.
- **Caption báo cáo:** Audit IDOR denied. Event invoice_access_denied cùng trace ID.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 26_profile_original_fields.png

- **Mục đích:** Các trường profile vulnerable
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Parameter Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Form có user_id=12, email và role=user.
- **Kết quả mong đợi:** Form có user_id=12, email và role=user.
- **Caption báo cáo:** Các trường profile vulnerable. Form có user_id=12, email và role=user.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 27_profile_role_modified.png

- **Mục đích:** Role bị sửa phía client
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** role=admin
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Parameter Diff
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Parameter Diff đánh dấu role là sensitive field modified.
- **Kết quả mong đợi:** Parameter Diff đánh dấu role là sensitive field modified.
- **Caption báo cáo:** Role bị sửa phía client. Parameter Diff đánh dấu role là sensitive field modified.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 28_profile_tampered_request.png

- **Mục đích:** Request profile bị sửa
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** role=admin
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Request Inspector
- **Bước timeline:** HTTP Request
- **Nội dung bắt buộc:** POST chứa role=admin.
- **Kết quả mong đợi:** POST chứa role=admin.
- **Caption báo cáo:** Request profile bị sửa. POST chứa role=admin.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 29_profile_vulnerable_update.png

- **Mục đích:** Mass assignment đổi database
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** role=admin
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Database Inspector
- **Bước timeline:** Database Write
- **Nội dung bắt buộc:** Role trước user, role sau admin.
- **Kết quả mong đợi:** Role trước user, role sau admin.
- **Caption báo cáo:** Mass assignment đổi database. Role trước user, role sau admin.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 30_profile_privilege_escalation.png

- **Mục đích:** Nâng quyền vulnerable
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /vulnerable/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** role=admin
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Final Security Verdict
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** UI và session hiển thị role admin.
- **Kết quả mong đợi:** UI và session hiển thị role admin.
- **Caption báo cáo:** Nâng quyền vulnerable. UI và session hiển thị role admin.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 31_profile_secure_field_allowlist.png

- **Mục đích:** Secure field allowlist
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** role=admin
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Authorization Inspector
- **Bước timeline:** Input Validation
- **Nội dung bắt buộc:** accepted_fields=email; rejected_fields có role.
- **Kết quả mong đợi:** accepted_fields=email; rejected_fields có role.
- **Caption báo cáo:** Secure field allowlist. accepted_fields=email; rejected_fields có role.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 32_profile_secure_role_unchanged.png

- **Mục đích:** Role secure không đổi
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/profile
- **Dữ liệu gốc:** role=user
- **Dữ liệu cần sửa:** role=admin
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Database Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Database giữ role=user.
- **Kết quả mong đợi:** Database giữ role=user.
- **Caption báo cáo:** Role secure không đổi. Database giữ role=user.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 33_code_comparison_checkout.png

- **Mục đích:** So sánh code checkout
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /comparison
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Code Comparison
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Code chạy thật cho client price và database price.
- **Kết quả mong đợi:** Code chạy thật cho client price và database price.
- **Caption báo cáo:** So sánh code checkout. Code chạy thật cho client price và database price.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 34_code_comparison_idor.png

- **Mục đích:** So sánh code IDOR
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /comparison
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Code Comparison
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Query theo id so với query theo id và owner.
- **Kết quả mong đợi:** Query theo id so với query theo id và owner.
- **Caption báo cáo:** So sánh code IDOR. Query theo id so với query theo id và owner.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 35_code_comparison_role.png

- **Mục đích:** So sánh mass assignment
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /comparison
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Code Comparison
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Submitted role so với allowlist email.
- **Kết quả mong đợi:** Submitted role so với allowlist email.
- **Caption báo cáo:** So sánh mass assignment. Submitted role so với allowlist email.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 36_parameter_tampering_vs_sqli.png

- **Mục đích:** Phân biệt với SQL Injection
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /comparison
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Comparison Table
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Bảng nêu khác mục tiêu, kỹ thuật và bản vá.
- **Kết quả mong đợi:** Bảng nêu khác mục tiêu, kỹ thuật và bản vá.
- **Caption báo cáo:** Phân biệt với SQL Injection. Bảng nêu khác mục tiêu, kỹ thuật và bản vá.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 37_security_controls.png

- **Mục đích:** Các lớp kiểm soát
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /security-controls
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Security Control Panel
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Server price, session identity, authorization, allowlist và audit.
- **Kết quả mong đợi:** Server price, session identity, authorization, allowlist và audit.
- **Caption báo cáo:** Các lớp kiểm soát. Server price, session identity, authorization, allowlist và audit.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 38_audit_logs_overview.png

- **Mục đích:** Audit ba tình huống
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /audit-logs
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Audit Inspector
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Có checkout mismatch, IDOR denied và sensitive field submitted.
- **Kết quả mong đợi:** Có checkout mismatch, IDOR denied và sensitive field submitted.
- **Caption báo cáo:** Audit ba tình huống. Có checkout mismatch, IDOR denied và sensitive field submitted.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 39_presentation_mode.png

- **Mục đích:** Trình chiếu trace
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** user_a
- **URL:** /secure/invoice?id=1002
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Mở trang
- **Panel cần mở:** Presentation Mode
- **Bước timeline:** Authorization
- **Nội dung bắt buộc:** Một bước Authorization ở cỡ chữ lớn và có thanh tiến trình.
- **Kết quả mong đợi:** Một bước Authorization ở cỡ chữ lớn và có thanh tiến trình.
- **Caption báo cáo:** Trình chiếu trace. Một bước Authorization ở cỡ chữ lớn và có thanh tiến trình.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

- **Mục đích:** Kết quả kiểm thử
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** Không áp dụng
- **URL:** Terminal local
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.

## 41_report_files.png

- **Mục đích:** Artifact báo cáo
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** Không áp dụng
- **URL:** Thư mục report
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Chạy scripts/generate_report.py
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** DOCX đúng tên.
- **Kết quả mong đợi:** DOCX đúng tên.
- **Caption báo cáo:** Artifact báo cáo. DOCX đúng tên.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.
### Bằng chứng cũ tùy chọn

- `40_pytest_passed.png`: giữ tên để tương thích manifest cũ; không chạy lại pytest cho nhiệm vụ này. Chỉ dùng nếu ảnh thật đã có từ trước.
