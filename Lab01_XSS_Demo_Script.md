# Kịch bản demo Lab01: Reflected XSS, Stored XSS và DOM-based XSS

## 1. Chuẩn bị chung

- Chỉ chạy ứng dụng tại `http://127.0.0.1:5000`.
- Mở Chrome và nhấn `F12`.
- Chọn tab `Network`.
- Bật `Preserve log` và `Disable cache`.
- Khi cần xem request chính, chọn bộ lọc `Doc`.
- Khi cần kiểm tra DOM, chọn tab `Elements`.
- Trước mỗi demo, bấm `Clear` trong Network và `Xóa timeline` trên giao diện lab.
- Chỉ dùng payload alert có sẵn trong lab.

## 2. Mở đầu phần XSS

### Lời nói

“XSS xảy ra khi dữ liệu do người dùng kiểm soát bị trình duyệt hiểu thành HTML hoặc JavaScript của ứng dụng.

Ba loại XSS trong Lab01 khác nhau ở đường đi của dữ liệu:

- Reflected XSS: payload nằm trong request và được server phản chiếu ngay trong response.
- Stored XSS: payload được lưu trong database rồi phát lại cho người xem trang.
- DOM-based XSS: JavaScript phía trình duyệt đọc dữ liệu từ URL rồi đưa vào DOM sink nguy hiểm.”

---

# 3. Demo Reflected XSS

## 3.1. Mục tiêu

Chứng minh dữ liệu từ query `q` được server phản chiếu vào HTML. Bản có lỗi dùng `Markup(q)`, còn bản đã vá để Jinja autoescape dữ liệu.

## 3.2. Route

- Có lỗi: `http://127.0.0.1:5000/vulnerable/search`
- Đã vá: `http://127.0.0.1:5000/secure/search`

## 3.3. Bước 1: Thử dữ liệu bình thường

### Thao tác

1. Mở route có lỗi.
2. Nhập:

```text
laptop
```

3. Bấm `Tìm kiếm`.
4. Trong Network, chọn request `search?q=laptop`.
5. Mở `Payload` và chỉ ra `q: laptop`.
6. Mở `Response`, tìm `Kết quả cho`.

### Lời nói

“Browser gửi từ khóa qua query parameter `q`. Server đọc dữ liệu và phản chiếu lại trong vùng ‘Kết quả cho’. Với chuỗi bình thường, trang chỉ hiển thị văn bản.”

## 3.4. Bước 2: Gửi payload an toàn

### Payload

```html
<img src=x onerror="alert('Reflected XSS')">
```

### Thao tác

1. Xóa Network và timeline cũ.
2. Dán payload vào ô tìm kiếm.
3. Bấm `Tìm kiếm`.
4. Giữ hộp thoại alert vài giây rồi bấm `OK`.
5. Trong Network, chọn request document mới.
6. Mở `Payload`, chỉ ra toàn bộ payload trong `q`.
7. Mở `Response`, tìm `onerror`.
8. Mở `Elements`, tìm `onerror`.

### Lời nói

“Thẻ `img` yêu cầu browser tải ảnh `x`. Ảnh không tồn tại nên sự kiện `error` xảy ra. Thuộc tính `onerror` chạy alert.

Trong Response, payload vẫn còn nguyên dấu `<`, `>` và thuộc tính `onerror`. Trong Elements, payload đã trở thành một node `img` thật. Điều này chứng minh browser đã hiểu input là HTML, không phải văn bản.”

## 3.5. Giải thích Source → Sink

```text
Ô tìm kiếm
→ query q
→ request.args["q"]
→ Markup(q)
→ template {{ q }}
→ HTML response
→ browser tạo img
→ onerror chạy
```

### Lời nói

“Source là query `q`. Sink là vùng HTML nhận dữ liệu qua `Markup(q)`. `Markup` đánh dấu input là nội dung an toàn, làm Jinja bỏ qua autoescape.”

## 3.6. Kiểm chứng bản secure

### Thao tác

1. Bấm `So sánh bản vá` hoặc mở route secure.
2. Gửi lại đúng payload cũ.
3. Kiểm tra không có alert.
4. Trong Response, tìm `&lt;img`.
5. Trong Elements, kiểm tra payload chỉ là text, không có node `img` do input tạo.

### Lời nói

“Bản secure vẫn nhận cùng payload. Điểm khác nằm ở output. Jinja autoescape đổi `<` thành `&lt;` và `>` thành `&gt;`. Browser tạo text node nên không có `img` và không có `onerror`.”

## 3.7. Trả lời câu hỏi Reflected XSS

- Dữ liệu được đưa vào HTML ở đâu?  
  Query `q` được đưa vào vùng “Kết quả cho” trong HTML response.

- Ứng dụng có escape `<`, `>`, `"`, `'` không?  
  Bản vulnerable không escape tại sink vì dùng `Markup(q)`. Bản secure dùng Jinja autoescape.

- Nạn nhân mở URL chứa payload thì sao?  
  Browser gửi request chứa `q`, server phản chiếu payload chưa encode, browser tạo node HTML và JavaScript chạy.

---

# 4. Demo Stored XSS

## 4.1. Mục tiêu

Chứng minh payload được lưu trong SQLite, tiếp tục tồn tại sau khi reload và chạy lại khi trang bình luận được mở.

## 4.2. Route

- Có lỗi: `http://127.0.0.1:5000/vulnerable/post/1/comments`
- Đã vá: `http://127.0.0.1:5000/secure/post/1/comments`

## 4.3. Bước 1: Đăng bình luận bình thường

### Thao tác

1. Mở route vulnerable.
2. Nhập tên:

```text
Sinh viên kiểm thử
```

3. Nhập bình luận:

```text
Bình luận bình thường
```

4. Bấm gửi.
5. Reload trang.

### Lời nói

“Trước tiên, tôi gửi một bình luận bình thường để xác nhận chức năng lưu dữ liệu đang hoạt động. Sau khi reload, bình luận vẫn còn vì server đã lưu nội dung vào database.”

## 4.4. Bước 2: Đăng payload an toàn

### Payload

```html
<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>
```

### Thao tác

1. Xóa Network và timeline cũ.
2. Nhập tên người gửi.
3. Dán payload vào ô bình luận.
4. Bấm gửi.
5. Khi alert xuất hiện, bấm `OK`.
6. Reload trang.
7. Quan sát alert chạy lại.
8. Mở `Database Inspector`.
9. Chỉ ra giá trị raw trong `comments.body`.
10. Trong Network, quan sát `POST` gửi bình luận và request `GET` khi trang tải lại.
11. Trong Elements, tìm `onerror`.

### Lời nói

“Khác Reflected XSS, payload này không phụ thuộc vào URL hiện tại. Server lưu payload vào bảng `comments`, cột `body`.

Khi trang được mở lại, server đọc dữ liệu từ SQLite và đưa vào HTML. Browser tạo lại node `img`, nên alert tiếp tục chạy. Đây là lý do Stored XSS có thể ảnh hưởng nhiều người xem cùng một trang.”

## 4.5. Giải thích Source → Sink

```text
Form bình luận
→ POST comment
→ SQLite comments.body
→ server SELECT comment
→ Markup(body)
→ HTML response
→ browser tạo img
→ onerror chạy
```

### Lời nói

“Source là nội dung bình luận. Payload được lưu trong database. Sink xuất hiện khi server đọc bình luận và render bằng `Markup(body)`.

Việc câu lệnh INSERT dùng parameter binding không tự chống Stored XSS. SQL an toàn và HTML output an toàn là hai vấn đề khác nhau.”

## 4.6. Chứng minh phạm vi ảnh hưởng

### Thao tác

1. Mở tab mới hoặc cửa sổ ẩn danh.
2. Truy cập lại route vulnerable.
3. Quan sát payload chạy lại.

### Lời nói

“Người xem mới không cần gửi payload. Chỉ cần mở trang chứa bình luận đã lưu, browser của họ sẽ nhận payload và thực thi.”

## 4.7. Kiểm chứng bản secure

### Thao tác

1. Mở route secure.
2. Gửi lại cùng payload.
3. Quan sát không có alert.
4. Kiểm tra phần `<strong>Xin chào</strong>` vẫn được hiển thị đậm.
5. Kiểm tra `img` và `onerror` đã bị loại.
6. Mở `Biến đổi dữ liệu` hoặc `Database Inspector` để so sánh raw và sanitized.

### Lời nói

“Bản secure dùng `bleach.clean` với allowlist. Thẻ `strong` được phép nên vẫn hiển thị. Thẻ `img` và event handler `onerror` không được phép nên bị loại trước khi render.

Database có thể vẫn giữ raw input để phục vụ lab, nhưng nội dung đưa ra browser phải là giá trị đã sanitize.”

## 4.8. Trả lời câu hỏi Stored XSS

- Vì sao Stored XSS nguy hiểm hơn Reflected XSS?  
  Payload được lưu và tự phát lại cho nhiều phiên hoặc nhiều người xem. Attacker không cần gửi URL riêng cho từng nạn nhân.

- Payload có ảnh hưởng mọi người xem trang không?  
  Có, khi mọi người nhận cùng dữ liệu stored chưa được encode hoặc sanitize.

- Cookie không có HttpOnly có rủi ro gì?  
  JavaScript từ XSS có thể đọc cookie không-HttpOnly. HttpOnly chỉ giảm hậu quả, không vá lỗi XSS.

---

# 5. Demo DOM-based XSS

## 5.1. Mục tiêu

Chứng minh payload nằm trong URL fragment, không được gửi tới server. JavaScript phía client đọc `location.hash` rồi đưa dữ liệu vào `innerHTML`.

## 5.2. Route

- Có lỗi: `http://127.0.0.1:5000/vulnerable/dom-search`
- Đã vá: `http://127.0.0.1:5000/secure/dom-search`

## 5.3. Bước 1: Thử fragment bình thường

### Thao tác

1. Mở route vulnerable.
2. Trong thanh địa chỉ, thêm:

```text
#laptop
```

3. Nhấn Enter.
4. Quan sát nội dung `laptop` xuất hiện trên trang.
5. Trong Network, bấm Clear trước khi thay đổi hash lần nữa.
6. Đổi `#laptop` thành `#phone`.
7. Quan sát trang đổi nhưng không có request document mới.

### Lời nói

“Phần sau dấu `#` gọi là URL fragment. Browser giữ fragment ở phía client. Khi fragment thay đổi, browser không cần gửi request mới tới server.”

## 5.4. Bước 2: Gửi payload trong fragment

### Payload

```html
#<img src=x onerror="alert('DOM XSS')">
```

### Thao tác

1. Xóa Network và timeline cũ.
2. Dán fragment payload vào cuối URL.
3. Nhấn Enter.
4. Khi alert xuất hiện, bấm `OK`.
5. Quan sát Network không có request document chứa fragment.
6. Mở Elements và tìm `onerror`.
7. Mở tab `Source → Sink`.
8. Mở `So sánh mã`.

### Lời nói

“Payload không đi tới Flask. JavaScript đã có sẵn trong trang đọc `location.hash`, decode giá trị rồi gán vào `innerHTML`.

`innerHTML` yêu cầu browser phân tích chuỗi như HTML. Vì vậy payload trở thành node `img` và `onerror` chạy.”

## 5.5. Giải thích Source → Sink

### Code vulnerable

```javascript
const raw = location.hash.slice(1);
const value = decodeURIComponent(raw);
result.innerHTML = value;
```

### Luồng

```text
URL fragment
→ location.hash
→ decodeURIComponent
→ result.innerHTML
→ browser tạo img
→ onerror chạy
```

### Lời nói

“Source là `location.hash`. Sink là `innerHTML`. Server không cần phản chiếu hay lưu payload. Lỗi xảy ra hoàn toàn trong JavaScript phía browser.”

## 5.6. Kiểm chứng fragment không lên server

### Thao tác

1. Trong Network, chọn request document ban đầu.
2. Mở Headers.
3. Chỉ ra Request URL không chứa phần sau dấu `#`.
4. Đổi fragment thêm một lần và chỉ ra không có request document mới.

### Lời nói

“Fragment không nằm trong HTTP request. Server không nhìn thấy payload. Đây là điểm phân biệt DOM-based XSS với Reflected và Stored XSS.”

## 5.7. Kiểm chứng bản secure

### Thao tác

1. Mở route secure.
2. Dùng cùng fragment payload.
3. Quan sát không có alert.
4. Kiểm tra payload hiển thị như văn bản.
5. Trong Elements, kiểm tra không có node `img` do fragment tạo.
6. Mở `So sánh mã`.

### Code secure

```javascript
const raw = location.hash.slice(1);
const value = decodeURIComponent(raw);
result.textContent = value;
```

### Lời nói

“Bản secure thay `innerHTML` bằng `textContent`. `textContent` tạo text node và không phân tích chuỗi như HTML. Vì vậy fragment vẫn được hiển thị, nhưng không tạo element hoặc event handler.”

---

# 6. So sánh ba loại XSS

| Loại | Source | Nơi payload tồn tại | Sink chính | Ai bị ảnh hưởng |
|---|---|---|---|---|
| Reflected | Query `q` | Request và response hiện tại | HTML render qua `Markup(q)` | Người mở URL chứa payload |
| Stored | Comment form | SQLite `comments.body` | HTML render sau khi đọc DB | Mọi người xem trang chứa payload |
| DOM-based | `location.hash` | URL fragment phía client | `innerHTML` | Người mở URL fragment |

### Lời kết

“Ba loại XSS đều có cùng bản chất: dữ liệu không đáng tin đi vào một sink khiến browser hiểu dữ liệu là mã.

- Reflected được phản chiếu trong một request.
- Stored được lưu rồi phát lại.
- DOM-based diễn ra hoàn toàn ở browser.”

---

# 7. Trả lời 5 câu hỏi báo cáo Lab01

## 1. So sánh Reflected, Stored và DOM-based XSS

Reflected tồn tại trong request và response hiện tại. Stored được lưu ở server rồi phát lại. DOM-based đi từ DOM source tới DOM sink trong JavaScript phía client.

## 2. Vì sao validate input chưa đủ?

Validation kiểm tra dữ liệu có đúng yêu cầu nghiệp vụ. Một chuỗi hợp lệ vẫn nguy hiểm khi được đặt vào HTML, JavaScript, URL hoặc attribute. Output encoding hoặc safe DOM API vẫn bắt buộc.

## 3. Vì sao cần output encoding?

Output encoding biến ký tự cú pháp thành dữ liệu. Browser không tạo thẻ hoặc event handler từ input.

## 4. CSP có thay thế sửa code không?

Không. CSP là lớp giảm khả năng thực thi và giảm hậu quả. Source-to-sink không an toàn vẫn phải được sửa.

## 5. Cách vá từng lỗi

- Reflected XSS: bỏ `Markup(q)`, dùng Jinja autoescape theo đúng context.
- Stored XSS: sanitize bằng allowlist đáng tin cậy hoặc encode khi render.
- DOM-based XSS: dùng `textContent` hoặc DOM API an toàn thay `innerHTML`.

---

# 8. Kết thúc Lab01

### Lời nói

“Kết luận của Lab01 là không tin dữ liệu từ URL, form, database hoặc DOM source.

Bản vá phải nằm đúng sink:

- HTML server-rendered dùng contextual output encoding.
- Rich HTML stored dùng sanitization theo allowlist.
- DOM text dùng `textContent`.

CSP và cookie flags là defense in depth, không thay bản vá gốc.”
