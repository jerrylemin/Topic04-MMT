# Demo script Lab02 — Buffer Overflow

## Mục tiêu demo

- Chứng minh `char name[32]` chỉ chứa 31 byte dữ liệu và byte `null`.
- Phân biệt vượt capacity, ASan phát hiện và process crash.
- Quan sát native trace/GDB rồi đối chiếu length check và `snprintf`.
- Giải thích hardening là defense in depth, không thay thế kiểm tra độ dài.

## Chuẩn bị

- Thư mục làm việc: `cd Lab02`
- Khởi động: `scripts\run_lab.bat`. Native/WSL demo cần Ubuntu có `pip`, `gcc`, `make` và `gdb`; nếu Ubuntu thiếu `pip`, launcher rơi vào Windows fallback, UI vẫn lên nhưng Linux ELF không chạy và POST native trả HTTP `503` với `status=unavailable`.
- URL: `http://127.0.0.1:5002`
- Native tool: WSL/Ubuntu có `make`, `gdb`; đặt `ulimit -c 0` trước GDB.
- Dùng UI với `Build profile`, `Trường name`, các mẫu `A × 31`, `A × 32`, `A × 64`.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`; bấm tab `Network`, bật `Preserve log` và `Disable cache`, rồi bấm thùng rác `Clear` trước từng lần submit.
- Ở ô `Filter` gõ đúng một phần endpoint: `/submit`, `/secure/length/submit` hoặc `/secure/snprintf/submit`. Bấm từng dòng mới nhất; sau đó vào `Headers` → `General` kiểm tra `Request Method=POST` và đúng `Request URL` trước khi show.
- Nếu có nhiều dòng cùng tên, chọn dòng vừa phát sinh sau lần bấm submit; nếu vẫn không chắc, mở `Payload` → `Form Data` và đối chiếu `mode`/mẫu `name` (31, 32 hay 64 ký tự).
- Trong pane bên phải bấm `Headers` → mở `General` để chỉ URL/method/status; bấm `Payload` → mở `Form Data` để chỉ `mode` và `name`; bấm `Response` hoặc `Preview` để chỉ trace/status. Khi tìm trong response, dùng từ khóa đặc trưng của mode như `stack-buffer-overflow`, `Rejected`, `written` hoặc `Compiler Hardening Inspector`, không tìm một từ quá chung.
- Sau khi xem F12, quay lại trang Lab02, cuộn xuống `Trace Panel` và bấm đúng tab ứng dụng `Request`, `Native process`, `Memory` hoặc `ASan`. Tab `ASan` có tiêu đề `AddressSanitizer Inspector`.
- GDB không nằm trong F12: output frame/backtrace phải chỉ từ cửa sổ WSL. Tab `Sources` của browser không thể chứng minh binary C đã chạy.


## Kịch bản trình bày

*Quy ước: đọc từng mục theo thứ tự **Thao tác → Nói khi demo → F12 show → Quan sát**. Chỉ kết luận ASan/GDB khi runtime native hoặc WSL thật sự trả bằng chứng.*

### Bước 1 — Xác lập đường đi HTTP → tiến trình C

1. **Thao tác:** Mở `http://127.0.0.1:5002`, rồi bấm `Bắt đầu bản lỗi`.
   - **Nói khi demo:** “Tôi bắt đầu ở flow vulnerable để nối request HTTP với tiến trình C phía sau.”
   - **F12 show:** Nhấn `F12` → bấm tab `Network` → bấm biểu tượng thùng rác `Clear`. Tích `Preserve log` và `Disable cache`. Trong ô `Filter` ở góc trên trái, nhập `/submit`.
   - **Quan sát:** Trang Lab02 và form nhập liệu xuất hiện. Chưa có dòng request phù hợp để chọn cho đến khi form được gửi.
2. **Thao tác:** Ở ô `Build profile`, bấm mũi tên dropdown và chọn `Vulnerable + AddressSanitizer`.
   - **Nói khi demo:** “Tôi chọn đúng binary vulnerable có ASan để nếu toolchain hỗ trợ thì lỗi native sẽ được ghi nhận.”
   - **F12 show:** Giữ tab `Network` và bộ lọc `/submit`. Chưa chọn request khi chưa bấm gửi. Không tìm ASan trong `Sources` của browser vì đây là profile chạy phía server/native.
   - **Quan sát:** Tên profile trên form đổi đúng lựa chọn. Đây mới là bằng chứng UI đã chọn profile, chưa phải bằng chứng binary đã chạy.
3. **Thao tác:** Bấm textarea `Trường name` → nhấn `Ctrl+A` → nhập `Le Minh` → bấm `Gửi đến tiến trình C`.
   - **Nói khi demo:** “Input ngắn tạo baseline để đối chiếu byte length, buffer và exit code trước khi thử chuỗi dài.”
   - **F12 show:** Trong Network, bấm dòng mới nhất có tên `submit`. Bấm `Headers` → mở mục `General` để kiểm tra `Request Method: POST`, URL và status. Sau đó bấm `Payload` → mở `Form Data` và chỉ vào `mode=vulnerable_asan` cùng `name=Le Minh`. Nếu không thấy `Form Data`, đang chọn nhầm dòng hoặc form chưa gửi lại.
   - **Quan sát:** Ghi status và response thực tế. Request thành công không đồng nghĩa đã có overflow.
4. **Thao tác:** Cuộn trang đến `Trace Panel`, lần lượt mở các tab `Request`, `Native process` và nếu có thì `Memory`.
   - **Nói khi demo:** “HTTP chỉ là điểm kích hoạt; trace panel mới cho thấy input đã đi vào tiến trình native như thế nào.”
   - **F12 show:** Quay lại dòng `submit` vừa chọn → bấm `Response` → tìm `trace_id`; sau đó mở tab ứng dụng `Request`/`Native process` và đọc `exit_code` nếu runtime có trả. Chỉ mở `Elements` hoặc `Sources` khi cần xem giao diện, không dùng chúng để kết luận stack.
   - **Quan sát:** Chỉ đọc bytes và exit code đang hiển thị thật. Nếu trace không có dữ liệu, nói rõ “chưa có bằng chứng runtime” thay vì tự suy luận.
**Kết luận:** HTTP là điểm kích hoạt; sink nguy hiểm nằm ở `strcpy(name, user_input)`.

### Bước 2 — Chạm ranh giới 31/32/64 byte

1. **Thao tác:** Giữ `Build profile = Vulnerable + AddressSanitizer` và bảo đảm ô `Trường name` đang ở trạng thái có thể nhập.
   - **Nói khi demo:** “Tôi giữ nguyên binary vulnerable để so sánh ba độ dài trên cùng một đường xử lý.”
   - **F12 show:** Trong `Network`, bấm `Clear`, giữ `Preserve log`, và đặt `Filter` là `/submit`. Làm vậy để ba request mới không bị lẫn với baseline.
   - **Quan sát:** Network chưa có ba dòng mới; đây là mốc bắt đầu phép so sánh.
2. **Thao tác:** Nhập lần lượt `A × 31`, `A × 32` và `A × 64` vào textarea; sau mỗi lần bấm `Gửi đến tiến trình C`, chờ trace/status cập nhật rồi mới gửi độ dài tiếp theo.
   - **Nói khi demo:** “Tôi tăng từ 31 lên 32 rồi 64 byte để kiểm tra ranh giới của buffer, không gọi mọi lỗi HTTP là overflow.”
   - **F12 show:** Sau mỗi lần gửi, trong Network chọn đúng dòng mới nhất có tên `submit` → `Headers` → `General` kiểm tra `POST` và status → `Payload` → `Form Data`. Xác nhận trường `name` lần lượt có 31, 32 và 64 ký tự `A`. Nếu các dòng gần giống nhau, chọn bằng cách đối chiếu số lượng `A` trong `Payload`, không chọn chỉ dựa vào vị trí dòng.
   - **Quan sát:** Ghi riêng kết quả của 31, 32 và 64 byte ở Trace Panel/status. Một request 200 vẫn có thể chứa thông tin lỗi trong response, nên phải xem cả response và trace.
3. **Thao tác:** Sau khi gửi `A × 64`, mở phần ASan/trace và cuộn đến dòng kết quả lỗi.
   - **Nói khi demo:** “Ở payload 64 byte, tôi tìm thông báo sanitizer cụ thể để chứng minh lỗi bộ nhớ.”
   - **F12 show:** Chọn lại request có `name` dài 64 → bấm `Response` → `Ctrl+F` nhập chính xác `stack-buffer-overflow`. Chỉ chọn occurrence nằm trong kết quả của request 64 byte; không lấy chữ mẫu trong hướng dẫn. Trên UI, mở tab `ASan` có tiêu đề `AddressSanitizer Inspector`.
   - **Quan sát:** Nếu thấy `stack-buffer-overflow` và trace tương ứng, đó là bằng chứng runtime. Nếu không thấy, trình bày kết quả đang có và ghi rõ ASan chưa trả marker này.
**Kết luận:** 31/32/64 byte là phép đo ranh giới; chỉ marker ASan/trace thật mới xác nhận overflow.

### Bước 3 — Quan sát stack frame bằng GDB

1. **Thao tác:** Giữ request browser ở trạng thái đã gửi và chuẩn bị mở WSL/terminal; không tìm nút GDB trong trang.
   - **Nói khi demo:** “GDB chạy ngoài browser, còn DevTools chỉ giúp tôi xác định request và input cần tương quan.”
   - **F12 show:** Trong `Network`, chọn request `submit` có payload 64 byte → `Payload` → `Form Data` → chỉ vào trường `name`. Không dùng `Elements` hoặc `Sources` để nói rằng đã xem được stack frame.
   - **Quan sát:** Browser chỉ cho thấy HTTP/response/trace. Cửa sổ WSL mới là nơi hiển thị frame, local và backtrace.
2. **Thao tác:** Trong WSL, chạy `cd /mnt/c/Users/Administrator/Documents/MEGA/mmt/Topic04/Lab02` rồi `make all`.
   - **Nói khi demo:** “Tôi build các binary của Lab02 trước khi mở GDB để tránh debug nhầm file cũ.”
   - **F12 show:** F12 chỉ dùng để giữ request làm mốc: `Network` → chọn `submit` → `Headers` → `General` để đọc URL/status và `Response` → `Ctrl+F` tìm `trace_id` nếu có. Không nói F12 đã kiểm tra compiler/debug symbols.
   - **Quan sát:** Chỉ tiếp tục khi terminal báo build thành công. Nếu build lỗi, dừng phần GDB và báo đúng lỗi terminal.
3. **Thao tác:** Chạy `ulimit -c 0`, sau đó chạy `gdb -q -x gdb/inspect_normal.gdb`.
   - **Nói khi demo:** “Tôi mở kịch bản GDB cho input bình thường để có stack frame baseline.”
   - **F12 show:** Quay lại Network request baseline → `Payload` để chỉ ra input ngắn tương ứng. Không tìm tên lệnh GDB trong response HTML.
   - **Quan sát:** Trong terminal, chỉ vào frame/local/backtrace mà script thật sự in ra; không thay output terminal bằng suy luận từ UI.
4. **Thao tác:** Mở phiên GDB mới bằng `gdb -q -x gdb/inspect_overflow.gdb`; script thật chạy `build/vulnerable_debug` với 64 chữ `A`.
   - **Nói khi demo:** “GDB dùng binary debug riêng; đây là bằng chứng SIGSEGV/backtrace, không phải ASan của request web.”
   - **F12 show:** Network → chọn request có `name` gồm 64 chữ `A` → `Payload` → xác nhận input trước khi nói về kết quả GDB. Không ghép output GDB vào HTTP response hay trace ID của web.
   - **Quan sát:** Ghi đúng `SIGSEGV`, frame/backtrace và register nếu GDB in ra; không gọi là ASan. Nếu script không dừng hoặc không có backtrace, nói rõ trạng thái đó.
5. **Thao tác:** Trở lại browser và đối chiếu trace panel với cửa sổ WSL; chỉ ra phần nào đến từ HTTP và phần nào đến từ native debugger.
   - **Nói khi demo:** “Tôi tách hai nguồn bằng chứng: DevTools chứng minh request/payload, GDB chứng minh stack frame.”
   - **F12 show:** Network → chọn request → `Headers`/`Payload`/`Response`; không mở `Elements` để minh họa GDB. Trace web và phiên GDB là hai tiến trình khác nhau, chỉ tương quan bằng input/độ dài.
   - **Quan sát:** Người xem thấy được ranh giới bằng chứng: DevTools xác nhận request, còn WSL/GDB xác nhận native frame.
**Kết luận:** DevTools xác nhận input đi vào endpoint; GDB/ASan mới cho bằng chứng về stack frame và lỗi native.

### Bước 4 — Cùng input 64 byte qua secure length

1. **Thao tác:** Nhấn `Ctrl+L`, nhập `http://127.0.0.1:5002` và nhấn `Enter` để quay về trang chính.
   - **Nói khi demo:** “Tôi chuyển sang secure length check nhưng giữ nguyên độ dài 64 byte để so sánh công bằng.”
   - **F12 show:** F12 → `Network` → `Clear`; bật `Preserve log`/`Disable cache`; ô `Filter` nhập `/secure/length/submit`.
   - **Quan sát:** Trang mới tải xong; bộ lọc chỉ chờ request secure length, không lấy lại request vulnerable.
2. **Thao tác:** Bấm card hoặc nút `Mở length check`.
   - **Nói khi demo:** “Đây là flow có kiểm tra độ dài trước khi gọi xử lý native.”
   - **F12 show:** Giữ Network filter `/secure/length/submit`. Nếu có request tải trang nhưng không khớp filter, bỏ qua; chỉ chọn request sau khi bấm gửi form.
   - **Quan sát:** Đúng form có tiêu đề `Bản vá kiểm tra độ dài` và badge `TỐI ĐA 31 BYTE` xuất hiện; trang này không có dropdown `Build profile`.
3. **Thao tác:** Nhập `A × 64` vào `Trường name` và bấm `Gửi đến tiến trình C`.
   - **Nói khi demo:** “Tôi gửi đúng input từng gây rủi ro để xem lớp length check chặn ở đâu.”
   - **F12 show:** Chọn dòng mới nhất có tên `submit` hoặc URL chứa `/secure/length/submit` → `Headers` → `General` kiểm tra method/status → `Payload` → `Form Data` xác nhận `name` là 64 chữ `A`. Nếu có nhiều dòng, đối chiếu URL đầy đủ, không chọn dòng vulnerable.
   - **Quan sát:** Ghi status và thông báo hiển thị; không nói “đã chặn” nếu chưa xem response/trace.
4. **Thao tác:** Cuộn `Trace Panel` và mở `Request` rồi `Native process`.
   - **Nói khi demo:** “Secure flow từ chối trước khi copy quá giới hạn, vì vậy trace phải thể hiện nhánh reject.”
   - **F12 show:** Request vừa chọn → `Response` → `Ctrl+F` tìm chính xác `Rejected: input exceeds 31 bytes`, rồi mở `Native process` để đọc exit code `65` nếu có. Nếu marker không xuất hiện hoặc HTTP là `503`, ghi đúng “native evidence bị block”, không tự gọi là reject live.
   - **Quan sát:** Chỉ kết luận length check đã chạy khi response/trace có marker reject; không dùng status `200`/`503` một mình.
**Kết luận:** Kiểm tra độ dài ở biên server/native làm input 64 byte bị từ chối trước thao tác copy nguy hiểm.

### Bước 5 — Secure `snprintf`

1. **Thao tác:** Nhấn `Ctrl+L` → nhập `http://127.0.0.1:5002` → `Enter`, rồi bấm card/nút `Mở snprintf`.
   - **Nói khi demo:** “Tôi chuyển sang nhánh dùng snprintf để minh họa cách giới hạn số byte được ghi.”
   - **F12 show:** Trong Network bấm `Clear`; ô `Filter` nhập `/secure/snprintf/submit`; chỉ chọn request submit sau khi gửi form.
   - **Quan sát:** Form snprintf xuất hiện và Network không còn các request cũ trong danh sách đang lọc.
2. **Thao tác:** Nhập `A × 64` và bấm `Gửi đến tiến trình C`; form `snprintf` không có checkbox kiểm tra độ dài.
   - **Nói khi demo:** “Tôi giữ payload 64 byte và để chính `snprintf` trả về thông tin truncate.”
   - **F12 show:** Chọn request mới nhất → `Headers` → `General` kiểm tra URL/method/status → `Payload` → `Form Data` xác nhận `name` 64 chữ `A`.
   - **Quan sát:** Ghi thông báo viết đủ, cắt ngắn hay từ chối; chưa kết luận chỉ từ status 200.
3. **Thao tác:** Cuộn `Trace Panel` đến output native và mở tab `Native process`; `ASan` chỉ dùng khi request thực sự chạy profile ASan. Kết luận cuối nằm ở thẻ `Final Security Verdict`, không phải tab `Verdict`.
   - **Nói khi demo:** “Bằng chứng an toàn ở đây là số byte được ghi và cách code xử lý phần dư.”
   - **F12 show:** Request → `Response` → `Ctrl+F` tìm chính xác `Rejected: snprintf would truncate input to 31 bytes`. Chỉ vào occurrence trong response của request vừa chọn; không lấy chữ trong menu/hướng dẫn HTML.
   - **Quan sát:** Nếu runtime chạy được, đối chiếu marker với exit code `67`; nếu không, ghi status/trace thực tế và không gọi là đã quan sát truncate.
**Kết luận:** `snprintf` giới hạn số byte ghi; cần xem written/truncate trong response hoặc trace để chứng minh nhánh đã chạy.

### Bước 6 — Hardening

1. **Thao tác:** Nhấn `Ctrl+L` → nhập `http://127.0.0.1:5002` → `Enter`, rồi bấm card/nút `Mở Hardening Inspector`.
   - **Nói khi demo:** “Tôi chuyển sang inspector để kiểm tra các lớp hardening ở build và loader.”
   - **F12 show:** F12 → `Network` → `Clear`; ô `Filter` nhập `/hardening`. Chờ trang inspector tải, sau đó chọn request GET mới nhất.
   - **Quan sát:** Đúng Hardening Inspector xuất hiện; đây là trang hiển thị metadata, chưa phải kết luận compiler flag nếu chưa có output cụ thể.
2. **Thao tác:** Trên trang `Compiler Hardening Inspector`, nhập `A × 64` vào `Trường name` và bấm `Chạy hardened`; mode `secure_hardened` là hidden input, không có dropdown `Build profile` trên trang này.
   - **Nói khi demo:** “Tôi chạy cùng payload dài trên form hardened để đối chiếu với bản lỗi.”
   - **F12 show:** Chọn request POST `/submit` mới nhất → `Headers` → `General` kiểm tra endpoint/status → `Payload` → `Form Data` xác nhận `mode=secure_hardened` và `name` dài 64. Nếu không có body, chỉ dùng URL/response, không bịa Form Data.
   - **Quan sát:** Ghi verdict/status thực tế và giữ trace ID để liên kết với inspector.
3. **Thao tác:** Nếu cần kiểm tra bằng WSL, chạy `make all` trong thư mục Lab02 rồi mở `gdb -q -x gdb/inspect_hardened.gdb`.
   - **Nói khi demo:** “Tôi dùng WSL để xác nhận binary hardened, vì browser không thể tự chứng minh flag compile/link.”
   - **F12 show:** Network → chọn request `/submit` → `Response` → `Ctrl+F` tìm `Compiler Hardening Inspector` hoặc `trace_id`. Đây chỉ là mốc liên kết; flag thật phải đọc từ WSL `file`/`readelf`/`objdump`.
   - **Quan sát:** Chỉ trình bày flag/output mà terminal thật sự in ra; UI hiện tại có thể hiển thị `TẮT`/`Chưa xác định` do chưa có measured metadata.
4. **Thao tác:** Trên Hardening Inspector, chỉ vào bảng build profile và ghi đúng trạng thái đang hiển thị; nếu cần kết luận PIE/NX/RELRO/canary, mở WSL và chạy công cụ binary cho đúng file.
   - **Nói khi demo:** “Tôi tách bằng chứng UI và bằng chứng build: F12 xác nhận request, WSL xác nhận thuộc tính ELF.”
   - **F12 show:** Request GET `/hardening` → `Headers` → `General` kiểm tra đúng host/route. Không dùng DevTools hoặc các ô `TẮT` mặc định để suy ra compiler flag.
   - **Quan sát:** Nếu chưa có output `file`/`readelf`/`objdump`, kết luận là “chưa đo được”, không gọi bảng UI là flag runtime.
**Kết luận:** Hardening là thuộc tính build/loader cần kiểm tra bằng inspector hoặc WSL; DevTools chỉ chứng minh route và response đã được gọi.

## Demo Vulnerable → Secure

| Cùng input | Vulnerable → nguyên nhân | Secure → primary fix |
|---|---|---|
| `Le Minh` | `vulnerable_asan` + `strcpy(name, user_input)`; input bình thường chưa kích hoạt lỗi | `/secure/length` và `/secure/snprintf` vẫn giới hạn buffer |
| `A × 32` | Đã vượt 31 byte dữ liệu; crash không phải điều kiện bắt buộc | Từ chối theo byte length trước copy |
| `A × 64` | ASan kỳ vọng báo `stack-buffer-overflow` nếu runtime có sanitizer; không gọi đây là live evidence nếu chưa chạy | Length check trả reject; `snprintf` kiểm tra `written` và không silent truncation |

## Câu hỏi trong BaiTapTopic04.docx

**Câu 12. Buffer nằm ở vùng nhớ nào?**  
**Trả lời khi demo:** `char name[32]` là biến local nên nằm trong stack frame của hàm native. GDB/source hiện tại dùng chính buffer này để minh họa việc `strcpy` ghi qua ranh giới.

**Câu 13. Điều gì xảy ra khi input vượt quá kích thước buffer?**  
**Trả lời khi demo:** Byte vượt giới hạn có thể ghi đè vùng nhớ lân cận, làm hỏng dữ liệu điều khiển hoặc trạng thái stack. ASan có thể phát hiện và dừng có kiểm soát, nhưng overflow không đồng nghĩa chắc chắn với crash ở mọi lần chạy.

**Câu 14. Vì sao `strcpy`, `gets`, `sprintf` nguy hiểm?**  
**Trả lời khi demo:** Các API này không tự giới hạn dữ liệu theo kích thước vùng đích hoặc dễ bị dùng sai. Lab hiện tại trực tiếp minh họa `strcpy`; `gets` và `sprintf` có cùng rủi ro nếu nhận input không giới hạn.

**Câu 15. Vì sao lỗi memory corruption có thể nghiêm trọng hơn lỗi logic thông thường?**  
**Trả lời khi demo:** Lỗi logic thường làm sai một kết quả nghiệp vụ, còn memory corruption có thể làm hỏng state, crash process hoặc tạo primitive cho thực thi ngoài ý muốn. Vì vậy cần ngăn ghi vượt ranh giới trước khi dựa vào phát hiện hậu kỳ.

**Câu 16. Các cơ chế bảo vệ như stack canary, ASLR, DEP/NX có tác dụng gì?**  
**Trả lời khi demo:** Canary phát hiện một số ghi đè stack; ASLR làm địa chỉ khó đoán; DEP/NX ngăn thực thi tại vùng nhớ dữ liệu. Chúng giảm khả năng khai thác nhưng không sửa được thao tác `strcpy` sai.

**Câu 17. Buffer Overflow khác gì với lỗi Injection?**  
**Trả lời khi demo:** Buffer Overflow phá vỡ ranh giới bộ nhớ của chương trình native. Injection làm dữ liệu được diễn giải như cú pháp của interpreter khác, như SQL hoặc shell; hai lỗi có thể cùng xuất phát từ việc tin input nhưng fix kỹ thuật khác nhau.

**Câu 18. Vì sao một lỗi ở backend native có thể bị kích hoạt qua HTTP?**  
**Trả lời khi demo:** Route Flask nhận body/query rồi truyền chuỗi đó vào subprocess C. HTTP là transport; sink nguy hiểm nằm ở native `strcpy`, nên attacker chỉ cần gửi input đủ dài tới route.

**Câu 19. Vì sao không nên chỉ dựa vào firewall để chống Buffer Overflow?**  
**Trả lời khi demo:** Firewall không biết giới hạn object trong tiến trình và input hợp lệ cũng có thể dài đủ để kích hoạt lỗi. Phải validate byte length và dùng API bounded ngay tại server/native boundary.

**Câu 20. Trình bày bản vá và giải thích vì sao bản vá có hiệu quả.**  
**Trả lời khi demo:** `secure_length` từ chối khi length lớn hơn 31 trước `memcpy`; `secure_snprintf` giới hạn vùng đích và kiểm tra `written`. Cả hai giữ invariant của `name[32]`, nên input 64 không được copy vào buffer.

**Câu 21. Nêu ít nhất 3 cơ chế hardening ở cấp compiler/hệ điều hành.**  
**Trả lời khi demo:** Có thể nêu stack protector/canary, ASLR/PIE, DEP/NX, `_FORTIFY_SOURCE` và RELRO. `/hardening` hiện là inspector; trạng thái đo được phải lấy từ `file`/`readelf`/`objdump` trong WSL, và các lớp này chỉ là defense in depth sau khi code đã được sửa.

## Nếu demo lỗi

- Nếu WSL không có hoặc `make all` lỗi, ghi rõ native demo chưa chạy; không gọi ASan/GDB là observed, và dùng source/trace có sẵn để giải thích.
- Nếu `scripts\run_lab.bat` không khởi động được, kiểm tra `http://127.0.0.1:5002`, dừng phiên cũ rồi chạy lại script; không tự thay bằng binary chưa build.
- Nếu UI báo quá 256 byte, dùng đúng mẫu `A × 64`; giới hạn UI là 256 byte, còn invariant native là 31 byte dữ liệu.
- Nếu 32 byte không crash, vẫn kết luận đã vượt capacity; chỉ kết luận process crash khi response/exit code hoặc runtime log cho thấy.

## Chốt lab

Root cause: `strcpy` ghi input dài vào `char name[32]` không có giới hạn.
Primary fix: kiểm tra byte length hoặc dùng bounded API và kiểm tra truncate/error.
Defense in depth: ASan, stack canary, ASLR/PIE, DEP/NX, FORTIFY và RELRO.
