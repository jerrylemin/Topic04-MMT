# Demo script Lab05 — SQL Injection

## Mục tiêu demo

- Chứng minh SQL Injection ở login và search bằng input cố định, read-only.
- So sánh nối chuỗi SQL với prepared statement bằng cùng username/keyword.
- Quan sát error handling, auth bypass, result count và query trace.
- Giữ phạm vi demo ở `SELECT`; không dùng UNION, write, DDL hay dữ liệu ngoài lab.

## Chuẩn bị

- Thư mục làm việc: `cd Lab05`
- Khởi động: `scripts\run_lab.bat`
- URL: `http://127.0.0.1:5005`
- Reset khi cần: `python seed.py` tại `Lab05`; hoặc gửi `POST /reset-lab`.
- Tài khoản: `admin_lab / AdminLab123!`, `student_a / StudentA123!`, `student_b / StudentB123!`
- Giữ nguyên khoảng trắng cuối payload; dùng các panel của Lab05: `Error Inspector`, `Query Trace`, `Database Inspector`.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`, mở `Network`, bật `Preserve log`/`Disable cache` và bấm `Clear` trước mỗi login/search.
- Login: `Network → POST` show endpoint, status và username trong `Payload`; không đọc password ra trước lớp. Search: show query parameter `keyword` trong URL/`Headers`.
- `Response/Preview` show generic error, auth result hoặc số sản phẩm; `Query Trace`/`Database Inspector` của Lab05 show câu SQL, placeholder, result count và read-only scope.

## Kịch bản trình bày

*Quy ước bằng chứng: “8 products”, status và auth state là kết quả cần xác nhận live; payload có khoảng trắng cuối phải được nhập nguyên văn.*

**Bước 1 — Login bình thường làm baseline**

* Thao tác:
  1. Mở `http://127.0.0.1:5005`, bấm card `Login · vulnerable` hoặc bấm menu `Đăng nhập yếu`.
  2. Bấm nút mẫu `Dữ liệu bình thường` để điền form; kiểm tra ô `Username` và `Password`, rồi bấm `Chạy vulnerable login`.
  3. Trên thanh menu bấm `Đăng nhập an toàn`; bấm `Dữ liệu bình thường` và bấm `Chạy secure login`.
  4. Giữ hai kết quả/trace đủ gần nhau để đối chiếu status và query.
* Nói: “Tôi chứng minh chức năng hợp lệ trước khi đưa SQL syntax vào. Cùng một tài khoản phải được xử lý ở cả hai route.”
* Quan sát: login vulnerable và secure kỳ vọng thành công với account thật; trace cho thấy vulnerable query là string-built còn secure query có placeholder, nhưng phải lấy query/status từ live trace.
* F12 show: chọn `POST /vulnerable/login` rồi `POST /secure/login`; `Payload` chỉ show username, `Headers/Response` show status; panel `Query Trace` show string-built đối chiếu placeholder.
* Kết luận: lỗi không phải do mọi login đều hỏng; nó xuất hiện khi input được ghép vào SQL.

**Bước 2 — Quote input tạo SQL error có kiểm soát**

* Thao tác:
  1. Bấm menu `Đăng nhập yếu`; bấm `Ký tự dấu nháy đơn` để điền nhanh, hoặc bấm ô `Username`, nhấn `Ctrl+A`, nhập đúng `'`; bấm ô `Password`, nhập `x`.
  2. Bấm `Chạy vulnerable login`.
  3. Bấm menu `Đăng nhập an toàn`; bấm `Ký tự dấu nháy đơn`, kiểm tra lại username là `'` và password là `x`, rồi bấm `Chạy secure login`.
* Nói: “Một dấu quote đủ phá cú pháp câu SQL nối chuỗi. Error Inspector phải redacted lỗi chi tiết, không đưa raw SQL cho người dùng.”
* Quan sát: vulnerable kỳ vọng nhận handled SQLite syntax error/decision error; secure coi `'` là literal và reject generic, không thực thi SQL syntax. Chỉ ghi trạng thái thật từ response.
* F12 show: `Network → POST /vulnerable/login` và `/secure/login`, `Payload` show username `'`/password được che, `Response` show status/error generic; panel `Error Inspector` show lỗi đã redacted.
* Kết luận: escaping thủ công không phải prepared statement; lỗi phải được xử lý mà không lộ thông tin nội bộ.

**Bước 3 — Auth bypass với input cố định**

* Thao tác:
  1. Bấm menu `Đăng nhập yếu`. Bấm ô `Username`, nhấn `Ctrl+A`, nhập chính xác `admin_lab' -- ` với một khoảng trắng ở cuối; bấm ô `Password`, nhập `x`.
  2. Bấm `Chạy vulnerable login`. Không dùng nút mẫu `Điều kiện đăng nhập local` nếu nút đó tự điền chuỗi khác; input source/config yêu cầu phải nhập thủ công.
  3. Bấm menu `Đăng nhập an toàn`. Nhập lại đúng username/password ở trên, rồi bấm `Chạy secure login`; không dùng nút `Cùng input logic` nếu nó tự điền chuỗi khác.
* Nói: “Payload đóng quote, comment phần kiểm tra password trong câu vulnerable. Tôi giữ password sai để chứng minh bypass không đến từ credential hợp lệ.”
* Quan sát: vulnerable kỳ vọng thành công với session marker `authenticated_via=vulnerable_local_demo`; secure phải reject cùng username như literal và không tạo bypass session. Xác nhận marker/status live.
* F12 show: `Payload` phải giữ nguyên username có khoảng trắng cuối; `Response/Headers` show auth result/status; panel `Query Trace` show comment trong vulnerable và parameter binding ở secure, không đọc password ra.
* Kết luận: nối chuỗi cho phép input đổi cấu trúc authentication query; parameter binding giữ input là giá trị.

**Bước 4 — Search bình thường và expanded result**

* Thao tác:
  1. Bấm menu `Tìm kiếm`; nếu trang mở bản vulnerable, bấm ô `Từ khóa`, nhập `USB`, rồi bấm `Chạy vulnerable search` và ghi số result.
  2. Bấm ô `Từ khóa` lần nữa, nhấn `Ctrl+A`, nhập chính xác `%' OR 1=1 -- ` với khoảng trắng cuối, rồi bấm `Chạy vulnerable search`.
  3. Sau khi có kết quả vulnerable, ở đầu trang bấm nút `Thử cùng input ở secure mode`; nếu đã rời trang kết quả, nhấn `Ctrl+L` mở `http://127.0.0.1:5005/secure/search`.
  4. Bấm ô `Từ khóa`, nhấn `Ctrl+A`, nhập lại đúng keyword, rồi bấm `Chạy secure search`.
  5. Nếu nút `Cùng input mở rộng` tự điền thiếu khoảng trắng cuối, không dùng nguyên giá trị đó; hãy sửa trực tiếp trong ô `Từ khóa` trước khi submit.
* Nói: “Tôi dùng SELECT read-only và cùng keyword ở hai bản. Khoảng trắng cuối sau `--` là một phần payload.”
* Quan sát: `USB` cho kết quả sản phẩm bình thường; vulnerable với expanded input kỳ vọng trả 8 products theo seed hiện tại, query trace là nối chuỗi; secure dùng `LIKE ?` và kỳ vọng 0 result cho cùng input. Xác nhận count live.
* F12 show: chọn từng `GET /vulnerable/search` và `GET /secure/search`; `Headers/Query String Parameters` show nguyên keyword và khoảng trắng cuối; `Response/Preview` show result count; panel `Database Inspector` show read-only result.
* Kết luận: parameter binding giữ keyword nguyên văn, không cho nó trở thành toán tử SQL.

**Bước 5 — Đối chiếu prepared statement và error boundary**

* Thao tác:
  1. Trên thanh menu bấm `So sánh mã`; nếu cần bấm `Kiểm soát` để mở trang controls.
  2. Nếu trace login không còn do đã chuyển trang, bấm menu `Đăng nhập yếu`, bấm `Dữ liệu bình thường`, bấm `Chạy vulnerable login`, rồi cuộn tới Trace Panel; bấm lần lượt các tab `Query`, `Parameters`, `Execution`, `Authentication` và `Verdict`.
  3. Bấm menu `Tìm kiếm`, nhập `USB`, bấm `Chạy vulnerable search`, rồi trong trace kết quả bấm các tab `Query`, `Parameters`, `Result Set`, `Error`, `Code` và `Verdict`.
  4. Ở footer trace, bấm `Mở Query` hoặc `Mở Verdict` để phóng to đúng bằng chứng cần trình bày; không chạy thêm payload ngoài kịch bản.
* Nói: “Prepared statement tách query structure khỏi value. Password hashing và thông báo lỗi redacted là lớp bổ sung, không phải primary SQLi fix.”
* Quan sát: trang/trace hiện read-only scope, placeholder secure, error detail không trả raw SQL; không chạy `UNION`, `UPDATE`, `DROP` hoặc DDL.
* F12 show: `Network → GET /comparison` và `/security-controls` chỉ để xác nhận trang/response; phần query/placeholder phải show ở `Query Trace` và `Database Inspector`, không dùng Network để kết luận đã chạy câu write.
* Kết luận: primary fix là parameterized query ở mọi value boundary, kèm xử lý lỗi không lộ schema/query.

## Demo Vulnerable → Secure

| Tình huống | Cùng input | Vulnerable → nguyên nhân | Secure → primary fix |
|---|---|---|---|
| Quote error | username `'`, password `x` | f-string login tạo syntax error; error được handle/redact | Prepared query coi `'` là literal và reject generic |
| Auth bypass | username `admin_lab' -- `, password `x` | comment phần password, tạo local demo bypass | Cùng input không đổi cấu trúc query; không bypass |
| Search expansion | keyword `%' OR 1=1 -- ` | nối chuỗi `LIKE`, kỳ vọng 8 products theo seed | `LIKE ?`, cùng input là value literal, kỳ vọng 0 |

## Câu hỏi trong BaiTapTopic04.docx

**Câu 32. SQL Injection xảy ra ở tầng nào của ứng dụng?**  
**Trả lời khi demo:** SQL Injection xảy ra ở ranh giới ứng dụng–database khi input được ghép vào câu SQL trước khi execute. Lab05 nhận input ở HTTP nhưng sink nguy hiểm là query builder nối chuỗi trong backend.

**Câu 33. Vì sao escaping thủ công dễ sai?**  
**Trả lời khi demo:** Quy tắc escape phụ thuộc SQL dialect, context và encoding; chỉ cần quên một branch hoặc ghép thêm field là có thể lọt. Prepared statement không yêu cầu lập danh sách escape thủ công cho value.

**Câu 34. Prepared statement khác nối chuỗi SQL như thế nào?**  
**Trả lời khi demo:** Prepared statement gửi cấu trúc query và value qua placeholder như `?` tách biệt. Nối chuỗi biến value thành một phần cú pháp SQL, nên payload có thể đổi ý nghĩa query.

**Câu 35. ORM có tự động chống SQL Injection trong mọi trường hợp không?**  
**Trả lời khi demo:** Không. ORM thường bind parameter khi dùng API chuẩn, nhưng raw SQL, string interpolation hoặc filter động vẫn có thể tạo injection; Lab05 hiện dùng sqlite3 trực tiếp nên phải nhìn vào query cụ thể.

**Câu 36. Vì sao thông báo lỗi SQL chi tiết không nên hiển thị cho người dùng?**  
**Trả lời khi demo:** Raw error có thể lộ engine, bảng, cột, query và gợi ý cho bước tấn công tiếp theo. User chỉ nên nhận lỗi generic; chi tiết giữ ở log/trace nội bộ được kiểm soát.

## Nếu demo lỗi

- Nếu payload auth không bypass, nhập lại chính xác `admin_lab' -- ` với khoảng trắng cuối và password không rỗng; không thay bằng biến thể khác.
- Nếu search không ra 8, chạy `python seed.py` trong `Lab05`, rồi ghi số result live thay vì khẳng định seed cũ.
- Nếu UI/URL làm mất khoảng trắng cuối, dán vào ô form hoặc dùng DevTools Request/Query Trace để kiểm tra value thực tế.
- Nếu server lỗi, kiểm tra `http://127.0.0.1:5005` và route; không chạy payload write/DDL để “tạo” kết quả.

## Chốt lab

Root cause: input được nối trực tiếp vào câu SQL ở backend.
Primary fix: prepared/parameterized statements cho mọi giá trị query.
Defense in depth: least privilege, read-only scope, generic errors, password hashing và logging an toàn.
