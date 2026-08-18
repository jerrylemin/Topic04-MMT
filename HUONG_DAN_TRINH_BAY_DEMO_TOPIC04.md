# Hướng dẫn trình bày và demo Topic04

Tài liệu này đi cùng `Topic04_Broadside_Demo.pptx`. Trình tự được thiết kế theo đúng `BaiTapTopic04.docx`: nêu cơ chế → demo bản vulnerable → giải thích bằng trace/code → demo bản secure → trả lời câu hỏi ngay tại chỗ.

## 1. Chuẩn bị trước buổi trình bày

### Phạm vi an toàn

- Chỉ chạy các ứng dụng cố tình có lỗ hổng trong thư mục Topic04 và chỉ dùng `127.0.0.1`.
- Chỉ dùng các payload cố định đã có trong lab. Không thay host, không gửi payload ra website thật.
- Không chiếu toàn bộ cookie, token, password, password hash hoặc secret. Khi mở DevTools chỉ tập trung vào tên cookie, thuộc tính, phần giá trị đã che hoặc giá trị demo được README cho phép.
- Lab02 chỉ minh họa ghi tràn/crash có kiểm soát; không shellcode, ROP, reverse shell hoặc persistence.

### Bố trí màn hình

1. Màn hình chính: PowerPoint ở chế độ Presenter View.
2. Cửa sổ trình duyệt thứ nhất: ứng dụng lab, zoom 110–125%.
3. Cửa sổ trình duyệt thứ hai hoặc tab riêng: DevTools, chủ yếu dùng Network, Elements và Application/Storage.
4. Terminal riêng cho từng lab; giữ terminal Lab02/WSL độc lập.
5. Dùng tài khoản trình duyệt sạch hoặc cửa sổ Incognito để cookie của các lần chạy cũ không làm sai kết quả.

### Khởi động

Từ thư mục gốc:

```powershell
cd C:\Users\Administrator\Documents\MEGA\mmt\Topic04
```

Mở từng terminal, vào đúng thư mục lab rồi chạy launcher. Không cần quyền Administrator.

| Lab | Lệnh Windows | URL |
|---|---|---|
| Lab01 | `cd Lab01; scripts\run_lab.bat` | `http://127.0.0.1:5000` |
| Lab02 | `cd Lab02; scripts\run_lab_wsl.bat` | `http://127.0.0.1:5002` |
| Lab03 | `cd Lab03; scripts\run_lab.bat` | `http://127.0.0.1:5003` |
| Lab04 | `cd Lab04; scripts\run_lab.bat` | Victim `:5004`, Demo Page `:9004` |
| Lab05 | `cd Lab05; scripts\run_lab.bat` | `http://127.0.0.1:5005` |
| Lab06 | `cd Lab06; scripts\run_lab.bat` | `http://127.0.0.1:5006` |

Lab02 phụ thuộc Linux/WSL, GCC, GDB và các binary native. Nếu launcher WSL không chạy, vào WSL tại thư mục Lab02 rồi dùng:

```bash
sh scripts/run_lab.sh
```

### Kiểm tra nhanh trước khi chiếu

- Mở đủ các URL và xác nhận trang chủ trả về bình thường.
- Reset Lab03–Lab06 trước buổi demo để dữ liệu khớp seed:

```powershell
cd C:\Users\Administrator\Documents\MEGA\mmt\Topic04\Lab03
python scripts\reset_database.py

cd ..\Lab04
python scripts\reset_database.py

cd ..\Lab05
python scripts\reset_database.py

cd ..\Lab06
python scripts\reset_database.py
```

- Lab01 có thể reset bằng `python scripts\reset_database.py` nếu comment cũ còn tồn tại.
- Chuẩn bị sẵn payload trong Notepad để tránh gõ sai khi đang nói.
- Tắt extension chặn script cho site local; giữ popup/alert được phép ở Lab01.

## 2. Nhịp trình bày chung

Với mỗi lab, dùng đúng năm nhịp:

1. **Nhận diện trust boundary:** dữ liệu nào do client kiểm soát?
2. **Dự đoán:** nếu server/DOM tin dữ liệu đó, điều gì sẽ xảy ra?
3. **Demo vulnerable:** dùng một input cố định và quan sát request → xử lý → sink/quyết định.
4. **Demo secure:** gửi lại cùng input, chỉ thay cơ chế xử lý.
5. **Kết luận và trả lời câu hỏi:** root cause, primary fix, defense in depth, remaining risk.

Không đọc nguyên văn slide. Slide là biển chỉ đường; bằng chứng nằm ở ứng dụng, trace, inspector và đoạn mã so sánh.

## 3. Kịch bản chi tiết theo slide

### Mở đầu — slide 1–5

- Slide 1: giới thiệu Topic04 và nguyên tắc “trình bày tới đâu, demo đúng lab tới đó”.
- Slide 2: nói rõ phạm vi local/hợp pháp.
- Slide 3: chốt luận điểm xuyên suốt: mọi input từ client đều không đáng tin.
- Slide 4: cho khán giả thấy sơ đồ port 5000, 5002, 5003, 5004/9004, 5005, 5006.
- Slide 5: giải thích nhịp demo năm bước ở trên.

### Lab01 — Cross-Site Scripting — slide 6–16

#### A. Reflected XSS — demo tại slide 8, trả lời tại slide 9

1. Mở `http://127.0.0.1:5000/vulnerable/search`.
2. Dán payload:

```html
<img src=x onerror="alert('Reflected XSS')">
```

3. Trước khi gửi, dự đoán: input đi trong query, server trả lại vào HTML, trình duyệt tạo node `<img>` và chạy event handler khi ảnh lỗi.
4. Gửi form. Kết quả mong đợi: alert xuất hiện ở bản vulnerable.
5. Mở trace theo thứ tự Request → Flask/Jinja → Response → Source→Sink → Verdict. Nhấn mạnh query không được lưu; nó quay lại trong chính response của request hiện tại.
6. Mở DevTools > Network, chọn request search, chỉ ra query string và đoạn response liên quan.
7. Mở bản secure `/secure/search`, gửi lại đúng payload. Kết quả mong đợi: chuỗi được hiển thị như text/được escape; không có alert.
8. Khi trả lời ba câu ở slide 9, nói rõ:
   - Request mang payload: request search có query do người dùng nhập.
   - Response vulnerable tạo HTML executable; secure biến ký tự đặc biệt thành dữ liệu.
   - XSS xảy ra trong browser vì browser parse response và thực thi handler, dù source taint bắt đầu từ server request.

#### B. Stored XSS — demo tại slide 10, trả lời tại slide 11

1. Mở `/vulnerable/post/1/comments`.
2. Đăng comment:

```html
<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>
```

3. Kết quả mong đợi: comment được ghi vào SQLite; alert xuất hiện khi trang render.
4. Reload trang hoặc mở tab mới cùng URL. Alert tiếp tục xuất hiện, chứng minh payload tồn tại qua request khác.
5. Trong Database Inspector chỉ ra bản ghi comment; trong code comparison chỉ ra sink `Markup(row["body"])` của bản vulnerable.
6. Reset database hoặc xóa comment demo, rồi mở `/secure/post/1/comments` và gửi cùng payload.
7. Kết quả mong đợi: sanitization bằng allowlist loại event handler/thẻ nguy hiểm; không alert. Phần markup được cho phép chỉ tồn tại theo policy của sanitizer.
8. Khi trả lời slide 11, phân biệt rõ:
   - Stored khác Reflected ở chỗ payload được lưu rồi ảnh hưởng nhiều request/người xem.
   - Dữ liệu đi qua form → Flask → SQLite → Jinja/HTML → browser.
   - Encode output là mặc định an toàn; sanitize chỉ dùng khi nghiệp vụ thực sự cho phép một phần HTML.

#### C. DOM-based XSS — demo tại slide 12

1. Mở `/vulnerable/dom-search`.
2. Thay fragment sau dấu `#` bằng:

```text
#<img src=x onerror="alert('DOM XSS')">
```

3. Kết quả mong đợi: alert xuất hiện; Network không có request mới chứa fragment.
4. Mở DevTools > Network để chứng minh fragment không được gửi lên server.
5. Mở Sources/Code Comparison: vulnerable dùng `innerHTML`; secure dùng `textContent`.
6. Mở `/secure/dom-search` với cùng fragment. Kết quả mong đợi: payload chỉ là text.
7. Kết luận: DOM XSS vẫn là XSS nhưng source và sink có thể nằm hoàn toàn phía client.

#### D. Trả lời phần báo cáo — slide 13–16

- Slide 13–14 trả lời lần lượt năm câu báo cáo của Lab01; slide 15–16 chốt code fix và defense in depth.
- Câu trả lời miệng nên luôn theo công thức: **bằng chứng quan sát được → root cause → bản vá chính → lớp bổ sung**.
- Không nói CSP hay HttpOnly “chữa” XSS. Primary fix là output encoding/sanitization đúng ngữ cảnh và tránh sink nguy hiểm; CSP/HttpOnly chỉ giảm tác động.

### Lab02 — Buffer Overflow — slide 17–26

#### A. Chuẩn bị và giải thích stack — slide 17–18

- Chỉ chạy Lab02 trong WSL/Linux hoặc container/profile phù hợp.
- Nêu dữ kiện từ source: `char name[32]`; chuỗi C cần một byte `\0`, nên capacity dữ liệu là 31 byte.
- Vulnerable dùng `strcpy` không có giới hạn. Hai bản secure dùng kiểm tra chiều dài hoặc `snprintf` và kiểm tra giá trị trả về.

#### B. So sánh độ dài — demo tại slide 19

1. Mở `http://127.0.0.1:5002/vulnerable`.
2. Chọn input bình thường `Le Minh`; chạy `vulnerable_asan`. Kết quả mong đợi: xử lý bình thường.
3. Chọn 31 byte. Kết quả mong đợi: vừa đủ capacity dữ liệu.
4. Chọn 32 byte. Giải thích: đã cần 33 byte nếu tính null terminator; đây là lần đầu chắc chắn vượt capacity, nhưng không được khẳng định nó luôn làm tiến trình crash.
5. Chọn 64 byte với `vulnerable_asan`. Kết quả mong đợi khi runtime ASan đầy đủ: báo stack-buffer-overflow, trỏ tới thao tác copy và exit khác 0.
6. Chạy lại 64 byte ở `/secure/length` và `/secure/snprintf`. Kết quả mong đợi: từ chối/truncate theo contract của từng bản vá, không ghi ngoài buffer.
7. Mở Memory Visualizer và ASan Inspector; phân biệt “vượt capacity”, “ASan phát hiện” và “process crash” là ba mốc có thể khác nhau.

Có thể dùng client cố định trong WSL:

```bash
python scripts/send_request.py --mode vulnerable_asan --text "Le Minh"
python scripts/send_request.py --mode vulnerable_asan --length 64
python scripts/send_request.py --mode secure_length --length 64
python scripts/send_request.py --mode secure_snprintf --length 64
```

#### C. GDB — demo tại slide 20

```bash
ulimit -c 0
gdb -q -x gdb/inspect_normal.gdb
gdb -q -x gdb/inspect_overflow.gdb
gdb -q -x gdb/inspect_hardened.gdb
```

Trong GDB chỉ quan sát:

- frame hiện tại và backtrace;
- địa chỉ buffer/stack xung quanh;
- khác biệt giữa input bình thường và input dài;
- binary debug so với hardened.

Không sửa register, instruction pointer hoặc luồng thực thi.

#### D. Trả lời câu hỏi — slide 21–26

- Slide 21–22: năm câu phân tích.
- Slide 23–24: năm câu báo cáo.
- Slide 25: đối chiếu root fix với hardening.
- Slide 26: kết luận Lab02.

Thông điệp bắt buộc:

- Root cause là copy không giới hạn vào buffer kích thước cố định.
- Kiểm tra length/`snprintf` là primary fix.
- Canary, PIE/ASLR, NX, RELRO và FORTIFY là defense in depth; không biến `strcpy` sai thành đúng.
- Nếu máy trình bày chưa có log GDB/ASan runtime thật, nói thẳng đó là phần chưa thu thập; dùng source, visualizer và lệnh tái hiện, không trình bày output giả.

### Lab03 — Parameter Tampering — slide 27–34

#### Tài khoản và seed

| Tài khoản | Mật khẩu | Vai trò |
|---|---|---|
| `user_a` | `UserA123!` | user |
| `user_b` | `UserB123!` | user |
| `admin` | `Admin123!` | admin |

Product 5 có giá server `100000`; invoice 1001/1003 thuộc User A, invoice 1002 thuộc User B.

#### A. Sửa giá — demo tại slide 29

1. Reset database, đăng nhập `user_a`.
2. Mở `/vulnerable/checkout` và chọn product 5.
3. Dùng Request Editor/DevTools đổi giá client từ `100000` thành `1`, giữ nguyên `product_id=5`.
4. Submit. Kết quả mong đợi: vulnerable dùng giá client và tạo kết quả sai.
5. Gửi cùng dữ liệu tới `/secure/checkout`.
6. Kết quả mong đợi: server bỏ qua giá client, lấy `products.price_vnd=100000`, ghi mismatch vào audit.
7. Nói: validate “giá là số dương” vẫn chưa đủ; invariant đúng là giá authoritative phải đến từ database/server.

#### B. IDOR — demo tại slide 30

1. Vẫn đăng nhập `user_a`, mở `/vulnerable/invoice?id=1001`.
2. Đổi URL thành `id=1002`.
3. Kết quả mong đợi: vulnerable lộ invoice của User B.
4. Mở `/secure/invoice?id=1002`.
5. Kết quả mong đợi: HTTP 403; nội dung invoice không được render; audit ghi `invoice_access_denied`.
6. Nói: authentication chỉ biết “ai đang đăng nhập”; authorization theo object mới trả lời “người đó có được xem invoice này không”.

#### C. Role tampering/mass assignment — demo tại slide 31

1. Mở `/vulnerable/profile`.
2. Đổi hidden field `role=user` thành `role=admin`, rồi submit.
3. Kết quả mong đợi: vulnerable ghi role từ client vào database/session.
4. Reset lab và đăng nhập lại `user_a`.
5. Gửi thêm `role=admin` tới `/secure/profile`.
6. Kết quả mong đợi: server chỉ allowlist `email`, lấy user ID từ session, giữ role `user`, audit ghi `sensitive_field_submitted`.

#### D. Trả lời câu hỏi — slide 32–34

- Slide 32 trả lời câu 1–2; slide 33 trả lời câu 3–5; slide 34 kết luận.
- IDOR thuộc Broken Access Control. Theo OWASP Top 10 hiện hành trong deck, nó được đặt ở A01:2025.
- Audit giúp phát hiện và điều tra nhưng không thay authorization.

### Lab04 — CSRF — slide 35–42

#### Tài khoản và origin

| Tài khoản | Mật khẩu |
|---|---|
| `victim` | `Victim123!` |
| `receiver` | `Receiver123!` |

- Victim Application: `http://127.0.0.1:5004`
- Demo Page: `http://127.0.0.1:9004`
- `127.0.0.1:9004 → 127.0.0.1:5004`: cross-origin nhưng same-site.
- `localhost:9004 → 127.0.0.1:5004`: cross-origin và cross-site.

#### A. Vulnerable email change — demo tại slide 37

1. Mở Victim `/login`, đăng nhập `victim`.
2. Mở dashboard/profile và chỉ ra email ban đầu `victim_old@lab.local`.
3. Ở tab khác, mở `http://127.0.0.1:9004/attack/vulnerable-email`.
4. Bấm gửi và xác nhận form local cố định.
5. Kết quả mong đợi: POST tới Victim không có CSRF token/Origin check; email đổi thành `demo_changed@lab.local` vì browser gửi cookie phiên theo quy tắc hiện hành.
6. Mở Network để chỉ ra request phát sinh từ origin khác và trạng thái mutation.

Lưu ý trung thực: phiên bản lab hiện tại **không auto-submit**. Người dùng phải bấm và xác nhận. Đây là chủ ý an toàn của implementation và khác với mô tả CSRF auto-submit kinh điển trong đề; cơ chế server thiếu kiểm tra ý định vẫn là điểm cần quan sát.

#### B. Secure route — demo tại slide 38

1. Reset email hoặc reset database rồi đăng nhập lại.
2. Mở Demo Page `/attack/secure-email`, gửi request thiếu token.
3. Kết quả mong đợi: HTTP 403 và state không đổi.
4. Nếu UI có scenario bad token, gửi token sai; kết quả vẫn 403.
5. Mở trực tiếp Victim `/secure/change-email`.
6. Submit form hợp lệ. Kết quả mong đợi: hidden token hợp lệ, Origin/Referer hợp lệ, UPDATE thành công rồi token rotate.
7. Chỉ ra nguyên tắc “deny trước mutation”: mọi kiểm tra phải xong trước khi cập nhật database.

#### C. Trả lời câu hỏi — slide 39–42

- Slide 39: câu 1–2; slide 40: câu 3–5; slide 41: ba lớp phòng thủ; slide 42: kết luận.
- Token chống CSRF chứng minh request đi qua form/flow hợp lệ của ứng dụng; cookie phiên một mình chỉ chứng minh browser có phiên.
- SameSite giảm một số request cross-site nhưng không thay token/Origin validation và không đồng nghĩa same-origin.
- SOP chủ yếu hạn chế đọc response; nó không đảm bảo request gây thay đổi trạng thái không được gửi.
- Hành vi SameSite/SOP phải quan sát bằng browser thật; test client Flask không phải bằng chứng đầy đủ cho policy của browser.

### Lab05 — SQL Injection — slide 43–50

#### Tài khoản demo

| Tài khoản | Mật khẩu |
|---|---|
| `admin_lab` | `AdminLab123!` |
| `student_a` | `StudentA123!` |
| `student_b` | `StudentB123!` |

Lab chỉ dùng scenario SELECT/read-only cố định. Không tự chế payload ghi/xóa dữ liệu.

#### A. Login injection — demo tại slide 45

1. Mở `/vulnerable/login`, đăng nhập bình thường `admin_lab` / `AdminLab123!`; cho thấy query được nối chuỗi và session được tạo khi có user.
2. Chọn scenario **Dấu nháy đơn**. Kết quả mong đợi: SQLite báo lỗi cú pháp đã được Error Inspector rút gọn; không lộ traceback/path.
3. Chọn scenario cố định với username:

```text
admin_lab' -- 
```

4. Nhập password bất kỳ. Kết quả mong đợi: comment làm phần điều kiện digest không còn tham gia; vulnerable tạo session demo.
5. Gửi cùng input tới `/secure/login`.
6. Kết quả mong đợi: `WHERE username = ?` coi toàn bộ chuỗi là dữ liệu; không match user và trả thông báo chung.
7. Đăng nhập secure bình thường để chỉ ra bước lookup bằng placeholder rồi xác minh PBKDF2 ở application layer.

#### B. Search injection — demo tại slide 46

1. Mở `/vulnerable/search?keyword=USB`; kết quả chỉ chứa sản phẩm có `USB`.
2. Chọn scenario cố định:

```text
%' OR 1=1 -- 
```

3. Kết quả mong đợi: vulnerable mở rộng result set trong bảng `products` thành 8 dòng; không đọc bảng khác và không ghi database.
4. Gửi cùng chuỗi tới `/secure/search`.
5. Kết quả mong đợi: chuỗi được bind trong `LIKE ?`, cấu trúc SQL không đổi và trả 0 dòng.
6. Mở Query Construction → SQL Execution → Result Set để chứng minh khác biệt giữa “chuỗi SQL cuối bị thay logic” và “query template cố định + parameter”.

#### C. Trả lời câu hỏi — slide 47–50

- Slide 47: câu 1–2; slide 48: câu 3–5; slide 49–50 chốt code và kết luận.
- Root cause: trộn dữ liệu vào cấu trúc SQL bằng nối chuỗi.
- Primary fix: parameterized query ở mọi vị trí có thể bind; với identifier/order direction phải dùng allowlist, không cố bind cú pháp.
- Validation, least privilege, generic error và logging là defense in depth.
- Password hashing ngăn lộ password khi database bị lấy; nó không sửa SQL injection.

### Lab06 — Cookie Poisoning — slide 51–60

#### Tài khoản demo

| Tài khoản | Mật khẩu | Vai trò |
|---|---|---|
| `student` | `Student123!` | user |
| `admin_lab` | `AdminLab123!` | admin |

Mở DevTools > Application/Storage > Cookies > `http://127.0.0.1:5006`.

#### A. Plain cookie — demo tại slide 53

1. Mở `/login`, chọn **Plain Cookie Demo**, đăng nhập `student`.
2. Quan sát `lab06_username=student` và `lab06_role=user` cùng Path/HttpOnly/SameSite/Secure.
3. Mở `/vulnerable/plain/admin`; ban đầu bị từ chối.
4. Trong DevTools, sửa duy nhất `lab06_role` từ `user` thành `admin`.
5. Reload `/vulnerable/plain/admin`.
6. Kết quả mong đợi: vulnerable cho phép vì server tin role do client gửi.
7. Nói rõ: HttpOnly chỉ cản JavaScript đọc cookie; người sở hữu browser vẫn có thể sửa bằng DevTools và request vẫn mang giá trị đã sửa.

#### B. Base64 cookie — demo tại slide 54

1. Logout/reset, chọn **Base64 Cookie Demo**, đăng nhập `student`.
2. Mở profile và Base64 Inspector; giải mã trạng thái cố định `role=user`.
3. Copy đúng giá trị demo `role=admin` đã hiển thị read-only trong UI.
4. Sửa cookie bằng DevTools rồi reload `/vulnerable/base64/admin`.
5. Kết quả mong đợi: được phép. Kết luận: Base64 là encoding có thể đảo ngược, không có secret và không tạo integrity.

#### C. Signed và encrypted cookie — demo tại slide 55

1. Chọn **Signed Cookie Demo**, đăng nhập `student`.
2. Mở `/secure/signed/profile` và Signature Inspector; chỉ quan sát payload/signature đã che.
3. Sửa một ký tự trong signed cookie, reload.
4. Kết quả mong đợi: chữ ký không hợp lệ, server từ chối trước khi dùng payload.
5. Mở `/secure/encrypted-demo`; giải thích encryption che nội dung và cơ chế authenticated encryption đồng thời bảo vệ integrity.
6. Không hiển thị secret key hoặc toàn bộ token.

#### D. Server-side session — demo tại slide 56

1. Logout/reset, chọn **Server-side Session Demo**, đăng nhập `student`.
2. Mở `/secure/session/profile`, chỉ ra cookie là opaque ID/fingerprint; role được lấy từ database.
3. Mở `/secure/session/admin`. Kết quả mong đợi: student bị từ chối.
4. Logout, đăng nhập `admin_lab` cùng mode.
5. Mở `/secure/session/admin`. Kết quả mong đợi: được phép vì server lấy role admin hiện tại từ database.
6. So sánh fingerprint trước/sau login để minh họa session rotation; sau POST logout, record server-side inactive/revoked và cookie browser hết hạn.

#### E. Trả lời câu hỏi — slide 57–60

- Slide 57: câu 1–2; slide 58: câu 3–5; slide 59–60 chốt ma trận và kết luận.
- Signed cookie bảo vệ integrity/authenticity nhưng payload thường vẫn đọc được.
- Encrypted cookie bảo vệ confidentiality và, với scheme đúng, integrity.
- Server-side session giảm dữ liệu tin cậy ở client và cho phép revoke/đổi role trung tâm; vẫn cần cookie ngẫu nhiên, rotation, expiry, CSRF protection và TLS.
- Với HTTP local, `Secure=false` có thể là cấu hình dev trung thực vì browser thường không gửi Secure cookie qua `http://127.0.0.1`. Production HTTPS phải bật Secure.

### Tổng hợp — slide 61–67

- Slide 61: nối sáu lab về một trust-boundary map.
- Slide 62: đặt ba câu hỏi root-cause: dữ liệu đến từ đâu, được parse ở đâu, quyết định nào đang tin nó?
- Slide 63: nhắc primary fix phải đứng trước defense in depth.
- Slide 64: chạy nhanh toàn bộ demo theo port nếu giảng viên yêu cầu kiểm tra lại.
- Slide 65: phương án dự phòng khi live demo lỗi.
- Slide 66: xác nhận đã trả lời 41/41 câu hỏi theo thứ tự đề.
- Slide 67: kết bằng thông điệp “đừng nhớ payload; hãy nhớ trust boundary”.

## 4. Bản đồ 41 câu hỏi trong BaiTapTopic04.docx

| Phần | Số câu | Slide trả lời |
|---|---:|---|
| Lab01 — Reflected XSS | 3 | 9 |
| Lab01 — Stored XSS | 3 | 11 |
| Lab01 — Câu hỏi báo cáo | 5 | 13–14 |
| Lab02 — Câu hỏi phân tích | 5 | 21–22 |
| Lab02 — Câu hỏi báo cáo | 5 | 23–24 |
| Lab03 — Câu hỏi báo cáo | 5 | 32–33 |
| Lab04 — Câu hỏi phân tích | 5 | 39–40 |
| Lab05 — Câu hỏi phân tích | 5 | 47–48 |
| Lab06 — Câu hỏi phân tích | 5 | 57–58 |
| **Tổng** | **41** | **Đủ theo thứ tự đề** |

Speaker notes của từng slide chứa lời dẫn và nguồn file local để đối chiếu khi tập.

## 5. Phương án dự phòng và khôi phục

### Khi port bận

Không đổi sang host public. Dừng đúng process lab cũ rồi chạy lại. Có thể kiểm tra PID:

```powershell
Get-NetTCPConnection -State Listen | Where-Object LocalPort -in 5000,5002,5003,5004,5005,5006,9004
```

### Khi state demo sai

- Lab01: reset database rồi chạy lại đúng payload.
- Lab03–Lab06: chạy `python scripts\reset_database.py`, xóa cookie site local và đăng nhập lại.
- Lab04: nhớ reset email trước secure comparison.
- Lab06: mỗi mode dùng cookie khác; logout/reset trước khi chuyển mode để khán giả không nhầm trạng thái.

### Khi live demo không chạy

1. Không giả vờ kết quả thành công.
2. Nói rõ lỗi hiện tại: port, WSL/GDB, cookie cũ hay state database.
3. Dùng trace/evidence đã có trong UI hoặc log repository và chỉ ra lệnh tái hiện.
4. Tiếp tục phần giải thích bằng source comparison và expected invariant.
5. Riêng Lab02, không gọi source/visualizer là “ASan/GDB runtime evidence” nếu chưa chạy được trên máy trình bày.

## 6. Checklist 10 phút trước giờ trình bày

- [ ] PPT mở đúng font fallback, không báo repair.
- [ ] Presenter notes hiển thị.
- [ ] Sáu URL local truy cập được; Lab04 có cả 5004 và 9004.
- [ ] Database Lab03–Lab06 đã reset.
- [ ] Ba payload XSS và hai scenario SQLi đã copy sẵn.
- [ ] Tài khoản demo đã thử đăng nhập.
- [ ] DevTools đang ở đúng site và không lộ secret/full cookie.
- [ ] Lab02 WSL/GDB đã build; nếu chưa, chuẩn bị nói rõ giới hạn evidence.
- [ ] Lab04 đã tập thao tác bấm + xác nhận, không nói là auto-submit.
- [ ] Có kế hoạch chuyển ngay sang trace/code comparison nếu browser hoặc terminal trục trặc.

