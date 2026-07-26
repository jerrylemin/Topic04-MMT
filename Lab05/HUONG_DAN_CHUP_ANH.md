# HƯỚNG DẪN CHỤP ẢNH THỦ CÔNG - LAB05 SQL INJECTION

## 1. Mục đích tài liệu

Tài liệu giúp sinh viên tự cài môi trường, tự chạy lab, tự thực hiện kịch bản và tự chụp bằng chứng thật. Chỉ thao tác trên localhost của repository; không thử trên website/hệ thống thật, không dùng ảnh dựng, Playwright, Selenium, extension/macro chụp tự động hoặc công cụ chỉnh DOM để giả kết quả. Đóng tab riêng tư, không để lộ cookie/token thật, dữ liệu cá nhân, password, session ID hay chữ ký dài.

## 2. Chuẩn bị môi trường từ đầu

Từ Command Prompt tại thư mục repository, vào `Topic04\Lab05`, rồi chạy `scripts\run_lab.bat`. Script tạo `.venv`, cài requirements, seed `lab05.sqlite3` khi thiếu và chạy `app.py`. Mở `http://127.0.0.1:5005`; dừng bằng `Ctrl+C`. Reset dữ liệu local trước nhóm mới bằng `.venv\Scripts\python scripts\reset_database.py`. Chỉ dùng các input cố định trong `config.py`; không dùng DROP/DELETE/UNION hay payload phá hủy.

### Tài khoản và dữ liệu cố định

`admin_lab` / `AdminLab123!`; `student_a` / `StudentA123!`; `student_b` / `StudentB123!`. Password trong ảnh phải che.

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

### F12-01. `37_login_normal_request.png`

- **Mục tiêu:** Chứng minh login bình thường
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/login`
- **Tài khoản:** admin_lab / AdminLab123!
- **Dữ liệu nhập:** `username=admin_lab; password che`
- **Thao tác/nút:** Submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/login`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** Username nhìn thấy; password che trong ảnh
- **Kết quả mong đợi:** Login local hợp lệ
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request đăng nhập bình thường
- **Mục báo cáo:** F12 / Login / Normal

### F12-02. `38_login_normal_response.png`

- **Mục tiêu:** Ghi response login bình thường
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/login`
- **Tài khoản:** admin_lab
- **Dữ liệu nhập:** `Credential hợp lệ`
- **Thao tác/nút:** Chọn POST
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers/Response
- **Request cần chọn:** `POST /vulnerable/login`
- **Trường cần mở:** Status/Response/Set-Cookie
- **Nội dung bắt buộc:** Redirect/success và session cookie che
- **Kết quả mong đợi:** Ứng dụng xác thực demo
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response đăng nhập bình thường
- **Mục báo cáo:** F12 / Login / Response

### F12-03. `39_login_quote_request.png`

- **Mục tiêu:** Chứng minh input dấu nháy đơn
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/login`
- **Tài khoản:** Không cần tài khoản thật
- **Dữ liệu nhập:** `username='; password giả lập`
- **Thao tác/nút:** Chọn scenario dấu nháy cố định và submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/login`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** Username chỉ là `'`; password che
- **Kết quả mong đợi:** Input tới vulnerable query
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request kiểm tra dấu nháy đơn
- **Mục báo cáo:** F12 / Login / Quote

### F12-04. `40_login_quote_response.png`

- **Mục tiêu:** Ghi lỗi an toàn/hành vi bất thường
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/login`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `username='`
- **Thao tác/nút:** Chọn request
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /vulnerable/login`
- **Trường cần mở:** Status/Response
- **Nội dung bắt buộc:** Thông báo lỗi chung hoặc trace error category; không traceback/DB path
- **Kết quả mong đợi:** Lỗi được xử lý
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response của input dấu nháy
- **Mục báo cáo:** F12 / Login / Quote response

### F12-05. `41_login_bypass_payload.png`

- **Mục tiêu:** Chứng minh authentication logic input cố định
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/login`
- **Tài khoản:** Payload local cố định
- **Dữ liệu nhập:** `username=admin_lab' -- ; password bất kỳ giả lập`
- **Thao tác/nút:** Bấm scenario Authentication Logic
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/login`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** Username đúng chuỗi trong config; không payload khác
- **Kết quả mong đợi:** Comment làm thay đổi logic vulnerable
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload authentication bypass local
- **Mục báo cáo:** F12 / Login / Vulnerable payload

### F12-06. `42_login_bypass_response.png`

- **Mục tiêu:** Chứng minh vulnerable đăng nhập sai logic
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/login`
- **Tài khoản:** admin_lab qua demo local
- **Dữ liệu nhập:** `Payload cố định`
- **Thao tác/nút:** Chọn POST bypass
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /vulnerable/login`
- **Trường cần mở:** Response và status
- **Nội dung bắt buộc:** Response/UI cho thấy session tạo qua `vulnerable_local_demo`
- **Kết quả mong đợi:** Vulnerable chấp nhận không đúng logic password
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response vulnerable authentication bypass
- **Mục báo cáo:** F12 / Login / Vulnerable response

### F12-07. `43_secure_login_same_payload.png`

- **Mục tiêu:** Chứng minh prepared statement giữ logic
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/secure/login`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Cùng username admin_lab' -- `
- **Thao tác/nút:** Submit secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Response
- **Request cần chọn:** `POST /secure/login`
- **Trường cần mở:** Form Data và Response
- **Nội dung bắt buộc:** Input được coi là username literal; response từ chối chung
- **Kết quả mong đợi:** Bản secure không bypass
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Secure login từ chối cùng payload
- **Mục báo cáo:** F12 / Login / Secure

### F12-08. `44_search_normal_request.png`

- **Mục tiêu:** Chứng minh query search bình thường
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/search?keyword=USB`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `keyword=USB`
- **Thao tác/nút:** Tìm kiếm
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/search?keyword=USB`
- **Trường cần mở:** Query String Parameters
- **Nội dung bắt buộc:** keyword=USB
- **Kết quả mong đợi:** Kết quả chỉ tên chứa USB
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request search bình thường
- **Mục báo cáo:** F12 / Search / Normal

### F12-09. `45_search_normal_response.png`

- **Mục tiêu:** Ghi response search bình thường
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/search?keyword=USB`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `USB`
- **Thao tác/nút:** Chọn GET
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `GET /vulnerable/search?keyword=USB`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Danh sách dự kiến chứa USB; status 200
- **Kết quả mong đợi:** Baseline result set
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response search bình thường
- **Mục báo cáo:** F12 / Search / Response

### F12-10. `46_search_expanded_request.png`

- **Mục tiêu:** Chứng minh điều kiện search bị thay đổi
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/search`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `keyword=%' OR 1=1 -- `
- **Thao tác/nút:** Dùng scenario Expanded local search
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/search?keyword=...`
- **Trường cần mở:** Query String Parameters
- **Nội dung bắt buộc:** Keyword fixed được URL encode/decoded đúng
- **Kết quả mong đợi:** Request chỉ đọc database local
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request search thay đổi điều kiện
- **Mục báo cáo:** F12 / Search / Tampered

### F12-11. `47_search_expanded_response.png`

- **Mục tiêu:** Chứng minh result set ngoài dự kiến
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/vulnerable/search`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `Payload expanded cố định`
- **Thao tác/nút:** Chọn GET expanded
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `GET /vulnerable/search?keyword=...`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Nhiều sản phẩm ngoài từ khóa bình thường; không dữ liệu bảng khác
- **Kết quả mong đợi:** Vulnerable logic bị mở rộng
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response vulnerable trả dữ liệu ngoài dự kiến
- **Mục báo cáo:** F12 / Search / Vulnerable response

### F12-12. `48_secure_search_request.png`

- **Mục tiêu:** Chứng minh secure bind cùng input
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/secure/search`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `keyword=%' OR 1=1 -- `
- **Thao tác/nút:** Submit secure search
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /secure/search?keyword=...`
- **Trường cần mở:** Query String Parameters
- **Nội dung bắt buộc:** Cùng keyword tới route secure
- **Kết quả mong đợi:** Dữ liệu tách khỏi cấu trúc SQL
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Request secure search cùng input
- **Mục báo cáo:** F12 / Search / Secure request

### F12-13. `49_secure_search_response.png`

- **Mục tiêu:** Chứng minh secure không đổi logic query
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/secure/search`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `Payload expanded cố định`
- **Thao tác/nút:** Chọn request secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `GET /secure/search?keyword=...`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Không mở rộng toàn bộ product; prepared=true/placeholder nếu UI trace hiện
- **Kết quả mong đợi:** Prepared statement hiệu quả
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure không mở rộng kết quả
- **Mục báo cáo:** F12 / Search / Secure response

### F12-14. `50_login_cookie_masked.png`

- **Mục tiêu:** Chứng minh session sau login nhưng không lộ token
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5005/dashboard`
- **Tài khoản:** admin_lab
- **Dữ liệu nhập:** `Login hợp lệ`
- **Thao tác/nút:** Reload dashboard
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Application Cookies; Network Headers
- **Request cần chọn:** `GET /dashboard`
- **Trường cần mở:** Cookie name/flags và Request Header
- **Nội dung bắt buộc:** `lab05_session` hiện diện; Value che; HttpOnly/SameSite phản ánh config
- **Kết quả mong đợi:** Session được tạo mà không lộ secret
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Cookie phiên Lab05 đã che
- **Mục báo cáo:** F12 / Session

## 5. Bảng mô tả ảnh F12

| STT | Tên file | Mục tiêu | Chuẩn bị | URL/lệnh | Dữ liệu và thao tác | F12 cần mở | Nội dung bắt buộc | Kết quả | Caption | Mục báo cáo |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `37_login_normal_request.png` | Chứng minh login bình thường | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/login` | username=admin_lab; password che; Submit | Network > Payload; Form Data | Username nhìn thấy; password che trong ảnh | Login local hợp lệ | Request đăng nhập bình thường | F12 / Login / Normal |
| 2 | `38_login_normal_response.png` | Ghi response login bình thường | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/login` | Credential hợp lệ; Chọn POST | Network > Headers/Response; Status/Response/Set-Cookie | Redirect/success và session cookie che | Ứng dụng xác thực demo | Response đăng nhập bình thường | F12 / Login / Response |
| 3 | `39_login_quote_request.png` | Chứng minh input dấu nháy đơn | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/login` | username='; password giả lập; Chọn scenario dấu nháy cố định và submit | Network > Payload; Form Data | Username chỉ là `'`; password che | Input tới vulnerable query | Request kiểm tra dấu nháy đơn | F12 / Login / Quote |
| 4 | `40_login_quote_response.png` | Ghi lỗi an toàn/hành vi bất thường | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/login` | username='; Chọn request | Network > Response/Preview; Status/Response | Thông báo lỗi chung hoặc trace error category; không traceback/DB path | Lỗi được xử lý | Response của input dấu nháy | F12 / Login / Quote response |
| 5 | `41_login_bypass_payload.png` | Chứng minh authentication logic input cố định | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/login` | username=admin_lab' -- ; password bất kỳ giả lập; Bấm scenario Authentication Logic | Network > Payload; Form Data | Username đúng chuỗi trong config; không payload khác | Comment làm thay đổi logic vulnerable | Payload authentication bypass local | F12 / Login / Vulnerable payload |
| 6 | `42_login_bypass_response.png` | Chứng minh vulnerable đăng nhập sai logic | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/login` | Payload cố định; Chọn POST bypass | Network > Response/Preview; Response và status | Response/UI cho thấy session tạo qua `vulnerable_local_demo` | Vulnerable chấp nhận không đúng logic password | Response vulnerable authentication bypass | F12 / Login / Vulnerable response |
| 7 | `43_secure_login_same_payload.png` | Chứng minh prepared statement giữ logic | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/secure/login` | Cùng username admin_lab' -- ; Submit secure | Network > Payload/Response; Form Data và Response | Input được coi là username literal; response từ chối chung | Bản secure không bypass | Secure login từ chối cùng payload | F12 / Login / Secure |
| 8 | `44_search_normal_request.png` | Chứng minh query search bình thường | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/search?keyword=USB` | keyword=USB; Tìm kiếm | Network > Headers; Query String Parameters | keyword=USB | Kết quả chỉ tên chứa USB | Request search bình thường | F12 / Search / Normal |
| 9 | `45_search_normal_response.png` | Ghi response search bình thường | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/search?keyword=USB` | USB; Chọn GET | Network > Response/Preview; Response | Danh sách dự kiến chứa USB; status 200 | Baseline result set | Response search bình thường | F12 / Search / Response |
| 10 | `46_search_expanded_request.png` | Chứng minh điều kiện search bị thay đổi | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/search` | keyword=%' OR 1=1 -- ; Dùng scenario Expanded local search | Network > Headers; Query String Parameters | Keyword fixed được URL encode/decoded đúng | Request chỉ đọc database local | Request search thay đổi điều kiện | F12 / Search / Tampered |
| 11 | `47_search_expanded_response.png` | Chứng minh result set ngoài dự kiến | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/vulnerable/search` | Payload expanded cố định; Chọn GET expanded | Network > Response/Preview; Response | Nhiều sản phẩm ngoài từ khóa bình thường; không dữ liệu bảng khác | Vulnerable logic bị mở rộng | Response vulnerable trả dữ liệu ngoài dự kiến | F12 / Search / Vulnerable response |
| 12 | `48_secure_search_request.png` | Chứng minh secure bind cùng input | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/secure/search` | keyword=%' OR 1=1 -- ; Submit secure search | Network > Headers; Query String Parameters | Cùng keyword tới route secure | Dữ liệu tách khỏi cấu trúc SQL | Request secure search cùng input | F12 / Search / Secure request |
| 13 | `49_secure_search_response.png` | Chứng minh secure không đổi logic query | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/secure/search` | Payload expanded cố định; Chọn request secure | Network > Response/Preview; Response | Không mở rộng toàn bộ product; prepared=true/placeholder nếu UI trace hiện | Prepared statement hiệu quả | Response secure không mở rộng kết quả | F12 / Search / Secure response |
| 14 | `50_login_cookie_masked.png` | Chứng minh session sau login nhưng không lộ token | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5005/dashboard` | Login hợp lệ; Reload dashboard | Application Cookies; Network Headers; Cookie name/flags và Request Header | `lab05_session` hiện diện; Value che; HttpOnly/SameSite phản ánh config | Session được tạo mà không lộ secret | Cookie phiên Lab05 đã che | F12 / Session |

## 6. Xử lý lỗi thường gặp

- **Port 5005 bị chiếm:** dừng server lab cũ bằng `Ctrl+C`; dùng `Get-NetTCPConnection -LocalPort 5005 -ErrorAction SilentlyContinue` để xác định tiến trình, không tự đổi port tài liệu.
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

Ảnh được chụp **thủ công**, lưu đúng tên trong `evidence/screenshots/`. Trước khi chụp, chạy app tại `http://127.0.0.1:5005`, đặt zoom trình duyệt 100%, mở rộng cửa sổ tối thiểu 1280×720 và reset lab khi hướng dẫn yêu cầu. Không dùng công cụ tự động điều khiển trình duyệt, không tạo ảnh giả. Ảnh terminal chỉ chụp kết quả lệnh đã chạy thật.

## 01_home_overview.png

**Tên file:** `01_home_overview.png` · **Mục đích:** Tổng quan phạm vi LAB 5. · **URL:** `/` · **Điều kiện ban đầu:** App đang chạy, chưa cần đăng nhập. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Mở trang chủ. · **Inspector cần mở:** Không. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Tiêu đề LAB 5, bốn phần học tập và nhãn local-only. · **Kết quả mong đợi:** Thấy rõ vulnerable/secure và địa chỉ 127.0.0.1:5005. · **Caption báo cáo:** Tổng quan ứng dụng học tập SQL Injection trong phạm vi local. · **Lỗi thường gặp:** Chụp thiếu scope card. · **Cách làm lại:** Cuộn lên đầu trang và chụp toàn bộ hero.

## 02_database_seed.png

**Tên file:** `02_database_seed.png` · **Mục đích:** Xác nhận dữ liệu giả lập đã seed. · **URL:** `/dashboard` · **Điều kiện ban đầu:** Bấm Reset dữ liệu lab một lần. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Reset dữ liệu lab. · **Inspector cần mở:** Database Inspector nếu dashboard có trace reset. · **Timeline step cần chọn:** Final Result. · **Nội dung bắt buộc:** 3 users, ít nhất 8 products và trạng thái local database. · **Kết quả mong đợi:** Seed hoàn tất, không có dữ liệu thật. · **Caption báo cáo:** Database SQLite local sau khi seed dữ liệu giả lập. · **Lỗi thường gặp:** Số liệu cũ do chưa reset. · **Cách làm lại:** Reset, xác nhận POST hoàn tất rồi tải lại dashboard.

## 03_vulnerable_login_normal.png

**Tên file:** `03_vulnerable_login_normal.png` · **Mục đích:** Login legacy với input hợp lệ. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Reset lab và chưa đăng nhập. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Dữ liệu bình thường, rồi Chạy vulnerable login. · **Inspector cần mở:** Final Security Verdict. · **Timeline step cần chọn:** Final verdict. · **Nội dung bắt buộc:** Decision authenticated và mode vulnerable. · **Kết quả mong đợi:** Session demo được tạo từ tài khoản hợp lệ. · **Caption báo cáo:** Vulnerable login bình thường trong database local. · **Lỗi thường gặp:** Session cũ còn tồn tại. · **Cách làm lại:** Đăng xuất, reset và chạy lại đúng tài khoản.

## 04_vulnerable_login_request.png

**Tên file:** `04_vulnerable_login_request.png` · **Mục đích:** Quan sát request login thật đã che password. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Vừa chạy normal vulnerable login. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Mở Request. · **Inspector cần mở:** Request Inspector. · **Timeline step cần chọn:** HTTP Request. · **Nội dung bắt buộc:** POST, path, form field names; password chỉ hiện metadata/giá trị che. · **Kết quả mong đợi:** Không thấy plaintext password. · **Caption báo cáo:** Request Inspector của vulnerable login với trường nhạy cảm đã che. · **Lỗi thường gặp:** Chụp form trước khi submit. · **Cách làm lại:** Submit lại rồi mở tab Request trong trace mới.

## 05_vulnerable_login_query.png

**Tên file:** `05_vulnerable_login_query.png` · **Mục đích:** Chứng minh phương thức nối chuỗi. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Có trace normal vulnerable login. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** Construction type, query template và final query masked. · **Kết quả mong đợi:** Thấy string concatenation, chưa dùng placeholder. · **Caption báo cáo:** Query vulnerable được tạo bằng nối chuỗi. · **Lỗi thường gặp:** Mở nhầm trace secure. · **Cách làm lại:** Kiểm tra badge vulnerable và chạy lại flow.

## 06_quote_login_input.png

**Tên file:** `06_quote_login_input.png` · **Mục đích:** Phát hiện ký tự đơn giản có nguy cơ. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Đăng xuất khỏi session trước. · **Dữ liệu cần nhập:** Username `'`, password `x`. · **Nút cần bấm:** Ký tự dấu nháy đơn, rồi Chạy vulnerable login. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Input Validation. · **Nội dung bắt buộc:** Raw input, độ dài và quote_detected=true. · **Kết quả mong đợi:** Scenario cố định được nhận diện. · **Caption báo cáo:** Input Inspector phát hiện dấu nháy đơn trong login. · **Lỗi thường gặp:** Gõ dấu nháy kiểu cong. · **Cách làm lại:** Dùng đúng nút scenario cố định.

## 07_quote_login_error.png

**Tên file:** `07_quote_login_error.png` · **Mục đích:** Quan sát lỗi query có kiểm soát. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Vừa submit quote login. · **Dữ liệu cần nhập:** Username `'`, password `x`. · **Nút cần bấm:** Mở tab Error. · **Inspector cần mở:** Error Inspector. · **Timeline step cần chọn:** Error Handling. · **Nội dung bắt buộc:** Category `sql_syntax_error`, handled status, không có traceback/absolute path. · **Kết quả mong đợi:** Diagnostic local đã che thông tin nhạy cảm. · **Caption báo cáo:** Quote input tạo lỗi cú pháp được phân loại an toàn. · **Lỗi thường gặp:** Chụp trang lỗi Flask debug. · **Cách làm lại:** Tắt debug, chạy lại app và scenario.

## 08_auth_logic_input.png

**Tên file:** `08_auth_logic_input.png` · **Mục đích:** Ghi nhận scenario authentication logic cố định. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Đã đăng xuất. · **Dữ liệu cần nhập:** Dùng nút Điều kiện đăng nhập local; password `wrong`. · **Nút cần bấm:** Điều kiện đăng nhập local, rồi submit. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Browser UI. · **Nội dung bắt buộc:** Boolean expression và comment marker của scenario cố định được nhận diện. · **Kết quả mong đợi:** Input category là local auth logic demo. · **Caption báo cáo:** Input cố định dùng minh họa authentication logic trong local lab. · **Lỗi thường gặp:** Tự sửa chuỗi scenario. · **Cách làm lại:** Reset form và dùng đúng nút được cung cấp.

## 09_auth_query_changed.png

**Tên file:** `09_auth_query_changed.png` · **Mục đích:** Cho thấy cấu trúc WHERE bị thay đổi. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Có trace auth logic vulnerable. · **Dữ liệu cần nhập:** Scenario Điều kiện đăng nhập local. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** SQLite Parser. · **Nội dung bắt buộc:** Final query masked và `sql_structure_changed=true`. · **Kết quả mong đợi:** Visualizer đánh dấu String Concatenation/Unexpected Result. · **Caption báo cáo:** Nối chuỗi làm thay đổi cấu trúc điều kiện xác thực. · **Lỗi thường gặp:** Chọn trace quote error. · **Cách làm lại:** Chạy đúng nút auth logic rồi mở trace mới nhất.

## 10_auth_decision_vulnerable.png

**Tên file:** `10_auth_decision_vulnerable.png` · **Mục đích:** Quan sát quyết định xác thực sai. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Auth logic scenario đã trả result set. · **Dữ liệu cần nhập:** Scenario auth logic, password `wrong`. · **Nút cần bấm:** Tab Authentication. · **Inspector cần mở:** Authentication Decision Inspector. · **Timeline step cần chọn:** Authentication Decision. · **Nội dung bắt buộc:** Decision local_demo_bypass, password không hợp lệ và authentication_bypassed=true. · **Kết quả mong đợi:** Server chọn user do WHERE đã đổi. · **Caption báo cáo:** Authentication decision vulnerable chấp nhận sai trong demo local. · **Lỗi thường gặp:** Password đúng làm mất ý nghĩa. · **Cách làm lại:** Đăng xuất và dùng password `wrong`.

## 11_auth_session_created.png

**Tên file:** `11_auth_session_created.png` · **Mục đích:** Chứng minh state change của bypass demo. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Auth logic vulnerable vừa hoàn tất. · **Dữ liệu cần nhập:** Scenario auth logic, password `wrong`. · **Nút cần bấm:** Mở Verdict. · **Inspector cần mở:** Final Security Verdict. · **Timeline step cần chọn:** Session Management. · **Nội dung bắt buộc:** `session_created=true` và `authenticated_via=vulnerable_local_demo`. · **Kết quả mong đợi:** UI cảnh báo session chỉ để minh họa. · **Caption báo cáo:** Session demo được tạo sau quyết định vulnerable. · **Lỗi thường gặp:** Đã mở trace khác sau đó. · **Cách làm lại:** Đăng xuất và chạy lại duy nhất scenario này.

## 12_secure_login_same_input.png

**Tên file:** `12_secure_login_same_input.png` · **Mục đích:** Dùng cùng input trên bản secure. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Đăng xuất khỏi vulnerable session. · **Dữ liệu cần nhập:** Nút Cùng input logic, password `wrong`. · **Nút cần bấm:** Cùng input logic, rồi Chạy secure login. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Input Validation. · **Nội dung bắt buộc:** Cùng raw input như ảnh 08, mode secure. · **Kết quả mong đợi:** Request được xử lý như dữ liệu, không chạy logic ngoài scenario. · **Caption báo cáo:** Cùng input authentication logic đi qua secure route. · **Lỗi thường gặp:** Chưa đăng xuất session vulnerable. · **Cách làm lại:** POST logout rồi submit lại secure flow.

## 13_secure_login_parameter_binding.png

**Tên file:** `13_secure_login_parameter_binding.png` · **Mục đích:** Chứng minh parameterized query. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Có trace secure same-input. · **Dữ liệu cần nhập:** Scenario Cùng input logic. · **Nút cần bấm:** Tab Parameters. · **Inspector cần mở:** Parameter Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** `WHERE username = ?`, parameter count và bound_by_driver=true. · **Kết quả mong đợi:** SQL structure preserved=true. · **Caption báo cáo:** Secure login bind username vào placeholder. · **Lỗi thường gặp:** Chụp Query tab nhưng thiếu parameter. · **Cách làm lại:** Mở riêng tab Parameters và chọn step binding.

## 14_secure_login_rejected.png

**Tên file:** `14_secure_login_rejected.png` · **Mục đích:** Xác nhận secure route từ chối cùng input. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Secure same-input đã chạy. · **Dữ liệu cần nhập:** Scenario auth logic, password `wrong`. · **Nút cần bấm:** Tab Authentication hoặc Verdict. · **Inspector cần mở:** Authentication Decision Inspector. · **Timeline step cần chọn:** Final Result. · **Nội dung bắt buộc:** Decision rejected, session_created=false và generic message. · **Kết quả mong đợi:** Không xác thực, không tiết lộ username tồn tại. · **Caption báo cáo:** Secure login từ chối input từng đổi logic ở bản vulnerable. · **Lỗi thường gặp:** Session cũ làm header vẫn hiện user. · **Cách làm lại:** Đăng xuất, reset và chạy secure flow trước.

## 15_secure_login_normal_success.png

**Tên file:** `15_secure_login_normal_success.png` · **Mục đích:** Xác nhận bản secure vẫn hỗ trợ login hợp lệ. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Chưa đăng nhập. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Dữ liệu bình thường, rồi Chạy secure login. · **Inspector cần mở:** Authentication Decision Inspector. · **Timeline step cần chọn:** Password Processing. · **Nội dung bắt buộc:** `check_password_hash`, authenticated, `authenticated_via=secure_pbkdf2`. · **Kết quả mong đợi:** Login thành công và session rotate. · **Caption báo cáo:** Secure normal login với PBKDF2 thành công. · **Lỗi thường gặp:** Nhập sai chữ hoa/thường password. · **Cách làm lại:** Đăng xuất và dùng nút tài khoản demo.

## 16_vulnerable_search_normal.png

**Tên file:** `16_vulnerable_search_normal.png` · **Mục đích:** Baseline tìm kiếm vulnerable. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Database đã reset. · **Dữ liệu cần nhập:** `USB`. · **Nút cần bấm:** Dữ liệu bình thường, rồi Chạy vulnerable search. · **Inspector cần mở:** Result Set Inspector. · **Timeline step cần chọn:** Result Set. · **Nội dung bắt buộc:** Các sản phẩm có USB và số rows baseline. · **Kết quả mong đợi:** Chỉ kết quả phù hợp từ products. · **Caption báo cáo:** Kết quả tìm kiếm bình thường ở vulnerable mode. · **Lỗi thường gặp:** Dùng từ khóa khác làm sai baseline. · **Cách làm lại:** Xóa ô và dùng nút USB.

## 17_vulnerable_search_query.png

**Tên file:** `17_vulnerable_search_query.png` · **Mục đích:** Quan sát keyword nối vào LIKE. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Có trace normal vulnerable search. · **Dữ liệu cần nhập:** `USB`. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** Final SQL masked và construction type concatenation. · **Kết quả mong đợi:** Keyword nằm trong SQL text, chưa dùng placeholder. · **Caption báo cáo:** Vulnerable search ghép keyword trực tiếp vào LIKE. · **Lỗi thường gặp:** Chụp trang secure search. · **Cách làm lại:** Kiểm tra badge vulnerable rồi chạy lại.

## 18_quote_search_error.png

**Tên file:** `18_quote_search_error.png` · **Mục đích:** Phát hiện lỗi search bằng dấu nháy đơn. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Database bình thường. · **Dữ liệu cần nhập:** `'`. · **Nút cần bấm:** Ký tự dấu nháy đơn, rồi submit. · **Inspector cần mở:** Error Inspector. · **Timeline step cần chọn:** Error Handling. · **Nội dung bắt buộc:** sql_syntax_error, rows_changed=0, không traceback. · **Kết quả mong đợi:** Lỗi được ghi audit và UI vẫn an toàn. · **Caption báo cáo:** Quote search tạo lỗi cú pháp trong query nối chuỗi. · **Lỗi thường gặp:** Chụp thông báo trình duyệt thay vì inspector. · **Cách làm lại:** Mở tab Error của trace mới nhất.

## 19_expanded_search_input.png

**Tên file:** `19_expanded_search_input.png` · **Mục đích:** Ghi nhận scenario mở rộng kết quả cố định. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Reset database nếu cần. · **Dữ liệu cần nhập:** Dùng nút Mở rộng kết quả local. · **Nút cần bấm:** Mở rộng kết quả local, rồi submit. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Browser UI. · **Nội dung bắt buộc:** Input category fixed expanded search; trust level untrusted. · **Kết quả mong đợi:** Scenario chỉ nhắm products local. · **Caption báo cáo:** Input cố định minh họa thay đổi điều kiện tìm kiếm. · **Lỗi thường gặp:** Tự tạo payload khác. · **Cách làm lại:** Dùng nút scenario, không sửa chuỗi.

## 20_expanded_search_query.png

**Tên file:** `20_expanded_search_query.png` · **Mục đích:** Cho thấy điều kiện search bị thay đổi. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Có trace expanded vulnerable search. · **Dữ liệu cần nhập:** Scenario mở rộng local. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** SQLite Parser. · **Nội dung bắt buộc:** sql_structure_changed=true, final query masked và visualizer vulnerable. · **Kết quả mong đợi:** SQLite parse điều kiện rộng hơn dự kiến. · **Caption báo cáo:** Cấu trúc LIKE bị thay đổi bởi phép nối chuỗi. · **Lỗi thường gặp:** Chọn quote-error trace. · **Cách làm lại:** Submit scenario expanded rồi mở trace mới.

## 21_expanded_search_results.png

**Tên file:** `21_expanded_search_results.png` · **Mục đích:** Chứng minh result set ngoài điều kiện mong muốn. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Expanded search đã chạy. · **Dữ liệu cần nhập:** Scenario mở rộng local. · **Nút cần bấm:** Tab Result Set. · **Inspector cần mở:** Result Set Inspector. · **Timeline step cần chọn:** Result Set. · **Nội dung bắt buộc:** Actual rows lớn hơn baseline, table=products, database_modified=false. · **Kết quả mong đợi:** Chỉ sản phẩm local được trả về; không đọc users. · **Caption báo cáo:** Vulnerable search trả thêm rows trong bảng products. · **Lỗi thường gặp:** Kết quả không lớn hơn do dùng sai input. · **Cách làm lại:** Reset và dùng nút expanded chính xác.

## 22_secure_search_same_input.png

**Tên file:** `22_secure_search_same_input.png` · **Mục đích:** Đối chiếu cùng input qua secure search. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Đã ghi nhận expanded vulnerable baseline. · **Dữ liệu cần nhập:** Nút Cùng input mở rộng. · **Nút cần bấm:** Cùng input mở rộng, rồi Chạy secure search. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Input Validation. · **Nội dung bắt buộc:** Cùng raw input, mode secure, validation pass. · **Kết quả mong đợi:** Input được coi là literal search value. · **Caption báo cáo:** Cùng input mở rộng được xử lý ở secure route. · **Lỗi thường gặp:** Nhập khác chuỗi vulnerable. · **Cách làm lại:** Dùng nút cố định ở secure search.

## 23_secure_search_binding.png

**Tên file:** `23_secure_search_binding.png` · **Mục đích:** Chứng minh `LIKE ?` và parameter tuple. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Có trace secure same-input. · **Dữ liệu cần nhập:** Cùng input mở rộng. · **Nút cần bấm:** Tab Parameters. · **Inspector cần mở:** Parameter Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** Template có `LIKE ?`, parameter masked, bound_by_driver=true. · **Kết quả mong đợi:** sql_structure_preserved=true. · **Caption báo cáo:** Secure search bind `%keyword%` qua SQLite driver. · **Lỗi thường gặp:** Chụp final query nhưng thiếu placeholder. · **Cách làm lại:** Mở Parameter Inspector và chọn step binding.

## 24_secure_search_expected_results.png

**Tên file:** `24_secure_search_expected_results.png` · **Mục đích:** Xác nhận secure result set đúng điều kiện. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Secure same-input đã chạy. · **Dữ liệu cần nhập:** Cùng input mở rộng. · **Nút cần bấm:** Tab Result Set. · **Inspector cần mở:** Result Set Inspector. · **Timeline step cần chọn:** Final Result. · **Nội dung bắt buộc:** Unexpected rows=false, limit=50, actual rows theo literal input. · **Kết quả mong đợi:** Không mở rộng toàn bộ products. · **Caption báo cáo:** Parameter binding giữ kết quả search đúng ý nghĩa. · **Lỗi thường gặp:** Chụp normal `USB` thay vì same-input. · **Cách làm lại:** Dùng lại nút Cùng input mở rộng.

## 25_query_visualizer.png

**Tên file:** `25_query_visualizer.png` · **Mục đích:** So sánh data flow vulnerable/secure. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Có trace secure search. · **Dữ liệu cần nhập:** `USB`. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** Parameter Binding. · **Nội dung bắt buộc:** User Input → Python Value → SQL Template → Binding → SQLite Parser → Expected Result. · **Kết quả mong đợi:** Sơ đồ có placeholder và structure preserved. · **Caption báo cáo:** Query visualizer của secure parameter binding. · **Lỗi thường gặp:** Sơ đồ nằm dưới fold. · **Cách làm lại:** Cuộn trong Query Inspector đến toàn bộ flow.

## 26_code_comparison_login.png

**Tên file:** `26_code_comparison_login.png` · **Mục đích:** So sánh source login thật. · **URL:** `/comparison#login-code` · **Điều kiện ban đầu:** Source backend đã có line markers. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Login trong subnav. · **Inspector cần mở:** Code Comparison. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** File/function/line range, nối chuỗi đối chiếu placeholder + check_password_hash. · **Kết quả mong đợi:** Hai cột source thật hiển thị đầy đủ. · **Caption báo cáo:** So sánh code vulnerable và secure login. · **Lỗi thường gặp:** Source excerpt chưa được backend cung cấp. · **Cách làm lại:** Chạy lại app sau khi source hoàn tất rồi tải trang.

## 27_code_comparison_search.png

**Tên file:** `27_code_comparison_search.png` · **Mục đích:** So sánh source search thật. · **URL:** `/comparison#search-code` · **Điều kiện ban đầu:** Trang comparison đã tải. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Search trong subnav. · **Inspector cần mở:** Code Comparison. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Keyword nối LIKE đối chiếu `LIKE ?` và parameter tuple. · **Kết quả mong đợi:** Line reference khớp source. · **Caption báo cáo:** So sánh code vulnerable và secure product search. · **Lỗi thường gặp:** Chụp nhầm section login. · **Cách làm lại:** Dùng anchor Search và kiểm tra heading.

## 28_error_comparison.png

**Tên file:** `28_error_comparison.png` · **Mục đích:** So sánh xử lý error. · **URL:** `/comparison#error-code` · **Điều kiện ban đầu:** Trang comparison đã tải. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Error handling trong subnav. · **Inspector cần mở:** Code Comparison. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Vulnerable diagnostic local đối chiếu generic message + internal error ID. · **Kết quả mong đợi:** Không cột nào chứa traceback/path tuyệt đối. · **Caption báo cáo:** So sánh error handling trước và sau vá. · **Lỗi thường gặp:** Source excerpt trống. · **Cách làm lại:** Tải lại sau khi backend hoàn tất comparison data.

## 29_password_hashing.png

**Tên file:** `29_password_hashing.png` · **Mục đích:** Giải thích lưu trữ mật khẩu. · **URL:** `/comparison#storage` · **Điều kiện ban đầu:** Database đã seed. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Password storage. · **Inspector cần mở:** Database Inspector nếu có trace secure login. · **Timeline step cần chọn:** Password Processing. · **Nội dung bắt buộc:** Legacy SHA-256 unsalted đối chiếu PBKDF2-SHA256 600000 + unique salt; không full hash. · **Kết quả mong đợi:** Secure route chỉ dùng PBKDF2/check_password_hash. · **Caption báo cáo:** Password hashing legacy và PBKDF2 trong LAB 5. · **Lỗi thường gặp:** Chụp lộ full hash trong terminal. · **Cách làm lại:** Chỉ chụp UI metadata/fingerprint ngắn.

## 30_security_controls.png

**Tên file:** `30_security_controls.png` · **Mục đích:** Tổng hợp defense in depth runtime. · **URL:** `/security-controls` · **Điều kiện ban đầu:** App chạy với config cuối. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Kiểm soát trên nav. · **Inspector cần mở:** Security Control Panel. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Prepared statement, PBKDF2, validation, limit, session, CSP, audit, least privilege và WAF limitation. · **Kết quả mong đợi:** Mỗi control có status/source/route/risk/limit. · **Caption báo cáo:** Security controls phản ánh cấu hình runtime thật. · **Lỗi thường gặp:** Chụp thiếu cột do cửa sổ hẹp. · **Cách làm lại:** Mở rộng cửa sổ hoặc cuộn ngang và ghép trong báo cáo thủ công nếu cần.

## 31_audit_logs.png

**Tên file:** `31_audit_logs.png` · **Mục đích:** Chứng minh logging và monitoring. · **URL:** `/audit-logs` · **Điều kiện ban đầu:** Đã chạy normal, quote, auth logic và expanded search. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Audit trên nav. · **Inspector cần mở:** Bảng Audit Logs. · **Timeline step cần chọn:** Audit Logging nếu mở trace. · **Nội dung bắt buộc:** Action, route, decision, error category, result count và trace ID. · **Kết quả mong đợi:** Không chứa password, cookie hoặc full hash. · **Caption báo cáo:** Audit events đã che dữ liệu nhạy cảm từ các flow thật. · **Lỗi thường gặp:** Bảng trống vì chưa chạy demo flows. · **Cách làm lại:** Chạy các scenario yêu cầu rồi tải lại audit log.

## 32_trace_timeline.png

**Tên file:** `32_trace_timeline.png` · **Mục đích:** Trình bày Action Timeline chi tiết. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Có trace auth logic vulnerable. · **Dữ liệu cần nhập:** Scenario auth logic. · **Nút cần bấm:** Chọn một timeline summary. · **Inspector cần mở:** Timeline. · **Timeline step cần chọn:** Query Construction hoặc Authentication Decision. · **Nội dung bắt buộc:** Step number, timestamp, layer, technique, input/output, code reference, security meaning, status. · **Kết quả mong đợi:** Step mở rộng và progress phản ánh vị trí. · **Caption báo cáo:** Action Timeline từ request đến final verdict. · **Lỗi thường gặp:** Step đang đóng. · **Cách làm lại:** Bấm đúng step để mở chi tiết trước khi chụp.

## 33_presentation_mode.png

**Tên file:** `33_presentation_mode.png` · **Mục đích:** Minh họa chế độ trình chiếu trace hiện có. · **URL:** Trang kết quả có trace. · **Điều kiện ban đầu:** Trace có nhiều steps. · **Dữ liệu cần nhập:** Không thêm input. · **Nút cần bấm:** Presentation Mode, rồi bước sau nếu cần. · **Inspector cần mở:** Timeline. · **Timeline step cần chọn:** Authentication Decision hoặc Result Set. · **Nội dung bắt buộc:** Một step cỡ chữ lớn, progress, nút trước/sau, Auto Play và Chạy lại trace. · **Kết quả mong đợi:** Điều khiển chỉ đổi step, không gửi request. · **Caption báo cáo:** Presentation Mode trình bày một bước của trace thật. · **Lỗi thường gặp:** Nhấn Escape làm thoát trước khi chụp. · **Cách làm lại:** Bật lại mode và chọn step bằng phím mũi tên.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

## 36_report_files.png

**Tên file:** `36_report_files.png` · **Mục đích:** Xác nhận artifact báo cáo. · **URL:** Thư mục `Lab05/report/`. · **Điều kiện ban đầu:** `scripts/generate_report.py` đã chạy thành công. · **Dữ liệu cần nhập:** Lệnh `python scripts/generate_report.py`. · **Nút cần bấm:** Mở thư mục report sau khi script kết thúc. · **Inspector cần mở:** Không. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** `21127645_LeMinh_21127224_NguyenVuBach_Lab05_SQLInjection.docx`, kích thước file khác 0. · **Kết quả mong đợi:** Artifact DOCX đúng tên và mở được. · **Caption báo cáo:** DOCX hoàn chỉnh của LAB 5. · **Lỗi thường gặp:** DOCX chưa tạo nhưng vẫn chụp tên placeholder. · **Cách làm lại:** Đọc lỗi script, sửa nguyên nhân, tạo lại và mở kiểm tra thật.

## Kiểm tra bộ ảnh

Sau khi chụp đủ ảnh, chạy:

```text
python scripts/check_screenshots.py
```

Checker chỉ kiểm tra tên, PNG signature/IHDR, file rỗng, kích thước, ảnh thiếu/thừa và hash trùng. Checker không dùng OCR, không phân tích nội dung và không tạo ảnh.
### Bằng chứng cũ tùy chọn

- `34_pytest_passed.png` và `35_coverage.png`: giữ tên để tương thích manifest cũ; không chạy lại pytest/coverage cho nhiệm vụ này. Chỉ dùng nếu ảnh thật đã có từ trước.
