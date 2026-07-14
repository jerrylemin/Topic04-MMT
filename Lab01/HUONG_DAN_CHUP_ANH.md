# Hướng dẫn chụp ảnh thủ công — Lab01 XSS

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
| `28_pytest_passed.png` | Kiểm thử tự động | Terminal ở `Lab01` | Chạy `pytest -q` | Không | Toàn bộ dòng tổng kết pass, không cắt lệnh | Kết quả pytest của Lab01 |

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
