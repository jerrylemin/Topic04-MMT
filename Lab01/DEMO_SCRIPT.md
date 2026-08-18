# Demo script Lab01 — XSS

## Mục tiêu demo

- Chứng minh đường đi source → sink của Reflected, Stored và DOM-based XSS.
- Dùng cùng payload để đối chiếu bản vulnerable và secure.
- Phân biệt output encoding/sanitization với CSP và HttpOnly.
- Ghi nhận alert, HTML/DOM, SQLite và trace đúng theo lần chạy live.

## Chuẩn bị

- Thư mục làm việc: `cd Lab01`
- Khởi động: `scripts\run_lab.bat`
- URL: `http://127.0.0.1:5000`
- Reset khi cần: `python seed.py` tại `Lab01`; hoặc dùng nút `Reset database` trên trang bình luận.
- Không cần tài khoản.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`, dock DevTools bên phải; trong `Network` bật `Preserve log` và `Disable cache`, trước mỗi flow bấm `Clear`.
- `Network`: show request document/POST, `Headers` hoặc `Payload`, rồi `Response`; dùng bộ lọc `Doc` khi cần request trang.
- `Elements`: dùng `Ctrl+F` tìm `onerror`, `<img>` hoặc vùng kết quả để chứng minh browser tạo node hay chỉ tạo text.
- `Sources`/`Console`: mở file `static/js/dom_vulnerable.js` hoặc `dom_secure.js` để chỉ ra `innerHTML`/`textContent`; Console chỉ show alert nếu lần chạy live thật sự có alert.
- `Database Inspector` và `Action Timeline` là panel của Lab01, không phải tab F12; mở chúng sau khi đã chụp request/response làm bằng chứng.

## Kịch bản trình bày

*Quy ước bằng chứng: các dòng “Quan sát” là kết quả cần xác nhận trong lần chạy live; không gọi kết quả kỳ vọng là đã quan sát.*

**Bước 1 — Xác lập input bình thường và Reflected XSS**

* Thao tác:
  1. Mở `http://127.0.0.1:5000`. Trong thẻ `Reflected XSS`, bấm nút `Có lỗ hổng`.
  2. Bấm vào ô có placeholder `Tìm sản phẩm`, nhấn `Ctrl+A`, nhập `laptop`, rồi bấm `Tìm kiếm`.
  3. Bấm lại ô `Tìm sản phẩm`, nhấn `Ctrl+A`, nhập `<img src=x onerror="alert('Reflected XSS')">`, rồi bấm `Tìm kiếm` lần nữa.
  4. Giữ alert trên màn hình để chỉ vào bằng chứng, sau đó mới bấm `OK` nếu browser hiện hộp thoại.
* Nói: “Query `q` đi từ form vào response. Với payload, tôi kiểm tra xem browser nhận văn bản hay tạo HTML.”
* Quan sát: Network có request `GET /vulnerable/search?q=...`; lần payload có thể hiện alert, Response còn `onerror`, và Elements có node `img` do input tạo.
* F12 show: `Network → request document → Headers/Query String Parameters` để chỉ `q`; `Response` tìm `onerror`; `Elements` tìm node `img`; `Console` chỉ ra alert nếu đã chạy live.
* Kết luận: `q` là source; output chưa encode và `Markup(q)` đưa input vào HTML sink.

**Bước 2 — Vá Reflected XSS bằng output encoding**

* Thao tác:
  1. Từ trang vulnerable, bấm link `So sánh bản vá`; nếu link không còn trên màn hình, về `http://127.0.0.1:5000` và trong thẻ `Reflected XSS` bấm `Đã vá`.
  2. Bấm ô `Tìm sản phẩm`, nhấn `Ctrl+A`, nhập đúng `<img src=x onerror="alert('Reflected XSS')">`, rồi bấm `Tìm kiếm`.
  3. Khi trang trả kết quả, cuộn tới phần kết quả để chỉ ra payload đang hiển thị như chữ, không phải HTML chạy được.
* Nói: “Input không đổi; chỉ sink thay đổi. Bản secure để Jinja autoescape dữ liệu thay vì đánh dấu input là safe.”
* Quan sát: không có alert; Response chứa dạng escaped như `&lt;img`; Elements hiển thị payload như text, không có node `img` do input tạo.
* F12 show: cùng request tại `/secure/search`; `Response` tìm `&lt;img` thay vì raw `<img>`; `Elements` chọn vùng kết quả và chỉ ra text node, không có node `img`.
* Kết luận: fix chính là context-aware output encoding/autoescape tại sink.

**Bước 3 — Chứng minh Stored XSS tồn tại sau reload**

* Thao tác:
  1. Về `http://127.0.0.1:5000`. Trong thẻ `Stored XSS`, bấm `Có lỗ hổng`.
  2. Bấm ô `Tên`, nhấn `Ctrl+A`, nhập `Kiểm thử`; bấm ô `Bình luận`, nhập `<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>`.
  3. Bấm `Đăng bình luận`. Nếu alert xuất hiện, ghi nhận nó rồi bấm `OK`.
  4. Nhấn `Ctrl+R` để tải lại trang, cuộn xuống danh sách bình luận, rồi trong trace panel bấm tab `Database`.
* Nói: “Payload được lưu trước, rồi phát lại cho người xem. Tôi kiểm tra cả giá trị raw trong SQLite và HTML sau khi render.”
* Quan sát: `POST` bình luận ghi payload vào `comments.body`; sau reload alert có thể chạy lại; Elements có `img`/`strong` tương ứng và timeline chỉ ra sink `Markup(row["body"])`.
* F12 show: `Network → POST comment → Payload/Form Data` để show body; request `GET` sau reload; `Elements` tìm `onerror`; sau đó chuyển sang panel `Database Inspector` để show raw `comments.body`.
* Kết luận: lưu vào database không làm input an toàn; sink render raw HTML biến Stored XSS thành lỗi có phạm vi ảnh hưởng rộng.

**Bước 4 — Vá Stored XSS bằng allowlist sanitization**

* Thao tác:
  1. Từ trang vulnerable bấm link `So sánh bản vá`; hoặc về trang chủ và trong thẻ `Stored XSS` bấm `Đã vá`.
  2. Bấm ô `Tên`, nhập `Kiểm thử`; bấm ô `Bình luận`, nhập lại đúng payload của Bước 3, rồi bấm `Đăng bình luận`.
  3. Nhấn `Ctrl+R`, cuộn tới bình luận vừa gửi và mở các tab trace `Database` rồi `Source → Sink` để đối chiếu raw value với output đã lọc.
* Nói: “Bản secure vẫn nhận bình luận nhưng làm sạch tại ranh giới HTML. `<strong>` được giữ nếu thuộc allowlist, còn handler JavaScript bị loại.”
* Quan sát: không có alert; `<img>`/`onerror` không còn là node thực thi; phần `<strong>Xin chào</strong>` chỉ còn nếu sanitizer allowlist hiện tại cho phép.
* F12 show: `Network → POST/GET` để chứng minh cùng payload; `Elements` tìm `strong` và xác nhận không có `img`/`onerror`; panel `Action Timeline` show bước sanitize/secure verdict.
* Kết luận: fix chính là sanitize theo allowlist ở output; parameterized `INSERT` chỉ giải quyết SQL, không giải quyết XSS.

**Bước 5 — Chứng minh DOM-based XSS không cần request chứa payload**

* Thao tác:
  1. Về `http://127.0.0.1:5000`. Trong thẻ `DOM-based XSS`, bấm `Có lỗ hổng`.
  2. Bấm ô fragment, nhấn `Ctrl+A`, nhập `<img src=x onerror="alert('DOM XSS')">`.
  3. Bấm `Thay fragment không reload`. Không nhấn Enter và không tải lại trang, vì mục tiêu là chứng minh thay đổi DOM phía client.
  4. Giữ nguyên URL có phần sau dấu `#`, rồi chỉ vào vùng kết quả và node mới trong Elements.
* Nói: “Fragment sau dấu `#` do browser giữ ở client. JavaScript đọc `location.hash`, decode rồi đưa thẳng vào `innerHTML`.”
* Quan sát: payload không xuất hiện trong request Network; nếu live chạy đúng, alert xuất hiện và Elements có node `img`; source code/trace chỉ ra sink `result.innerHTML=value`.
* F12 show: `Network` không có fragment sau dấu `#`; `Sources` mở `static/js/dom_vulnerable.js` và tìm `result.innerHTML`; `Elements` tìm node `img`; `Console` show alert nếu live.
* Kết luận: source nằm ở URL fragment và sink nằm trong JavaScript browser, nên server-side escaping không đủ để vá DOM sink.

**Bước 6 — Vá DOM-based XSS bằng `textContent`**

* Thao tác:
  1. Từ trang DOM vulnerable bấm link `So sánh bản vá`; nếu không thấy link, về trang chủ và trong thẻ `DOM-based XSS` bấm `Đã vá`.
  2. Bấm ô fragment, nhấn `Ctrl+A`, nhập lại `<img src=x onerror="alert('DOM XSS')">`, rồi bấm `Thay fragment không reload`.
  3. Chỉ vào vùng kết quả để chứng minh payload hiện như text; mở trace tab `Source → Sink` nếu có để đối chiếu sink secure.
* Nói: “Bản secure không biến chuỗi thành HTML. `textContent` tạo text node nên cùng input không còn là markup.”
* Quan sát: không có alert; payload hiện như chữ trong vùng kết quả; không có node `img` do fragment tạo.
* F12 show: `Sources` mở `static/js/dom_secure.js` và tìm `textContent`; `Elements` chọn vùng kết quả để show text node; `Network` vẫn không có fragment.
* Kết luận: fix chính của DOM XSS là dùng API text-safe (`textContent`) hoặc sanitize đúng context, không dùng `innerHTML` cho input không tin cậy.

## Demo Vulnerable → Secure

| Lỗi | Cùng input | Vulnerable → nguyên nhân | Secure → fix chính |
|---|---|---|---|
| Reflected | `<img src=x onerror="alert('Reflected XSS')">` | `/vulnerable/search`, `Markup(q)`, payload thành HTML trong response | `/secure/search`, Jinja autoescape, payload thành text |
| Stored | `<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>` | `/vulnerable/post/1/comments`, raw `comments.body` → `Markup(body)` | `/secure/post/1/comments`, Bleach allowlist loại tag/handler nguy hiểm |
| DOM-based | `#<img src=x onerror="alert('DOM XSS')">` | `location.hash` → `innerHTML` | `location.hash` → `textContent` |

## Câu hỏi trong BaiTapTopic04.docx

**Câu 1. Dữ liệu người dùng được đưa vào HTML ở vị trí nào?**  
**Trả lời khi demo:** Reflected dùng query `q` ở vùng kết quả tìm kiếm. Stored dùng `comments.body` khi trang bình luận render lại; DOM dùng fragment trong `location.hash` để cập nhật vùng kết quả bằng JavaScript.

**Câu 2. Ứng dụng có escape ký tự đặc biệt như `<`, `>`, `"`, `'` không?**  
**Trả lời khi demo:** Sink vulnerable dùng `Markup` nên input không được Jinja autoescape và `<`/`>` vẫn thành markup. Sink secure giữ autoescape hoặc dùng text-safe API, vì vậy payload hiện như văn bản.

**Câu 3. Nếu nạn nhân bấm vào URL có payload thì điều gì xảy ra?**  
**Trả lời khi demo:** Browser gửi request chứa query hoặc tự xử lý fragment. Ở bản vulnerable, payload trở thành HTML/JavaScript trong ngữ cảnh trang và có thể chạy; bản secure chỉ hiển thị text.

**Câu 4. Vì sao Stored XSS nguy hiểm hơn Reflected XSS?**  
**Trả lời khi demo:** Payload Stored được lưu trong SQLite và tự phát lại mỗi lần trang được mở. Người xem không cần bấm đúng URL tấn công nên phạm vi ảnh hưởng có thể rộng hơn.

**Câu 5. Payload có ảnh hưởng tới mọi người dùng xem trang không?**  
**Trả lời khi demo:** Có thể, nếu mọi người cùng nhận trang vulnerable chứa payload và browser thực thi nó. Khi demo, mở lại route bằng tab mới để chứng minh payload đã lưu; chỉ gọi là đã ảnh hưởng khi lần chạy live thực sự cho thấy điều đó.

**Câu 6. Nếu cookie không có thuộc tính HttpOnly, rủi ro là gì?**  
**Trả lời khi demo:** JavaScript chạy trong XSS có thể đọc cookie qua `document.cookie` nếu cookie không có HttpOnly, từ đó làm tăng rủi ro chiếm phiên. HttpOnly là defense in depth, không thay thế việc sửa sink XSS.

**Câu 7. So sánh Reflected XSS, Stored XSS và DOM-based XSS.**  
**Trả lời khi demo:** Reflected đi từ request qua server vào response ngay; Stored đi qua database rồi phát lại; DOM-based đi từ dữ liệu client như fragment tới sink JavaScript. Điểm chung là dữ liệu không tin cậy bị diễn giải như code/HTML.

**Câu 8. Vì sao validate input chưa đủ để chống XSS?**  
**Trả lời khi demo:** Validation khó bao phủ mọi context HTML, attribute, URL và JavaScript. Input có thể hợp lệ theo nghiệp vụ nhưng vẫn nguy hiểm khi được đặt vào sink sai, nên phải encode/sanitize tại output đúng context.

**Câu 9. Vì sao cần output encoding?**  
**Trả lời khi demo:** Encoding làm ký tự điều khiển như `<` thành text trong context đích. Nó giữ được dữ liệu người dùng mà ngăn browser diễn giải dữ liệu đó thành markup hoặc script.

**Câu 10. CSP có thay thế được việc sửa lỗi code không?**  
**Trả lời khi demo:** Không. CSP có thể giảm tác động của một số payload nhưng không loại bỏ source-to-sink sai; primary fix vẫn là output encoding, sanitization hoặc API DOM an toàn.

**Câu 11. Trình bày cách vá từng lỗi trong bài lab.**  
**Trả lời khi demo:** Reflected dùng Jinja autoescape, Stored dùng Bleach allowlist trước khi render, và DOM đổi `innerHTML` thành `textContent`. CSP, HttpOnly, SameSite và security headers chỉ là lớp phòng thủ bổ sung.

## Nếu demo lỗi

- Kiểm tra server đúng `http://127.0.0.1:5000`; nếu chưa chạy, dừng phiên cũ và chạy lại `scripts\run_lab.bat`.
- Nếu dữ liệu bình luận làm rối lần demo, dừng app, chạy `python seed.py` trong `Lab01`, rồi khởi động lại.
- Nếu alert bị trình duyệt chặn, vẫn kiểm tra Response/Elements/Console; không tuyên bố JavaScript đã chạy khi chưa thấy bằng chứng live.
- Nếu trace/Database Inspector trống, reload đúng route và ghi “chưa có bằng chứng runtime”, không tự điền kết quả.

## Chốt lab

Root cause: dữ liệu không tin cậy đi vào HTML/DOM sink như `Markup`, raw body, `innerHTML`.
Primary fix: output encoding, allowlist sanitization và `textContent` đúng context.
Defense in depth: CSP, HttpOnly, SameSite, security headers và kiểm thử source → sink.
