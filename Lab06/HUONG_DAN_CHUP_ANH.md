# HƯỚNG DẪN CHỤP ẢNH LAB06

## 1. Chuẩn bị

Chạy `python scripts/reset_database.py`, `python app.py`, mở `http://127.0.0.1:5006` và DevTools. Chỉ chụp thủ công trên localhost; không automation, OCR hoặc ảnh giả. Xóa cookie và đăng nhập lại trước mỗi cơ chế. Có thể ghép UI với DevTools/inspector nếu chữ vẫn đọc được.

## 2. Danh sách ảnh cần chụp

`01_cookie_flags.png`, `02_plain_role_tamper.png`, `03_base64_role_tamper.png`, `04_signed_valid.png`, `05_signed_tampered.png`, `06_encrypted_tampered.png`, `07_server_session_authz.png`, `08_session_lifecycle.png`, `09_audit_test_report.png`.

## 3. Cách chụp từng ảnh

### 01. `01_cookie_flags.png`
- Tên file: `01_cookie_flags.png`
- Mục đích: Quan sát cookie demo và flags.
- Trạng thái ban đầu: Xóa cookie, database reset.
- URL hoặc lệnh: `/` rồi luồng đăng nhập user demo.
- Dữ liệu cần nhập: Tài khoản student demo.
- Nút cần bấm: **Đăng nhập**.
- Tab DevTools hoặc inspector cần mở: Application > Storage > Cookies.
- Nội dung bắt buộc phải xuất hiện: Name, Value, Domain, Path, HttpOnly, Secure, SameSite.
- Kết quả đúng: Các thuộc tính local đọc rõ; che phần bí mật nếu có.
- Caption dùng trong báo cáo: Cookie demo và các thuộc tính bảo vệ được quan sát trong DevTools.

Bước 1. Xóa cookie. Bước 2. Đăng nhập. Bước 3. Mở Application. Bước 4. Chọn cookie. Bước 5. Chụp UI và bảng flags. Bước 6. Lưu đúng tên.

### 02. `02_plain_role_tamper.png`
- Tên file: `02_plain_role_tamper.png`
- Mục đích: Chứng minh vulnerable authorization tin Plain Cookie.
- Trạng thái ban đầu: Xóa cookie, đăng nhập student ở luồng Plain.
- URL hoặc lệnh: `/vulnerable/plain` và trang admin tương ứng.
- Dữ liệu cần nhập: Sửa `role=user` thành `role=admin`.
- Nút cần bấm: **Đăng nhập**, tải lại trang admin.
- Tab DevTools hoặc inspector cần mở: Application > Cookies.
- Nội dung bắt buộc phải xuất hiện: Giá trị trước/sau và quyền admin được cấp sai.
- Kết quả đúng: Server vulnerable chấp nhận role do client sửa.
- Caption dùng trong báo cáo: Sửa Plain Cookie làm vượt kiểm soát truy cập ở bản vulnerable.

Bước 1. Đăng nhập student. Bước 2. Mở admin và ghi trạng thái từ chối. Bước 3. Sửa role. Bước 4. Tải lại. Bước 5. Chụp trước/sau trong một ảnh. Bước 6. Lưu đúng tên.

### 03. `03_base64_role_tamper.png`
- Tên file: `03_base64_role_tamper.png`
- Mục đích: Chứng minh Base64 không bảo vệ toàn vẹn.
- Trạng thái ban đầu: Xóa cookie, đăng nhập student ở luồng Base64.
- URL hoặc lệnh: `/vulnerable/base64`.
- Dữ liệu cần nhập: Decode JSON, đổi role thành admin, encode lại.
- Nút cần bấm: Các nút inspector tích hợp và tải lại admin.
- Tab DevTools hoặc inspector cần mở: Base64 Inspector + Application > Cookies.
- Nội dung bắt buộc phải xuất hiện: JSON gốc, JSON sửa và server chấp nhận.
- Kết quả đúng: Role client sửa được dùng sai để cấp quyền.
- Caption dùng trong báo cáo: Cookie Base64 bị sửa role vì không có kiểm tra toàn vẹn.

Bước 1. Đăng nhập. Bước 2. Decode bằng inspector local. Bước 3. Sửa/encode role. Bước 4. Thay cookie và tải admin. Bước 5. Chụp JSON và kết quả. Bước 6. Lưu đúng tên.

### 04. `04_signed_valid.png`
- Tên file: `04_signed_valid.png`
- Mục đích: Chứng minh Signed Cookie nguyên vẹn hợp lệ.
- Trạng thái ban đầu: Xóa cookie; đăng nhập ở luồng Signed.
- URL hoặc lệnh: `/secure/signed`.
- Dữ liệu cần nhập: Tài khoản demo hợp lệ.
- Nút cần bấm: **Đăng nhập**, mở profile/admin phù hợp role.
- Tab DevTools hoặc inspector cần mở: Signature Inspector + Network.
- Nội dung bắt buộc phải xuất hiện: Cookie nguyên vẹn, chữ ký hợp lệ, request được xử lý.
- Kết quả đúng: Server xác minh chữ ký trước khi dùng dữ liệu.
- Caption dùng trong báo cáo: Signed Cookie nguyên vẹn vượt qua bước kiểm tra chữ ký.

Bước 1. Xóa cookie. Bước 2. Đăng nhập. Bước 3. Gửi request hợp lệ. Bước 4. Mở Signature Inspector. Bước 5. Chụp trạng thái valid. Bước 6. Lưu đúng tên.

### 05. `05_signed_tampered.png`
- Tên file: `05_signed_tampered.png`
- Mục đích: Chứng minh chữ ký phát hiện sửa đổi.
- Trạng thái ban đầu: Có Signed Cookie hợp lệ từ ảnh 04.
- URL hoặc lệnh: `/secure/signed`.
- Dữ liệu cần nhập: Sửa đúng một ký tự trong cookie.
- Nút cần bấm: Tải lại trang.
- Tab DevTools hoặc inspector cần mở: Application > Cookies + Signature Inspector.
- Nội dung bắt buộc phải xuất hiện: Cookie bị sửa, signature invalid và response từ chối.
- Kết quả đúng: Server không dùng dữ liệu đã bị can thiệp.
- Caption dùng trong báo cáo: Thay đổi một ký tự làm Signed Cookie bị server từ chối.

Bước 1. Giữ cookie ảnh 04. Bước 2. Sửa một ký tự. Bước 3. Tải lại. Bước 4. Mở inspector. Bước 5. Chụp invalid và response. Bước 6. Lưu đúng tên.

### 06. `06_encrypted_tampered.png`
- Tên file: `06_encrypted_tampered.png`
- Mục đích: Chứng minh authenticated encryption kiểm tra toàn vẹn.
- Trạng thái ban đầu: Xóa cookie; tạo encrypted token hợp lệ.
- URL hoặc lệnh: `/secure/encrypted`.
- Dữ liệu cần nhập: Sửa một ký tự của token.
- Nút cần bấm: Tạo token, gửi token hợp lệ, gửi token sửa.
- Tab DevTools hoặc inspector cần mở: Encryption Inspector + Network.
- Nội dung bắt buộc phải xuất hiện: Token hợp lệ, token sửa và kiểm tra thất bại.
- Kết quả đúng: Token can thiệp bị từ chối.
- Caption dùng trong báo cáo: Authenticated encryption phát hiện và từ chối token bị sửa.

Bước 1. Tạo token. Bước 2. Gửi bản hợp lệ. Bước 3. Sửa một ký tự. Bước 4. Gửi lại và mở inspector. Bước 5. Chụp hai kết quả. Bước 6. Lưu đúng tên.

### 07. `07_server_session_authz.png`
- Tên file: `07_server_session_authz.png`
- Mục đích: Chứng minh role lấy từ server/database.
- Trạng thái ban đầu: Xóa cookie và session; database seed.
- URL hoặc lệnh: `/secure/session`.
- Dữ liệu cần nhập: Đăng nhập student, sau đó logout và đăng nhập admin.
- Nút cần bấm: **Đăng nhập**, **Logout**, mở admin.
- Tab DevTools hoặc inspector cần mở: Server Session + Authorization Inspector.
- Nội dung bắt buộc phải xuất hiện: Cookie chỉ có session ID, student bị từ chối, admin được phép.
- Kết quả đúng: Authorization kiểm tra role server-side ở từng request.
- Caption dùng trong báo cáo: Server-side Session lấy quyền từ dữ liệu server cho từng request.

Bước 1. Đăng nhập student. Bước 2. Mở admin. Bước 3. Logout/login admin. Bước 4. Mở inspector. Bước 5. Ghép hai quyết định rõ chữ. Bước 6. Lưu đúng tên.

### 08. `08_session_lifecycle.png`
- Tên file: `08_session_lifecycle.png`
- Mục đích: Chứng minh rotation và logout invalidation.
- Trạng thái ban đầu: Xóa cookie; chưa đăng nhập.
- URL hoặc lệnh: `/secure/session`.
- Dữ liệu cần nhập: Tài khoản demo; giữ lại token cũ chỉ trong lab.
- Nút cần bấm: **Đăng nhập**, **Logout**, gửi lại token cũ.
- Tab DevTools hoặc inspector cần mở: Application > Cookies + Session/Audit Inspector.
- Nội dung bắt buộc phải xuất hiện: ID trước/sau rotate, logout invalidation, token cũ bị từ chối.
- Kết quả đúng: Phiên cũ không còn dùng được.
- Caption dùng trong báo cáo: Vòng đời phiên an toàn gồm rotation và hủy server-side khi logout.

Bước 1. Ghi session trước login. Bước 2. Login và ghi ID mới. Bước 3. Logout. Bước 4. Thử token cũ. Bước 5. Chụp timeline/audit và kết quả. Bước 6. Lưu đúng tên.

### 09. `09_audit_test_report.png`
- Tên file: `09_audit_test_report.png`
- Mục đích: Ghi nhận audit, pytest và report thật.
- Trạng thái ban đầu: Đã thực hiện các luồng trên.
- URL hoặc lệnh: `/audit-logs`; `python -m pytest -q`; `python scripts/generate_report.py`; `Get-ChildItem report`.
- Dữ liệu cần nhập: Không có.
- Nút cần bấm: Không có.
- Tab DevTools hoặc inspector cần mở: Audit Inspector + Terminal.
- Nội dung bắt buộc phải xuất hiện: Sự kiện tamper, tổng kết pytest thật, tên DOCX/PDF thật.
- Kết quả đúng: Chỉ ghi kết quả vừa chạy; không hard-code PASS.
- Caption dùng trong báo cáo: Audit, kiểm thử và báo cáo của Lab06 được ghi nhận từ dữ liệu thật.

Bước 1. Mở audit. Bước 2. Chạy pytest. Bước 3. Sinh report. Bước 4. Liệt kê report. Bước 5. Ghép audit và terminal nếu chữ rõ. Bước 6. Lưu đúng tên.

## 4. Cách kiểm tra và sinh báo cáo

Đặt ảnh vào `evidence/screenshots`, không xóa ảnh cũ. Chạy `python scripts/check_screenshots.py --list-required`, `python scripts/check_screenshots.py` và `python scripts/generate_report.py`. Khi thiếu ảnh, DOCX/PDF giữ khung hướng dẫn đúng vị trí; khi đủ PNG hợp lệ, generator tự chèn ảnh và giữ caption.
