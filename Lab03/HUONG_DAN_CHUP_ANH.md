# Hướng dẫn chụp ảnh Lab03

## 1. Chuẩn bị

- Chỉ dùng `http://127.0.0.1:5003` và dữ liệu lab. Không dùng website thật, Playwright hoặc Selenium.
- Chạy `python scripts/reset_database.py`, sau đó `python app.py`. Đăng nhập `user_a / UserA123!`.
- Lưu ảnh PNG vào `evidence/screenshots/`. Có thể ghép UI với DevTools nếu mọi chữ vẫn đọc được.
- Reset database và đăng nhập lại trước ảnh 01-07; ảnh 06 phải reset xong mới làm ảnh 07.

## 2. Danh sách ảnh cần chụp

1. `01_checkout_normal.png` - Chứng minh checkout bình thường dùng giá gốc.
2. `02_checkout_tampered.png` - Chứng minh server vulnerable chấp nhận giá bị sửa.
3. `03_checkout_secure.png` - Chứng minh bản secure bỏ qua giá client.
4. `04_idor_vulnerable.png` - Chứng minh User A xem được hóa đơn của User B.
5. `05_idor_secure.png` - Chứng minh object-level authorization chặn IDOR.
6. `06_role_vulnerable.png` - Chứng minh mass assignment đổi role thành admin.
7. `07_role_secure.png` - Chứng minh secure profile bỏ qua field nhạy cảm.
8. `08_audit_test_report.png` - Chứng minh audit, kiểm thử và report artifacts.

## 3. Cách chụp từng ảnh

### Ảnh 01 - Chứng minh checkout bình thường dùng giá gốc.

- **Tên file:** 01_checkout_normal.png
- **Mục đích:** Chứng minh checkout bình thường dùng giá gốc.
- **Trạng thái ban đầu:** Reset database, đăng nhập user_a và thêm product 5, quantity 1 vào giỏ.
- **URL hoặc lệnh:** http://127.0.0.1:5003/vulnerable/checkout
- **Dữ liệu cần nhập:** product_id=5, quantity=1, price=100000
- **Nút cần bấm:** Gửi checkout vulnerable
- **Tab DevTools hoặc inspector cần mở:** DevTools Network > request Payload; ghép với kết quả UI.
- **Nội dung bắt buộc phải xuất hiện:** URL localhost, request POST có price=100000 và invoice/total=100000 VND.
- **Kết quả đúng:** Checkout thành công với giá gốc 100000 VND.
- **Caption dùng trong báo cáo:** Checkout bình thường với giá sản phẩm gốc.

Bước 1. Mở URL checkout vulnerable.
Bước 2. Giữ product_id=5, quantity=1 và price=100000.
Bước 3. Bấm Gửi checkout vulnerable.
Bước 4. Mở Network, chọn request POST vừa gửi.
Bước 5. Chụp chung Payload và kết quả invoice 100000 VND.
Bước 6. Lưu thành 01_checkout_normal.png.

### Ảnh 02 - Chứng minh server vulnerable chấp nhận giá bị sửa.

- **Tên file:** 02_checkout_tampered.png
- **Mục đích:** Chứng minh server vulnerable chấp nhận giá bị sửa.
- **Trạng thái ban đầu:** Reset database, đăng nhập user_a và thêm product 5, quantity 1.
- **URL hoặc lệnh:** http://127.0.0.1:5003/vulnerable/checkout
- **Dữ liệu cần nhập:** Sửa hidden price từ 100000 thành 1.
- **Nút cần bấm:** Gửi checkout vulnerable
- **Tab DevTools hoặc inspector cần mở:** DevTools Elements hoặc Request Inspector; ghép với invoice/Database Inspector.
- **Nội dung bắt buộc phải xuất hiện:** price=1 trong request, server dùng giá client, unit price/total=1 VND.
- **Kết quả đúng:** Bản vulnerable tạo hóa đơn sai giá.
- **Caption dùng trong báo cáo:** Bản vulnerable tin giá do client gửi và tạo hóa đơn 1 VND.

Bước 1. Reset rồi mở URL checkout vulnerable.
Bước 2. Sửa hidden field price=1 bằng Elements hoặc console cố định.
Bước 3. Bấm Gửi checkout vulnerable.
Bước 4. Mở Request hoặc Database Inspector.
Bước 5. Chụp chung price=1 và invoice/total=1 VND.
Bước 6. Lưu thành 02_checkout_tampered.png.

### Ảnh 03 - Chứng minh bản secure bỏ qua giá client.

- **Tên file:** 03_checkout_secure.png
- **Mục đích:** Chứng minh bản secure bỏ qua giá client.
- **Trạng thái ban đầu:** Reset database, đăng nhập user_a và thêm product 5, quantity 1.
- **URL hoặc lệnh:** http://127.0.0.1:5003/secure/checkout
- **Dữ liệu cần nhập:** Gửi product_id=5, quantity=1, price=1.
- **Nút cần bấm:** Gửi checkout secure
- **Tab DevTools hoặc inspector cần mở:** Request/Parameter Diff và Database hoặc Audit Inspector.
- **Nội dung bắt buộc phải xuất hiện:** Giá client=1, giá database=100000, server dùng giá database và có checkout_price_mismatch.
- **Kết quả đúng:** Invoice secure có total=100000 VND; giá client không quyết định kết quả.
- **Caption dùng trong báo cáo:** Bản secure lấy giá từ database và ghi nhận price mismatch.

Bước 1. Reset rồi mở URL checkout secure.
Bước 2. Nhập product_id=5, quantity=1 và thêm price=1 trong console cố định.
Bước 3. Bấm Gửi checkout secure.
Bước 4. Mở Parameter Diff và Database/Audit Inspector.
Bước 5. Chụp vùng thấy cả client price, database price và total 100000.
Bước 6. Lưu thành 03_checkout_secure.png.

### Ảnh 04 - Chứng minh User A xem được hóa đơn của User B.

- **Tên file:** 04_idor_vulnerable.png
- **Mục đích:** Chứng minh User A xem được hóa đơn của User B.
- **Trạng thái ban đầu:** Reset database và đăng nhập user_a.
- **URL hoặc lệnh:** http://127.0.0.1:5003/vulnerable/invoice?id=1002
- **Dữ liệu cần nhập:** Đổi id từ 1001 thành 1002.
- **Nút cần bấm:** GET invoice
- **Tab DevTools hoặc inspector cần mở:** Network hoặc Request Inspector; ghép với invoice và Database Inspector.
- **Nội dung bắt buộc phải xuất hiện:** Session user_id=12, invoice 1002 owner_id=13 nhưng nội dung hóa đơn vẫn hiển thị.
- **Kết quả đúng:** IDOR vulnerable thành công trong dữ liệu lab.
- **Caption dùng trong báo cáo:** Bản vulnerable thiếu kiểm tra ownership nên lộ invoice 1002.

Bước 1. Reset, đăng nhập User A và mở invoice vulnerable.
Bước 2. Đổi id=1001 thành id=1002.
Bước 3. Bấm GET invoice.
Bước 4. Mở Request hoặc Database Inspector.
Bước 5. Chụp URL, owner_id=13 và nội dung invoice 1002.
Bước 6. Lưu thành 04_idor_vulnerable.png.

### Ảnh 05 - Chứng minh object-level authorization chặn IDOR.

- **Tên file:** 05_idor_secure.png
- **Mục đích:** Chứng minh object-level authorization chặn IDOR.
- **Trạng thái ban đầu:** Reset database và đăng nhập user_a.
- **URL hoặc lệnh:** http://127.0.0.1:5003/secure/invoice?id=1002
- **Dữ liệu cần nhập:** id=1002 khi session thuộc user_id=12.
- **Nút cần bấm:** GET với authorization
- **Tab DevTools hoặc inspector cần mở:** Authorization Inspector hoặc Network Response.
- **Nội dung bắt buộc phải xuất hiện:** HTTP 403, policy owner-or-admin=deny và không có dữ liệu dòng hàng invoice 1002.
- **Kết quả đúng:** Server từ chối truy cập trái quyền trước khi render hóa đơn.
- **Caption dùng trong báo cáo:** Bản secure trả 403 khi User A yêu cầu invoice của User B.

Bước 1. Reset, đăng nhập User A và mở invoice secure.
Bước 2. Nhập id=1002.
Bước 3. Bấm GET với authorization.
Bước 4. Mở Authorization Inspector hoặc Network Response.
Bước 5. Chụp HTTP 403, decision deny và thông báo không trả dữ liệu.
Bước 6. Lưu thành 05_idor_secure.png.

### Ảnh 06 - Chứng minh mass assignment đổi role thành admin.

- **Tên file:** 06_role_vulnerable.png
- **Mục đích:** Chứng minh mass assignment đổi role thành admin.
- **Trạng thái ban đầu:** Reset database và đăng nhập user_a.
- **URL hoặc lệnh:** http://127.0.0.1:5003/vulnerable/profile
- **Dữ liệu cần nhập:** Sửa hidden role=user thành role=admin; giữ user_id=12.
- **Nút cần bấm:** Cập nhật vulnerable
- **Tab DevTools hoặc inspector cần mở:** Elements hoặc Request Inspector; ghép với Database/Session Inspector.
- **Nội dung bắt buộc phải xuất hiện:** POST có role=admin, database trước=user sau=admin và UI/session hiển thị admin.
- **Kết quả đúng:** Bản vulnerable cho phép nâng quyền trong lab.
- **Caption dùng trong báo cáo:** Mass assignment vulnerable chấp nhận role do client gửi.

Bước 1. Reset, đăng nhập User A và mở profile vulnerable.
Bước 2. Sửa hidden role thành admin.
Bước 3. Bấm Cập nhật vulnerable.
Bước 4. Mở Request và Database/Session Inspector.
Bước 5. Chụp request role=admin và kết quả role admin.
Bước 6. Lưu thành 06_role_vulnerable.png.

### Ảnh 07 - Chứng minh secure profile bỏ qua field nhạy cảm.

- **Tên file:** 07_role_secure.png
- **Mục đích:** Chứng minh secure profile bỏ qua field nhạy cảm.
- **Trạng thái ban đầu:** Reset database và đăng nhập user_a.
- **URL hoặc lệnh:** http://127.0.0.1:5003/secure/profile
- **Dữ liệu cần nhập:** Gửi email hợp lệ kèm role=admin và user_id khác qua console cố định/DevTools.
- **Nút cần bấm:** Cập nhật secure
- **Tab DevTools hoặc inspector cần mở:** Authorization, Database hoặc Audit Inspector.
- **Nội dung bắt buộc phải xuất hiện:** accepted_fields chỉ có email; role/user_id bị loại; database và session vẫn role=user.
- **Kết quả đúng:** Server lấy identity từ session và giữ đúng quyền user.
- **Caption dùng trong báo cáo:** Bản secure dùng field allowlist và không nhận role từ client.

Bước 1. Reset, đăng nhập User A và mở profile secure.
Bước 2. Thêm role=admin và user_id khác vào request.
Bước 3. Bấm Cập nhật secure.
Bước 4. Mở Authorization/Database/Audit Inspector.
Bước 5. Chụp rejected_fields và role=user không đổi.
Bước 6. Lưu thành 07_role_secure.png.

### Ảnh 08 - Chứng minh audit, kiểm thử và report artifacts.

- **Tên file:** 08_audit_test_report.png
- **Mục đích:** Chứng minh audit, kiểm thử và report artifacts.
- **Trạng thái ban đầu:** Đã chạy ba luồng secure; mở hai cửa sổ terminal cạnh trang audit.
- **URL hoặc lệnh:** http://127.0.0.1:5003/audit-logs và terminal tại Lab03
- **Dữ liệu cần nhập:** python -m pytest -q; python scripts/generate_report.py
- **Nút cần bấm:** Filter (nếu cần), sau đó chạy hai lệnh terminal.
- **Tab DevTools hoặc inspector cần mở:** Audit Inspector; terminal phải đọc được kết quả thật và danh sách report.
- **Nội dung bắt buộc phải xuất hiện:** Audit có checkout_price_mismatch, invoice_access_denied, sensitive_field_submitted; terminal có pytest summary thật và hai artifact report.
- **Kết quả đúng:** Audit, pytest và report đều xuất hiện; không che phần tổng kết lệnh.
- **Caption dùng trong báo cáo:** Audit log cùng kết quả kiểm thử và report artifacts của Lab03.

Bước 1. Chạy các flow secure rồi mở /audit-logs.
Bước 2. Chạy python -m pytest -q trong terminal.
Bước 3. Chạy python scripts/generate_report.py.
Bước 4. Đặt terminal cạnh Audit Inspector.
Bước 5. Chụp vùng đọc được ba audit event, pytest summary và tên DOCX/PDF.
Bước 6. Lưu thành 08_audit_test_report.png.

## 4. Cách kiểm tra và sinh báo cáo

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Nếu còn thiếu ảnh, generator vẫn tạo DOCX/PDF với khung placeholder đúng vị trí. Khi đặt đủ PNG đúng tên và hợp lệ, chạy lại generator để ảnh thật tự thay khung.
