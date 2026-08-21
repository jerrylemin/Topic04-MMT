# Demo script Lab03 — Parameter Tampering

## Mục tiêu demo

- Chứng minh giá, invoice ID và role là dữ liệu client không được tự quyết định.
- So sánh checkout, IDOR và mass assignment bằng cùng request/input ở hai route.
- Quan sát before/after, authorization inspector, database inspector và audit log.
- Phân biệt Parameter Tampering với SQL Injection.

## Chuẩn bị

- Thư mục làm việc: `cd Lab03`
- Khởi động: `scripts\run_lab.bat`
- URL: `http://127.0.0.1:5003`
- Trước mỗi buổi demo, reset bắt buộc bằng `python -X utf8 seed.py` tại `Lab03`; launcher chỉ seed khi `lab03.db` chưa tồn tại. `POST /reset-lab` là route POST cần session, không thay cho việc chuẩn bị seed sạch.
- Tài khoản: `user_a / UserA123!`, `user_b / UserB123!`, `admin / Admin123!`; invoice `1001, 1003` thuộc User A, `1002` thuộc User B.
- Dùng các panel của Lab03: `Action Timeline`, `Database Inspector`, `Authorization Inspector`, `Audit`.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`; bấm `Network`, bật `Preserve log` và `Disable cache`, rồi bấm thùng rác `Clear` trước scenario mới.
- Ở ô `Filter` gõ một phần route như `/login`, `/products`, `/checkout`, `/invoice` hoặc `/profile/update`. Bấm đúng dòng request trong bảng, không chỉ nhìn URL trên thanh địa chỉ.
- Trong pane phải bấm `Headers` → mở `General` để chỉ URL/method/status. Với GET, query chính là phần sau dấu `?` trên dòng `Request URL`; chỉ mở `Query String Parameters` nếu Chrome có hiển thị mục này. Với POST, bấm `Payload` → `Form Data`; bấm `Response` hoặc `Preview` để chỉ kết quả.
- Chỉ checkout/profile vulnerable có hidden field cần sửa: dùng `Elements` → `Ctrl+F` → chọn input nằm trong form có đúng `action`, rồi sửa `value` và kiểm tra lại `Payload`. Secure checkout có ô `price` dạng text trong `<details>`, còn secure profile có ô `role` dạng text trong `<details>`; không gọi hai ô này là hidden.
- Nếu có nhiều form/occurrence, chọn theo `form[action="..."]`, tên field và giá trị trong form đang trình bày; không sửa dòng chữ mẫu hoặc Request Tampering Console khác.
- Trace panel trên trang Lab03 là panel ứng dụng, không phải F12. Sau request, các tab đúng là `Timeline`, `Request`, `Session`, `Database`, `Authorization`, `Audit`, `Code`, `Verdict`; tiêu đề pane gồm `Action Timeline`, `Database Inspector` và `Authorization Inspector`. Trang `/products` không tạo trace panel hoặc `trace_id`.


## Kịch bản trình bày

*Quy ước: đọc từng mục theo thứ tự **Thao tác → Nói khi demo → F12 show → Quan sát**. Khi có nhiều kết quả giống nhau, luôn chọn request/element bằng URL, tên field và giá trị cụ thể.*

### Bước 1 — Đăng nhập và xác lập giá server

1. **Thao tác:** Mở `http://127.0.0.1:5003`, bấm link `Bắt đầu với User A`, rồi tại form `Đăng nhập` nhập username/password.
   - **Nói khi demo:** “Tôi bắt đầu với User A để mọi phép thử checkout và authorization có cùng một session.”
   - **F12 show:** Nhấn `F12` → `Network` → bấm `Clear`; tích `Preserve log` và `Disable cache`. Trong ô `Filter` nhập `/login`.
   - **Quan sát:** Trang `Đăng nhập vào dữ liệu mẫu` xuất hiện; không có control chọn User A, username chỉ được điền trong form.
2. **Thao tác:** Nhập username `user_a`, password `UserA123!` rồi bấm nút đăng nhập.
   - **Nói khi demo:** “Tôi đăng nhập bằng tài khoản lab cố định; password chỉ dùng để nhập, không trình bày ra DevTools.”
   - **F12 show:** Trong Network bấm dòng mới nhất có tên `login` → `Headers` → mở `General`, kiểm tra `Request Method: POST` và status. Bấm `Payload` → `Form Data`, chỉ vào `username=user_a`; che hoặc không mở trường password khi trình bày.
   - **Quan sát:** Ghi status thực tế và session/redirect nếu UI trả về; không kết luận đăng nhập thành công chỉ vì request có status 200.
3. **Thao tác:** Bấm menu `Sản phẩm` để mở trang danh sách sản phẩm.
   - **Nói khi demo:** “Trước khi checkout, tôi lấy giá hiện tại từ response sản phẩm để đối chiếu với giá gửi lên form.”
   - **F12 show:** Đổi ô `Filter` thành `/products` → chọn request GET mới nhất → `Headers` → `General` kiểm tra `Request URL` và status → bấm `Response` hoặc `Preview` → nhấn `Ctrl+F` tìm `USB Security Key` và `ID 5`.
   - **Quan sát:** Chỉ vào sản phẩm ID 5 và giá hiển thị `100,000 VND`. `/products` không có Trace Panel; không tìm `trace_id` ở baseline này.
**Kết luận:** Giá chuẩn phải được xác lập từ dữ liệu server/product response trước khi kiểm tra checkout.

### Bước 2 — Vulnerable checkout nhận `price=1`

1. **Thao tác:** Mở trang checkout vulnerable, chọn sản phẩm ID 5 và để Quantity là 1.
   - **Nói khi demo:** “Tôi mở checkout vulnerable và giữ product_id=5, quantity=1 để chỉ thay đổi trường price.”
   - **F12 show:** Nhấn `F12` → `Elements` → nhấn `Ctrl+F` → nhập chính xác `name="price"`. Nếu có nhiều kết quả, bấm Enter để chuyển từng kết quả và chọn dòng trong form checkout có dạng input hidden với `name="price"` và `value="100000"`; bỏ qua ô hiển thị giá, ví dụ mẫu trong script và các form khác.
   - **Quan sát:** Trước khi sửa phải nhìn thấy đúng giá trị hidden là 100000; nếu không thấy, quay lại đúng form checkout.
2. **Thao tác:** Trong dòng DOM vừa chọn, bấm đúp vào giá trị của thuộc tính `value`, nhấn `Ctrl+A`, nhập `1` rồi nhấn `Enter`.
   - **Nói khi demo:** “Tôi chỉ sửa giá trị hidden trong DOM của request hiện tại; đây là bằng chứng client có thể gửi giá giả, chưa phải server đã chấp nhận.”
   - **F12 show:** Vẫn ở `Elements`, nhìn ngay trên dòng input đã chọn để xác nhận `name="price" value="1"`. Không sửa dòng có giá hiển thị hoặc kết quả mẫu khác; nếu mất node, nhấn `Ctrl+F` tìm lại `name="price"` và chọn occurrence có `value="1"` trong form checkout.
   - **Quan sát:** UI có thể vẫn hiển thị giá 100000 dù hidden value đã là 1; đó là lý do phải kiểm tra Payload sau submit.
3. **Thao tác:** Bấm nút checkout vulnerable/submit đơn hàng.
   - **Nói khi demo:** “Bây giờ tôi gửi request với price=1 và kiểm tra server dùng giá nào để tính.”
   - **F12 show:** Bấm `Network` → trong ô `Filter` nhập `/vulnerable/checkout` → chọn request mới nhất có tên/URL chứa endpoint. Bấm `Headers` → `General` kiểm tra `POST` và status → `Payload` → `Form Data`, chỉ vào `product_id=5`, `quantity=1` và `price=1`.
   - **Quan sát:** Nếu Payload không có price=1, thao tác sửa DOM chưa áp dụng hoặc chọn nhầm form; không kết luận từ màn hình checkout.
4. **Thao tác:** Mở `Response`/`Preview` của request và cuộn `Trace Panel` đến `Database Inspector`/`Audit`.
   - **Nói khi demo:** “Tôi đối chiếu input client với phép tính và bản ghi server để xem giá có bị tin tưởng hay không.”
   - **F12 show:** Trong `Response` nhấn `Ctrl+F` tìm `price`, `total` hoặc `accepted`; nếu nhiều occurrence, chọn đoạn gần object/order vừa tạo, có cả product ID hoặc order ID. Không chọn chữ `price` trong menu/hướng dẫn HTML.
   - **Quan sát:** Ghi giá/total và bản ghi Database/Audit thật sự hiển thị.
**Kết luận:** Vulnerable checkout nhận giá từ client; hidden field không phải ranh giới tin cậy.

### Bước 3 — Secure checkout với cùng `price=1`

1. **Thao tác:** Mở checkout secure, chọn lại sản phẩm ID 5 và Quantity là 1.
   - **Nói khi demo:** “Tôi lặp lại đúng dữ liệu để phép so sánh chỉ khác ở server-side validation.”
   - **F12 show:** `Network` → bấm `Clear` → ô `Filter` tạm nhập `/secure/checkout`. Trong `Elements`, nhấn `Ctrl+F` tìm `name="price"`; chọn đúng input hidden trong form secure có value 100000, không chọn hidden input của form vulnerable còn trong DOM.
   - **Quan sát:** Đúng form secure và đúng product ID 5 được chọn.
2. **Thao tác:** Sửa đúng thuộc tính `value` của input hidden từ `100000` thành `1` rồi nhấn `Enter`.
   - **Nói khi demo:** “Client vẫn có thể gửi price=1, nên secure không được chứng minh bằng việc ẩn field.”
   - **F12 show:** Ngay trên dòng Elements đã chọn, xác nhận `name="price" value="1"`. Nếu có nhiều kết quả, dùng vị trí trong form secure và tên action/form để phân biệt; không dùng occurrence ở phần template mẫu.
   - **Quan sát:** Giá hiển thị và hidden value có thể khác nhau; đây là trạng thái trước submit.
3. **Thao tác:** Bấm submit secure, sau đó mở response và trace.
   - **Nói khi demo:** “Tôi xem server có tính lại giá từ product_id hay từ chối mismatch.”
   - **F12 show:** Network → chọn request mới nhất có URL `/secure/checkout` → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` xác nhận `product_id=5`, `quantity=1`, `price=1` → `Response` → `Ctrl+F` tìm `mismatch`; nếu không có, tìm `100000`. Nếu nhiều occurrence, chọn đoạn JSON/message của checkout secure.
   - **Quan sát:** Đối chiếu status, thông báo mismatch/total và tab `Database`/`Audit`. Không gọi secure nếu request thực tế không chứa price=1.
**Kết luận:** Secure checkout không tin giá hidden từ client; server phải lấy giá chuẩn và kiểm tra mismatch.

### Bước 4 — Vulnerable IDOR invoice

1. **Thao tác:** Mở menu invoice vulnerable và tải invoice với ID `1001`.
   - **Nói khi demo:** “Tôi bắt đầu bằng invoice thuộc phạm vi được mong đợi để có baseline quyền truy cập.”
   - **F12 show:** `Network` → `Clear` → ô `Filter` nhập `/vulnerable/invoice`. Chọn request mới nhất sau khi tải invoice → `Headers` → `General` kiểm tra `Request URL` có `id=1001` và status. Nếu không thấy mục Query String Parameters, dùng chính `Request URL` trong General làm bằng chứng.
   - **Quan sát:** Invoice 1001 và thông tin user/owner hiển thị theo response thực tế.
2. **Thao tác:** Trên thanh địa chỉ, giữ nguyên session rồi thay duy nhất `id=1001` thành `id=1002` và nhấn `Enter`.
   - **Nói khi demo:** “Tôi không đổi cookie hay đăng nhập lại; chỉ đổi object ID để kiểm tra IDOR.”
   - **F12 show:** Trong Network chọn dòng mới nhất có URL chứa `/vulnerable/invoice` và `id=1002` → `Headers` → `General` → nhìn `Request URL` đầy đủ. Chỉ mở Query String Parameters nếu phiên bản Chrome đang hiển thị; đây là mục tùy chọn, không phải nơi bắt buộc phải có.
   - **Quan sát:** So sánh response của 1001 và 1002; nếu invoice 1002 trả về mà không có kiểm tra owner, đó là dấu hiệu vulnerable.
3. **Thao tác:** Mở `Response`/`Preview` và `Trace Panel → Database` để đối chiếu owner của invoice 1002.
   - **Nói khi demo:** “Tôi chứng minh object khác đã được đọc, không chỉ chứng minh URL đã đổi.”
   - **F12 show:** Request 1002 → `Response` → `Ctrl+F` tìm `invoice_id` hoặc `1002`; nếu nhiều occurrence, chọn object JSON/HTML có tên invoice, owner và amount. Sau đó đối chiếu tab Database trên trang.
   - **Quan sát:** Chỉ vào dữ liệu invoice 1002 thực sự trả về; không lấy số 1002 trong URL làm bằng chứng duy nhất.
**Kết luận:** Vulnerable invoice dùng object ID từ client mà thiếu kiểm tra quyền sở hữu.

### Bước 5 — Secure IDOR kiểm tra owner/admin

1. **Thao tác:** Với session User A, gửi request secure invoice tới `id=1002`.
   - **Nói khi demo:** “Tôi giữ User A và thử cùng object ID đã đọc được ở vulnerable.”
   - **F12 show:** `Network` → `Clear` → Filter `/secure/invoice` → chọn request mới nhất → `Headers` → `General` kiểm tra URL có `id=1002` và status. Nếu URL dài, dùng `Request URL` đầy đủ; không dựa vào tên rút gọn trong cột Name.
   - **Quan sát:** Ghi status và response của User A; không đổi session trước khi chụp bằng chứng.
2. **Thao tác:** Đăng xuất/đổi sang session Admin theo flow của lab, rồi gửi lại secure invoice với `id=1002`.
   - **Nói khi demo:** “Tôi lặp lại bằng admin để phân biệt bị chặn do owner hay do mọi tài khoản đều không được xem.”
   - **F12 show:** Network vẫn bật `Preserve log`; chọn request secure mới nhất sau khi đổi session → `Headers` → `General` kiểm tra status → `Response`. Nếu có cookie, chỉ nói session User A/Admin, không đọc giá trị cookie.
   - **Quan sát:** Hai kết quả phải được ghi riêng theo session; không gộp request User A và Admin vì chúng có cùng URL.
3. **Thao tác:** Mở `Trace Panel → Database` và `Authorization Inspector/Audit` nếu có.
   - **Nói khi demo:** “Bằng chứng secure nằm ở bước kiểm tra owner/role trước khi trả object.”
   - **F12 show:** Chọn từng request trong Network → `Response` → `Ctrl+F` tìm `owner`, `forbidden` hoặc `authorized`; chọn occurrence nằm trong kết quả request, sau đó đối chiếu Authorization Inspector.
   - **Quan sát:** Chỉ kết luận theo status/message và trace thật: User A bị từ chối hay Admin được phép phải nhìn thấy rõ.
**Kết luận:** Secure IDOR phải kiểm tra owner hoặc role trước khi trả invoice, dù ID hợp lệ.

### Bước 6 — Vulnerable mass assignment role

1. **Thao tác:** Mở `/vulnerable/profile` và chuẩn bị form profile hiện tại.
   - **Nói khi demo:** “Tôi kiểm tra mass assignment bằng cách đưa role vào form mà người dùng bình thường không nên điều khiển.”
   - **F12 show:** F12 → `Elements` → `Ctrl+F` nhập chính xác `name="role"`. Nếu có nhiều kết quả, chọn input trong form profile vulnerable có value `user`; bỏ qua text mẫu, form secure hoặc node trong script.
   - **Quan sát:** Xác nhận field role thật sự nằm trong form gửi đi và giá trị ban đầu là user.
2. **Thao tác:** Sửa value của input role từ `user` thành `admin`, giữ nguyên `user_id` và email, rồi bấm nút cập nhật vulnerable.
   - **Nói khi demo:** “Tôi chỉ đổi role, giữ các field khác để cô lập tác động của mass assignment.”
   - **F12 show:** Trong `Elements` xác nhận đúng dòng có `name="role" value="admin"`. Sau khi submit, Network → Filter `/vulnerable/profile/update` → chọn request mới nhất → `Headers` → `General` kiểm tra POST/status → `Payload` → `Form Data`, chỉ vào `role=admin` và các field profile.
   - **Quan sát:** Nếu Payload không có role=admin, đã sửa nhầm node hoặc form đã render lại; kiểm tra Payload trước khi xem kết quả.
3. **Thao tác:** Mở response và `Trace Panel → Database/Audit`.
   - **Nói khi demo:** “Tôi kiểm tra role được bind và lưu ở server, không chỉ nhìn field đã sửa trên browser.”
   - **F12 show:** Request vulnerable → `Response` → `Ctrl+F` tìm `accepted`; nếu không có, tìm `role`. Khi có nhiều occurrence, chọn object/message của profile update có role=admin, không chọn HTML label.
   - **Quan sát:** Ghi role sau update và bản ghi Database/Audit thật tế.
**Kết luận:** Vulnerable profile bind field role từ client vào model mà không allowlist field.

### Bước 7 — Secure profile allowlist field

1. **Thao tác:** Mở profile secure và tìm input role trong đúng form secure.
   - **Nói khi demo:** “Tôi dùng lại thao tác client giống vulnerable để kiểm tra server secure có bỏ qua field role hay không.”
   - **F12 show:** `Elements` → `Ctrl+F` → `name="role"`. Nếu có nhiều kết quả, chọn node thuộc form secure dựa vào form/action gần node; xác nhận value ban đầu. Không chọn node của form vulnerable còn ở trang.
   - **Quan sát:** Đúng form secure đã được nhận diện trước khi sửa.
2. **Thao tác:** Đổi value role thành `admin`, giữ email/username, rồi bấm cập nhật secure.
   - **Nói khi demo:** “Request vẫn có role=admin ở phía client; secure phải quyết định ở server, không dựa vào việc ẩn field.”
   - **F12 show:** Sau submit, Network → Filter `/secure/profile/update` → chọn request mới nhất → `Headers` → `General` kiểm tra POST/status → `Payload` → `Form Data` xác nhận có `role=admin` và email. Nếu không có role trong Payload, phép thử chưa đúng.
   - **Quan sát:** Ghi status/response trước khi mở trace; không suy ra reject từ việc UI vẫn hiển thị role cũ.
3. **Thao tác:** Mở response và các tab `Database`, `Authorization`, `Audit` trong Trace Panel.
   - **Nói khi demo:** “Tôi tìm thông báo server đã loại field ngoài allowlist và kiểm tra role lưu cuối cùng.”
   - **F12 show:** Request secure → `Response` → `Ctrl+F` tìm chính xác `Fields rejected`; nếu không có, tìm `role`. Nếu nhiều occurrence, chọn message/object của response update secure, rồi đối chiếu Database/Authorization/Audit.
   - **Quan sát:** Role cuối cùng vẫn là user hoặc response báo field bị loại; chỉ kết luận theo dữ liệu trace/response đang có.
**Kết luận:** Secure profile chỉ bind các field được allowlist; role do client gửi không được phép nâng quyền.

## Demo Vulnerable → Secure

| Lỗi | Cùng input | Vulnerable → nguyên nhân | Secure → primary fix |
|---|---|---|---|
| Checkout | `product_id=5&quantity=1&price=1` | Dùng `request.form["price"]`, hóa đơn có thể thành `1 VND` | Query `products.price_vnd`, bỏ qua giá client, audit mismatch |
| IDOR | `id=1002` trong session user A | `get_invoice(id)` không kiểm tra owner | Owner-scoped query + owner/admin authorization, user A nhận 403 |
| Mass assignment | `role=admin` (+ `user_id` trong form vulnerable) | Update nhận field nhạy cảm từ client | User ID từ session, allowlist chỉ `email`, role bị reject |

## Câu hỏi trong BaiTapTopic04.docx

**Câu 22. Parameter Tampering khác SQL Injection như thế nào?**  
**Trả lời khi demo:** Parameter Tampering sửa giá trị hợp lệ về cú pháp để làm sai business logic, như `price=1` hoặc `id=1002`. SQL Injection chèn cú pháp SQL để đổi ý nghĩa câu truy vấn; Lab03 tập trung vào tin dữ liệu nghiệp vụ, không phải SQL syntax.

**Câu 23. Vì sao hidden field không phải là cơ chế bảo mật?**  
**Trả lời khi demo:** Hidden chỉ làm field không hiện trong giao diện, nhưng người dùng vẫn sửa được DOM hoặc POST request. Bước checkout sửa `price=100000` thành `1` chứng minh server phải tự xác định trusted source.

**Câu 24. IDOR thuộc nhóm lỗi nào trong OWASP Top 10?**  
**Trả lời khi demo:** IDOR là biểu hiện của Broken Access Control, thường được mô tả là truy cập object trực tiếp nhưng thiếu kiểm tra quyền. Route secure phải gắn invoice với subject hiện tại trước khi trả dữ liệu.

**Câu 25. Server cần kiểm tra gì trước khi trả về hóa đơn?**  
**Trả lời khi demo:** Server cần xác thực session, lấy owner thực của invoice, rồi áp policy owner hoặc admin trước khi trả object. User A gọi `id=1002` phải nhận 403; admin chỉ được phép khi policy cho phép và điều đó phải có trace.

**Câu 26. Vì sao không nên truyền giá sản phẩm từ client lên server?**  
**Trả lời khi demo:** Client có thể sửa hidden field hoặc request nên giá không phải nguồn đáng tin. Server phải lookup `products.price_vnd` theo product ID, kiểm tra quantity và tính total ở server.

## Nếu demo lỗi

- Nếu login/product không đúng dữ liệu, dừng app và chạy `python seed.py` trong `Lab03`, rồi đăng nhập lại bằng tài khoản demo.
- Nếu vừa demo mass assignment làm user A thành admin, reset trước bước tiếp theo; ghi rõ reset đã thực hiện, không dùng state cũ làm bằng chứng.
- Nếu profile POST bị 404, dùng đúng `/vulnerable/profile/update` và `/secure/profile/update`; link GET `/vulnerable/profile`/`/secure/profile` chỉ mở form.
- Nếu expected status/total không xuất hiện, giữ request/trace/audit để kiểm tra và báo “chưa xác nhận live”, không sửa kết quả bằng tay.

## Chốt lab

Root cause: server tin giá, object ID hoặc field quyền do client gửi.
Primary fix: trusted source từ database/session, object authorization và field allowlist.
Defense in depth: validation, audit log, transaction, least privilege và kiểm thử tampering.
