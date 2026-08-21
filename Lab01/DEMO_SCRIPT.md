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
- Reset khi cần: chạy `python -X utf8 seed.py` tại `Lab01`; hoặc dùng nút `Reset database` trên trang bình luận. `-X utf8` tránh lỗi mã hóa output trong PowerShell sau khi seed đã chạy.
- Không cần tài khoản.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`; nếu DevTools mở ở dưới, bấm menu ba chấm → `Dock side` → chọn biểu tượng dock bên phải.
- Bấm tab `Network`, tích `Preserve log` và `Disable cache`, bấm biểu tượng thùng rác `Clear`. Khi cần tìm request, gõ một phần URL vào ô `Filter`, ví dụ `vulnerable/search`.
- Bấm đúng dòng request trong bảng Network. Sau khi bấm, nhìn `Headers` → `General` → `Request Method` để chắc chắn đã chọn đúng GET/POST; nếu không đúng, đóng pane hoặc chọn dòng kế tiếp.
- Với request GET, bằng chứng query luôn nằm trong `Headers` → `General` → `Request URL`, ở phần sau dấu `?` (ví dụ `?q=...`). Một số bản Chrome không hiện mục `Query String Parameters`; nếu không thấy mục này thì không tìm tiếp, dùng `Request URL` làm bằng chứng. Chỉ bấm `Query String Parameters` khi mục đó thực sự xuất hiện.
- Với request POST, bấm `Payload` → `Form Data`; với cả GET/POST có thể bấm `Response` hoặc `Preview` để xem kết quả.
- Để tìm bằng chứng trong response, trước hết chọn đúng request rồi bấm `Response` → nhấn `Ctrl+F` theo marker của scenario: vulnerable reflected dùng raw `<img src=x`, secure reflected dùng `&lt;img`, vulnerable stored dùng raw `<img src=x`, secure stored dùng `Xin chào` hoặc `&lt;img`. Exact `alert('Reflected XSS')` không phải marker ổn định của secure response vì Jinja encode dấu nháy thành entity; không tìm `onerror` một mình vì template/mã mẫu có thể chứa nhiều occurrence.
- Nếu cần kiểm tra DOM, bấm tab `Elements` → nhấn `Ctrl+F` → nhập nguyên chuỗi như `alert('Reflected XSS')` hoặc `src=x`; bấm kết quả có breadcrumb nằm trong vùng kết quả/bình luận. Nếu có nhiều kết quả, nhấn `Enter` để chuyển từng kết quả và chọn node trong vùng demo, không chọn script/mã mẫu.
- Alert là hộp thoại của browser, không nhất thiết xuất hiện thành một dòng trong `Console`. Nếu alert đang che trang, bấm `OK` sau khi người xem nhìn thấy; sau đó dùng `Elements` và `Response` làm bằng chứng chính.
- `Sources` mở file JavaScript bằng `Ctrl+P` → gõ tên file → `Enter`, rồi `Ctrl+F` tìm `innerHTML` hoặc `textContent`. `Database`/`Action Timeline` là panel của Lab01 trên trang, không phải tab F12.


## Kịch bản trình bày

*Quy ước bằng chứng: mỗi mục dưới đây đi theo đúng thứ tự `Thao tác → Nói khi demo → F12 show → Quan sát`. Các kết quả kỳ vọng chỉ được gọi là “đã quan sát” sau khi lần chạy live xác nhận.*

**Bước 1 — Xác lập input bình thường và Reflected XSS**

1. **Thao tác:** Mở `http://127.0.0.1:5000`. Trong thẻ `Reflected XSS`, bấm nút `Có lỗ hổng`.
   - **Nói khi demo:** “Tôi mở đúng flow Reflected XSS vulnerable để theo dõi input đi từ form tới response.”
   - **F12 show:** Nhấn `F12` → bấm `Network` → bấm thùng rác `Clear`; bật `Preserve log` và `Disable cache`. Chưa cần chọn request; chỉ để Network sẵn sàng bắt lần gửi tiếp theo.
   - **Quan sát:** Form tìm kiếm vulnerable xuất hiện; không kết luận về request trước khi gửi input.

2. **Thao tác:** Bấm ô placeholder `Tìm sản phẩm`, nhấn `Ctrl+A`, nhập `laptop`, rồi bấm `Tìm kiếm`.
   - **Nói khi demo:** “Tôi gửi một giá trị bình thường trước để có baseline, rồi mới thay bằng payload.”
   - **F12 show:** Trong Network, ô `Filter` gõ `vulnerable/search` → bấm dòng mới nhất sau lần submit. Bấm `Headers` → `General` → chỉ `Request Method=GET` và `Request URL`; kiểm tra phần sau `?q=` thay vì dựa vào cột Name của DevTools.
   - **Quan sát:** Response/trang trả kết quả bình thường; đây là request baseline để so sánh với dòng payload.

3. **Thao tác:** Bấm lại ô `Tìm sản phẩm`, nhấn `Ctrl+A`, nhập `<img src=x onerror="alert('Reflected XSS')">`, rồi bấm `Tìm kiếm` lần nữa.
   - **Nói khi demo:** “Cùng một source `q`, nhưng lần này tôi kiểm tra browser nhận chuỗi như văn bản hay diễn giải nó thành HTML.”
   - **F12 show:** Trong Network vẫn lọc `vulnerable/search` → bấm dòng mới nhất sau lần submit. Vào `Headers` → `General` → chỉ `Request URL` và phần `?q=`; nếu Chrome không có `Query String Parameters` thì không tìm mục đó. Bấm `Response` → `Ctrl+F` → nhập `<img src=x`; chọn occurrence trong `<section class="result">` có `onerror="alert('Reflected XSS')"`, không chọn payload mẫu an toàn.
   - **Quan sát:** URL có thể mã hóa bằng `%3Cimg`, `+`, `%27`; đó vẫn là payload. Response có thể còn raw HTML.

4. **Thao tác:** Giữ alert trên màn hình cho người xem nhìn thấy; sau đó bấm `OK` nếu browser hiện hộp thoại.
   - **Nói khi demo:** “Alert là bằng chứng runtime; sau khi người xem thấy nó, tôi mở DOM để chỉ chính xác node đã được tạo.”
   - **F12 show:** Sau khi bấm `OK`, chọn `Elements` → nhấn `Ctrl+F` → nhập `alert('Reflected XSS')` (fallback `src=x`). Nhấn `Enter` qua các kết quả; chọn breadcrumb kết thúc bằng `img` trong vùng kết quả. Bấm `Console` chỉ để ghi log/error nếu có; Console trống không phủ nhận alert.
   - **Quan sát:** Nếu có node `img` và handler đúng trong Elements thì ghi nhận bằng chứng DOM live; nếu alert không xuất hiện, chỉ báo những gì Response/Elements thực tế cho thấy.
**Kết luận:** `q` là source; output chưa encode và `Markup(q)` đưa input vào HTML sink.

**Bước 2 — Vá Reflected XSS bằng output encoding**

1. **Thao tác:** Từ trang vulnerable bấm link `So sánh bản vá`; nếu không thấy, về `http://127.0.0.1:5000` và trong thẻ `Reflected XSS` bấm `Đã vá`.
   - **Nói khi demo:** “Tôi chuyển sang secure route nhưng giữ nguyên payload để so sánh công bằng.”
   - **F12 show:** Trong `Network` bấm `Clear` → ô `Filter` gõ `secure/search`. Giữ `Preserve log` để chỉ request của secure flow.
   - **Quan sát:** Trang secure và form tìm kiếm xuất hiện.

2. **Thao tác:** Bấm ô `Tìm sản phẩm`, nhấn `Ctrl+A`, nhập lại `<img src=x onerror="alert('Reflected XSS')">`, rồi bấm `Tìm kiếm`.
   - **Nói khi demo:** “Input không đổi; thay đổi nằm ở sink xử lý output.”
   - **F12 show:** Bấm dòng mới nhất có `Request URL` chứa `secure/search?q=` → `Headers` → `General` → chỉ `Request Method=GET` và `Request URL`. Nếu có `Query String Parameters` thì chỉ `q`; nếu không có, Request URL là bằng chứng chính.
   - **Quan sát:** Request secure vẫn nhận cùng query; không suy ra an toàn chỉ từ việc URL giống nhau.

3. **Thao tác:** Khi trang trả kết quả, cuộn tới vùng kết quả và chỉ ra payload đang hiện như chữ.
   - **Nói khi demo:** “Autoescape biến ký tự điều khiển thành text; browser không còn tạo thẻ HTML từ input.”
   - **F12 show:** Bấm `Response` → `Ctrl+F` → nhập `&lt;img`; chọn occurrence trong section `Payload hiển thị như văn bản`. Không tìm exact `alert('Reflected XSS')` trong raw Response: autoescape encode dấu nháy thành `&#34;`/`&#39;`. Sau đó bấm `Elements` → `Ctrl+F` → tìm `Reflected XSS` và chọn text node/span/div trong vùng output, không chọn `img`.
   - **Quan sát:** Raw Response có dạng `&lt;img` và entity cho dấu nháy; Elements không có node `img` do payload tạo.
**Kết luận:** Fix chính là context-aware output encoding/autoescape tại sink.

**Bước 3 — Chứng minh Stored XSS tồn tại sau reload**

1. **Thao tác:** Về `http://127.0.0.1:5000`. Trong thẻ `Stored XSS`, bấm `Có lỗ hổng`.
   - **Nói khi demo:** “Tôi dùng flow lưu bình luận vulnerable để chứng minh payload có thể tồn tại sau lần gửi.”
   - **F12 show:** Bấm `Network` → `Clear`; giữ `Preserve log`. Ô `Filter` gõ `comments` trước khi submit.
   - **Quan sát:** Form tên và bình luận xuất hiện.

2. **Thao tác:** Nhập tên `Kiểm thử`; trong ô `Bình luận` nhập `<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>`.
   - **Nói khi demo:** “Dữ liệu này sẽ được lưu vào body; tôi không mở cookie hay thông tin ngoài payload.”
   - **F12 show:** Chưa cần chọn request; chuẩn bị để sau submit bấm request mới. Nếu muốn kiểm tra sau khi gửi, mở `Payload` → `Form Data` và chỉ hai field `author`, `body`.
   - **Quan sát:** Hai ô giữ đúng payload; không gọi là đã lưu trước khi submit thành công.

3. **Thao tác:** Bấm `Đăng bình luận`. Nếu alert xuất hiện, ghi nhận rồi bấm `OK`.
   - **Nói khi demo:** “POST này là thời điểm payload đi vào database.”
   - **F12 show:** Trong Network bấm request mới xuất hiện ngay sau click → `Headers` → `General` xác nhận `Request Method=POST` và URL `/vulnerable/post/1/comments` → `Payload` → `Form Data` chỉ `author=Kiểm thử` và `body`. Không mở raw cookie.
   - **Quan sát:** Ghi status và response live; chỉ nói POST đã lưu khi response/trace xác nhận.

4. **Thao tác:** Nhấn `Ctrl+R`, cuộn xuống danh sách bình luận, rồi mở trace tab `Database`.
   - **Nói khi demo:** “Sau reload, tôi kiểm tra cả raw database value và HTML được render lại.”
   - **F12 show:** Với `Preserve log` vẫn bật, bấm request mới nhất có `Request Method=GET` và URL `/vulnerable/post/1/comments` → `Response` → `Ctrl+F` → tìm nguyên cụm `alert('Stored XSS')`, fallback `Xin chào`. Sau đó bấm `Elements` → `Ctrl+F` → tìm `alert('Stored XSS')`; chọn breadcrumb kết thúc bằng `img` trong danh sách bình luận.
   - **Quan sát:** Nếu response/DOM có payload và alert/node live thì ghi nhận Stored XSS; trace `Database` chỉ raw `comments.body`.
**Kết luận:** Lưu vào database không làm input an toàn; raw HTML sink có thể phát lại payload sau mỗi reload.

**Bước 4 — Vá Stored XSS bằng allowlist sanitization**

1. **Thao tác:** Từ vulnerable bấm `So sánh bản vá`; hoặc về trang chủ và trong thẻ `Stored XSS` bấm `Đã vá`.
   - **Nói khi demo:** “Tôi chuyển sang secure comment route và vẫn dùng cùng payload.”
   - **F12 show:** Bấm `Network` → `Clear`; ô `Filter` gõ `secure/post/1/comments`.
   - **Quan sát:** Form secure xuất hiện.

2. **Thao tác:** Nhập tên `Kiểm thử`, nhập lại đúng payload Bước 3, rồi bấm `Đăng bình luận`.
   - **Nói khi demo:** “Secure vẫn nhận dữ liệu nghiệp vụ, nhưng sẽ làm sạch tại ranh giới HTML.”
   - **F12 show:** Bấm request mới nhất → `Headers` → `General` xác nhận `Request Method=POST` → `Payload` → `Form Data` chỉ payload giống Bước 3.
   - **Quan sát:** Ghi status/response live; không gọi sanitizer thành công nếu chưa xem output.

3. **Thao tác:** Nhấn `Ctrl+R`, cuộn tới bình luận vừa gửi và mở trace tab `Database` rồi `Source → Sink`.
   - **Nói khi demo:** “Tôi tách raw database value khỏi output đã sanitize để chỉ ra vị trí fix.”
   - **F12 show:** Bấm `Response` → `Ctrl+F` → tìm `Xin chào` hoặc `&lt;img`; không dùng exact `alert('Stored XSS')` trong raw Response vì phần raw DB được HTML-escape. Bấm `Elements` → `Ctrl+F` → tìm `Xin chào` và chọn occurrence trong subtree bình luận; breadcrumb có thể là `strong`. Tìm tiếp `Stored XSS` nếu cần; không tìm `onerror` một mình.
   - **Quan sát:** Ghi đúng live output: `strong` chỉ còn nếu allowlist cho phép; handler không được gọi khi không có bằng chứng.
**Kết luận:** Sanitize allowlist ở output là fix XSS; parameterized INSERT chỉ giải quyết SQL.

**Bước 5 — Chứng minh DOM-based XSS không cần request chứa payload**

1. **Thao tác:** Về `http://127.0.0.1:5000`. Trong thẻ `DOM-based XSS`, bấm `Có lỗ hổng`.
   - **Nói khi demo:** “DOM XSS lấy source từ phía client; tôi mở flow để theo dõi fragment.”
   - **F12 show:** Bấm `Network` → `Clear` trước khi nhập; sau này chỉ quan sát request phát sinh sau nút.
   - **Quan sát:** Ô fragment và vùng kết quả xuất hiện.

2. **Thao tác:** Bấm ô fragment, nhấn `Ctrl+A`, nhập `<img src=x onerror="alert('DOM XSS')">`.
   - **Nói khi demo:** “Payload đang nằm sau dấu #; phần này chưa được gửi lên server.”
   - **F12 show:** Network chưa cần chọn request. Sau khi click nút, dùng `Headers` → `General` → `Request URL` của document để chỉ URL không chứa phần sau `#`.
   - **Quan sát:** Thanh địa chỉ có fragment; không gọi đây là request query.

3. **Thao tác:** Bấm `Thay fragment không reload`; không nhấn Enter và không tải lại trang.
   - **Nói khi demo:** “JavaScript đọc location.hash rồi đưa giá trị vào innerHTML ngay trong browser.”
   - **F12 show:** Trong Network chỉ nhìn các dòng phát sinh sau click; xác nhận không có request mới chứa payload fragment. Bấm `Sources` → `Ctrl+P` → gõ `dom_vulnerable.js` → `Enter` → `Ctrl+F` tìm chính xác `result.innerHTML`.
   - **Quan sát:** DOM cập nhật mà không cần request mới; alert có thể xuất hiện live.

4. **Thao tác:** Nếu alert hiện, bấm `OK`; sau đó chỉ vào vùng kết quả và node mới trong `Elements`.
   - **Nói khi demo:** “Bằng chứng chính nằm ở DOM node, không phải Console.”
   - **F12 show:** `Elements` → `Ctrl+F` → nhập `alert('DOM XSS')` hoặc `DOM XSS`; nhấn `Enter` qua kết quả và chọn node trong vùng fragment, breadcrumb kết thúc bằng `img` nếu đã tạo thẻ. `Console` chỉ là thông tin phụ.
   - **Quan sát:** Ghi alert/node thực tế; nếu không có thì không tuyên bố JavaScript đã chạy.
**Kết luận:** Source là URL fragment, sink là JavaScript `innerHTML`; server-side escaping không đủ.

**Bước 6 — Vá DOM-based XSS bằng `textContent`**

1. **Thao tác:** Từ trang DOM vulnerable bấm `So sánh bản vá`; nếu không thấy, về trang chủ và trong thẻ `DOM-based XSS` bấm `Đã vá`.
   - **Nói khi demo:** “Tôi chuyển sang secure DOM sink và giữ nguyên payload.”
   - **F12 show:** Bấm `Network` → `Clear`; ô fragment vẫn là input chuẩn bị cho flow secure.
   - **Quan sát:** Trang secure xuất hiện.

2. **Thao tác:** Nhập lại `<img src=x onerror="alert('DOM XSS')">` rồi bấm `Thay fragment không reload`.
   - **Nói khi demo:** “Secure dùng textContent nên chuỗi được đặt thành text node, không được diễn giải thành HTML.”
   - **F12 show:** Bấm `Sources` → `Ctrl+P` → gõ `dom_secure.js` → `Enter` → `Ctrl+F` tìm `result.textContent` hoặc `textContent`. Network vẫn không có request chứa fragment.
   - **Quan sát:** Không có alert; vùng kết quả hiển thị payload như chữ.

3. **Thao tác:** Chỉ vào vùng kết quả và mở trace tab `Source → Sink` nếu có.
   - **Nói khi demo:** “Tôi chốt bằng DOM: cùng input nhưng không có node img.”
   - **F12 show:** `Elements` → `Ctrl+F` → nhập `alert('DOM XSS')` hoặc `src=x`; chọn occurrence trong vùng secure. Breadcrumb phải là text node/span/div, không phải `img`; nếu 0 kết quả cho handler exact thì chỉ nói “không thấy handler này”.
   - **Quan sát:** Payload là text, không có node thực thi.
**Kết luận:** Fix DOM XSS là dùng API text-safe như `textContent` hoặc sanitize đúng context, không đưa input không tin cậy vào `innerHTML`.

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
- Nếu dữ liệu bình luận làm rối lần demo, dừng app, chạy `python -X utf8 seed.py` trong `Lab01`, rồi khởi động lại.
- Nếu alert bị trình duyệt chặn, vẫn kiểm tra Response/Elements/Console; không tuyên bố JavaScript đã chạy khi chưa thấy bằng chứng live.
- Nếu trace/Database Inspector trống, reload đúng route và ghi “chưa có bằng chứng runtime”, không tự điền kết quả.

## Chốt lab

Root cause: dữ liệu không tin cậy đi vào HTML/DOM sink như `Markup`, raw body, `innerHTML`.
Primary fix: output encoding, allowlist sanitization và `textContent` đúng context.
Defense in depth: CSP, HttpOnly, SameSite, security headers và kiểm thử source → sink.
