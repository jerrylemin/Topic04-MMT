# Hướng dẫn chụp ảnh Lab04

## 1. Chuẩn bị

- Chỉ dùng Victim `http://127.0.0.1:5004` và Demo Page `http://127.0.0.1:9004`. Không dùng website thật hoặc browser automation.
- Chạy `python scripts/reset_database.py`, sau đó `python run_both.py`. Tài khoản: `victim / Victim123!`.
- Lưu PNG vào `evidence/screenshots/`. Có thể ghép UI và DevTools nếu chữ vẫn đọc được.
- Reset database, xóa cookie cũ và đăng nhập lại trước ảnh 04-06 để state/token rõ ràng.

## 2. Danh sách ảnh cần chụp

1. `01_login_valid_request.png` - Chứng minh victim đã đăng nhập và request đổi email hợp lệ ban đầu.
2. `02_csrf_demo_form.png` - Chứng minh trang Demo Page có form CSRF local cố định.
3. `03_csrf_vulnerable_changed.png` - Chứng minh CSRF vulnerable đổi email của victim.
4. `04_csrf_secure_403.png` - Chứng minh token thiếu hoặc sai bị từ chối và state không đổi.
5. `05_origin_blocked.png` - Chứng minh Origin/Referer validation chặn request từ Demo Page.
6. `06_csrf_secure_success.png` - Chứng minh token hợp lệ cho phép request và được rotate.
7. `07_audit_test_report.png` - Chứng minh audit, kiểm thử và report artifacts.

## 3. Cách chụp từng ảnh

### Ảnh 01 - Chứng minh victim đã đăng nhập và request đổi email hợp lệ ban đầu.

- **Tên file:** 01_login_valid_request.png
- **Mục đích:** Chứng minh victim đã đăng nhập và request đổi email hợp lệ ban đầu.
- **Trạng thái ban đầu:** Reset database; Victim và Demo Page đang chạy; chưa đăng nhập.
- **URL hoặc lệnh:** http://127.0.0.1:5004/login rồi http://127.0.0.1:5004/vulnerable/change-email
- **Dữ liệu cần nhập:** victim / Victim123!; email=victim_initial@lab.local
- **Nút cần bấm:** Đăng nhập; Đổi email
- **Tab DevTools hoặc inspector cần mở:** DevTools Network > request POST; ghép với Dashboard.
- **Nội dung bắt buộc phải xuất hiện:** Session victim, POST /vulnerable/change-email và email mới trên Dashboard.
- **Kết quả đúng:** Request cùng origin hợp lệ ban đầu đổi email thành công.
- **Caption dùng trong báo cáo:** Victim đăng nhập và gửi request đổi email hợp lệ ban đầu.

Bước 1. Mở trang login của Victim Application.
Bước 2. Đăng nhập victim / Victim123! rồi mở form vulnerable.
Bước 3. Nhập victim_initial@lab.local và bấm Đổi email.
Bước 4. Mở Network, chọn POST /vulnerable/change-email.
Bước 5. Chụp chung request và Dashboard có email mới.
Bước 6. Lưu thành 01_login_valid_request.png.

### Ảnh 02 - Chứng minh trang Demo Page có form CSRF local cố định.

- **Tên file:** 02_csrf_demo_form.png
- **Mục đích:** Chứng minh trang Demo Page có form CSRF local cố định.
- **Trạng thái ban đầu:** Victim vẫn đăng nhập; mở Demo Page ở cửa sổ/tab khác.
- **URL hoặc lệnh:** http://127.0.0.1:9004/attack/vulnerable-email
- **Dữ liệu cần nhập:** Form cố định gửi email=demo_changed@lab.local đến 127.0.0.1:5004.
- **Nút cần bấm:** Chưa gửi; chỉ mở trang
- **Tab DevTools hoặc inspector cần mở:** Form Inspector hoặc DevTools Elements.
- **Nội dung bắt buộc phải xuất hiện:** method POST, action /vulnerable/change-email, hidden/input email cố định và cảnh báo chỉ localhost.
- **Kết quả đúng:** Mã/giao diện form local đúng kịch bản, không có target tùy ý.
- **Caption dùng trong báo cáo:** Trang Demo Page chứa form CSRF local cố định.

Bước 1. Giữ phiên victim và mở URL Demo Page.
Bước 2. Kiểm tra target/email đã cố định.
Bước 3. Chưa bấm Gửi form.
Bước 4. Mở Form Inspector hoặc Elements.
Bước 5. Chụp form, method, action và email cùng thanh địa chỉ localhost.
Bước 6. Lưu thành 02_csrf_demo_form.png.

### Ảnh 03 - Chứng minh CSRF vulnerable đổi email của victim.

- **Tên file:** 03_csrf_vulnerable_changed.png
- **Mục đích:** Chứng minh CSRF vulnerable đổi email của victim.
- **Trạng thái ban đầu:** Victim đang đăng nhập và email chưa là demo_changed@lab.local.
- **URL hoặc lệnh:** http://127.0.0.1:9004/attack/vulnerable-email
- **Dữ liệu cần nhập:** email=demo_changed@lab.local.
- **Nút cần bấm:** Gửi form rồi xác nhận
- **Tab DevTools hoặc inspector cần mở:** DevTools Network; ghép response/trace với Dashboard Victim.
- **Nội dung bắt buộc phải xuất hiện:** POST được gửi, cookie/session hiện diện trong trace và email đổi thành demo_changed@lab.local.
- **Kết quả đúng:** Route vulnerable chấp nhận request không có token và state thay đổi.
- **Caption dùng trong báo cáo:** CSRF vulnerable dùng session cookie để đổi email victim.

Bước 1. Mở Demo Page vulnerable khi victim còn đăng nhập.
Bước 2. Giữ email demo_changed@lab.local.
Bước 3. Bấm Gửi form và xác nhận.
Bước 4. Mở Network hoặc Request Inspector của kết quả.
Bước 5. Chụp request cùng Dashboard/State Inspector có email mới.
Bước 6. Lưu thành 03_csrf_vulnerable_changed.png.

### Ảnh 04 - Chứng minh token thiếu hoặc sai bị từ chối và state không đổi.

- **Tên file:** 04_csrf_secure_403.png
- **Mục đích:** Chứng minh token thiếu hoặc sai bị từ chối và state không đổi.
- **Trạng thái ban đầu:** Reset database, đăng nhập lại victim và ghi nhớ email hiện tại.
- **URL hoặc lệnh:** http://127.0.0.1:9004/attack/secure-email hoặc /attack/bad-token
- **Dữ liệu cần nhập:** Thiếu token hoặc token sai; email=blocked@lab.local.
- **Nút cần bấm:** Gửi form rồi xác nhận
- **Tab DevTools hoặc inspector cần mở:** Network Response và CSRF/State Inspector.
- **Nội dung bắt buộc phải xuất hiện:** HTTP 403, token missing/invalid, database update skipped và email không đổi.
- **Kết quả đúng:** Bản secure từ chối request trước mutation.
- **Caption dùng trong báo cáo:** CSRF token thiếu hoặc sai bị từ chối, state không đổi.

Bước 1. Reset, đăng nhập lại victim và mở Demo Page secure/bad-token.
Bước 2. Giữ token thiếu/sai và email kiểm thử.
Bước 3. Bấm Gửi form và xác nhận.
Bước 4. Mở Network Response cùng CSRF/State Inspector.
Bước 5. Chụp HTTP 403 và email trước/sau không đổi.
Bước 6. Lưu thành 04_csrf_secure_403.png.

### Ảnh 05 - Chứng minh Origin/Referer validation chặn request từ Demo Page.

- **Tên file:** 05_origin_blocked.png
- **Mục đích:** Chứng minh Origin/Referer validation chặn request từ Demo Page.
- **Trạng thái ban đầu:** Victim đã đăng nhập; dùng scenario Origin denied của Demo Page.
- **URL hoặc lệnh:** http://127.0.0.1:9004/attack/secure-email
- **Dữ liệu cần nhập:** Origin=http://127.0.0.1:9004; token không phải điều kiện quyết định ảnh này.
- **Nút cần bấm:** Gửi form rồi xác nhận
- **Tab DevTools hoặc inspector cần mở:** Origin Inspector và Network Response.
- **Nội dung bắt buộc phải xuất hiện:** submitted origin 9004, expected origin 5004, exact match=false, HTTP 403 và state không đổi.
- **Kết quả đúng:** Request khác origin bị chặn trước khi cập nhật database.
- **Caption dùng trong báo cáo:** Exact Origin/Referer validation chặn request từ Demo Page.

Bước 1. Reset/đăng nhập rồi mở Demo Page secure.
Bước 2. Giữ form gửi từ origin 127.0.0.1:9004.
Bước 3. Bấm Gửi form và xác nhận.
Bước 4. Mở Origin Inspector và Network Response.
Bước 5. Chụp origin submitted/expected, deny và HTTP 403.
Bước 6. Lưu thành 05_origin_blocked.png.

### Ảnh 06 - Chứng minh token hợp lệ cho phép request và được rotate.

- **Tên file:** 06_csrf_secure_success.png
- **Mục đích:** Chứng minh token hợp lệ cho phép request và được rotate.
- **Trạng thái ban đầu:** Reset database và đăng nhập victim; chỉ thao tác trên Victim Application.
- **URL hoặc lệnh:** http://127.0.0.1:5004/secure/change-email
- **Dữ liệu cần nhập:** email=secure_success@lab.local; dùng hidden token do server cấp.
- **Nút cần bấm:** Đổi email an toàn
- **Tab DevTools hoặc inspector cần mở:** CSRF Token, Origin và State Inspector.
- **Nội dung bắt buộc phải xuất hiện:** Origin hợp lệ, token valid, email đổi thành công và rotation status=rotated.
- **Kết quả đúng:** Request có token/session/origin hợp lệ thành công; token cũ không còn dùng lại.
- **Caption dùng trong báo cáo:** Bản secure chấp nhận token hợp lệ và rotate token sau mutation.

Bước 1. Reset, đăng nhập và mở secure change-email trên Victim App.
Bước 2. Nhập secure_success@lab.local; không sửa hidden token.
Bước 3. Bấm Đổi email an toàn.
Bước 4. Mở CSRF Token, Origin và State Inspector.
Bước 5. Chụp valid/rotated cùng email sau cập nhật.
Bước 6. Lưu thành 06_csrf_secure_success.png.

### Ảnh 07 - Chứng minh audit, kiểm thử và report artifacts.

- **Tên file:** 07_audit_test_report.png
- **Mục đích:** Chứng minh audit, kiểm thử và report artifacts.
- **Trạng thái ban đầu:** Đã chạy các flow vulnerable, denied và secure success.
- **URL hoặc lệnh:** http://127.0.0.1:5004/audit-logs và terminal tại Lab04
- **Dữ liệu cần nhập:** python -m pytest -q; python scripts/generate_report.py
- **Nút cần bấm:** Filter nếu cần; chạy hai lệnh terminal
- **Tab DevTools hoặc inspector cần mở:** Audit Inspector; terminal phải đọc được output thật.
- **Nội dung bắt buộc phải xuất hiện:** Audit có vulnerable_email_changed, csrf_token_invalid/origin denied, secure_email_changed; terminal có pytest summary và tên DOCX/PDF.
- **Kết quả đúng:** Audit, pytest và report artifacts xuất hiện trong một ảnh đọc được.
- **Caption dùng trong báo cáo:** Audit log cùng kết quả kiểm thử và report artifacts của Lab04.

Bước 1. Mở /audit-logs sau khi chạy các flow.
Bước 2. Chạy python -m pytest -q trong terminal.
Bước 3. Chạy python scripts/generate_report.py.
Bước 4. Đặt terminal cạnh Audit Inspector.
Bước 5. Chụp vùng đọc được audit events, pytest summary và tên report.
Bước 6. Lưu thành 07_audit_test_report.png.

## 4. Cách kiểm tra và sinh báo cáo

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Thiếu ảnh thì DOCX/PDF vẫn có placeholder đúng vị trí. Đặt PNG hợp lệ đúng tên rồi chạy lại generator để tự thay bằng ảnh thật.
