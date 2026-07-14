# Hướng dẫn chụp ảnh thủ công Lab03

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

## 40_pytest_passed.png

- **Mục đích:** Kết quả kiểm thử
- **Điều kiện ban đầu:** Chạy app tại 127.0.0.1:5003 và reset lab nếu trạng thái trước đó ảnh hưởng kết quả.
- **Tài khoản:** Không áp dụng
- **URL:** Terminal local
- **Dữ liệu gốc:** Không áp dụng
- **Dữ liệu cần sửa:** Không sửa
- **Nút cần bấm:** Chạy pytest
- **Panel cần mở:** Không bắt buộc
- **Bước timeline:** Không bắt buộc
- **Nội dung bắt buộc:** Dòng tổng kết pytest đạt.
- **Kết quả mong đợi:** Dòng tổng kết pytest đạt.
- **Caption báo cáo:** Kết quả kiểm thử. Dòng tổng kết pytest đạt.
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
- **Nội dung bắt buộc:** DOCX và PDF đúng tên.
- **Kết quả mong đợi:** DOCX và PDF đúng tên.
- **Caption báo cáo:** Artifact báo cáo. DOCX và PDF đúng tên.
- **Lỗi thường gặp và cách làm lại:** Nếu sai trạng thái, reset lab, đăng nhập lại đúng tài khoản và chạy lại đúng một request.
