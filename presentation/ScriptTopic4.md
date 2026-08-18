# Kịch bản thuyết trình chi tiết — Topic04 Official2

- **Bộ slide:** `Topic04_Official2.pptx` / `Topic04_Official2.html`
- **Số slide:** 24
- **Thành viên:** Lê Minh — 21127645; Nguyễn Vũ Bách — 21127224
- **Phạm vi:** Chỉ môi trường local có kiểm soát; không website hoặc dữ liệu thật.

## Cách sử dụng

- Mỗi mục bên dưới tương ứng đúng một slide.
- Khi trình bày, ưu tiên đọc phần “Kịch bản thuyết trình chi tiết”; phần từ khóa dùng để giải thích nhanh.
- Các câu trả lời gợi ý nên được diễn đạt tự nhiên và gắn với route/hàm thực tế trong bài.
- Tổng thời lượng gợi ý: 35–50 phút; mỗi slide kỹ thuật 1,5–2 phút, slide mở/kết 30–45 giây.
- Nếu thầy yêu cầu chứng cứ, mở route/trace/report tương ứng; bản deck cố ý không chèn ảnh chứng cứ.

---

## Slide 01 — Sáu lỗ hổng, một ranh giới niềm tin

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Sáu lỗ hổng, một ranh giới niềm tin.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Các ý cần trình bày**
  - Giới thiệu nhóm: Lê Minh — 21127645 và Nguyễn Vũ Bách — 21127224.
  - Sáu lab khác kỹ thuật nhưng cùng đặt ra câu hỏi: ứng dụng đang tin dữ liệu hoặc quyết định ở đâu.
  - Mục tiêu không phải ghi nhớ payload; mục tiêu là truy vết source, điểm diễn giải dữ liệu và nơi ra quyết định bảo mật.
  - Toàn bộ ứng dụng, dữ liệu và tài khoản đều giả lập; các dịch vụ chỉ chạy trên loopback.
  - Kết quả đúng phải gồm cả bản vulnerable, bản secure và retest bằng cùng dữ liệu đầu vào.

- **Giải nghĩa từ khóa**
  - **Lỗ hổng:** Điểm yếu làm hệ thống xử lý ngoài ý muốn.
  - **Trust boundary:** Ranh giới giữa vùng ít tin cậy và vùng ra quyết định.
  - **Payload:** Dữ liệu kiểm thử dùng để làm lộ hành vi sai.
  - **Root fix:** Bản vá loại bỏ nguyên nhân gốc, không chỉ giảm triệu chứng.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Điểm chung sâu nhất của sáu lab là gì?
    - **Trả lời gợi ý:** Đều có một ranh giới tin cậy bị đặt sai: dữ liệu client được diễn giải hoặc dùng để quyết định mà thiếu kiểm tra phù hợp.
  - **Câu hỏi:** Vì sao không lấy payload làm trung tâm?
    - **Trả lời gợi ý:** Payload thay đổi theo ngữ cảnh; source, sink, invariant và policy mới mô tả nguyên nhân ổn định của lỗi.

- **Câu chuyển sang slide tiếp theo**
  - Trước khi đi vào từng lỗi, cần thống nhất phạm vi an toàn và cách đọc luồng.

---

## Slide 02 — Phạm vi an toàn và chu trình đánh giá

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Phạm vi an toàn và chu trình đánh giá.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Chỉ môi trường hợp pháp: Máy local/VM/Docker; ứng dụng cố tình có lỗi; không website thật, không dữ liệu thật.
  - Không mở rộng khai thác: Không reverse shell, malware, persistence, botnet, keylogger, shellcode hay ROP.
  - Chu trình bắt buộc: Nhận diện → khai thác local → quan sát → phân tích → đánh giá → vá → retest.
  - Bài nộp: PDF, ảnh từng bước, nguyên nhân, ảnh hưởng, phòng chống và mã vá minh họa.
  - Khung đọc: Source ở đâu? Dữ liệu được diễn giải tại đâu? Ai giữ quyết định cuối?
  - Nguyên tắc chứng cứ: Không biến source code hoặc hướng dẫn thành kết quả runtime; chỉ kết luận điều đã quan sát.

- **Các ý cần trình bày**
  - Đề bài cho phép máy ảo local, Docker local, ứng dụng cố tình có lỗi và nền tảng đào tạo hợp pháp.
  - Bài làm chọn sáu ứng dụng Flask/SQLite hoặc Flask kết hợp chương trình C, mỗi ứng dụng có cổng loopback riêng.
  - Các kịch bản chỉ dùng dữ liệu giả lập và payload an toàn; không phát triển công cụ nhắm mục tiêu tùy ý.
  - Chu trình đánh giá luôn kết thúc bằng retest secure, vì đọc code vá chưa chứng minh được hành vi runtime.
  - Trong phần trình bày này không chèn ảnh chứng cứ theo yêu cầu; thay vào đó nêu rõ luồng hoạt động, quyết định và nguyên lý của từng control.
  - Cấu trúc báo cáo 11 mục của đề được gom thành bốn khối: bối cảnh, thực hành, phân tích và kết luận/phụ lục.

- **Giải nghĩa từ khóa**
  - **Localhost:** Máy hiện tại; thường dùng 127.0.0.1 để giới hạn truy cập.
  - **Invariant:** Điều kiện phải luôn đúng, ví dụ input tối đa 31 byte.
  - **Retest:** Chạy lại đúng ca kiểm thử sau khi vá để chứng minh lỗi bị chặn.
  - **Evidence:** Ảnh, request, response, log, trace hoặc debugger xác nhận hành vi.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao phải retest cùng input?
    - **Trả lời gợi ý:** Để cô lập tác động của bản vá; nếu input thay đổi thì chưa biết kết quả khác do control hay do ca thử khác.
  - **Câu hỏi:** Ảnh chụp có thay được log/trace không?
    - **Trả lời gợi ý:** Không hoàn toàn. Ảnh chứng minh giao diện; log, request, response và trace chứng minh phần xử lý phía sau.

- **Câu chuyển sang slide tiếp theo**
  - Áp dụng khung này trước tiên cho XSS — lỗi xảy ra khi dữ liệu chạm một sink có khả năng tạo mã trong browser.

---

## Slide 03 — XSS là luồng dữ liệu từ source đến sink

- **Mục tiêu của slide**
  - Làm rõ thông điệp: XSS là luồng dữ liệu từ source đến sink.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Reflected → URL query q → Markup(q) trong response → Browser parse → Một URL/một request
  - Stored → Comment form → SQLite comments.body → Markup(body) → Phát lại cho mọi viewer
  - DOM-based → location.hash → JS phía client → innerHTML → Server không thấy fragment

- **Các ý cần trình bày**
  - Reflected XSS của bài đọc `request.args['q']`; bản lỗi bọc giá trị bằng `Markup`, làm mất cơ chế autoescape của Jinja.
  - Stored XSS nhận comment, lưu nguyên văn vào SQLite rồi bản vulnerable phát lại bằng `Markup(row['body'])`.
  - Stored nguy hiểm hơn về phạm vi vì một lần ghi có thể tác động nhiều lượt xem và nhiều người dùng.
  - DOM-based XSS đọc `location.hash`; fragment không được gửi trong HTTP request nên Flask có thể không thấy source.
  - JavaScript vulnerable gán `innerHTML`, khiến browser parse chuỗi thành element và event handler; bản secure dùng `textContent` để tạo text node.
  - Điểm chung không phải vị trí lưu mà là dữ liệu không tin cậy đến một sink tạo ngữ nghĩa thực thi.

- **Giải nghĩa từ khóa**
  - **Source:** Nơi dữ liệu không tin cậy đi vào luồng xử lý.
  - **Sink:** Nơi dữ liệu được diễn giải thành HTML, DOM hoặc mã.
  - **Reflected XSS:** Payload đi trong request và phản chiếu ngay ở response.
  - **Stored XSS:** Payload được lưu rồi phát lại ở các lượt xem sau.
  - **DOM XSS:** Source và sink nằm trong JavaScript phía browser.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Fragment có xuất hiện trong access log của server không?
    - **Trả lời gợi ý:** Thông thường không; phần sau dấu # được browser giữ lại và xử lý phía client.
  - **Câu hỏi:** XSS xảy ra ở server hay browser?
    - **Trả lời gợi ý:** Thực thi xảy ra ở browser; nguyên nhân có thể nằm ở server render hoặc ở JavaScript client.

- **Câu chuyển sang slide tiếp theo**
  - Sau khi phân loại, cần chứng minh từng luồng bằng ca thử và phân tích ảnh hưởng.

---

## Slide 04 — Ba ca thử XSS cho thấy ba phạm vi ảnh hưởng

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Ba ca thử XSS cho thấy ba phạm vi ảnh hưởng.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Reflected: Mở `/vulnerable/search?q=...`; thử text thường rồi payload alert an toàn. Payload nằm trong HTML response; nạn nhân phải mở URL đã gắn dữ liệu.
  - Stored: Gửi comment thường rồi payload; reload hoặc xem lại bằng phiên khác. Payload còn trong SQLite và được phát lại ở mỗi lần render.
  - DOM-based: Mở `/vulnerable/dom-search#...`; kiểm tra file JS và DOM trước/sau. `location.hash → innerHTML`; không cần server phản chiếu fragment.

- **Các ý cần trình bày**
  - Với mỗi biến thể, thực hiện dữ liệu bình thường trước để xác nhận chức năng baseline.
  - Reflected: quan sát chính xác vị trí `q` đi vào response và xem các ký tự `<`, `>`, dấu nháy có được encode hay không.
  - Stored: xác nhận nơi lưu là bảng comments trong SQLite, sau đó reload để chứng minh persistence.
  - DOM: đối chiếu DOM trước/sau; bản vulnerable tạo element và event attribute, bản secure chỉ tạo một text node.
  - Ảnh hưởng không chỉ là hộp thoại alert: script chạy trong origin của ứng dụng có thể đọc DOM, thay nội dung và gửi request với quyền phiên.
  - Kịch bản an toàn dừng ở alert/đổi giao diện; không đánh cắp cookie hay dữ liệu.

- **Giải nghĩa từ khóa**
  - **Autoescape:** Jinja mã hóa ký tự đặc biệt khi đưa dữ liệu vào HTML.
  - **HTML parser:** Bộ phân tích biến chuỗi markup thành cây DOM.
  - **Event handler:** Thuộc tính như onerror có thể chạy JavaScript khi sự kiện xảy ra.
  - **Origin:** Bộ ba scheme, host và port xác định phạm vi bảo mật của trang.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao Stored XSS thường nguy hiểm hơn Reflected?
    - **Trả lời gợi ý:** Payload tồn tại trong storage và tự phát lại cho nhiều người xem, không cần gửi một URL riêng cho từng nạn nhân.
  - **Câu hỏi:** HttpOnly có vá XSS không?
    - **Trả lời gợi ý:** Không. Nó chỉ ngăn JavaScript đọc cookie; script vẫn có thể sửa DOM hoặc gửi request trong phiên.

- **Câu chuyển sang slide tiếp theo**
  - Các kết quả này dẫn đến bản vá theo đúng loại sink, không phải một bộ lọc input chung.

---

## Slide 05 — Vá XSS tại đúng context; CSP chỉ là lớp bổ sung

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Vá XSS tại đúng context; CSP chỉ là lớp bổ sung.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Reflected: `Markup(q)`; Jinja autoescape / output encoding; Browser nhận text thay vì markup
  - Stored: `Markup(body)`; `bleach.clean` allowlist trước khi render; Loại tag/attribute không được phép
  - DOM: `innerHTML`; `textContent`; Tạo text node, không tạo element/event
  - Mọi route: Input không tin cậy; Validate server-side; Giới hạn kiểu/độ dài nhưng không thay encoding
  - Defense in depth: Script còn lọt; CSP + cookie flags + headers; Giảm khả năng và hậu quả, không sửa sink

- **Các ý cần trình bày**
  - Bản vá Reflected khôi phục autoescape; output encoding phải đúng context nơi dữ liệu được chèn.
  - Stored có thể encode toàn bộ nếu chỉ cần text; bài dùng Bleach allowlist để minh họa trường hợp cho phép rich text hạn chế.
  - DOM thay `innerHTML` bằng `textContent` vì chức năng chỉ cần hiển thị chuỗi tìm kiếm.
  - Validation vẫn cần để giới hạn độ dài/định dạng, nhưng một input hợp lệ ở form có thể nguy hiểm khi đi vào HTML attribute hoặc JavaScript.
  - Lab bật CSP và các security header ở secure flow; đây là defense in depth, không được dùng để biện minh giữ sink lỗi.
  - Retest cùng payload phải cho thấy payload xuất hiện như văn bản hoặc bị loại khỏi output, không tạo element/event.

- **Giải nghĩa từ khóa**
  - **Sanitization:** Lọc nội dung theo allowlist khi vẫn cần cho phép một phần HTML.
  - **CSP:** Content Security Policy — chính sách giới hạn nguồn và cách thực thi tài nguyên.
  - **HttpOnly:** Cookie không thể được đọc qua JavaScript.
  - **Secure:** Cookie chỉ được gửi qua HTTPS.
  - **SameSite:** Giới hạn tình huống cookie được gửi trong request cross-site.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao validate input chưa đủ chống XSS?
    - **Trả lời gợi ý:** Validation không biết mọi context output; dữ liệu hợp lệ theo nghiệp vụ vẫn cần encoding khi đưa vào HTML/JS/URL/attribute.
  - **Câu hỏi:** CSP có thay sửa code không?
    - **Trả lời gợi ý:** Không. CSP giảm xác suất thực thi và hậu quả nhưng sink nguy hiểm vẫn là nguyên nhân gốc.

- **Câu chuyển sang slide tiếp theo**
  - Lab02 chuyển từ parser của browser sang vùng nhớ của một backend native.

---

## Slide 06 — HTTP hợp lệ vẫn có thể chạm vùng nhớ stack

- **Mục tiêu của slide**
  - Làm rõ thông điệp: HTTP hợp lệ vẫn có thể chạm vùng nhớ stack.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - 01 → Browser → Input text local → POST /submit → HTTP hợp lệ
  - 02 → Flask → Giới hạn request → subprocess.run → shell=False
  - 03 → C backend → char name[32] → strcpy(name,input) → Không biết capacity
  - 04 → OS → Exit code/signal → Flask chuẩn hóa → Trace + response

- **Các ý cần trình bày**
  - Lab02 mô phỏng một backend native nhận dữ liệu từ web: Browser → Flask → subprocess → binary C.
  - Flask dùng allowlist mode, giới hạn input, timeout và `shell=False`; các control này ngăn lỗi command injection nhưng không tự vá `strcpy` bên trong binary.
  - Hàm vulnerable khai báo `char name[32]` rồi gọi `strcpy`, nên nguồn không truyền capacity của đích.
  - Chuỗi C cần byte null; do đó invariant là tối đa 31 byte dữ liệu.
  - Khi input vượt biên, byte tiếp theo có thể chạm padding, canary, saved frame hoặc control data; hành vi phụ thuộc build và runtime.
  - Một request có cú pháp HTTP hoàn toàn hợp lệ vẫn kích hoạt lỗi nếu backend native xử lý dữ liệu không an toàn.

- **Giải nghĩa từ khóa**
  - **Buffer:** Vùng nhớ có kích thước hữu hạn dùng để chứa dữ liệu.
  - **Stack:** Vùng nhớ cho frame hàm, biến cục bộ và control data.
  - **Capacity:** Số byte tối đa vùng đích có thể chứa an toàn.
  - **Null terminator:** Byte 0 kết thúc chuỗi kiểu C.
  - **Memory corruption:** Dữ liệu ghi sai làm hỏng vùng nhớ lân cận.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao lỗi native có thể bị kích hoạt qua HTTP?
    - **Trả lời gợi ý:** HTTP chỉ là kênh vận chuyển; dữ liệu cuối cùng được copy vào buffer C nên lỗi ở tầng native vẫn reachable từ web.
  - **Câu hỏi:** 32 byte có luôn làm chương trình crash không?
    - **Trả lời gợi ý:** Không. Nó đã vượt capacity chuỗi nhưng crash phụ thuộc layout, build, canary và vùng bị ghi đè.

- **Câu chuyển sang slide tiếp theo**
  - Vì undefined behavior không cho phép suy đoán ngưỡng crash, bài phải đo bằng ASan và GDB.

---

## Slide 07 — Crash phải được đo, không suy từ source

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Crash phải được đo, không suy từ source.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Baseline: Gửi tên ngắn và 31 byte. Binary in PID/length/buffer size rồi exit bình thường.
  - Overflow có kiểm soát: Gửi 32, 64, 128 byte A/B qua `vulnerable_asan`. ASan có thể báo stack-buffer-overflow; process dừng có kiểm soát.
  - GDB: Chạy script normal/overflow/hardened local. Xem backtrace, frame, stack bytes và điểm dừng.

- **Các ý cần trình bày**
  - Đầu tiên chạy baseline để tránh nhầm lỗi build hoặc route với lỗi overflow.
  - Các mốc 31/32/64/128 byte có ý nghĩa khác nhau: 31 vừa capacity, 32 vượt capacity, 64/128 giúp ASan quan sát rõ.
  - ASan là detector phục vụ test, không phải cơ chế production chính; dữ liệu phải lấy từ stderr thật.
  - GDB cho biết crash ở đâu, stack có bị ghi đè và backtrace như thế nào; không dùng GDB để thay đổi điều khiển chương trình.
  - Bài tách ba mốc: vượt capacity theo lý thuyết, ASan phát hiện và process thực sự crash/dừng.
  - Memory corruption nghiêm trọng hơn lỗi logic vì có thể phá cả dữ liệu lẫn control flow; lab chỉ quan sát phần crash.

- **Giải nghĩa từ khóa**
  - **ASan:** AddressSanitizer — công cụ runtime phát hiện truy cập bộ nhớ sai.
  - **GDB:** Debugger dùng để dừng chương trình và quan sát frame, stack, backtrace.
  - **Undefined behavior:** Chuẩn C không quy định kết quả sau thao tác không hợp lệ.
  - **Backtrace:** Chuỗi lời gọi hàm tại thời điểm chương trình dừng.
  - **Signal:** Cơ chế hệ điều hành báo sự kiện như lỗi truy cập bộ nhớ.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** ASan có nên bật trong production không?
    - **Trả lời gợi ý:** Thông thường dùng cho test/debug do overhead; production ưu tiên source fix và hardening phù hợp.
  - **Câu hỏi:** Vì sao memory corruption nghiêm trọng?
    - **Trả lời gợi ý:** Nó có thể làm hỏng dữ liệu, metadata hoặc control flow, không chỉ trả kết quả nghiệp vụ sai.

- **Câu chuyển sang slide tiếp theo**
  - Bản vá phải khôi phục invariant độ dài; hardening chỉ giảm khả năng khai thác nếu lỗi còn tồn tại.

---

## Slide 08 — Source fix trước; compiler và OS hardening sau

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Source fix trước; compiler và OS hardening sau.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Source #1: `strnlen(input,33)`; reject nếu >31; Giữ invariant trước copy; Phải tính theo byte
  - Source #2: `snprintf(name,32,"%s",input)` + check return; Bounded write và phát hiện truncation; Không bỏ qua return value
  - HTTP: `MAX_CONTENT_LENGTH=4096`; input lab ≤256; Giảm request quá lớn; Không biết capacity từng buffer
  - Compiler: stack protector, FORTIFY, PIE; Phát hiện/giảm khai thác; Không thay code an toàn
  - Loader/OS: RELRO, ASLR, NX/DEP; Bảo vệ relocation, layout, execution; Defense in depth

- **Các ý cần trình bày**
  - Bản secure_length kiểm tra chiều dài trước khi copy; bản secure_snprintf dùng bounded write và kiểm tra return để từ chối truncation.
  - Kiểm tra theo byte vì buffer C được cấp theo byte, trong khi ký tự Unicode có thể chiếm nhiều byte UTF-8.
  - Request limit và allowlist mode là ranh giới ngoài; source fix giữ invariant tại nơi biết capacity.
  - Makefile của bản secure bật `-fstack-protector-strong`, `_FORTIFY_SOURCE=2`, PIE, Full RELRO và noexecstack.
  - PIE hỗ trợ ASLR; NX/DEP ngăn thực thi vùng dữ liệu; canary phát hiện ghi tràn; RELRO bảo vệ bảng relocation.
  - Firewall không thể thay source fix vì nó không biết `name[32]` hay null terminator.

- **Giải nghĩa từ khóa**
  - **Stack Canary:** Giá trị bảo vệ phát hiện ghi đè stack trước khi return.
  - **ASLR:** Ngẫu nhiên hóa vị trí vùng nhớ giữa các lần chạy.
  - **PIE:** Executable độc lập vị trí để ASLR áp dụng cho code chính.
  - **RELRO:** Làm vùng relocation khó hoặc không thể ghi sau khi nạp.
  - **NX/DEP:** Đánh dấu vùng dữ liệu không được thực thi như mã.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Buffer Overflow khác Injection thế nào?
    - **Trả lời gợi ý:** Overflow phá biên vùng nhớ; Injection làm dữ liệu được parser hiểu thành cú pháp hoặc lệnh.
  - **Câu hỏi:** Nêu ba hardening cấp compiler/OS?
    - **Trả lời gợi ý:** Ví dụ stack canary, PIE+ASLR, NX/DEP; có thể bổ sung RELRO và FORTIFY.

- **Câu chuyển sang slide tiếp theo**
  - Lab03 rời memory safety để xem lỗi logic khi server tin giá, ID và role từ client.

---

## Slide 09 — Client gửi tham số; server phải giữ policy

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Client gửi tham số; server phải giữ policy.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Checkout → price=1 → Hidden field bị sửa → Server tin giá → Invoice total sai
  - Invoice → id=1002 → Đổi object ID → Không check owner → Lộ hóa đơn user B
  - Profile → role=admin → Mass assignment → Update role từ form → Privilege escalation

- **Các ý cần trình bày**
  - Request Tampering Console của Lab03 chỉ có ba scenario cố định và hiển thị diff giữa giá trị gốc với giá trị gửi.
  - Checkout vulnerable lấy `price` từ hidden field; secure route đọc `products.price_vnd` từ database rồi tính tổng.
  - Invoice vulnerable query theo ID nhưng bỏ qua ownership; secure route áp policy owner-or-admin và trả 403 trước khi render dữ liệu.
  - Profile vulnerable nhận `user_id`, `email`, `role` và cập nhật trực tiếp; đây là mass assignment trường nhạy cảm.
  - Secure profile lấy identity từ session, chỉ allowlist `email`, bỏ `role`, `user_id`, `balance`, `is_admin`.
  - Parameterized SQL vẫn được dùng ở cả vulnerable flow để cô lập lỗi mục tiêu: sai policy, không phải SQL Injection.

- **Giải nghĩa từ khóa**
  - **Parameter Tampering:** Thay đổi tham số request để làm server xử lý ngoài policy.
  - **Hidden field:** Trường chỉ ẩn trong giao diện; client vẫn đọc và sửa được.
  - **IDOR:** Đổi tham chiếu object để truy cập tài nguyên không thuộc quyền.
  - **Mass assignment:** Tự động gán nhiều field client vào object/database.
  - **Authorization:** Kiểm tra chủ thể có quyền thực hiện hành động trên object hay không.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Hidden field có phải cơ chế bảo mật không?
    - **Trả lời gợi ý:** Không. Nó chỉ ảnh hưởng giao diện; request do client tạo nên giá trị vẫn hoàn toàn sửa được.
  - **Câu hỏi:** Validation kiểu dữ liệu có chặn IDOR không?
    - **Trả lời gợi ý:** Không. ID=1002 có thể là số hợp lệ nhưng vẫn là object không thuộc quyền.

- **Câu chuyển sang slide tiếp theo**
  - Ba scenario cần được retest ở cả vulnerable và secure để thấy nguồn authoritative thay đổi.

---

## Slide 10 — Ba retest xác định đúng nguồn authoritative

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Ba retest xác định đúng nguồn authoritative.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Giá checkout: User A thêm product 5; đổi `price=100000` thành `1`. Vulnerable lưu unit_price=1; secure bỏ giá client và dùng DB=100000.
  - Invoice IDOR: User A đổi `/invoice?id=1001` thành `1002`. Vulnerable trả invoice User B; secure owner-or-admin trả HTTP 403.
  - Role tampering: Đổi `role=user` thành `role=admin` trong profile. Vulnerable cập nhật DB+session; secure chỉ cập nhật email và giữ role.

- **Các ý cần trình bày**
  - Giá sản phẩm phải được server lấy lại theo product_id; client chỉ gửi lựa chọn và số lượng hợp lệ.
  - IDOR được chứng minh bằng hai invoice có owner khác nhau; secure route phải từ chối trước khi trả chi tiết.
  - Role tampering cần reset state trước retest secure để tránh session đã bị nâng quyền ở vulnerable flow.
  - Lab trace hiển thị Request Inspector, Session, Database, Authorization và Audit trên cùng trace_id.
  - Bằng chứng quan trọng là state trước/sau và database write, không chỉ status code.
  - Audit giúp phát hiện hành vi bất thường nhưng không thay authorization ở request hiện tại.

- **Giải nghĩa từ khóa**
  - **Authoritative source:** Nguồn được server công nhận là sự thật để ra quyết định.
  - **Object-level authz:** Kiểm quyền trên đúng bản ghi/tài nguyên đang được yêu cầu.
  - **Field allowlist:** Chỉ nhận tập field được phép cập nhật.
  - **HTTP 403:** Server hiểu request nhưng từ chối vì thiếu quyền.
  - **Audit event:** Bản ghi có cấu trúc về hành động, quyết định và lý do.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao server không nên nhận giá sản phẩm?
    - **Trả lời gợi ý:** Giá là dữ liệu nghiệp vụ do server quản lý và có thể thay đổi; client chỉ trình bày giá, không có quyền quyết định.
  - **Câu hỏi:** Vì sao cần reset giữa các flow?
    - **Trả lời gợi ý:** Tampering vulnerable có thể thay đổi DB/session; nếu không reset thì secure retest bị nhiễu bởi state cũ.

- **Câu chuyển sang slide tiếp theo**
  - Từ kết quả này, bản vá được mô tả bằng bốn nguồn server-authoritative.

---

## Slide 11 — Identity, object, field và value đều cần policy phía server

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Identity, object, field và value đều cần policy phía server.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Identity: `user_id` trong form; Session đã xác thực; Không cho client chọn subject
  - Value: `price` hidden field; Product trong SQLite; Tính lại total server-side
  - Object: `invoice id`; Owner + role hiện tại; Owner-or-admin mỗi request
  - Property: `role/is_admin/balance`; Schema/policy cập nhật; Allowlist `email`
  - Detection: Input bất thường; Audit + trace_id; Log mismatch/denial/rejected field

- **Các ý cần trình bày**
  - Secure checkout lấy giá database; secure invoice kiểm tra owner hoặc admin; secure profile chỉ nhận email.
  - Identity không được chọn từ form mà phải lấy từ session đã xác thực.
  - IDOR thuộc A01:2025 Broken Access Control trong OWASP Top 10; trong OWASP API Security Top 10 2023, mẫu tương ứng là API1 BOLA.
  - Mass assignment trường nhạy cảm liên quan property-level authorization; allowlist giúp thu hẹp bề mặt cập nhật.
  - Audit mismatch và denied event phục vụ phát hiện/điều tra, không phải lớp cho phép.
  - Retest cần chứng minh role/owner/price trong database vẫn đúng sau input bị sửa.

- **Giải nghĩa từ khóa**
  - **Authentication:** Xác minh danh tính của chủ thể.
  - **Broken Access Control:** Nhóm lỗi cho phép hành động hoặc tài nguyên trái quyền.
  - **BOLA:** Broken Object Level Authorization — thiếu quyền trên object cụ thể.
  - **Privilege escalation:** Tăng quyền từ user lên mức cao hơn trái phép.
  - **Least fields:** Chỉ tiếp nhận và trả các field thực sự cần cho nghiệp vụ.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** IDOR thuộc nhóm nào?
    - **Trả lời gợi ý:** Thuộc Broken Access Control; với API thường mô tả cụ thể là Broken Object Level Authorization.
  - **Câu hỏi:** Parameter Tampering khác SQL Injection?
    - **Trả lời gợi ý:** Tampering đổi giá trị để phá policy nghiệp vụ; SQLi làm dữ liệu thay đổi cú pháp truy vấn.

- **Câu chuyển sang slide tiếp theo**
  - Lab04 tiếp tục với session cookie: session chứng minh danh tính nhưng không chứng minh ý định thao tác.

---

## Slide 12 — Session chứng minh danh tính, không chứng minh ý định

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Session chứng minh danh tính, không chứng minh ý định.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - 01 → Victim login :5004 → Session cookie → Browser lưu → Đã xác thực
  - 02 → Mở Demo Page :9004 → Cross-origin form → POST change-email → Không cần đọc cookie
  - 03 → Browser gửi request → Cookie có thể tự kèm → Server chỉ tin session → Thiếu proof of intent
  - 04 → Vulnerable route → Không token/origin check → UPDATE SQLite → Email bị đổi

- **Các ý cần trình bày**
  - Victim đã đăng nhập nên browser có session cookie hợp lệ.
  - Demo Page ở port khác tạo form POST cố định đến route đổi email; attacker không cần biết mật khẩu hoặc giá trị cookie.
  - Browser quản lý cookie và có thể đính kèm theo cookie policy, nên server thấy một phiên đã xác thực.
  - Nếu route chỉ dựa vào session, nó không phân biệt request từ form thật với request bị kích hoạt từ trang khác.
  - SOP chủ yếu ngăn script đọc response cross-origin; form submission vẫn có thể xảy ra.
  - CORS điều khiển quyền đọc response của script, không tạo token chống giả mạo ý định.

- **Giải nghĩa từ khóa**
  - **CSRF:** Ép browser đã đăng nhập gửi request thay đổi trạng thái ngoài ý muốn.
  - **Session cookie:** Cookie gắn request với phiên đăng nhập phía server.
  - **SOP:** Same-Origin Policy — hạn chế script truy cập dữ liệu khác origin.
  - **Cross-origin:** Khác scheme, host hoặc port.
  - **Proof of intent:** Bằng chứng request được tạo từ UI/phiên hợp lệ với ý định người dùng.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Attacker không biết cookie thì CSRF hoạt động thế nào?
    - **Trả lời gợi ý:** Browser tự quản lý và gửi cookie theo policy; attacker chỉ cần khiến browser tạo request.
  - **Câu hỏi:** CSRF có đọc được response không?
    - **Trả lời gợi ý:** Thường không do SOP, nhưng tấn công chỉ cần tạo state change nên không nhất thiết phải đọc response.

- **Câu chuyển sang slide tiếp theo**
  - Lab04 chứng minh điều này bằng state trước/sau và sau đó retest với các gate secure.

---

## Slide 13 — Deny phải xảy ra trước mutation

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Deny phải xảy ra trước mutation.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Vulnerable email: Victim login; mở `/attack/vulnerable-email`; xác nhận gửi form. POST có session, không token/Origin check; email đổi trong SQLite.
  - Secure bị tấn công: Gửi thiếu token hoặc token giả từ Demo Page. Exact Origin/Referer hoặc token check thất bại; HTTP 403.
  - Secure hợp lệ: Gửi từ form victim có token gắn session và Origin hợp lệ. Server validate, UPDATE, rồi rotate token.

- **Các ý cần trình bày**
  - Flow vulnerable chỉ kiểm tra session và email input rồi cập nhật database.
  - Secure flow kiểm tra Origin/Referer trước, sau đó token bằng `hmac.compare_digest`; thiếu hoặc sai gate nào đều trả 403.
  - State Inspector đọc `state_history` theo trace_id để chứng minh denial xảy ra trước UPDATE.
  - Sau secure success, token được rotate; điều này giới hạn replay của token cũ.
  - Đổi mật khẩu và transfer bổ sung re-authentication vì token chứng minh nguồn request, không chứng minh người dùng hiện vẫn kiểm soát phiên.
  - Thao tác thay đổi state không dùng GET để tránh prefetch/link/crawler vô tình kích hoạt.

- **Giải nghĩa từ khóa**
  - **Mutation:** Thao tác làm thay đổi state như UPDATE, transfer hoặc đổi mật khẩu.
  - **Synchronizer token:** Token ngẫu nhiên lưu trong session và nhúng vào form hợp lệ.
  - **403 Forbidden:** Request bị từ chối trước khi thực hiện thao tác.
  - **Token rotation:** Phát token mới sau sự kiện để giảm tái sử dụng.
  - **Re-authentication:** Yêu cầu xác minh lại mật khẩu cho thao tác nhạy cảm.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao state change không nên dùng GET?
    - **Trả lời gợi ý:** GET có semantics an toàn/idempotent và có thể bị prefetch, cache, crawler hoặc link kích hoạt ngoài ý muốn.
  - **Câu hỏi:** Tại sao kiểm tra phải trước UPDATE?
    - **Trả lời gợi ý:** Nếu update rồi mới reject thì side effect đã xảy ra; response 403 không thể hoàn tác an toàn mọi mutation.

- **Câu chuyển sang slide tiếp theo**
  - Bản vá CSRF là một chuỗi gate; SameSite chỉ là một phần của chuỗi đó.

---

## Slide 14 — Token là lớp chính; Origin, SameSite và re-auth hỗ trợ

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Token là lớp chính; Origin, SameSite và re-auth hỗ trợ.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Method: POST cho mutation; GET vô tình thay state; Không xác minh nguồn
  - Origin/Referer: Parse + exact allowlist; Nguồn ngoài dự kiến; Header có thể thiếu
  - CSRF token: 32-byte URL-safe; session-bound; constant-time compare; Form giả thiếu secret theo phiên; Phải bảo vệ XSS
  - SameSite: Lax/Strict theo môi trường; Giảm cookie cross-site; Không bao phủ mọi browser/flow
  - Sensitive action: Re-authentication; Phiên bị bỏ quên/chiếm dụng; Tăng ma sát

- **Các ý cần trình bày**
  - Token được tạo bằng `secrets.token_urlsafe(32)`, lưu trong session và so sánh constant-time.
  - Origin/Referer được parse và so sánh exact, tránh lỗi prefix/suffix hoặc hostname giả.
  - SameSite là lớp browser-side hỗ trợ; secure flow vẫn phải có token server-side.
  - Re-authentication áp dụng cho đổi mật khẩu và chuyển số dư, nơi hậu quả cao hơn đổi email demo.
  - CAPTCHA không ràng buộc request với session/form theo cách token làm, nên không phải biện pháp chính.
  - Nếu XSS tồn tại, script cùng origin có thể đọc token trong DOM hoặc gửi request; vì vậy XSS và CSRF phải được xử lý độc lập.

- **Giải nghĩa từ khóa**
  - **Origin header:** Nguồn request gồm scheme, host và port.
  - **Referer header:** URL trang tạo request; dùng fallback thận trọng.
  - **SameSite=Lax:** Giảm cookie trong nhiều request cross-site, vẫn cho một số top-level navigation.
  - **Constant-time compare:** So sánh tránh rò khác biệt thời gian theo vị trí sai.
  - **Defense in depth:** Nhiều control độc lập giảm rủi ro còn lại.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** SameSite có đủ chống CSRF không?
    - **Trả lời gợi ý:** Không. Nó phụ thuộc browser và loại request; token server-side vẫn là lớp chính.
  - **Câu hỏi:** CSRF khác XSS?
    - **Trả lời gợi ý:** CSRF lợi dụng browser gửi request có credential; XSS thực thi script trong origin của ứng dụng.

- **Câu chuyển sang slide tiếp theo**
  - Lab05 chuyển sang một parser khác: SQL parser, nơi nối chuỗi làm data biến thành syntax.

---

## Slide 15 — Nối chuỗi làm dữ liệu trở thành cú pháp SQL

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Nối chuỗi làm dữ liệu trở thành cú pháp SQL.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - 01 → Input → username/keyword → Validation scenario → Dữ liệu client
  - 02 → Concatenation → f-string/ghép chuỗi → Final SQL text → Ranh giới code-data mất
  - 03 → SQL parser → Đọc quote/comment/boolean → AST/logic khác → WHERE bị đổi
  - 04 → Execution → SELECT local → Auth/rows ngoài dự kiến → Trace + audit

- **Các ý cần trình bày**
  - Vulnerable login ghép username và legacy digest vào câu SELECT; vulnerable search ghép keyword vào LIKE.
  - Dấu nháy đơn đầu tiên là tín hiệu phát hiện: nó có thể làm query lỗi và cho thấy input chạm SQL text.
  - Scenario authentication logic dùng comment marker để loại điều kiện password khỏi logic.
  - Scenario search dùng boolean condition để mở rộng result set products.
  - Lab chỉ cho fixed input và SELECT-only để minh họa an toàn, không trở thành scanner hay công cụ khai thác tổng quát.
  - Lỗi nằm ở query construction trước khi SQLite thực thi; parser chỉ làm đúng với chuỗi mà ứng dụng tạo.

- **Giải nghĩa từ khóa**
  - **SQL Injection:** Input được SQL parser hiểu như một phần cú pháp truy vấn.
  - **Concatenation:** Ghép input trực tiếp vào chuỗi SQL.
  - **SQL parser:** Thành phần phân tích câu SQL thành cấu trúc thực thi.
  - **Comment marker:** Cú pháp làm phần còn lại của câu SQL bị bỏ qua.
  - **Result set:** Tập hàng truy vấn trả về.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** SQL Injection xảy ra ở tầng nào?
    - **Trả lời gợi ý:** Ở ranh giới xây dựng truy vấn/data-access trước khi SQL parser thực thi.
  - **Câu hỏi:** Dấu nháy đơn có phải luôn là exploit?
    - **Trả lời gợi ý:** Không; nó là ký tự kiểm thử giúp phát hiện input đi vào cú pháp, còn khả năng khai thác phụ thuộc query/context.

- **Câu chuyển sang slide tiếp theo**
  - Ba ca thử login/search/error giúp chứng minh sự thay đổi cấu trúc, sau đó retest bằng binding.

---

## Slide 16 — Cùng input, vulnerable đổi logic; secure giữ cấu trúc

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Cùng input, vulnerable đổi logic; secure giữ cấu trúc.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Quote detection: Nhập `'` vào login/search. Vulnerable SQLite báo lỗi đã phân loại; secure bind như literal.
  - Auth bypass local: Username cố định `admin_lab' -- `; password bất kỳ. Vulnerable bỏ điều kiện digest; secure không match username literal.
  - Expanded search: Keyword cố định `%' OR 1=1 -- `. Vulnerable trả nhiều products hơn baseline; secure tìm literal, tối đa 50.

- **Các ý cần trình bày**
  - Chạy input bình thường trước để biết expected rows và expected auth decision.
  - Dấu nháy đơn ở vulnerable tạo syntax error; Error Inspector chỉ hiển thị category và Error ID, không lộ chi tiết nhạy cảm.
  - Authentication bypass được giới hạn vào account/database lab và câu SELECT cố định.
  - Expanded search chỉ mở rộng bảng products, không thực hiện UNION hay đọc schema.
  - Cùng input ở secure flow trở thành bound value; query template và số placeholder không đổi.
  - Kết luận dựa vào final SQL masked, prepared flag, row count và decision chứ không dựa vào payload nhìn giống nguy hiểm.

- **Giải nghĩa từ khóa**
  - **Authentication bypass:** Vượt bước xác minh thông tin đăng nhập.
  - **Error-based signal:** Dùng phản ứng lỗi để suy ra input đã chạm parser.
  - **Read-only demo:** Kịch bản chỉ đọc dữ liệu, không DDL/DML ghi.
  - **Trace ID:** Mã nối request, query, audit và kết quả của cùng một flow.
  - **Baseline:** Kết quả bình thường dùng để so sánh hành vi bất thường.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao thông báo lỗi SQL chi tiết nguy hiểm?
    - **Trả lời gợi ý:** Nó có thể lộ schema, tên bảng/cột, query và đường dẫn, giúp thu hẹp việc khai thác.
  - **Câu hỏi:** Vì sao phải có baseline?
    - **Trả lời gợi ý:** Không có expected result thì không chứng minh được input đã mở rộng tập kết quả hay thay logic.

- **Câu chuyển sang slide tiếp theo**
  - Bản vá chính là tách code khỏi data; các control khác xử lý hậu quả và rủi ro còn lại.

---

## Slide 17 — Parameter binding khóa cấu trúc; password hash bảo vệ credential

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Parameter binding khóa cấu trúc; password hash bảo vệ credential.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Parameterized query: `WHERE username=?`; `LIKE ?`; tuple params; Input luôn là data; Authorization
  - Password hashing: PBKDF2-SHA256 600k + salt; `check_password_hash`; Chống lộ plaintext/offline cracking; SQL binding
  - Validation: Username/keyword/id theo kiểu và độ dài; Giảm input sai; Prepared statement
  - Safe errors: Generic response + Error ID nội bộ; Không lộ query/schema/path; Logging nội bộ
  - Least privilege: Fixed local SELECT, result limit, non-root; Giới hạn blast radius; Root fix

- **Các ý cần trình bày**
  - Secure login chỉ lookup username bằng placeholder rồi kiểm tra PBKDF2 trong ứng dụng.
  - Secure search tạo `%keyword%` ở tham số và bind vào `LIKE ?`; cấu trúc query không nhận ký tự cú pháp từ input.
  - Password không lưu plaintext; salt và work factor làm chậm tấn công offline nếu database lộ.
  - Validation theo kiểu/độ dài xử lý input sai sớm nhưng không thay prepared statement.
  - SQLite local không có database-user permission model như server DB; bài mô phỏng least privilege bằng SELECT cố định, non-root và không raw SQL tùy ý.
  - Retest kiểm tra prepared flag, placeholder count và kết quả literal.

- **Giải nghĩa từ khóa**
  - **Prepared statement:** Cấu trúc SQL được chuẩn bị tách biệt khỏi dữ liệu tham số.
  - **Parameterized query:** Truyền input qua placeholder thay vì nối chuỗi.
  - **ORM:** Lớp ánh xạ object với bảng; không tự an toàn khi dùng raw query sai.
  - **PBKDF2:** Hàm dẫn xuất khóa lặp nhiều vòng dùng để hash mật khẩu.
  - **Least privilege:** Chỉ cấp quyền và khả năng tối thiểu cần thiết.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** ORM có chống SQLi trong mọi trường hợp?
    - **Trả lời gợi ý:** Không. Raw SQL, interpolation hoặc API escape sai vẫn tái tạo lỗi.
  - **Câu hỏi:** Prepared statement khác escaping?
    - **Trả lời gợi ý:** Prepared statement tách cấu trúc và giá trị ở API/driver; escaping biến đổi chuỗi và dễ sai theo context.

- **Câu chuyển sang slide tiếp theo**
  - Lab06 quay lại cookie, nhưng lần này trọng tâm là toàn vẹn state và nguồn role.

---

## Slide 18 — Cookie quay lại server như dữ liệu do client kiểm soát

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Cookie quay lại server như dữ liệu do client kiểm soát.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - 01 → Server Set-Cookie → role=user → Browser lưu → Name/value/flags
  - 02 → DevTools → Client sửa → role=admin → Cookie header mới
  - 03 → Vulnerable route → Đọc `lab06_role` → So sánh admin → Không DB check
  - 04 → Authorization → Tin role client → Allow trái phép → Broken Access Control

- **Các ý cần trình bày**
  - Plain flow tạo `lab06_username` và `lab06_role`; vulnerable admin route tin role trong Cookie header.
  - Người dùng sửa `role=user` thành `admin` trong DevTools rồi reload route; server cho phép vì policy sai.
  - Cookie luôn là input của request khi quay lại server, kể cả ban đầu do server phát hành.
  - HttpOnly chỉ chặn JavaScript đọc cookie; nó không tạo chữ ký, không ngăn sửa thủ công và không xác minh role.
  - Secure/SameSite xử lý kênh truyền và cross-site sending, không bảo đảm dữ liệu cookie chưa bị thay đổi.
  - Root cause là dùng state client làm authorization source.

- **Giải nghĩa từ khóa**
  - **Cookie Poisoning:** Sửa nội dung cookie để làm server đưa ra quyết định sai.
  - **Cookie attribute:** Thuộc tính Path, Domain, HttpOnly, Secure, SameSite.
  - **Integrity:** Khả năng phát hiện dữ liệu đã bị thay đổi.
  - **Authorization source:** Nguồn role/permission dùng cho quyết định truy cập.
  - **Client-controlled:** Dữ liệu nằm ở phía người dùng và có thể bị thay đổi.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Cookie do server tạo sao lại không đáng tin?
    - **Trả lời gợi ý:** Sau khi gửi cho client, giá trị quay lại chỉ là header do client cung cấp; server phải xác minh integrity và policy.
  - **Câu hỏi:** HttpOnly có chống Cookie Poisoning không?
    - **Trả lời gợi ý:** Không. Nó ngăn script đọc cookie nhưng không ngăn sửa qua client/DevTools hay request tự tạo.

- **Câu chuyển sang slide tiếp theo**
  - Để chọn giải pháp đúng, cần phân biệt encoding, signing, encryption và server-side state.

---

## Slide 19 — Base64, signing, encryption và session bảo vệ thuộc tính khác nhau

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Base64, signing, encryption và session bảo vệ thuộc tính khác nhau.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Plain: Có; Không; Không; Client role — sai / không revoke
  - Base64 JSON: Có; Không; Không; Decoded role — sai / không revoke
  - Signed cookie: Có; Có — SHA-256 signature; Không; Verify rồi DB role / revoke hạn chế
  - Fernet encrypted: Không; Có — authenticated encryption; Có; Demo read-only; không mang role động
  - Server session: Opaque ID; Hash lookup server; State ở server; Current DB role / revoke tức thời

- **Các ý cần trình bày**
  - Base64 Inspector decode JSON thật; đổi role rồi encode lại vẫn hợp lệ vì không có secret hoặc chữ ký.
  - Signed cookie dùng serializer với SHA-256 signature; sửa một ký tự làm verification thất bại trước khi dùng payload.
  - Bài vẫn đọc current role từ database sau verify signature để tránh role cũ hoặc role bị thu hồi.
  - Fernet demo cho confidentiality và integrity, nhưng cố ý không dùng token để phân quyền role động.
  - Server-side session đưa role và lifecycle về database; cookie chỉ chứa random opaque token.
  - Chọn mô hình theo yêu cầu: cần đọc kín, phát hiện sửa, cập nhật role tức thời hay revoke.

- **Giải nghĩa từ khóa**
  - **Base64:** Cách biểu diễn bytes bằng ký tự; có thể đảo ngược, không phải mã hóa.
  - **Signed cookie:** Payload kèm chữ ký để phát hiện sửa đổi.
  - **Encrypted cookie:** Payload được mã hóa; cần thêm kiểm tra toàn vẹn.
  - **Fernet:** Cơ chế authenticated encryption dùng trong demo.
  - **Opaque ID:** Mã không tự mang ý nghĩa role/user cho client.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Base64 có phải encryption?
    - **Trả lời gợi ý:** Không. Ai có dữ liệu đều decode được; không có key, confidentiality hoặc integrity.
  - **Câu hỏi:** Signed và encrypted cookie khác gì?
    - **Trả lời gợi ý:** Signed phát hiện sửa nhưng payload vẫn đọc được; encrypted che nội dung và nên kèm integrity/authentication.

- **Câu chuyển sang slide tiếp theo**
  - Mô hình chính của bài là server-side session với vòng đời create/resolve/rotate/revoke.

---

## Slide 20 — Server-side session tách token khỏi state và quyền

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Server-side session tách token khỏi state và quyền.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - Create / rotate → secrets.token_urlsafe(32) → Cookie nhận raw token → DB lưu SHA-256 hash → Revoke token cũ
  - Resolve → Hash token request → Lookup active session → Check expiry/user active → Đọc role mới từ DB
  - Authorize → Policy current role=admin → Không tin payload cookie → Allow/deny → Audit + trace
  - Logout → Mark inactive/revoked → Expire browser cookie → Token cũ bị từ chối → Session lifecycle đóng

- **Các ý cần trình bày**
  - Khi login, service tạo token URL-safe 32 byte, lưu hash SHA-256 trong `server_sessions` và chỉ gửi raw token cho browser.
  - Nếu có token cũ, rotate đánh dấu inactive/revoked trước khi tạo phiên mới; log chỉ lưu fingerprint.
  - Mỗi request hash token, lookup session active, kiểm expiry, trạng thái user và lấy role hiện tại từ users table.
  - Authorization admin dựa vào `resolution.database_role`, không dựa vào dữ liệu trong cookie.
  - Logout revoke record server-side và expire cookie; replay token cũ phải bị từ chối.
  - Signed/encrypted token vẫn hữu ích cho trường hợp phù hợp, nhưng không thay database-backed authorization và revoke.

- **Giải nghĩa từ khóa**
  - **Session ID:** Mã ngẫu nhiên trỏ đến state phiên lưu phía server.
  - **Rotation:** Đổi token và thu hồi token cũ khi login/đổi ngữ cảnh.
  - **Revocation:** Đánh dấu phiên không còn hợp lệ trước khi hết hạn.
  - **Expiry:** Thời điểm phiên tự hết hiệu lực.
  - **Fingerprint:** Giá trị rút gọn để đối chiếu token mà không lộ token thô.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Vì sao DB chỉ lưu hash Session ID?
    - **Trả lời gợi ý:** Nếu database log/bản sao bị lộ, hash không trực tiếp là bearer token dùng để truy cập phiên.
  - **Câu hỏi:** Cookie Poisoning khác Session Hijacking?
    - **Trả lời gợi ý:** Poisoning sửa state để lừa server; hijacking lấy hoặc dùng lại token hợp lệ của người khác.

- **Câu chuyển sang slide tiếp theo**
  - Sau sáu lab, có thể gom toàn bộ root cause vào một ma trận ranh giới.

---

## Slide 21 — Điểm gãy khác nhau; root fix luôn gần quyết định nhất

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Điểm gãy khác nhau; root fix luôn gần quyết định nhất.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - XSS: URL/form/storage; HTML/DOM sink; Encode/sanitize đúng context; safe DOM API
  - Overflow: HTTP input vào C; Capacity buffer; Length invariant + bounded write
  - Tampering: Price/ID/role; Business/access policy; DB + session + object authz + allowlist
  - CSRF: Request có cookie; Ý định trước mutation; Token + Origin/Referer + deny-before-write
  - SQLi: Input ghép query; SQL parser; Parameterized query; tách code/data
  - Cookie: Role/state client; Authorization source; Server session + current DB role + revoke

- **Các ý cần trình bày**
  - XSS và SQLi đều là lỗi dữ liệu chạm interpreter, nhưng interpreter và context khác nhau.
  - Overflow là lỗi biên bộ nhớ; không dùng khái niệm escaping để vá.
  - Tampering và Cookie Poisoning là lỗi nguồn quyết định, nên bản vá là đưa giá/identity/role về server.
  - CSRF là lỗi thiếu bằng chứng ý định trước mutation, dù identity của session là thật.
  - Root fix luôn đặt ở nơi hiểu invariant hoặc policy nhất; defense in depth đặt ở các lớp còn lại.
  - Ma trận giúp tránh dùng một control cho mọi lỗi, ví dụ validation/WAF/firewall/cookie flags.

- **Giải nghĩa từ khóa**
  - **Interpreter:** Thành phần đọc dữ liệu thành HTML, SQL, lệnh hoặc thao tác bộ nhớ.
  - **Policy:** Quy tắc cho phép/từ chối hành động.
  - **Primary control:** Control trực tiếp ngăn nguyên nhân gốc.
  - **Residual risk:** Rủi ro còn lại sau khi control chính đã áp dụng.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Tại sao nói root fix ở gần quyết định nhất?
    - **Trả lời gợi ý:** Thành phần đó biết đầy đủ context, invariant và policy; lớp ngoài thường chỉ thấy chuỗi hoặc request chung.
  - **Câu hỏi:** Validation có phải root fix chung không?
    - **Trả lời gợi ý:** Không. Nó hỗ trợ nhiều lab nhưng không thay encoding, binding, authorization, token hay bounded write.

- **Câu chuyển sang slide tiếp theo**
  - Các lỗi dễ nhầm sẽ được đối chiếu trực tiếp theo điều kiện kích hoạt và hậu quả.

---

## Slide 22 — Phân biệt lỗi bằng thứ bị giả mạo hoặc diễn giải sai

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Phân biệt lỗi bằng thứ bị giả mạo hoặc diễn giải sai.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - XSS ↔ CSRF: Script chạy trong origin; Browser gửi request ngoài ý muốn; Có thực thi code trong trang không?
  - Tampering ↔ SQLi: Đổi value để phá policy; Đổi syntax của query; Parser SQL có đọc input như code không?
  - Cookie poisoning ↔ hijacking: Sửa nội dung/state; Đánh cắp/replay token hợp lệ; Token bị sửa hay bị chiếm?
  - Overflow ↔ Injection: Ghi vượt vùng nhớ; Data đổi cú pháp/ý nghĩa; Biên memory hay interpreter bị phá?
  - Authn ↔ Authz: Bạn là ai; Bạn được làm gì trên object; Identity đúng đã đủ quyền chưa?

- **Các ý cần trình bày**
  - XSS có thể phá CSRF token vì script chạy cùng origin; nhưng hai root cause vẫn khác và cần vá độc lập.
  - Tampering có thể dùng tham số hoàn toàn hợp lệ về cú pháp; SQLi thay đổi cách SQL parser hiểu chuỗi.
  - Cookie poisoning cần dữ liệu client được server tin; session hijacking chỉ cần bearer token hợp lệ bị lộ.
  - Overflow là memory-safety; Injection là interpreter boundary.
  - Authentication thành công không thay object-level authorization và không chứng minh intent cho state change.
  - Khi trả lời câu hỏi, luôn nêu source, điểm gãy, decision và root fix.

- **Giải nghĩa từ khóa**
  - **Authentication:** Xác minh danh tính.
  - **Authorization:** Kiểm quyền hành động trên tài nguyên.
  - **Credential:** Thông tin hoặc token dùng để chứng minh danh tính/phiên.
  - **Intent:** Ý định thực hiện thao tác cụ thể.
  - **Replay:** Dùng lại token/request hợp lệ ở thời điểm hoặc ngữ cảnh khác.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** XSS có thể dẫn đến CSRF không?
    - **Trả lời gợi ý:** Script cùng origin có thể gửi request với token/credential, nhưng cần gọi đúng tên hai lỗi và vá cả XSS lẫn CSRF.
  - **Câu hỏi:** Authn thành công có đủ xem invoice không?
    - **Trả lời gợi ý:** Không. Còn phải kiểm authz trên invoice cụ thể theo owner hoặc role.

- **Câu chuyển sang slide tiếp theo**
  - Cuối cùng, mọi kết luận phải được đóng gói thành báo cáo có thể kiểm chứng.

---

## Slide 23 — Báo cáo tốt nối bước thử với nguyên nhân và bản vá

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Báo cáo tốt nối bước thử với nguyên nhân và bản vá.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - 01 / Bối cảnh: Tên lab, mục tiêu, môi trường, route, tài khoản/dữ liệu giả lập, phạm vi an toàn.
  - 02 / Thực hành: Các bước, input, request/response, state trước/sau, kết quả quan sát.
  - 03 / Phân tích: Source, sink/decision, nguyên nhân kỹ thuật, ảnh hưởng, mức độ và giới hạn.
  - 04 / Bản vá: Before/after code, control chính, defense in depth, lý do hiệu quả.
  - 05 / Retest: Cùng input trên secure flow; expected result; không side effect ngoài ý muốn.
  - 06 / Phụ lục: Ảnh thủ công, log, trace, audit, ASan/GDB, test và cấu hình liên quan.

- **Các ý cần trình bày**
  - Đề yêu cầu 11 mục; có thể trình bày theo bốn khối nhưng không được bỏ mục tiêu, môi trường, bước, kết quả, nguyên nhân, ảnh hưởng, phòng chống, mã vá, bài học và phụ lục.
  - Mỗi ảnh hoặc log phải có hành động tạo ra nó, thành phần cần quan sát và ý nghĩa.
  - Before/after code chỉ có giá trị khi đi kèm retest runtime.
  - Không tuyên bố ASan/GDB/test/coverage pass nếu chưa chạy và chưa có log thật.
  - Không coi tên file, tên binary hoặc cấu hình dự kiến là bằng chứng runtime.
  - Bản trình bày này cố ý không chèn ảnh chứng cứ theo yêu cầu, nhưng script nêu rõ evidence cần dùng khi thầy yêu cầu đối chiếu.

- **Giải nghĩa từ khóa**
  - **Reproducibility:** Người khác có thể lặp lại ca thử và thu được kết quả tương đương.
  - **Traceability:** Mỗi kết luận lần ngược được tới evidence và source.
  - **Before/after:** Đối chiếu hành vi hoặc code trước và sau bản vá.
  - **Limitation:** Phần chưa đo hoặc điều kiện khiến kết luận không áp dụng rộng hơn.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Evidence tối thiểu cho một bản vá là gì?
    - **Trả lời gợi ý:** Input tái hiện, trạng thái vulnerable, code/control sửa, retest cùng input và kết quả secure không có side effect.
  - **Câu hỏi:** Vì sao phải ghi limitation?
    - **Trả lời gợi ý:** Để không mở rộng kết luận vượt ngoài môi trường, dữ liệu và phép đo thực tế.

- **Câu chuyển sang slide tiếp theo**
  - Kết luận của toàn bộ Topic04 là đưa dữ liệu, policy và state về đúng ranh giới tin cậy.

---

## Slide 24 — Đặt niềm tin đúng chỗ

- **Mục tiêu của slide**
  - Làm rõ thông điệp: Đặt niềm tin đúng chỗ.
  - Giải thích luồng hoạt động và lý do control vulnerable/secure cho kết quả khác nhau.
  - Chuẩn bị thuật ngữ và câu trả lời ngắn khi giảng viên hỏi.

- **Nội dung cần chỉ trên slide**
  - 01 / Data: Mọi dữ liệu từ client đều không đáng tin cậy.
  - 02 / Interpreter: Tách dữ liệu khỏi HTML, SQL và vùng nhớ thực thi.
  - 03 / Decision: Identity, authorization, intent và state thuộc về server.
  - 04 / Evidence: Chỉ kết luận điều đã quan sát và retest.

- **Các ý cần trình bày**
  - Sáu lab cho thấy client không phải vùng an toàn, kể cả field bị ẩn, cookie do server phát hành hay request có session hợp lệ.
  - Dữ liệu phải được encode/bind/giới hạn đúng tại interpreter hoặc vùng nhớ nhận nó.
  - Giá, owner, role, intent và session lifecycle phải được server xác minh trên từng request phù hợp.
  - Defense in depth rất cần nhưng không được thay root fix.
  - Một bản vá hoàn chỉnh phải fail closed, có audit phù hợp và được retest bằng cùng ca thử.
  - Thông điệp cuối: biết payload giúp phát hiện; hiểu ranh giới mới giúp sửa đúng.

- **Giải nghĩa từ khóa**
  - **Secure by design:** Đưa control vào thiết kế và luồng chính ngay từ đầu.
  - **Fail closed:** Khi thiếu bằng chứng hoặc lỗi kiểm tra, mặc định từ chối.
  - **Server authoritative:** Server giữ nguồn dữ liệu và policy quyết định cuối.
  - **Verification:** Kiểm tra có hệ thống rằng yêu cầu đã được đáp ứng.

- **Câu hỏi thầy có thể hỏi**
  - **Câu hỏi:** Bài học quan trọng nhất?
    - **Trả lời gợi ý:** Không tin dữ liệu client và đặt kiểm tra tại nơi hiểu đầy đủ context, invariant và policy.
  - **Câu hỏi:** Nếu chỉ được chọn một thói quen kỹ thuật?
    - **Trả lời gợi ý:** Luôn vẽ luồng dữ liệu/quyết định và hỏi nguồn nào là authoritative trước khi viết hoặc duyệt code.

- **Câu chuyển sang slide tiếp theo**
  - Sẵn sàng trả lời câu hỏi và mở source/trace của từng lab khi cần.

---

## Ngân hàng 24 câu hỏi nhanh toàn bài

- **Câu 1:** Vì sao validation không đủ chống XSS?
  - **Trả lời:** Vì validation chỉ đánh giá input theo quy tắc nghiệp vụ; output vẫn cần encoding theo context hoặc sanitization khi cho phép HTML.

- **Câu 2:** CSP có thay việc sửa sink không?
  - **Trả lời:** Không. CSP là defense in depth; sink nguy hiểm vẫn phải thay.

- **Câu 3:** Tại sao 32 byte đã vượt `char[32]`?
  - **Trả lời:** Chuỗi C cần một byte null terminator, nên chỉ còn 31 byte dữ liệu.

- **Câu 4:** Firewall có chặn Buffer Overflow không?
  - **Trả lời:** Không chắc; request hợp lệ vẫn có thể vượt capacity nội bộ của chương trình C.

- **Câu 5:** ASLR, PIE, NX, RELRO, canary khác nhau thế nào?
  - **Trả lời:** PIE cho phép code chính được randomize bởi ASLR; NX ngăn thực thi data; RELRO bảo vệ relocation; canary phát hiện stack overwrite.

- **Câu 6:** IDOR thuộc nhóm nào?
  - **Trả lời:** Broken Access Control; trong API Security Top 10 2023 là API1 Broken Object Level Authorization.

- **Câu 7:** Hidden field có an toàn hơn query parameter?
  - **Trả lời:** Không. Cả hai đều do client kiểm soát và sửa được.

- **Câu 8:** Session cookie chứng minh điều gì?
  - **Trả lời:** Nó giúp server gắn request với identity/phiên; không tự chứng minh intent hay quyền trên object.

- **Câu 9:** SOP có chống CSRF không?
  - **Trả lời:** SOP chủ yếu chặn đọc response; không ngăn mọi cách gửi form/request.

- **Câu 10:** CORS có phải bản vá CSRF?
  - **Trả lời:** Không. CORS kiểm soát script đọc response; synchronizer token và server-side checks mới là control chính.

- **Câu 11:** Vì sao token phải gắn với session?
  - **Trả lời:** Để request giả từ phiên/nguồn khác không có giá trị bí mật đúng của phiên nạn nhân.

- **Câu 12:** Prepared statement khác escape thủ công?
  - **Trả lời:** Prepared statement tách cấu trúc khỏi tham số tại driver; escaping phụ thuộc context và dễ sai.

- **Câu 13:** ORM có luôn an toàn?
  - **Trả lời:** Không; raw SQL hoặc interpolation sai vẫn gây injection.

- **Câu 14:** Base64 có phải mã hóa?
  - **Trả lời:** Không; chỉ là encoding đảo ngược được và không có key/integrity.

- **Câu 15:** Signed cookie có giữ bí mật payload?
  - **Trả lời:** Không; signing bảo vệ integrity/authenticity, payload vẫn có thể đọc.

- **Câu 16:** Fernet giải quyết gì?
  - **Trả lời:** Authenticated encryption cung cấp confidentiality và integrity cho token demo.

- **Câu 17:** Vì sao signed cookie vẫn kiểm role trong DB?
  - **Trả lời:** Để dùng role hiện tại và cho phép thay đổi/thu hồi quyền thay vì tin claim cũ.

- **Câu 18:** Poisoning khác hijacking?
  - **Trả lời:** Poisoning sửa dữ liệu; hijacking lấy/replay token hợp lệ.

- **Câu 19:** Root fix khác defense in depth?
  - **Trả lời:** Root fix loại bỏ nguyên nhân; defense in depth giảm khả năng/hậu quả nếu control chính thất bại.

- **Câu 20:** Tại sao phải retest cùng input?
  - **Trả lời:** Để chứng minh thay đổi kết quả đến từ bản vá, không phải do ca thử khác.

- **Câu 21:** Một kết luận runtime cần gì?
  - **Trả lời:** Input, hành vi quan sát được, log/trace/state tương ứng và retest sau bản vá.

- **Câu 22:** Vì sao audit không thay authorization?
  - **Trả lời:** Audit ghi lại sau/trong flow để phát hiện; authorization phải chặn request hiện tại trước side effect.

- **Câu 23:** Fail closed nghĩa là gì?
  - **Trả lời:** Thiếu token, role, session record hoặc kết quả kiểm tra hợp lệ thì mặc định từ chối.

- **Câu 24:** Điểm chung của sáu lab?
  - **Trả lời:** Dữ liệu hoặc quyết định đi qua ranh giới tin cậy mà thiếu control đúng context.

## Checklist trước khi thuyết trình

- Mở sẵn HTML hoặc PowerPoint và kiểm phím trái/phải.
- Nhớ cổng local: Lab01 5000, Lab02 5002, Lab03 5003, Lab04 victim 5004/attacker 9004, Lab05 5005, Lab06 5006.
- Không chạy payload ngoài môi trường lab.
- Không tuyên bố test/coverage/runtime pass nếu không có log của lần chạy tương ứng.
- Khi bị hỏi “vì sao”, trả lời theo bốn ý: source → điểm gãy/interpreter → quyết định sai → root fix.
