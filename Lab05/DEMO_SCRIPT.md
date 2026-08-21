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

- Nhấn `F12` hoặc `Ctrl+Shift+I`; bấm `Network`, bật `Preserve log` và `Disable cache`, rồi bấm thùng rác `Clear` trước mỗi login/search.
- Ở ô `Filter` gõ `/login` hoặc `/search`; bấm dòng vừa phát sinh, rồi vào `Headers` → `General` kiểm tra `Request Method` và URL để phân biệt đúng POST/GET. POST bấm `Payload` → `Form Data`; GET đọc query ở phần sau dấu `?` trên `Request URL`. Chỉ mở `Query String Parameters` nếu Chrome hiển thị mục đó; nếu không, `Request URL` là bằng chứng thay thế.
- Bấm `Response` hoặc `Preview`; nhấn `Ctrl+F` trong pane và tìm chuỗi đặc trưng đúng scenario: `syntax`/`generic`, `authenticated_via`, tên sản phẩm hoặc `products`. Không tìm `error` một mình nếu có nhiều kết quả; password chỉ được để masked, không đọc ra trước lớp.
- Sau F12 cuộn tới Trace Panel của Lab05 và bấm đúng tab ứng dụng `Query`, `Parameters`, `Execution`, `Authentication`, `Result Set`, `Error`, `Database`, `Code` hoặc `Verdict`.


## Kịch bản trình bày

*Quy ước: mỗi mục đọc theo thứ tự **Thao tác → Nói khi demo → F12 show → Quan sát**. Với payload có dấu cách cuối, giữ nguyên dấu cách khi nhập và xác nhận lại bằng Request URL/Payload.*

### Bước 1 — Baseline login vulnerable và secure

1. **Thao tác:** Mở `http://127.0.0.1:5005` và chọn menu/flow `Vulnerable login`.
   - **Nói khi demo:** “Tôi tạo baseline vulnerable trước để so sánh request, query và kết quả xác thực với secure.”
   - **F12 show:** Nhấn `F12` → `Network` → bấm `Clear`; tích `Preserve log` và `Disable cache`. Trong ô `Filter` nhập `/login`.
   - **Quan sát:** Đúng form vulnerable xuất hiện; chưa chọn request cũ trong Network.
2. **Thao tác:** Nhập dữ liệu đăng nhập bình thường theo lab, giữ username `admin_lab`, rồi bấm `Run`/`Đăng nhập`.
   - **Nói khi demo:** “Tôi dùng dữ liệu bình thường làm mốc, không đưa payload SQL ở bước baseline.”
   - **F12 show:** Chọn dòng mới nhất có URL chứa `/vulnerable/login` → `Headers` → `General` kiểm tra `POST` và status → `Payload` → `Form Data` chỉ vào `username=admin_lab`; che hoặc không mở trường password.
   - **Quan sát:** Ghi status và response thật; không gọi là authenticated chỉ vì request trả 200.
3. **Thao tác:** Chọn menu/flow `Secure login`, nhập lại cùng dữ liệu bình thường và bấm `Run`/`Đăng nhập`.
   - **Nói khi demo:** “Tôi gửi cùng dữ liệu qua secure endpoint để baseline có thể so sánh từng field.”
   - **F12 show:** Network → chọn dòng mới nhất có URL chứa `/secure/login` → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` xác nhận username giống bước trước, vẫn che password.
   - **Quan sát:** Giữ hai request riêng biệt theo URL; không chọn nhầm dòng vulnerable có cùng tên login.
4. **Thao tác:** Mở `Trace Panel` và lần lượt bấm `Query`, `Parameters`, `Authentication`, `Verdict` nếu có.
   - **Nói khi demo:** “Trace baseline cho thấy query/parameters và quyết định xác thực trước khi đưa chuỗi đặc biệt.”
   - **F12 show:** Chọn từng request login → `Response` → `Ctrl+F` tìm `authenticated_via`; nếu không có, tìm `success`. Nếu nhiều occurrence, chọn object/message của lần login, không chọn chữ trong HTML hướng dẫn.
   - **Quan sát:** Ghi kết quả live của vulnerable và secure, kể cả khi cả hai đều từ chối dữ liệu bình thường.
**Kết luận:** Baseline phải được lưu theo từng endpoint trước khi kiểm tra lỗi SQL injection.

### Bước 2 — Dấu nháy tạo lỗi SQL

1. **Thao tác:** Quay lại `Vulnerable login` và nhập username chỉ là `'`, password là `x` rồi bấm chạy.
   - **Nói khi demo:** “Tôi dùng một dấu nháy đơn tối thiểu để xem đầu vào có đi vào câu SQL chưa được xử lý hay không.”
   - **F12 show:** Network → Filter `/vulnerable/login` → chọn request mới nhất sau click → `Headers` → `General` kiểm tra URL/status → `Payload` → `Form Data` xác nhận username đúng một ký tự `'` và password không cần trình bày.
   - **Quan sát:** Nếu Payload không có dấu nháy, kiểm tra lại ô nhập hoặc URL encode; không suy luận từ text hiển thị trên form.
2. **Thao tác:** Mở response vulnerable và panel lỗi/trace.
   - **Nói khi demo:** “Tôi tìm marker lỗi SQL trong response nhưng chỉ kết luận nếu nó thuộc request vừa gửi.”
   - **F12 show:** Request vulnerable → `Response` → nhấn `Ctrl+F` tìm `syntax`. Nếu không có, tìm `generic`. Nếu từ khóa xuất hiện nhiều lần, bấm Enter để chuyển occurrence và chọn đoạn gần object/error message của login; bỏ qua chữ trong menu, script mẫu hoặc phần giải thích.
   - **Quan sát:** Ghi thông báo lỗi/ẩn lỗi và status thật; không đọc stack trace dài nếu lab đã redacted.
3. **Thao tác:** Chọn `Secure login`, gửi lại username `'` và password `x`.
   - **Nói khi demo:** “Tôi gửi cùng dấu nháy qua secure endpoint để xem lỗi có bị lộ và query có được xử lý an toàn hơn không.”
   - **F12 show:** Network → Filter `/secure/login` → chọn request mới nhất → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` xác nhận username là `'` → `Response` → `Ctrl+F` tìm `generic`; nếu không có, đọc thông báo hiện tại, không tự đi tìm stack trace.
   - **Quan sát:** So sánh response secure với vulnerable: status, thông báo và việc có/không có chi tiết SQL.
4. **Thao tác:** Mở `Trace Panel → Error` của hai lần chạy.
   - **Nói khi demo:** “Trace cho thấy server đã redacted lỗi hay để lộ chi tiết, còn F12 xác nhận payload thực sự đi qua HTTP.”
   - **F12 show:** Chọn từng request → `Response` → tìm `trace_id` hoặc `error`; chọn occurrence trong kết quả request và đối chiếu với Error trace. Không chọn error của request khác.
   - **Quan sát:** Chỉ kết luận theo lỗi/trace thật; nếu không có SQL marker, ghi rõ hệ thống đã ẩn hoặc không phát sinh marker.
**Kết luận:** Dấu nháy là phép thử lỗi đầu vào; lỗi chi tiết hay generic phải được xác nhận từ response của đúng request.

### Bước 3 — Auth bypass bằng comment SQL

1. **Thao tác:** Mở `Vulnerable login`, nhập username chính xác `admin_lab' -- ` trong đó ký tự cuối cùng là một dấu cách, nhập password `x` rồi bấm chạy.
   - **Nói khi demo:** “Payload này đóng chuỗi và dùng comment SQL; dấu cách sau hai dấu gạch rất quan trọng để phần còn lại thành comment.”
   - **F12 show:** Network → Filter `/vulnerable/login` → chọn request mới nhất → `Headers` → `General` nhìn `Request URL` nếu username được encode trên URL, hoặc bấm `Payload` → `Form Data`. Dùng `Ctrl+A` trong field username nếu cần, rồi xác nhận chuỗi kết thúc bằng `--` và một dấu cách trước khi submit.
   - **Quan sát:** Nếu Network encode dấu cách thành `%20` ở URL hoặc hiển thị khoảng trắng trong Payload, đó là cùng một ký tự; nếu mất dấu cách cuối, gửi lại.
2. **Thao tác:** Mở response vulnerable và trace authentication.
   - **Nói khi demo:** “Tôi kiểm tra server có trả authenticated bằng nhánh vulnerable hay không.”
   - **F12 show:** Request vừa chọn → `Response` → nhấn `Ctrl+F` tìm chính xác `authenticated_via=vulnerable_local_demo`. Nếu không có, tìm `bypass`. Với nhiều occurrence, chọn dòng JSON/message có username hoặc verdict của request này; không chọn label trong HTML.
   - **Quan sát:** Ghi verdict/authenticated và status thật. Đây là bước xác định kết quả bypass, không chỉ xác định payload đã gửi.
3. **Thao tác:** Gửi cùng username `admin_lab' -- ` và password `x` qua `Secure login`.
   - **Nói khi demo:** “Secure endpoint nhận cùng dữ liệu độc hại nhưng không được coi phần còn lại là câu lệnh.”
   - **F12 show:** Network → Filter `/secure/login` → chọn row mới nhất → `Headers` → `General` kiểm tra status → `Payload` xác nhận username còn dấu cách cuối → `Response` đọc reject/generic message. Nếu cần, nhấn `Ctrl+F` tìm `bypass` nhưng chọn occurrence trong kết quả secure.
   - **Quan sát:** So sánh hai verdict theo endpoint; không gọi secure pass nếu chỉ thấy request 200 mà không có authentication result.
4. **Thao tác:** Bấm `Trace Panel → Query`, `Parameters` và `Authentication` để đối chiếu hai flow.
   - **Nói khi demo:** “Trace cho thấy sự khác nhau nằm ở cách query/parameter được xử lý, không phải ở giao diện form.”
   - **F12 show:** Với từng request, `Payload` là bằng chứng input; `Response` → `Ctrl+F` tìm `trace_id`/`verdict` để chọn đúng trace. Không dùng Elements để suy luận câu SQL phía server.
   - **Quan sát:** Chỉ vào nhánh authenticated/rejected thật sự và giữ nguyên dấu cách trong mô tả payload.
**Kết luận:** Vulnerable query cho phép comment làm thay đổi logic; secure flow phải từ chối hoặc xử lý input như dữ liệu.

### Bước 4 — Search vulnerable/secure với keyword mở rộng

1. **Thao tác:** Mở menu search và gửi keyword bình thường `USB` trước.
   - **Nói khi demo:** “Tôi chạy một keyword bình thường để biết endpoint và kết quả baseline.”
   - **F12 show:** Network → bấm `Clear` → Filter `/search` → chọn request GET mới nhất → `Headers` → `General` → nhìn `Request URL` đầy đủ, đặc biệt phần sau dấu `?`. Nếu phiên bản Chrome có mục `Query String Parameters`, có thể mở mục đó; nếu không thấy, chỉ dùng `Request URL`, không cần tìm mục này.
   - **Quan sát:** Xác nhận keyword và kết quả bình thường trước khi dùng chuỗi mở rộng.
2. **Thao tác:** Ở search vulnerable, thay keyword bằng chính xác `%' OR 1=1 -- `, trong đó ký tự cuối là một dấu cách, rồi bấm tìm.
   - **Nói khi demo:** “Tôi mở rộng điều kiện bằng payload có comment SQL; dấu cách cuối giúp comment phần còn lại.”
   - **F12 show:** Chọn request GET mới nhất có tên/URL `/search`. Bấm `Headers` → `General` → đọc `Request URL` để xác nhận phần query; nếu URL dài, click/double-click vào giá trị hoặc chọn toàn bộ để copy, không cần nhìn cột Name. Kiểm tra dấu cách cuối được encode thành `%20` nếu browser encode URL.
   - **Quan sát:** Nếu Request URL không chứa keyword mong muốn, request vừa chọn không phải lần thử này; chọn row khác bằng timestamp và URL.
3. **Thao tác:** Mở response vulnerable và `Trace Panel → Query`/`Parameters`/`Result Set`/`Database`.
   - **Nói khi demo:** “Tôi xem số lượng/kết quả trả về và trace query để phân biệt input đã làm rộng result set hay chỉ lỗi.”
   - **F12 show:** Request vulnerable → `Response` hoặc `Preview` → `Ctrl+F` tìm `USB Security Key`; nếu không có, tìm `products`. Nếu nhiều occurrence, chọn object product trong response, không chọn tên sản phẩm ở menu/sidebar.
   - **Quan sát:** Ghi số result/record thực tế và marker trace; không suy ra 1=1 chỉ từ việc có nhiều dòng trên giao diện.
4. **Thao tác:** Gửi cùng keyword qua `Secure search`.
   - **Nói khi demo:** “Tôi giữ nguyên payload và so sánh kết quả secure, nơi input phải được bind như parameter.”
   - **F12 show:** Network → chọn request mới nhất `/search` thuộc secure flow → `Headers` → `General` xác nhận URL/status → dùng `Request URL` làm bằng chứng query; nếu có Query String Parameters thì mở thêm, nhưng không bắt buộc → `Response` → tìm `USB Security Key` hoặc `products` trong đoạn kết quả secure.
   - **Quan sát:** So sánh status, số result và trace giữa vulnerable/secure; chọn đúng response của secure bằng URL đầy đủ.
5. **Thao tác:** Mở `Trace Panel → Query`, `Parameters`, `Result Set` và `Database` của hai lần search.
   - **Nói khi demo:** “Tôi kết thúc bằng bằng chứng server-side: query parameter và result set, không chỉ nhìn URL.”
   - **F12 show:** Từng request → `Headers` → `General` → `Request URL`; `Response` → `Ctrl+F` tìm `trace_id` hoặc marker result; chọn occurrence gần object kết quả rồi đối chiếu trace.
   - **Quan sát:** Ghi rõ flow nào trả nhiều result, flow nào reject/giới hạn, và dữ liệu đó đến từ response nào.
**Kết luận:** Search vulnerable có thể nối input vào SQL; secure search phải truyền keyword như parameter và kiểm soát result set.

### Bước 5 — Comparison và ranh giới lỗi

1. **Thao tác:** Mở menu `Comparison` và nếu cần chạy lại một login/search ngắn để bảng so sánh có dữ liệu.
   - **Nói khi demo:** “Comparison dùng để tóm tắt hành vi đã quan sát; tôi không coi bảng tóm tắt là bằng chứng thay thế request.”
   - **F12 show:** Network → bấm `Clear` → Filter `/comparison` → mở trang comparison. Sau đó nếu chạy lại login/search, đổi filter tương ứng và giữ request mới nhất.
   - **Quan sát:** Bảng comparison hiển thị đúng lab/flow; ghi lại timestamp hoặc trace ID nếu có.
2. **Thao tác:** Bấm các tab/section `Vulnerable` và `Secure` trong comparison, rồi chỉ vào các ô khác biệt.
   - **Nói khi demo:** “Tôi đọc từng khác biệt theo endpoint và verdict, không suy luận thêm những gì bảng không hiển thị.”
   - **F12 show:** Chọn request GET mới nhất có URL `/comparison` → `Headers` → `General` kiểm tra URL/status → `Response` → nhấn `Ctrl+F` tìm `prepared`. Nếu không có, tìm `placeholder`; chỉ tìm `SELECT` nếu response thật sự chứa câu SQL đã redacted.
   - **Quan sát:** Chỉ vào marker đang có trong response. Nếu không có marker, nói “comparison không hiển thị chi tiết này” thay vì kết luận đã dùng prepared statement.
3. **Thao tác:** Mở `Trace Panel` và bấm `Verdict`/`Query`/`Parameters` tương ứng với bảng comparison.
   - **Nói khi demo:** “Trace là nơi tôi chốt hành vi từng flow; comparison chỉ là bản trình bày ngắn.”
   - **F12 show:** Network → request comparison hoặc request login/search liên quan → `Response` → `Ctrl+F` tìm `trace_id`; chọn occurrence nằm trong response của request đó và đối chiếu với trace panel.
   - **Quan sát:** Chốt các điểm đã có bằng chứng: payload, status, response, query/parameter và verdict; không thêm claim về write SQL nếu không có evidence.
4. **Thao tác:** Quay lại trang chính và nhấn `Ctrl+R` để dọn trạng thái UI trước khi kết thúc demo.
   - **Nói khi demo:** “Tôi kết thúc ở trạng thái sạch để không để payload/response của demo ảnh hưởng lần chạy tiếp theo.”
   - **F12 show:** Network → bấm `Clear`; đặt Filter rỗng hoặc filter phù hợp; không cần mở Elements để tìm payload cũ.
   - **Quan sát:** Trang trở về trạng thái ban đầu và các request cũ đã được loại khỏi bảng Network hiện tại.
**Kết luận:** Comparison giúp trình bày kết quả, còn request/response/trace mới là bằng chứng cho từng kết luận SQL injection.

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
