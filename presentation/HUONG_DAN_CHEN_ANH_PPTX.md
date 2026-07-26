# Hướng dẫn chèn ảnh vào PPTX Topic04

Tệp trình chiếu đích: `21127645_LeMinh_21127224_NguyenVuBach_Topic04_6Labs_final.pptx`  
Tỷ lệ ảnh khuyến nghị cho mọi placeholder: **16:9**.  
Nguyên tắc: chỉ dùng ảnh tự chụp từ phiên lab cục bộ; không dùng ảnh minh họa giả, ảnh web, hoặc ảnh do công cụ dựng lại.

## Cách thay placeholder mà không làm vỡ bố cục

1. Mở **Home → Select → Selection Pane** và tìm các shape có tên bắt đầu bằng `PH_Sxx_...` tương ứng với slide.
2. Chọn shape có hậu tố `_IMAGE`, vào **Shape Format → Shape Fill → Picture…** và chọn ảnh thật.
3. Chọn **Picture Format → Crop → Fill**, kéo ảnh để vùng bằng chứng bắt buộc nằm trọn trong khung; không thay đổi kích thước hoặc vị trí của shape.
4. Xóa hai shape hướng dẫn có hậu tố `_INSTRUCTION` và `_ICON` nếu chúng còn che ảnh. Giữ nguyên `_FRAME`, `_CAPTION` và mọi callout màu cam.
5. Không kéo ảnh vượt ra ngoài khung, không che tiêu đề/footer, và không thay đổi font hoặc cỡ chữ của caption.

## Danh sách 12 ảnh cần chèn

### 1. Slide 04 — Lab01 — `29_reflected_network_request.png`

- **Mục tiêu:** chứng minh payload Reflected XSS được gửi bằng GET và xuất hiện trong request thật.
- **Khởi động:** chạy `Lab01\scripts\run_lab.bat`.
- **URL:** `http://127.0.0.1:5000/vulnerable/search`.
- **Tài khoản:** không cần đăng nhập.
- **Input:** `<img src=x onerror="alert('Reflected XSS')">`.
- **Thao tác:** nhập payload, bấm **Tìm kiếm**, mở DevTools → **Network**, chọn request tìm kiếm.
- **Trạng thái cần giữ:** request đã hoàn tất; alert có thể đã đóng để không che bằng chứng.
- **Vùng bắt buộc:** thanh địa chỉ hoặc tên request cục bộ, phương thức **GET**, status, và phần **Query String Parameters** có khóa `q` với payload percent-encoded.
- **Crop:** ưu tiên DevTools Headers và một phần giao diện đủ nhận diện endpoint; bỏ vùng trống và thanh bookmark.
- **Caption giữ nguyên:** “Reflected XSS — request GET trong Network”.

### 2. Slide 06 — Lab01 — `41_secure_dom_textcontent.png`

- **Mục tiêu:** chứng minh bản secure dùng `textContent`, payload chỉ là văn bản chứ không trở thành phần tử DOM.
- **Khởi động:** chạy `Lab01\scripts\run_lab.bat`.
- **URL:** `http://127.0.0.1:5000/secure/dom-search`.
- **Tài khoản:** không cần đăng nhập.
- **Input/hash:** `#<img src=x onerror="alert('DOM XSS')">`.
- **Thao tác:** mở URL có fragment, sau đó DevTools → **Elements**, chọn node `#dom-result`.
- **Trạng thái cần giữ:** không có popup; chuỗi `<img ...>` hiển thị như text.
- **Vùng bắt buộc:** URL cục bộ, nội dung hiển thị, và cây Elements cho thấy không có phần tử `<img>` hay event handler được tạo.
- **Crop:** giữ node `#dom-result` cùng nội dung text và phần giao diện tương ứng.
- **Caption giữ nguyên:** “Elements chứng minh textContent an toàn”.

### 3. Slide 10 — Lab02 — `31_long_input_network_payload.png`

- **Mục tiêu:** ghi nhận chuỗi dài 64 byte được gửi tới binary vulnerable.
- **Khởi động:** chạy Lab02 theo `Lab02\README.md` trong WSL/Docker và mở web cục bộ.
- **URL:** `http://127.0.0.1:5002/vulnerable`.
- **Tài khoản:** không cần đăng nhập.
- **Input:** 64 ký tự `A`; chế độ `vulnerable_asan`.
- **Thao tác:** bấm nút submit/chạy input, mở DevTools → **Network** → request POST `/submit` → **Payload**.
- **Trạng thái cần giữ:** request đã gửi; UI hoặc trace thể hiện độ dài 64.
- **Vùng bắt buộc:** endpoint `/submit`, phương thức POST, Form Data có chuỗi 64 ký tự, và chế độ vulnerable.
- **Crop:** lấy cả Payload và vùng UI/trace xác nhận độ dài; không cần toàn bộ cửa sổ.
- **Caption giữ nguyên:** “Payload 64 byte gửi tới bản vulnerable”.

### 4. Slide 10 — Lab02 — `34_secure_length_network_response.png`

- **Mục tiêu:** chứng minh `secure_length` từ chối input dài trước thao tác copy.
- **Khởi động:** giữ Lab02 đang chạy.
- **URL:** `http://127.0.0.1:5002/secure/length`.
- **Tài khoản:** không cần đăng nhập.
- **Input:** 64 ký tự `A`; chế độ `secure_length`.
- **Thao tác:** bấm submit, DevTools → **Network** → POST `/secure/length/submit` → **Payload/Response**.
- **Trạng thái cần giữ:** phản hồi từ chối đã hiển thị, không crash.
- **Vùng bắt buộc:** endpoint secure, độ dài input 64, và nội dung Response cho biết input bị từ chối trước copy.
- **Crop:** cân đối Payload và Response; bỏ console/log không liên quan.
- **Caption giữ nguyên:** “Response secure_length từ chối input dài”.

### 5. Slide 14 — Lab03 — `45_checkout_tampered_payload.png`

- **Mục tiêu:** chứng minh giá sản phẩm là dữ liệu client có thể bị sửa trước khi POST.
- **Khởi động:** chạy Lab03 theo `Lab03\README.md`.
- **URL:** `http://127.0.0.1:5003/vulnerable/checkout`.
- **Tài khoản:** `user_a` / `UserA123!`.
- **Input:** sản phẩm `product_id=5`, `quantity=1`; sửa giá `100000` thành `1` bằng Elements hoặc Console.
- **Thao tác:** submit checkout, DevTools → **Network** → request POST → **Payload**.
- **Trạng thái cần giữ:** payload bị sửa đã được gửi; chưa cần hiển thị thông tin cá nhân khác.
- **Vùng bắt buộc:** Form Data có `product_id=5`, `quantity=1`, `price=1` và tên endpoint vulnerable.
- **Crop:** lấy Payload làm trọng tâm, kèm một phần UI đủ nhận diện checkout.
- **Caption giữ nguyên:** “Payload checkout sau sửa giá”.

### 6. Slide 15 — Lab03 — `51_invoice_secure_403_response.png`

- **Mục tiêu:** chứng minh kiểm tra ownership chặn user A đọc hóa đơn của user B.
- **Khởi động:** giữ Lab03 đang chạy.
- **URL:** `http://127.0.0.1:5003/secure/invoice?id=1002`.
- **Tài khoản:** `user_a` / `UserA123!`.
- **Thao tác:** mở trực tiếp URL, DevTools → **Network** → request invoice → **Headers/Response**.
- **Trạng thái cần giữ:** HTTP **403**; nội dung hóa đơn 1002 không bị lộ.
- **Vùng bắt buộc:** URL có `id=1002`, status 403 và response từ chối.
- **Crop:** giữ General/Headers và đoạn Response; loại bỏ cookie hoặc dữ liệu nhạy cảm không cần thiết.
- **Caption giữ nguyên:** “Response secure trả 403 cho invoice khác chủ”.

### 7. Slide 19 — Lab04 — `08_email_after_csrf.png`

- **Mục tiêu:** chứng minh request CSRF vulnerable đã đổi email của victim.
- **Khởi động:** trong Lab04 chạy `python run_both.py` để mở victim app và attacker demo.
- **URL kiểm chứng:** `http://127.0.0.1:5004/profile`.
- **Tài khoản:** `victim` / `Victim123!`.
- **Input từ attacker:** target `http://127.0.0.1:5004/vulnerable/change-email`, email `demo_changed@lab.local`, rồi bấm nút gửi form thủ công.
- **Thao tác kiểm chứng:** quay lại profile và refresh; có thể mở Network chọn GET `/profile`.
- **Trạng thái cần giữ:** email mới `demo_changed@lab.local` hiển thị trên profile.
- **Vùng bắt buộc:** origin/URL cục bộ, tên victim hoặc vùng profile, và email mới.
- **Crop:** tập trung phần profile sau tấn công; không cần chụp toàn bộ trang attacker.
- **Caption giữ nguyên:** “Email victim sau request CSRF”.

### 8. Slide 21 — Lab04 — `13_secure_missing_token_403.png`

- **Mục tiêu:** chứng minh endpoint secure từ chối request thiếu CSRF token.
- **Khởi động:** giữ cả hai ứng dụng Lab04 đang chạy.
- **URL đích:** endpoint secure change-email trên `http://127.0.0.1:5004`.
- **Tài khoản:** `victim` / `Victim123!`.
- **Input:** gửi từ attacker demo tới endpoint secure nhưng không có token hợp lệ.
- **Thao tác:** bấm nút gửi form thủ công, DevTools → **Network** → POST secure change-email → **Headers/Response**.
- **Trạng thái cần giữ:** HTTP **403** và email victim không đổi.
- **Vùng bắt buộc:** endpoint secure, status 403, thông báo token thiếu/không hợp lệ; nếu đủ chỗ, kèm profile giữ nguyên email.
- **Crop:** lấy response 403 làm trọng tâm, tránh chụp token hợp lệ thật.
- **Caption giữ nguyên:** “Response 403 khi thiếu CSRF token”.

### 9. Slide 24 — Lab05 — `42_login_bypass_response.png`

- **Mục tiêu:** chứng minh phép nối chuỗi SQL làm thay đổi logic xác thực ở route vulnerable.
- **Khởi động:** chạy Lab05 theo `Lab05\README.md`.
- **URL:** trang vulnerable login trên `http://127.0.0.1:5005`.
- **Tài khoản:** không đăng nhập trước; tài khoản đích demo là `admin_lab` / `AdminLab123!`.
- **Input cố định:** username `admin_lab' -- `; chọn scenario POST authentication bypass theo giao diện lab.
- **Thao tác:** submit, DevTools → **Network** → request login → **Response/Preview**.
- **Trạng thái cần giữ:** response cho thấy session/demo vulnerable đã xác thực, ví dụ `vulnerable_local_demo`.
- **Vùng bắt buộc:** payload hoặc request tương ứng, response bypass và origin cục bộ.
- **Crop:** ưu tiên Response/Preview và thông báo trạng thái đăng nhập; không lộ cookie ngoài phạm vi lab.
- **Caption giữ nguyên:** “Response vulnerable authentication bypass”.

### 10. Slide 26 — Lab05 — `43_secure_login_same_payload.png`

- **Mục tiêu:** chứng minh prepared statement xử lý cùng payload như dữ liệu literal và từ chối đăng nhập.
- **Khởi động:** giữ Lab05 đang chạy.
- **URL:** trang secure login trên `http://127.0.0.1:5005`.
- **Tài khoản:** không đăng nhập.
- **Input:** username `admin_lab' -- `; password bất kỳ theo scenario lab.
- **Thao tác:** submit secure login, DevTools → **Network** → **Payload/Response**.
- **Trạng thái cần giữ:** không tạo phiên admin; thông báo lỗi chung.
- **Vùng bắt buộc:** cùng payload username, endpoint secure, và response bị từ chối.
- **Crop:** đặt Payload và Response trong cùng ảnh nếu đọc được; bỏ dữ liệu ngoài lab.
- **Caption giữ nguyên:** “Secure login từ chối cùng payload”.

### 11. Slide 29 — Lab06 — `51_plain_cookie_modified_application.png`

- **Mục tiêu:** chứng minh người dùng có thể sửa role trong plain cookie bằng DevTools.
- **Khởi động:** chạy Lab06 theo `Lab06\README.md`.
- **URL:** trang plain-cookie/admin trên `http://127.0.0.1:5006`.
- **Tài khoản:** `student` / `Student123!`.
- **Thao tác:** DevTools → **Application/Storage → Cookies**, sửa `lab06_role` từ `user` thành `admin`, giữ nguyên origin/path/flags rồi reload.
- **Trạng thái cần giữ:** cookie đã có value `admin`; ứng dụng vulnerable cấp quyền theo giá trị client.
- **Vùng bắt buộc:** origin `127.0.0.1:5006`, cookie name `lab06_role`, value `admin`, và các cột Path/SameSite nếu hiển thị.
- **Crop:** tập trung bảng Cookies, kèm một phần giao diện admin nếu còn đọc được.
- **Caption giữ nguyên:** “Sửa role cookie bằng DevTools”.

### 12. Slide 31 — Lab06 — `56_signed_cookie_rejected_response.png`

- **Mục tiêu:** chứng minh signed cookie phát hiện sửa đổi nhờ kiểm tra chữ ký.
- **Khởi động:** giữ Lab06 đang chạy.
- **URL:** flow signed-profile trên `http://127.0.0.1:5006`.
- **Tài khoản:** `student` / `Student123!`.
- **Thao tác:** sau khi có `lab06_signed_profile`, sửa đúng một ký tự của value trong Application/Storage, reload, rồi chọn request tương ứng trong **Network → Headers/Response**.
- **Trạng thái cần giữ:** server từ chối cookie với lỗi chữ ký/invalid data; không cấp quyền admin.
- **Vùng bắt buộc:** endpoint signed-profile, response từ chối hoặc thông báo invalid signature, và status tương ứng.
- **Crop:** tập trung Response và tên request; không cần hiển thị toàn bộ giá trị signed cookie.
- **Caption giữ nguyên:** “Response secure từ chối signed cookie sửa”.

## Kiểm tra nhanh sau khi chèn

- Đủ đúng **12 ảnh**, mỗi filename xuất hiện đúng một lần trong slide được chỉ định.
- Mọi ảnh đều là ảnh thật từ localhost, không có dữ liệu cá nhân hoặc bí mật ngoài tài khoản lab.
- Chữ trong DevTools vẫn đọc được khi trình chiếu 100%; nếu quá nhỏ, crop hẹp hơn thay vì phóng khung.
- Không còn chữ “CHÈN ẢNH THẬT” hoặc icon placeholder phủ lên ảnh.
- Caption, callout, số slide, tiêu đề và footer không bị xê dịch.
- Không thay đổi kích thước slide 16:9 và không kéo ảnh ra ngoài safe area.
