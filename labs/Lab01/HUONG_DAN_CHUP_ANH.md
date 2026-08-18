# HƯỚNG DẪN CHỤP ẢNH THỦ CÔNG - LAB01 XSS

## 1. Mục đích tài liệu

Tài liệu giúp sinh viên tự cài môi trường, tự chạy lab, tự thực hiện kịch bản và tự chụp bằng chứng thật. Chỉ thao tác trên localhost của repository; không thử trên website/hệ thống thật, không dùng ảnh dựng, Playwright, Selenium, extension/macro chụp tự động hoặc công cụ chỉnh DOM để giả kết quả. Đóng tab riêng tư, không để lộ cookie/token thật, dữ liệu cá nhân, password, session ID hay chữ ký dài.

## 2. Chuẩn bị môi trường từ đầu

Mở Command Prompt và chạy:

```bat
cd /d <thu-muc-repository>\Topic04
cd Lab01
python --version
scripts\run_lab.bat
```

Script tạo `.venv`, cài `requirements.txt`, seed `lab01.db` nếu thiếu và chạy `app.py`. Cách trực tiếp: `.venv\Scripts\python app.py`. Khi terminal hiển thị Flask tại `http://127.0.0.1:5000`, mở URL đó; dừng bằng `Ctrl+C`. Reset khi cần: `.venv\Scripts\python scripts\reset_database.py`.

### Tài khoản và dữ liệu cố định

Không cần đăng nhập. Dùng tên bình luận `Kiểm thử`; cookie profile chỉ là dữ liệu giả lập local.

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

### F12-01. `29_reflected_network_request.png`

- **Mục tiêu:** Chứng minh GET Reflected XSS thật
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `<img src=x onerror="alert('Reflected XSS')">`
- **Thao tác/nút:** Nhập payload và bấm Tìm kiếm
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/search?q=...`
- **Trường cần mở:** General và Query String Parameters
- **Nội dung bắt buộc:** Request URL local, method GET, status và q đã percent-encode
- **Kết quả mong đợi:** Request được gửi tới bản vulnerable
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Reflected XSS - request GET trong Network
- **Mục báo cáo:** F12 / Reflected / Request

### F12-02. `30_reflected_query_parameters.png`

- **Mục tiêu:** Đối chiếu payload URL-encoded và giá trị decoded
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `<img src=x onerror="alert('Reflected XSS')">`
- **Thao tác/nút:** Chọn lại request tìm kiếm
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload hoặc Headers
- **Request cần chọn:** `GET /vulnerable/search?q=...`
- **Trường cần mở:** Query String Parameters
- **Nội dung bắt buộc:** q hiển thị payload decoded; Request URL có `%3C`, `%3E` hoặc encoding tương đương
- **Kết quả mong đợi:** DevTools phân biệt URL encoding với nội dung q
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Query String Parameters của payload Reflected XSS
- **Mục báo cáo:** F12 / Reflected / Payload

### F12-03. `31_reflected_response_html.png`

- **Mục tiêu:** Chứng minh response phản chiếu payload vào HTML
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload Reflected an toàn của lab`
- **Thao tác/nút:** Mở Response của request
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response
- **Request cần chọn:** `GET /vulnerable/search?q=...`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** HTML vùng `Kết quả cho` chứa thẻ img/onerror chưa encode
- **Kết quả mong đợi:** Response vulnerable chứa sink HTML
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response HTML phản chiếu payload chưa encode
- **Mục báo cáo:** F12 / Reflected / Response

### F12-04. `32_reflected_elements_node.png`

- **Mục tiêu:** Chứng minh browser tạo element/event handler
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload Reflected`
- **Thao tác/nút:** Đóng alert; Inspect vùng kết quả
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Elements
- **Request cần chọn:** `N/A - dùng cùng lần GET`
- **Trường cần mở:** DOM node và attributes
- **Nội dung bắt buộc:** Node `img` có thuộc tính `onerror` trong vùng kết quả
- **Kết quả mong đợi:** DOM tạo element từ response vulnerable
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Elements chứng minh img/onerror được tạo
- **Mục báo cáo:** F12 / Reflected / DOM

### F12-05. `33_stored_post_payload.png`

- **Mục tiêu:** Chứng minh POST lưu Stored XSS
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/post/1/comments`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `author=Kiểm thử; body=<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>`
- **Thao tác/nút:** Bấm Đăng bình luận
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /vulnerable/post/1/comments`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** author và body đúng payload; cookie nếu có phải che
- **Kết quả mong đợi:** POST được xử lý rồi redirect/reload
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Stored XSS - Form Data của POST
- **Mục báo cáo:** F12 / Stored / Request

### F12-06. `34_stored_reload_request.png`

- **Mục tiêu:** Chứng minh browser tải lại trang sau khi lưu
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/post/1/comments`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload đã lưu ở ảnh 33`
- **Thao tác/nút:** Bật Preserve log rồi submit/reload
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/post/1/comments sau POST`
- **Trường cần mở:** General
- **Nội dung bắt buộc:** Chuỗi POST rồi GET/redirect cùng origin local
- **Kết quả mong đợi:** Trang được tải lại sau khi lưu
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Stored XSS - request reload sau POST
- **Mục báo cáo:** F12 / Stored / Reload

### F12-07. `35_stored_response_persisted.png`

- **Mục tiêu:** Chứng minh payload tiếp tục tồn tại sau reload
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/post/1/comments`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload Stored đã lưu`
- **Thao tác/nút:** Reload và chọn GET
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response; Elements
- **Request cần chọn:** `GET /vulnerable/post/1/comments`
- **Trường cần mở:** Response hoặc DOM node
- **Nội dung bắt buộc:** Payload/img/onerror xuất hiện lại từ dữ liệu SQLite
- **Kết quả mong đợi:** Stored payload tồn tại qua request mới
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response/Elements chứng minh Stored XSS tồn tại
- **Mục báo cáo:** F12 / Stored / Persistence

### F12-08. `36_dom_fragment_not_sent.png`

- **Mục tiêu:** Chứng minh location.hash không được gửi lên server
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/dom-search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `#<img src=x onerror="alert('DOM XSS')">`
- **Thao tác/nút:** Xóa Network; nhập payload; bấm Thay fragment không reload
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /vulnerable/dom-search nếu có; không có request mới khi chỉ đổi hash`
- **Trường cần mở:** Request URL
- **Nội dung bắt buộc:** Request URL không chứa fragment; thay hash không phát sinh HTTP mới
- **Kết quả mong đợi:** Fragment chỉ ở client
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Network không gửi fragment DOM XSS
- **Mục báo cáo:** F12 / DOM / Network

### F12-09. `37_dom_elements_innerhtml.png`

- **Mục tiêu:** Chứng minh innerHTML tạo node
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/dom-search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload DOM an toàn`
- **Thao tác/nút:** Inspect `#dom-result` sau khi đổi hash
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Elements
- **Request cần chọn:** `Không có request chứa fragment`
- **Trường cần mở:** DOM subtree
- **Nội dung bắt buộc:** `section#dom-result` chứa `img` và `onerror`
- **Kết quả mong đợi:** innerHTML parse chuỗi thành HTML
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Elements chứng minh innerHTML tạo node
- **Mục báo cáo:** F12 / DOM / Sink

### F12-10. `38_dom_console_execution.png`

- **Mục tiêu:** Chứng minh JavaScript thực thi ở client
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/dom-search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload DOM an toàn`
- **Thao tác/nút:** Quan sát alert hoặc verdict; Console chỉ để xem lỗi/trạng thái
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Console hoặc UI
- **Request cần chọn:** `Không có request mới`
- **Trường cần mở:** Console/UI
- **Nội dung bắt buộc:** Alert `DOM XSS` hoặc verdict `payload_executed`; không chạy lệnh đọc cookie
- **Kết quả mong đợi:** Payload thực thi cục bộ
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** UI/Console chứng minh DOM XSS thực thi
- **Mục báo cáo:** F12 / DOM / Execution

### F12-11. `39_secure_reflected_encoding_response.png`

- **Mục tiêu:** Chứng minh output encoding ở bản secure
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/secure/search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Cùng payload Reflected`
- **Thao tác/nút:** Submit rồi mở Response
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response
- **Request cần chọn:** `GET /secure/search?q=...`
- **Trường cần mở:** Response
- **Nội dung bắt buộc:** Payload hiển thị dạng text/escaped, không tạo img/onerror
- **Kết quả mong đợi:** Bản secure không thực thi
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure dùng output encoding
- **Mục báo cáo:** F12 / Secure / Encoding

### F12-12. `40_secure_stored_sanitization.png`

- **Mục tiêu:** Chứng minh sanitization loại bỏ nội dung nguy hiểm
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/secure/post/1/comments`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Payload Stored có img/onerror và strong`
- **Thao tác/nút:** Submit rồi mở Response/Elements
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response; Elements
- **Request cần chọn:** `POST rồi GET /secure/post/1/comments`
- **Trường cần mở:** Response/DOM
- **Nội dung bắt buộc:** Không còn img/onerror; nội dung/strong cho phép vẫn an toàn
- **Kết quả mong đợi:** Bleach allowlist chặn handler
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Sanitization của Stored XSS secure
- **Mục báo cáo:** F12 / Secure / Sanitization

### F12-13. `41_secure_dom_textcontent.png`

- **Mục tiêu:** Chứng minh textContent tạo text node
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/secure/dom-search`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Cùng fragment DOM`
- **Thao tác/nút:** Đổi fragment; Inspect `#dom-result`
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Elements
- **Request cần chọn:** `Không có request chứa fragment`
- **Trường cần mở:** DOM subtree
- **Nội dung bắt buộc:** Chuỗi `<img...>` là text; không có element/event attribute
- **Kết quả mong đợi:** textContent không parse HTML
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Elements chứng minh textContent an toàn
- **Mục báo cáo:** F12 / Secure / DOM

### F12-14. `42_secure_csp_response_headers.png`

- **Mục tiêu:** Chứng minh CSP trong response headers
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/security-headers`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Không`
- **Thao tác/nút:** Reload trang
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers
- **Request cần chọn:** `GET /security-headers`
- **Trường cần mở:** Response Headers
- **Nội dung bắt buộc:** Content-Security-Policy và X-Content-Type-Options/Referrer-Policy/X-Frame-Options
- **Kết quả mong đợi:** Header defense-in-depth có mặt
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response Headers có CSP
- **Mục báo cáo:** F12 / Headers

### F12-15. `43_cookie_flags_application.png`

- **Mục tiêu:** Chứng minh cookie flags local
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/profile`
- **Tài khoản:** Không đăng nhập
- **Dữ liệu nhập:** `Không`
- **Thao tác/nút:** Reload rồi mở cookie của origin local
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Application/Storage > Cookies
- **Request cần chọn:** `GET /profile`
- **Trường cần mở:** Name, Domain, Path, HttpOnly, Secure, SameSite
- **Nội dung bắt buộc:** HttpOnly=true, SameSite=Lax, Secure phản ánh cấu hình local; che Value
- **Kết quả mong đợi:** Cookie flags khớp cấu hình Flask
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Application hiển thị cookie flags
- **Mục báo cáo:** F12 / Cookies

## 5. Bảng mô tả ảnh F12

| STT | Tên file | Mục tiêu | Chuẩn bị | URL/lệnh | Dữ liệu và thao tác | F12 cần mở | Nội dung bắt buộc | Kết quả | Caption | Mục báo cáo |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `29_reflected_network_request.png` | Chứng minh GET Reflected XSS thật | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/search` | <img src=x onerror="alert('Reflected XSS')">; Nhập payload và bấm Tìm kiếm | Network > Headers; General và Query String Parameters | Request URL local, method GET, status và q đã percent-encode | Request được gửi tới bản vulnerable | Reflected XSS - request GET trong Network | F12 / Reflected / Request |
| 2 | `30_reflected_query_parameters.png` | Đối chiếu payload URL-encoded và giá trị decoded | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/search` | <img src=x onerror="alert('Reflected XSS')">; Chọn lại request tìm kiếm | Network > Payload hoặc Headers; Query String Parameters | q hiển thị payload decoded; Request URL có `%3C`, `%3E` hoặc encoding tương đương | DevTools phân biệt URL encoding với nội dung q | Query String Parameters của payload Reflected XSS | F12 / Reflected / Payload |
| 3 | `31_reflected_response_html.png` | Chứng minh response phản chiếu payload vào HTML | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/search` | Payload Reflected an toàn của lab; Mở Response của request | Network > Response; Response | HTML vùng `Kết quả cho` chứa thẻ img/onerror chưa encode | Response vulnerable chứa sink HTML | Response HTML phản chiếu payload chưa encode | F12 / Reflected / Response |
| 4 | `32_reflected_elements_node.png` | Chứng minh browser tạo element/event handler | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/search` | Payload Reflected; Đóng alert; Inspect vùng kết quả | Elements; DOM node và attributes | Node `img` có thuộc tính `onerror` trong vùng kết quả | DOM tạo element từ response vulnerable | Elements chứng minh img/onerror được tạo | F12 / Reflected / DOM |
| 5 | `33_stored_post_payload.png` | Chứng minh POST lưu Stored XSS | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/post/1/comments` | author=Kiểm thử; body=<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>; Bấm Đăng bình luận | Network > Payload; Form Data | author và body đúng payload; cookie nếu có phải che | POST được xử lý rồi redirect/reload | Stored XSS - Form Data của POST | F12 / Stored / Request |
| 6 | `34_stored_reload_request.png` | Chứng minh browser tải lại trang sau khi lưu | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/post/1/comments` | Payload đã lưu ở ảnh 33; Bật Preserve log rồi submit/reload | Network > Headers; General | Chuỗi POST rồi GET/redirect cùng origin local | Trang được tải lại sau khi lưu | Stored XSS - request reload sau POST | F12 / Stored / Reload |
| 7 | `35_stored_response_persisted.png` | Chứng minh payload tiếp tục tồn tại sau reload | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/post/1/comments` | Payload Stored đã lưu; Reload và chọn GET | Network > Response; Elements; Response hoặc DOM node | Payload/img/onerror xuất hiện lại từ dữ liệu SQLite | Stored payload tồn tại qua request mới | Response/Elements chứng minh Stored XSS tồn tại | F12 / Stored / Persistence |
| 8 | `36_dom_fragment_not_sent.png` | Chứng minh location.hash không được gửi lên server | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/dom-search` | #<img src=x onerror="alert('DOM XSS')">; Xóa Network; nhập payload; bấm Thay fragment không reload | Network > Headers; Request URL | Request URL không chứa fragment; thay hash không phát sinh HTTP mới | Fragment chỉ ở client | Network không gửi fragment DOM XSS | F12 / DOM / Network |
| 9 | `37_dom_elements_innerhtml.png` | Chứng minh innerHTML tạo node | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/dom-search` | Payload DOM an toàn; Inspect `#dom-result` sau khi đổi hash | Elements; DOM subtree | `section#dom-result` chứa `img` và `onerror` | innerHTML parse chuỗi thành HTML | Elements chứng minh innerHTML tạo node | F12 / DOM / Sink |
| 10 | `38_dom_console_execution.png` | Chứng minh JavaScript thực thi ở client | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/vulnerable/dom-search` | Payload DOM an toàn; Quan sát alert hoặc verdict; Console chỉ để xem lỗi/trạng thái | Console hoặc UI; Console/UI | Alert `DOM XSS` hoặc verdict `payload_executed`; không chạy lệnh đọc cookie | Payload thực thi cục bộ | UI/Console chứng minh DOM XSS thực thi | F12 / DOM / Execution |
| 11 | `39_secure_reflected_encoding_response.png` | Chứng minh output encoding ở bản secure | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/secure/search` | Cùng payload Reflected; Submit rồi mở Response | Network > Response; Response | Payload hiển thị dạng text/escaped, không tạo img/onerror | Bản secure không thực thi | Response secure dùng output encoding | F12 / Secure / Encoding |
| 12 | `40_secure_stored_sanitization.png` | Chứng minh sanitization loại bỏ nội dung nguy hiểm | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/secure/post/1/comments` | Payload Stored có img/onerror và strong; Submit rồi mở Response/Elements | Network > Response; Elements; Response/DOM | Không còn img/onerror; nội dung/strong cho phép vẫn an toàn | Bleach allowlist chặn handler | Sanitization của Stored XSS secure | F12 / Secure / Sanitization |
| 13 | `41_secure_dom_textcontent.png` | Chứng minh textContent tạo text node | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/secure/dom-search` | Cùng fragment DOM; Đổi fragment; Inspect `#dom-result` | Elements; DOM subtree | Chuỗi `<img...>` là text; không có element/event attribute | textContent không parse HTML | Elements chứng minh textContent an toàn | F12 / Secure / DOM |
| 14 | `42_secure_csp_response_headers.png` | Chứng minh CSP trong response headers | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/security-headers` | Không; Reload trang | Network > Headers; Response Headers | Content-Security-Policy và X-Content-Type-Options/Referrer-Policy/X-Frame-Options | Header defense-in-depth có mặt | Response Headers có CSP | F12 / Headers |
| 15 | `43_cookie_flags_application.png` | Chứng minh cookie flags local | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5000/profile` | Không; Reload rồi mở cookie của origin local | Application/Storage > Cookies; Name, Domain, Path, HttpOnly, Secure, SameSite | HttpOnly=true, SameSite=Lax, Secure phản ánh cấu hình local; che Value | Cookie flags khớp cấu hình Flask | Application hiển thị cookie flags | F12 / Cookies |

## 6. Xử lý lỗi thường gặp

- **Port 5000 bị chiếm:** dừng server lab cũ bằng `Ctrl+C`; dùng `Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue` để xác định tiến trình, không tự đổi port tài liệu.
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

Tài liệu này không dùng Playwright, Selenium hay ảnh dựng. Mọi ảnh phải do người học tự thao tác trên ứng dụng đang chạy tại `127.0.0.1`.

## 1. Chuẩn bị

1. Mở PowerShell tại `Lab01`, chạy `scripts\run_lab.bat` (hoặc `python app.py` trong `.venv`). Mở `http://127.0.0.1:5000` bằng Chrome/Edge/Firefox.
2. Dùng màn hình 1366×768 trở lên, khuyến nghị 1920×1080; zoom 80–100% để thấy chức năng và trace trong cùng ảnh.
3. Nhấn `F12` mở DevTools. Các tab dùng trong bài: **Network** (request/response), **Application/Storage** (cookie), **Elements** (DOM) và **Console** (CSP/JavaScript).
4. Trong Network, bật **Preserve log** khi cần theo dõi reload; nhấn biểu tượng xóa để bỏ request cũ. Chọn đúng request có path đang thực hành, rồi xem Headers, Payload, Response và Cookies.
5. Reset dữ liệu bằng `python scripts/reset_database.py`. Trên UI, dùng **Reset database** cho comments và **Xóa timeline** cho trace hiện tại.
6. Để ghép UI và DevTools trong một ảnh: dock DevTools bên phải, kéo rộng trang khoảng 65%, giữ URL, timeline/inspector và tab DevTools cần chứng minh cùng nhìn thấy.

Payload an toàn:

```html
<img src=x onerror="alert('Reflected XSS')">
<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>
#<img src=x onerror="alert('DOM XSS')">
```

## 2. Quy tắc file

- Lưu PNG trực tiếp trong `evidence/screenshots/`.
- Tên không dấu, không khoảng trắng và phải khớp tuyệt đối danh sách bên dưới.
- Không cắt URL, timeline, inspector hoặc verdict cần chứng minh. Không để lộ tab cá nhân, cookie thật hay dữ liệu riêng tư.
- Với alert: chụp alert nếu hệ điều hành cho phép; sau đó đóng alert và chụp verdict. Không thay alert bằng ảnh dựng.

## 3. Hướng dẫn từng ảnh

Mỗi dòng dưới đây quy định trạng thái đầu, dữ liệu/nút, tab UI hoặc bước timeline, vùng bắt buộc, kết quả và caption. Nếu sai: đóng alert, reset timeline/database theo cột “Trạng thái đầu”, xóa request Network rồi làm lại đúng URL.

| File | Mục đích | URL và trạng thái đầu | Dữ liệu / nút | Tab hoặc bước cần mở | Phải thấy và kết quả mong đợi | Caption báo cáo |
|---|---|---|---|---|---|---|
| `01_home_overview.png` | Tổng quan lab | `/`; trang vừa mở | Không | Không | Tên Lab01, ba loại XSS, nút vulnerable/secure | Tổng quan ba bài thử XSS local |
| `02_reflected_input_step.png` | Ghi input trước submit | `/vulnerable/search`; input trống | Dán payload Reflected, chưa bấm Tìm kiếm | Timeline bước 1 | Ô input còn nguyên payload; mô tả số ký tự cập nhật | Dữ liệu không tin cậy tại Browser UI |
| `03_reflected_request_step.png` | Chứng minh GET thật | Như ảnh 02, Network đã xóa | Bấm Tìm kiếm | Request Inspector hoặc Network Headers | Method GET, `/vulnerable/search`, query string và percent encoding | Browser tạo request Reflected XSS |
| `04_reflected_server_step.png` | Flask đọc query | Sau ảnh 03 | Không | Timeline bước Flask Router/Server Validation | `request.args["q"]`, q decoded và giới hạn 200 | Flask định tuyến và đọc dữ liệu query |
| `05_reflected_template_step.png` | Chứng minh sink lỗi | Sau ảnh 03 | Không | Timeline Template Engine hoặc So sánh mã | `Markup(q)`, payload chưa escape | Markup vô hiệu hóa Jinja autoescape |
| `06_reflected_browser_parse_step.png` | Phân tích browser | Sau ảnh 03, alert đã đóng | Không | Browser HTML Parser | Thẻ img/event handler được nêu; verdict đỏ | HTML parser tạo element và onerror |
| `07_reflected_payload_executed.png` | Kết quả khai thác an toàn | `/vulnerable/search` | Gửi payload Reflected | Alert hoặc Final Security Verdict | Alert “Reflected XSS” hoặc verdict `payload_executed` | Reflected payload thực thi trong lab local |
| `08_reflected_secure_encoding.png` | Chứng minh bản vá | `/secure/search`; timeline mới | Gửi đúng payload Reflected | Biến đổi dữ liệu + verdict | `&lt;`/`&gt;`, text node, payload không chạy | Jinja autoescape biến payload thành văn bản |
| `09_reflected_comparison.png` | So sánh mã | `/secure/search?q=...` | Bấm tab So sánh mã | So sánh mã | `Markup(q)` cạnh `{{ q }}` | Mã Reflected trước và sau vá |
| `10_stored_post_request.png` | POST thật | Reset database; `/vulnerable/post/1/comments` | Tên “Kiểm thử”, body payload Stored; bấm Đăng | Request Inspector hoặc Network Payload | POST, form body, cookie chỉ `***` | Browser gửi bình luận chứa payload |
| `11_stored_database_insert.png` | INSERT thật | Ngay sau ảnh 10 | Không | SQLite INSERT | `VALUES(1,?,?)`, dữ liệu đã lưu | Parameterized INSERT lưu payload an toàn với SQL |
| `12_stored_database_record.png` | Dữ liệu thật trong DB | Sau ảnh 10 | Không | Database Inspector | table/columns/row count/latest/raw value | Payload tồn tại trong SQLite comments |
| `13_stored_template_render.png` | SELECT và render | Reload trang vulnerable | Không | SQLite SELECT rồi Template Engine | SELECT tham số, `Markup(row["body"])` | Stored payload được đọc và render lại |
| `14_stored_payload_reload.png` | Chứng minh lặp lại | Sau ảnh 10 | Reload | Alert hoặc verdict | Alert “Stored XSS” hoặc verdict đỏ | Stored XSS chạy lại sau reload |
| `15_stored_secure_escape.png` | Bản secure đọc cùng DB | `/secure/post/1/comments` | Không | Database + verdict | Raw value còn trong DB, không thực thi | Dữ liệu lưu trữ không còn thực thi ở bản secure |
| `16_stored_secure_sanitize.png` | Bleach allowlist | `/secure/post/1/comments`; form trống | Gửi payload img/onerror + strong | Biến đổi dữ liệu | Trước có img/onerror; sau còn nội dung/strong an toàn | Bleach loại HTML và thuộc tính nguy hiểm |
| `17_stored_comparison.png` | So sánh Stored | Trang secure | Không | So sánh mã | Markup cạnh `bleach.clean` | Mã Stored XSS trước và sau vá |
| `18_dom_hash_source.png` | Fragment source | `/vulnerable/dom-search`; timeline mới | Nhập payload DOM, bấm thay fragment | Request/Timeline | `location.href`, `location.hash`; request path không có fragment | Fragment chỉ tồn tại phía browser |
| `19_dom_javascript_read.png` | JS đọc hash | Sau ảnh 18 | Không | Browser JavaScript | Hash và giá trị decoded | JavaScript đọc và decode location.hash |
| `20_dom_innerhtml_sink.png` | Sink nguy hiểm | Sau ảnh 18, alert đã đóng | Không | DOM step hoặc So sánh mã | `innerHTML` và giá trị sink | innerHTML diễn giải chuỗi thành HTML |
| `21_dom_element_created.png` | DOM thật | Sau ảnh 18 | Không | DOM Inspector; có thể mở Elements | outerHTML sau, IMG, onerror, element count | DOM Inspector phát hiện element và event attribute |
| `22_dom_payload_executed.png` | Kết quả DOM XSS | Sau ảnh 18 | Không | Alert hoặc verdict | Alert “DOM XSS” hoặc `payload_executed` | DOM payload thực thi trong lab local |
| `23_dom_textcontent_fix.png` | Bản vá DOM | `/secure/dom-search` | Thay cùng fragment | DOM Inspector + verdict | `textContent`, text node, 0 element/event | textContent không parse payload thành HTML |
| `24_dom_comparison.png` | So sánh DOM | Trang secure | Không | So sánh mã | innerHTML cạnh textContent | Mã DOM-based XSS trước và sau vá |
| `25_csp_headers.png` | CSP thật | `/security-headers`; Network xóa | Reload | Bảng header + trace/Network Response Headers | CSP và các directive self/none; X-Lab-Mode secure | CSP được thêm bởi Flask after_request |
| `26_cookie_security.png` | Cookie flags | `/profile`; DevTools mở | Reload | Bảng UI + Application/Storage Cookies | HttpOnly, SameSite=Lax, Secure local False/production True | Cấu hình cookie local và production |
| `27_presentation_mode.png` | Trình bày từng bước | `/secure/search?q=demo` | Bấm Presentation Mode, bấm Sau | Timeline | Chỉ bước hiện tại, chữ lớn, tiêu đề và progress | Presentation Mode cho trace XSS |
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

## 4. Ảnh cần DevTools

Ảnh 03, 10 và 25 nên có Network; ảnh 21 nên có Elements; ảnh 26 nên có Application/Storage. Ảnh khác ưu tiên inspector tích hợp để chữ dễ đọc. Trong Network, lọc theo `search`, `comments`, `security-headers` hoặc `profile`; chọn request có Method/Path đúng rồi mở đúng tab Headers/Payload/Response/Cookies.

## 5. Checklist sau khi chụp

- [ ] Đủ 28 PNG và đúng tên; không ảnh trùng.
- [ ] Chỉ có URL localhost/127.0.0.1 và payload alert an toàn.
- [ ] Không có dữ liệu riêng tư, tab/app cá nhân hoặc session ID đầy đủ.
- [ ] Chữ đọc được; URL, timeline, inspector và kết quả không bị cắt.
- [ ] Mỗi ảnh khớp caption trong bảng.
- [ ] Chạy `python scripts/check_screenshots.py`; sửa mọi mục thiếu/thừa/rỗng/quá nhỏ/trùng hash.
- [ ] Chạy `python scripts/generate_report.py` để thay placeholder bằng ảnh thật.
### Bằng chứng cũ tùy chọn

- `28_pytest_passed.png`: giữ tên để tương thích manifest cũ; không chạy lại pytest cho nhiệm vụ này. Chỉ dùng nếu ảnh thật đã có từ trước.
