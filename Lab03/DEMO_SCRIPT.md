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
- Reset khi cần: `python seed.py` tại `Lab03`; hoặc gửi `POST /reset-lab` từ flow local.
- Tài khoản: `user_a / UserA123!`, `user_b / UserB123!`, `admin / Admin123!`; invoice `1001, 1003` thuộc User A, `1002` thuộc User B.
- Dùng các panel của Lab03: `Action Timeline`, `Database Inspector`, `Authorization Inspector`, `Audit`.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`, mở `Network`, bật `Preserve log` và `Disable cache`; dùng bộ lọc `Doc`/`Fetch/XHR` và bấm `Clear` trước mỗi scenario.
- `Network`: show method, URL/query, `Payload/Form Data`, status và `Response/Preview`; khi login chỉ show endpoint/status, không đọc mật khẩu ra trước lớp.
- Với tampering, giữ request vulnerable và secure cạnh nhau để chỉ ra cùng field/input; panel của Lab03 dùng để show giá database, authorization decision, before/after và audit.

## Kịch bản trình bày

*Quy ước bằng chứng: số tiền/status/role dưới đây là kết quả cần xác nhận ở lần chạy live; source hiện tại là căn cứ để chọn route và input.*

**Bước 1 — Đăng nhập và xác lập giá server**

* Thao tác:
  1. Mở `http://127.0.0.1:5003`, bấm `Bắt đầu với User A`.
  2. Ở form login, bấm ô `Tên đăng nhập`, nhập `user_a`; bấm ô `Mật khẩu`, nhập `UserA123!`; bấm `Đăng nhập`.
  3. Trên thanh đầu trang bấm `Sản phẩm`. Tìm card có dòng `ID 5` và tiêu đề `USB Security Key`, giữ ô `Số lượng` là `1`, rồi bấm `Thêm vào giỏ`.
  4. Bấm `Giỏ hàng` trên thanh đầu trang, kiểm tra sản phẩm trong giỏ, rồi bấm link `Checkout vulnerable`.
* Nói: “Giá hiển thị đến từ SQLite. Tôi dùng product 5 để so sánh giá client gửi với giá server đọc lại.”
* Quan sát: session có user A; product ID 5 có `price_vnd=100000` trong database/trace.
* F12 show: `Network → POST /login` chỉ ra status/Set-Cookie (không show password); `GET /products` mở `Response/Preview` để chỉ product `5` và giá `100000`.
* Kết luận: giá database là trusted source; hidden field chỉ là dữ liệu gửi từ client.

**Bước 2 — Vulnerable checkout nhận `price=1`**

* Thao tác:
  1. Ở trang checkout, giữ `Product ID=5` và `Quantity=1`.
  2. Nhấn `F12`, chọn tab `Elements`, nhấn `Ctrl+F`, tìm `name="price"`, rồi bấm đúp vào giá trị `100000` của hidden field và sửa thành `1`; nhấn `Enter` để lưu DOM.
  3. Quay lại form, bấm `Gửi checkout vulnerable`. Nếu trang cuộn lên đầu, cuộn xuống phần invoice/trace để chỉ vào giá đã gửi.
* Nói: “Tôi không đổi sản phẩm hay số lượng; chỉ sửa giá trước POST. Route vulnerable dùng giá client để tính hóa đơn.”
* Quan sát: response/Database Inspector kỳ vọng ghi unit price và total `1 VND`; trace chỉ ra `submitted_price=1`, route `/vulnerable/checkout`, và audit có thay đổi giá.
* F12 show: `Network → POST /vulnerable/checkout → Payload/Form Data` với `product_id=5`, `quantity=1`, `price=1`; `Response/Preview` show invoice result; panel `Database Inspector` show stored price/total.
* Kết luận: parameter tampering qua hidden field làm sai logic nghiệp vụ dù cú pháp request hoàn toàn hợp lệ.

**Bước 3 — Secure checkout dùng lại đúng `price=1`**

* Thao tác:
  1. Trên trang vulnerable checkout bấm link `Mở bản secure`.
  2. Bấm dòng mở rộng `Thử thêm giá client`; trong ô `Untrusted price` nhấn `Ctrl+A`, nhập `1`.
  3. Kiểm tra `Product ID=5` và `Quantity=1`, rồi bấm `Gửi checkout secure`.
  4. Cuộn tới kết quả và giữ trace panel mở để đối chiếu giá client với giá database.
* Nói: “Cùng input nhưng secure không tin giá từ form. Server query `products.price_vnd` rồi ghi mismatch để audit.”
* Quan sát: kỳ vọng `Giá client gửi=1`, `Giá database=100000`, total lưu là `100000 VND`, decision allow nhưng audit ghi mismatch; xác nhận các con số live.
* F12 show: `Network → POST /secure/checkout → Payload` vẫn có `price=1`; `Response` show secure result; panel `Database Inspector`/`Audit` show database price, total và mismatch.
* Kết luận: primary fix là server-side price lookup, không phải chỉ ẩn hoặc validate hidden field.

**Bước 4 — Vulnerable IDOR đọc invoice của user khác**

* Thao tác:
  1. Giữ session `user_a`, nhấn `Ctrl+L`, nhập `http://127.0.0.1:5003/vulnerable/invoice?id=1001`, nhấn `Enter`.
  2. Sau khi trang hiện invoice 1001, nhấn `Ctrl+L`, đổi riêng số cuối thành `http://127.0.0.1:5003/vulnerable/invoice?id=1002`, rồi nhấn `Enter`.
  3. Không đăng xuất hoặc đổi tài khoản giữa hai lần tải; đây là bước chứng minh chỉ sửa object ID trên thanh địa chỉ.
* Nói: “Invoice 1001 là object của subject hiện tại; 1002 thuộc user B. Tôi đổi object ID mà không đổi session.”
* Quan sát: route vulnerable kỳ vọng vẫn trả invoice `1002` và owner ID của user B; trace cho thấy lookup theo ID nhưng không có object authorization.
* F12 show: `Network → GET /vulnerable/invoice?id=1001` rồi `id=1002`; so sánh status và `Response/Preview` của hai invoice; panel `Database Inspector` show owner ID.
* Kết luận: IDOR là lỗi kiểm soát truy cập object, không phải lỗi đoán ID.

**Bước 5 — Secure IDOR kiểm tra owner/admin**

* Thao tác:
  1. Khi vẫn là user A, nhấn `Ctrl+L`, mở `http://127.0.0.1:5003/secure/invoice?id=1002`, rồi giữ nguyên trang lỗi/403 để chỉ vào bằng chứng.
  2. Bấm `Đăng xuất` trên thanh đầu trang; sau đó bấm `Đăng nhập`, nhập `admin` và `Admin123!`, bấm `Đăng nhập`.
  3. Nhấn `Ctrl+L`, mở lại đúng URL secure ở trên, nhấn `Enter`, rồi kiểm tra kết quả với session admin.
* Nói: “User A phải bị từ chối; admin chỉ được phép nếu policy hiện tại cho phép owner hoặc admin. Tôi tách hai subject để chứng minh authorization.”
* Quan sát: user A kỳ vọng nhận `403` và Authorization Inspector ghi owner mismatch; admin kỳ vọng được phép nếu live session là admin, với query/scoping và audit tương ứng.
* F12 show: `Network → GET /secure/invoice?id=1002` với session user A, show status `403`/response; sau khi đổi admin show cùng URL; panel `Authorization Inspector` chỉ subject, owner, policy và decision.
* Kết luận: secure route ràng buộc object với session subject và policy, thay vì chỉ kiểm tra invoice ID tồn tại.

**Bước 6 — Vulnerable mass assignment nhận role từ form**

* Thao tác:
  1. Bấm `Đăng xuất`, rồi bấm `Đăng nhập`; nhập `user_a` / `UserA123!` và bấm `Đăng nhập`.
  2. Nhấn `Ctrl+L`, mở `http://127.0.0.1:5003/vulnerable/profile`, nhấn `Enter`.
  3. Nhấn `F12`, chọn `Elements`, nhấn `Ctrl+F` tìm `name="role"`; bấm đúp value `user` và sửa thành `admin`, giữ nguyên `user_id` và email.
  4. Quay lại form, bấm `Cập nhật vulnerable`, rồi cuộn tới Database Inspector để chỉ vào before/after role.
* Nói: “Hidden không phải secret: người dùng sửa được DOM/request. Vulnerable update lấy cả `user_id` và `role` từ form.”
* Quan sát: response/Database Inspector kỳ vọng before `user`, after `admin`; trace route là `/vulnerable/profile/update`, audit ghi `role=admin`.
* F12 show: `Network → POST /vulnerable/profile/update → Payload/Form Data` với `user_id` và `role=admin`; `Response` show result; panel `Database Inspector` show role before/after và `Audit` show accepted update.
* Kết luận: mass assignment xảy ra khi server bind field nhạy cảm mà không có allowlist/authorization.

**Bước 7 — Secure profile giữ role và chỉ nhận email**

* Thao tác:
  1. Nếu cần làm sạch state, mở terminal tại thư mục Lab03 và chạy `python seed.py`; sau đó mở lại `http://127.0.0.1:5003`.
  2. Bấm `Đăng nhập`, nhập `user_a` / `UserA123!`, bấm `Đăng nhập`; nhấn `Ctrl+L` mở `http://127.0.0.1:5003/secure/profile`.
  3. Bấm dòng mở rộng `Thử thêm trường role`; giữ ô `Rejected role` là `admin`.
  4. Bấm `Cập nhật secure`, rồi đọc thông báo `Trường role đã bị từ chối` và mở Authorization/Audit Inspector để chỉ vào field bị reject.
* Nói: “Cùng trường nhạy cảm được gửi lại. Secure lấy user ID từ session, allowlist chỉ có `email` và từ chối role.”
* Quan sát: kỳ vọng response báo `Trường role đã bị từ chối`, `Fields accepted=email`, `Fields rejected=role`, role database vẫn `user`.
* F12 show: `Network → POST /secure/profile/update → Payload` vẫn có `role=admin`; `Response` show reject/result; panel `Database Inspector` show role không đổi và fields rejected là `role`.
* Kết luận: primary fix là session-based identity và field allowlist; validation hình thức không thay thế authorization.

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
