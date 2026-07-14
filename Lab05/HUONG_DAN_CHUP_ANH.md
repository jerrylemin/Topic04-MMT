# HƯỚNG DẪN CHỤP ẢNH LAB05

## 1. Chuẩn bị

Chạy `python scripts/reset_database.py`, `python app.py`, mở `http://127.0.0.1:5005` và DevTools. Chỉ chụp thủ công trên localhost; không dùng automation, OCR hoặc ảnh giả. Có thể ghép UI với DevTools/inspector nếu chữ vẫn đọc được. Đăng xuất trước khi đổi giữa luồng vulnerable và secure.

## 2. Danh sách ảnh cần chụp

`01_normal_login_search.png`, `02_quote_error.png`, `03_auth_bypass.png`, `04_search_expanded.png`, `05_secure_login.png`, `06_secure_search.png`, `07_password_error_code.png`, `08_test_report.png`.

## 3. Cách chụp từng ảnh

### 01. `01_normal_login_search.png`
- Tên file: `01_normal_login_search.png`
- Mục đích: Chứng minh input bình thường hoạt động đúng.
- Trạng thái ban đầu: Database vừa reset, chưa đăng nhập.
- URL hoặc lệnh: `/vulnerable/login`, sau đó `/vulnerable/search?keyword=USB`.
- Dữ liệu cần nhập: `admin_lab` / mật khẩu demo; keyword `USB`.
- Nút cần bấm: **Đăng nhập**, **Tìm kiếm**.
- Tab DevTools hoặc inspector cần mở: Network, request tương ứng.
- Nội dung bắt buộc phải xuất hiện: localhost, input, request, đăng nhập thành công và kết quả USB.
- Kết quả đúng: Luồng bình thường thành công; tìm kiếm không mở rộng dữ liệu.
- Caption dùng trong báo cáo: Luồng đăng nhập và tìm kiếm bình thường trên ứng dụng local.

Bước 1. Đăng nhập. Bước 2. Tìm `USB`. Bước 3. Mở Network. Bước 4. Ghép hai trạng thái nếu chữ rõ. Bước 5. Chụp UI và request. Bước 6. Lưu đúng tên.

### 02. `02_quote_error.png`
- Tên file: `02_quote_error.png`
- Mục đích: Chứng minh dấu nháy phá SQL nối chuỗi.
- Trạng thái ban đầu: Đăng xuất; trace cũ có thể xóa.
- URL hoặc lệnh: `/vulnerable/login`.
- Dữ liệu cần nhập: Kịch bản **Dấu nháy đơn** có sẵn.
- Nút cần bấm: **Dấu nháy đơn**, **Đăng nhập**.
- Tab DevTools hoặc inspector cần mở: Error Inspector hoặc Network Response.
- Nội dung bắt buộc phải xuất hiện: Input có `'`, lỗi query đã xử lý, không có traceback/path.
- Kết quả đúng: Bản vulnerable có lỗi cú pháp an toàn để quan sát.
- Caption dùng trong báo cáo: Dấu nháy đơn phá cấu trúc câu SQL nối chuỗi ở bản vulnerable.

Bước 1. Mở URL. Bước 2. Chọn kịch bản. Bước 3. Gửi form. Bước 4. Mở Error Inspector. Bước 5. Chụp cả input và lỗi. Bước 6. Lưu đúng tên.

### 03. `03_auth_bypass.png`
- Tên file: `03_auth_bypass.png`
- Mục đích: Chứng minh authentication bypass local.
- Trạng thái ban đầu: Đã logout; database ở trạng thái seed.
- URL hoặc lệnh: `/vulnerable/login`.
- Dữ liệu cần nhập: Kịch bản authentication logic cố định của giao diện.
- Nút cần bấm: **Authentication logic**, **Đăng nhập**.
- Tab DevTools hoặc inspector cần mở: Network + Query Construction/Authentication Decision.
- Nội dung bắt buộc phải xuất hiện: Request, SQL biến đổi và phiên được tạo khi không biết mật khẩu.
- Kết quả đúng: Điều kiện WHERE bị thay đổi và đăng nhập demo thành công.
- Caption dùng trong báo cáo: Nối chuỗi SQL làm thay đổi logic xác thực trong lab local.

Bước 1. Logout. Bước 2. Mở URL. Bước 3. Chọn kịch bản và gửi. Bước 4. Mở Query/Authentication Inspector. Bước 5. Chụp SQL và kết quả. Bước 6. Lưu đúng tên.

### 04. `04_search_expanded.png`
- Tên file: `04_search_expanded.png`
- Mục đích: Chứng minh SQL Injection mở rộng tập kết quả.
- Trạng thái ban đầu: Database seed; không cần đăng nhập.
- URL hoặc lệnh: `/vulnerable/search`.
- Dữ liệu cần nhập: Kịch bản mở rộng kết quả cố định.
- Nút cần bấm: **Mở rộng kết quả**, **Tìm kiếm**.
- Tab DevTools hoặc inspector cần mở: Query Construction + Result Set.
- Nội dung bắt buộc phải xuất hiện: Keyword, SQL biến đổi và nhiều sản phẩm ngoài từ khóa bình thường.
- Kết quả đúng: Chỉ tập `products` local bị mở rộng.
- Caption dùng trong báo cáo: Điều kiện tìm kiếm bị thay đổi làm mở rộng tập kết quả.

Bước 1. Mở URL. Bước 2. Chọn kịch bản. Bước 3. Tìm kiếm. Bước 4. Mở Query/Result Set. Bước 5. Chụp toàn vùng cần đọc. Bước 6. Lưu đúng tên.

### 05. `05_secure_login.png`
- Tên file: `05_secure_login.png`
- Mục đích: Chứng minh secure login dùng placeholder.
- Trạng thái ban đầu: Logout; dùng đúng chuỗi ở ảnh 03.
- URL hoặc lệnh: `/secure/login`.
- Dữ liệu cần nhập: Cùng kịch bản authentication logic.
- Nút cần bấm: **Authentication logic**, **Đăng nhập**.
- Tab DevTools hoặc inspector cần mở: Query Construction + Authentication Decision.
- Nội dung bắt buộc phải xuất hiện: SQL có placeholder, parameter tách riêng, đăng nhập bị từ chối.
- Kết quả đúng: Chuỗi chỉ là dữ liệu; cấu trúc SQL không đổi.
- Caption dùng trong báo cáo: Parameterized query từ chối cùng chuỗi kiểm thử đăng nhập.

Bước 1. Logout. Bước 2. Mở URL. Bước 3. Gửi cùng dữ liệu. Bước 4. Mở inspector. Bước 5. Chụp placeholder và kết quả. Bước 6. Lưu đúng tên.

### 06. `06_secure_search.png`
- Tên file: `06_secure_search.png`
- Mục đích: Chứng minh secure search bind tham số.
- Trạng thái ban đầu: Dùng đúng keyword ảnh 04.
- URL hoặc lệnh: `/secure/search`.
- Dữ liệu cần nhập: Kịch bản mở rộng kết quả cố định.
- Nút cần bấm: **Mở rộng kết quả**, **Tìm kiếm**.
- Tab DevTools hoặc inspector cần mở: Query Construction + Result Set.
- Nội dung bắt buộc phải xuất hiện: `LIKE ?`, parameter riêng, kết quả không mở rộng.
- Kết quả đúng: Không trả sản phẩm ngoài ý muốn.
- Caption dùng trong báo cáo: Bind tham số giữ nguyên cấu trúc SQL và không mở rộng kết quả.

Bước 1. Mở URL. Bước 2. Chọn cùng dữ liệu. Bước 3. Tìm kiếm. Bước 4. Mở inspector. Bước 5. Chụp query và result. Bước 6. Lưu đúng tên.

### 07. `07_password_error_code.png`
- Tên file: `07_password_error_code.png`
- Mục đích: Ghép root cause và các bản vá chính.
- Trạng thái ban đầu: App đang chạy.
- URL hoặc lệnh: `/comparison`, `/security-controls`.
- Dữ liệu cần nhập: Không có.
- Nút cần bấm: Chọn phần Login, Search và Password/Error.
- Tab DevTools hoặc inspector cần mở: Code Comparison hoặc Security Controls.
- Nội dung bắt buộc phải xuất hiện: Nối chuỗi, parameter binding, PBKDF2 và generic error.
- Kết quả đúng: Đoạn vulnerable và secure đọc được trong một ảnh ghép.
- Caption dùng trong báo cáo: Bản vá kết hợp parameter binding, PBKDF2 và thông báo lỗi an toàn.

Bước 1. Mở comparison. Bước 2. Chọn các đoạn cần thiết. Bước 3. Mở security controls nếu cần. Bước 4. Ghép tối đa hai vùng. Bước 5. Kiểm tra chữ rõ. Bước 6. Lưu đúng tên.

### 08. `08_test_report.png`
- Tên file: `08_test_report.png`
- Mục đích: Ghi nhận kiểm thử và báo cáo thật.
- Trạng thái ban đầu: Đã chụp 7 ảnh trước.
- URL hoặc lệnh: `python -m pytest -q`; `python -m pytest --cov=. --cov-report=term`; `python scripts/generate_report.py`; `Get-ChildItem report`.
- Dữ liệu cần nhập: Không có.
- Nút cần bấm: Không có.
- Tab DevTools hoặc inspector cần mở: Terminal.
- Nội dung bắt buộc phải xuất hiện: Tổng kết pytest, coverage và tên DOCX/PDF thật.
- Kết quả đúng: Chỉ ghi kết quả vừa chạy; không tự sửa thành PASS.
- Caption dùng trong báo cáo: Kết quả kiểm thử, coverage và báo cáo được sinh từ dữ liệu thật.

Bước 1. Chạy pytest. Bước 2. Chạy coverage. Bước 3. Sinh report. Bước 4. Liệt kê report. Bước 5. Chụp terminal đọc được. Bước 6. Lưu đúng tên.

## 4. Cách kiểm tra và sinh báo cáo

Đặt ảnh vào `evidence/screenshots`, không xóa ảnh cũ. Chạy `python scripts/check_screenshots.py --list-required`, rồi `python scripts/check_screenshots.py` và `python scripts/generate_report.py`. Khi thiếu ảnh, DOCX/PDF giữ khung hướng dẫn đúng vị trí; khi đủ PNG hợp lệ, generator tự chèn ảnh và giữ caption.
