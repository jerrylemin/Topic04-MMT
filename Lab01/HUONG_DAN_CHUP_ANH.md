# Hướng dẫn chụp ảnh Lab01

## 1. Chuẩn bị

Chỉ chụp thủ công tại `http://127.0.0.1:5000`. Chạy ứng dụng, mở DevTools khi được yêu cầu và lưu PNG tối thiểu 1024x600 vào `evidence/screenshots/`. Có thể ghép UI với DevTools/inspector nếu chữ vẫn đọc được. Trước ảnh Stored, chạy `python scripts/reset_database.py`; không xóa cookie trừ khi hướng dẫn nêu rõ.

## 2. Danh sách ảnh cần chụp

Theo đúng thứ tự: `01_reflected_vulnerable.png`, `02_reflected_secure.png`, `03_stored_submit.png`, `04_stored_reload.png`, `05_stored_secure.png`, `06_dom_vulnerable.png`, `07_dom_secure.png`, `08_code_fixes.png`, `09_csp_cookie.png`, `10_tests_reports.png`.

## 3. Cách chụp từng ảnh

### 01_reflected_vulnerable.png

- **Tên file:** `01_reflected_vulnerable.png`
- **Mục đích:** Chứng minh Reflected XSS vulnerable từ request đến kết quả chạy.
- **Trạng thái ban đầu:** Mở bản vulnerable, xóa kết quả cũ.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/search`
- **Dữ liệu cần nhập:** `<img src=x onerror="alert('XSS')">`
- **Nút cần bấm:** Tìm kiếm.
- **Tab DevTools hoặc inspector cần mở:** Network > request `search` hoặc Request Inspector.
- **Nội dung bắt buộc phải xuất hiện:** localhost, query/input, GET request và alert/verdict `payload_executed`.
- **Kết quả đúng:** Payload được phản chiếu không escape và chạy.
- **Caption dùng trong báo cáo:** Reflected XSS xảy ra khi dữ liệu q được đưa thẳng vào HTML.

Bước 1. Mở URL. Bước 2. Nhập payload. Bước 3. Bấm **Tìm kiếm**. Bước 4. Mở request. Bước 5. Chụp UI và request. Bước 6. Lưu đúng tên trên.

### 02_reflected_secure.png

- **Tên file:** `02_reflected_secure.png`
- **Mục đích:** Chứng minh cùng payload được encode và không chạy.
- **Trạng thái ban đầu:** Đóng alert, mở bản secure.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/secure/search`
- **Dữ liệu cần nhập:** `<img src=x onerror="alert('XSS')">`
- **Nút cần bấm:** Tìm kiếm.
- **Tab DevTools hoặc inspector cần mở:** Response Inspector hoặc Elements.
- **Nội dung bắt buộc phải xuất hiện:** Chuỗi đã escape/text node, không có element nguy hiểm, verdict blocked.
- **Kết quả đúng:** Payload hiển thị như văn bản và không chạy.
- **Caption dùng trong báo cáo:** Output encoding biến payload Reflected XSS thành văn bản an toàn.

Bước 1. Mở URL. Bước 2. Nhập cùng payload. Bước 3. Bấm **Tìm kiếm**. Bước 4. Mở Response/Elements. Bước 5. Chụp kết quả và text node. Bước 6. Lưu đúng tên.

### 03_stored_submit.png

- **Tên file:** `03_stored_submit.png`
- **Mục đích:** Chứng minh payload được POST và lưu trong SQLite.
- **Trạng thái ban đầu:** Chạy `python scripts/reset_database.py`, rồi mở trang vulnerable.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/post/1/comments`
- **Dữ liệu cần nhập:** Tác giả `SinhVien`; nội dung `<img src=x onerror="alert('XSS')">`.
- **Nút cần bấm:** Gửi bình luận.
- **Tab DevTools hoặc inspector cần mở:** Request và Database Inspector; có thể ghép cùng UI.
- **Nội dung bắt buộc phải xuất hiện:** POST body đã che cookie và bản ghi payload trong `comments`.
- **Kết quả đúng:** Payload thật được lưu; SQL tham số không tự ngăn XSS.
- **Caption dùng trong báo cáo:** Payload Stored XSS được gửi bằng POST và lưu trong cơ sở dữ liệu.

Bước 1. Reset DB và mở URL. Bước 2. Nhập tác giả/payload. Bước 3. Bấm **Gửi bình luận**. Bước 4. Mở Request và Database. Bước 5. Chụp vùng đọc được cả hai. Bước 6. Lưu đúng tên.

### 04_stored_reload.png

- **Tên file:** `04_stored_reload.png`
- **Mục đích:** Chứng minh Stored XSS chạy lại ở lần xem sau.
- **Trạng thái ban đầu:** Giữ bản ghi ảnh 03 và đóng alert.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/post/1/comments`
- **Dữ liệu cần nhập:** Không nhập thêm.
- **Nút cần bấm:** Reload trang.
- **Tab DevTools hoặc inspector cần mở:** Final Verdict/Timeline.
- **Nội dung bắt buộc phải xuất hiện:** Bình luận đã lưu và alert/verdict executed sau reload.
- **Kết quả đúng:** Payload chạy lại mà không cần POST mới.
- **Caption dùng trong báo cáo:** Stored XSS tiếp tục chạy từ dữ liệu đã lưu sau khi tải lại trang.

Bước 1. Giữ DB. Bước 2. Không nhập dữ liệu. Bước 3. Reload. Bước 4. Mở Final Verdict. Bước 5. Chụp bình luận và kết quả. Bước 6. Lưu đúng tên.

### 05_stored_secure.png

- **Tên file:** `05_stored_secure.png`
- **Mục đích:** Chứng minh dữ liệu vẫn hiển thị nhưng script bị sanitize/escape.
- **Trạng thái ban đầu:** Giữ DB của ảnh 03.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/secure/post/1/comments`
- **Dữ liệu cần nhập:** Không nhập thêm.
- **Nút cần bấm:** Reload trang.
- **Tab DevTools hoặc inspector cần mở:** Biến đổi sanitization và Final Verdict.
- **Nội dung bắt buộc phải xuất hiện:** Dữ liệu gốc, sau Bleach/escape và verdict không thực thi.
- **Kết quả đúng:** Event handler bị loại hoặc encode; nội dung an toàn vẫn hiện.
- **Caption dùng trong báo cáo:** Sanitization theo allowlist và escaping chặn Stored XSS.

Bước 1. Mở URL secure. Bước 2. Không nhập thêm. Bước 3. Reload. Bước 4. Mở biến đổi/Final Verdict. Bước 5. Chụp trước-sau và kết quả. Bước 6. Lưu đúng tên.

### 06_dom_vulnerable.png

- **Tên file:** `06_dom_vulnerable.png`
- **Mục đích:** Chứng minh `location.hash` đi tới `innerHTML`.
- **Trạng thái ban đầu:** Mở trang vulnerable, xóa fragment cũ.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/vulnerable/dom-search#%3Cimg%20src%3Dx%20onerror%3Dalert('XSS')%3E`
- **Dữ liệu cần nhập:** Fragment trong URL.
- **Nút cần bấm:** Enter hoặc kích hoạt `hashchange`.
- **Tab DevTools hoặc inspector cần mở:** DOM Inspector/Elements và bước `innerHTML`.
- **Nội dung bắt buộc phải xuất hiện:** `location.hash`, `innerHTML`, element `img/onerror` và alert/verdict executed.
- **Kết quả đúng:** Client tạo DOM nguy hiểm; fragment không gửi tới server.
- **Caption dùng trong báo cáo:** DOM-based XSS phát sinh khi location.hash được gán vào innerHTML.

Bước 1. Mở URL có fragment. Bước 2. Giữ payload đã encode. Bước 3. Nhấn Enter. Bước 4. Mở DOM/Elements. Bước 5. Chụp URL, sink và kết quả. Bước 6. Lưu đúng tên.

### 07_dom_secure.png

- **Tên file:** `07_dom_secure.png`
- **Mục đích:** Chứng minh cùng fragment chỉ tạo text node.
- **Trạng thái ban đầu:** Đóng alert, mở trang secure.
- **URL hoặc lệnh:** `http://127.0.0.1:5000/secure/dom-search#%3Cimg%20src%3Dx%20onerror%3Dalert('XSS')%3E`
- **Dữ liệu cần nhập:** Cùng fragment ảnh 06.
- **Nút cần bấm:** Enter hoặc kích hoạt `hashchange`.
- **Tab DevTools hoặc inspector cần mở:** DOM Inspector/Elements và bước `textContent`.
- **Nội dung bắt buộc phải xuất hiện:** `location.hash`, `textContent`, text node, không có element nguy hiểm.
- **Kết quả đúng:** Payload hiển thị nguyên văn và không chạy.
- **Caption dùng trong báo cáo:** textContent loại bỏ khả năng diễn giải fragment thành HTML.

Bước 1. Mở URL secure. Bước 2. Giữ cùng fragment. Bước 3. Nhấn Enter. Bước 4. Mở DOM/Elements. Bước 5. Chụp text node và verdict. Bước 6. Lưu đúng tên.

### 08_code_fixes.png

- **Tên file:** `08_code_fixes.png`
- **Mục đích:** Đối chiếu ba root cause và ba bản vá.
- **Trạng thái ban đầu:** Đã tạo trace cho ba kịch bản.
- **URL hoặc lệnh:** Các tab **So sánh mã** của ba trang secure.
- **Dữ liệu cần nhập:** Không nhập thêm.
- **Nút cần bấm:** So sánh mã.
- **Tab DevTools hoặc inspector cần mở:** Code Comparison tích hợp.
- **Nội dung bắt buộc phải xuất hiện:** `Markup/autoescape`, `Markup/Bleach`, `innerHTML/textContent`.
- **Kết quả đúng:** Đọc rõ ba sink lỗi và ba thay đổi sửa lỗi.
- **Caption dùng trong báo cáo:** So sánh nguyên nhân và bản vá cho ba loại XSS.

Bước 1. Mở lần lượt ba trang. Bước 2. Không nhập thêm. Bước 3. Bấm **So sánh mã**. Bước 4. Giữ ba panel đọc được. Bước 5. Ghép/chụp một ảnh. Bước 6. Lưu đúng tên.

### 09_csp_cookie.png

- **Tên file:** `09_csp_cookie.png`
- **Mục đích:** Chứng minh CSP và cookie flags.
- **Trạng thái ban đầu:** Mở `/profile` để tạo demo cookie.
- **URL hoặc lệnh:** `/security-headers` và `/profile` trên `127.0.0.1:5000`.
- **Dữ liệu cần nhập:** Không nhập.
- **Nút cần bấm:** Reload nếu cần.
- **Tab DevTools hoặc inspector cần mở:** Network > Response Headers và Application > Cookies.
- **Nội dung bắt buộc phải xuất hiện:** CSP; HttpOnly, SameSite, Path và trạng thái Secure local/production.
- **Kết quả đúng:** Các lớp defense in depth hiện rõ, không được mô tả là bản vá thay thế.
- **Caption dùng trong báo cáo:** CSP và cookie flags giảm tác động nhưng không thay thế sửa sink XSS.

Bước 1. Mở hai URL. Bước 2. Không nhập dữ liệu. Bước 3. Reload. Bước 4. Mở Headers và Cookies. Bước 5. Ghép hai panel khi chữ đọc được. Bước 6. Lưu đúng tên.

### 10_tests_reports.png

- **Tên file:** `10_tests_reports.png`
- **Mục đích:** Chứng minh pytest thật và report artifacts.
- **Trạng thái ban đầu:** Đóng ứng dụng đang giữ file report.
- **URL hoặc lệnh:** `python -m pytest -q`; `python scripts/generate_report.py`; `Get-ChildItem report`.
- **Dữ liệu cần nhập:** Ba lệnh trên.
- **Nút cần bấm:** Enter sau mỗi lệnh.
- **Tab DevTools hoặc inspector cần mở:** Terminal.
- **Nội dung bắt buộc phải xuất hiện:** Tổng kết pytest thực tế, tên DOCX/PDF, kích thước khác 0.
- **Kết quả đúng:** Chỉ ghi đạt nếu pytest trả exit code 0.
- **Caption dùng trong báo cáo:** Kết quả pytest thực tế và các report artifacts của Lab01.

Bước 1. Mở terminal tại Lab01. Bước 2. Nhập lệnh pytest. Bước 3. Chạy generator và liệt kê report. Bước 4. Cuộn để thấy tổng kết. Bước 5. Chụp terminal. Bước 6. Lưu đúng tên.

## 4. Cách kiểm tra và sinh báo cáo

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Thiếu ảnh vẫn sinh DOCX/PDF với placeholder đúng vị trí. Sau khi đặt đủ PNG đúng tên, chạy lại generator để tự thay placeholder bằng ảnh thật.
