# Demo script Lab02 — Buffer Overflow

## Mục tiêu demo

- Chứng minh `char name[32]` chỉ chứa 31 byte dữ liệu và byte `null`.
- Phân biệt vượt capacity, ASan phát hiện và process crash.
- Quan sát native trace/GDB rồi đối chiếu length check và `snprintf`.
- Giải thích hardening là defense in depth, không thay thế kiểm tra độ dài.

## Chuẩn bị

- Thư mục làm việc: `cd Lab02`
- Khởi động: `scripts\run_lab.bat` (cần WSL/Ubuntu; script tự `make all`)
- URL: `http://127.0.0.1:5002`
- Native tool: WSL/Ubuntu có `make`, `gdb`; đặt `ulimit -c 0` trước GDB.
- Dùng UI với `Build profile`, `Trường name`, các mẫu `A × 31`, `A × 32`, `A × 64`.

### F12 cần show

- Nhấn `F12` hoặc `Ctrl+Shift+I`, mở `Network`, bật `Preserve log` và `Disable cache`; mỗi lần gửi bấm `Clear` trước khi nhập mẫu tiếp theo.
- `Network → POST`: show đúng endpoint (`/submit`, `/secure/length/submit` hoặc `/secure/snprintf/submit`), `Payload/Form Data` với `mode`/`name` và `Response` chứa status/trace.
- Trên giao diện Lab02, mở `Trace Panel`/`ASan Inspector` để show input bytes, buffer size, exit code, raw stderr; đây là bằng chứng native, không phải nội dung của tab F12.
- `Sources` của browser không chứa binary C; GDB/ASan output phải show trong cửa sổ WSL/terminal, không gọi F12 là bằng chứng thay thế.

## Kịch bản trình bày

*Quy ước bằng chứng: kết quả ASan/GDB chưa được coi là observed nếu chưa chạy đúng runtime native; phân biệt “kỳ vọng” với output thực tế.*

**Bước 1 — Xác lập đường đi HTTP → tiến trình C**

* Thao tác:
  1. Mở `http://127.0.0.1:5002`, rồi bấm nút `Bắt đầu bản lỗi`.
  2. Ở ô chọn `Build profile`, bấm mũi tên dropdown và chọn `Vulnerable + AddressSanitizer`.
  3. Bấm ô textarea `Trường name`, nhấn `Ctrl+A`, nhập `Le Minh`, rồi bấm `Gửi đến tiến trình C`.
  4. Cuộn xuống khu vực Trace Panel để chuẩn bị chỉ vào input bytes, buffer và exit code.
* Nói: “Flask nhận input HTTP rồi gọi binary native với `shell=False`. Tôi bắt đầu bằng input bình thường để có mốc byte length và buffer.”
* Quan sát: trace hiển thị input bytes, `NAME_BUFFER_SIZE=32`, buffer bytes và exit code; input bình thường được copy mà không có overflow.
* F12 show: `Network → POST /submit → Payload` chỉ ra `mode=vulnerable_asan` và `name=Le Minh`; `Response` show trace ID/status; trên UI mở `Trace Panel` để chỉ input bytes và exit code.
* Kết luận: HTTP chỉ là điểm kích hoạt; lỗi xảy ra khi backend native thực hiện `strcpy(name, user_input)`.

**Bước 2 — Chạm ranh giới 31/32/64 byte**

* Thao tác:
  1. Giữ trang vulnerable và profile `Vulnerable + AddressSanitizer` đang chọn.
  2. Trong hàng `Input mẫu`, lần lượt bấm `A × 31` rồi `Gửi đến tiến trình C`; bấm `A × 32` rồi submit; cuối cùng bấm `A × 64` rồi submit.
  3. Sau mỗi lần gửi, cuộn tới Trace Panel và ghi lại status trước khi chuyển sang mẫu tiếp theo.
* Nói: “31 byte còn chỗ cho byte kết thúc chuỗi. 32 byte đã vượt capacity dữ liệu; 64 byte tạo lỗi rõ hơn nhưng không được đồng nhất overflow với crash.”
* Quan sát: 31 byte là mốc hợp lệ; 32 byte vượt `NAME_SAFE_CAPACITY=31` và không được xem là an toàn dù có thể chưa crash; 64 byte với binary ASan được kỳ vọng báo `stack-buffer-overflow`, ghi file/line native và exit bất thường nếu toolchain chạy đúng.
* F12 show: giữ ba request `POST /submit` trong Network để so sánh `name`/status; mở Response của mẫu 64 và UI `ASan Inspector` để chỉ `stack-buffer-overflow`, file/line, raw stderr nếu runtime thật sự trả các trường đó.
* Kết luận: có ba trạng thái khác nhau: vượt capacity, công cụ phát hiện và process bị crash; không suy luận trạng thái này từ trạng thái kia.

**Bước 3 — Quan sát stack frame bằng GDB**

* Thao tác:
  1. Trên web không có nút để chạy GDB. Giữ browser ở request của Bước 2 để lát nữa đối chiếu với output native.
  2. Mở WSL/terminal, chạy `cd /mnt/c/Users/Administrator/Documents/MEGA/mmt/Topic04/Lab02`, rồi chạy `make all`.
  3. Chạy `ulimit -c 0`; tiếp tục chạy `gdb -q -x gdb/inspect_normal.gdb`.
  4. Thoát hoặc mở phiên GDB mới, chạy `gdb -q -x gdb/inspect_overflow.gdb`; script overflow dùng input 64 ký tự `A`.
  5. Quay lại browser chỉ để show request/response tương ứng; phần frame, local variable và backtrace phải chỉ từ cửa sổ WSL.
* Nói: “GDB chỉ quan sát frame/local/`sizeof(name)` và backtrace theo script có sẵn. Tôi không sửa control flow hay địa chỉ.”
* Quan sát: normal cho thấy `name` có kích thước 32; overflow script, nếu GDB/native binary chạy được, cho thấy input dài hơn vùng local và trạng thái stack/backtrace tương ứng; ghi output thật thay cho mô tả kỳ vọng.
* F12 show: không dùng Network để thay thế GDB; nếu cần liên hệ request HTTP, show `POST /submit` và `Response` trước, sau đó chuyển sang WSL show đúng output của `inspect_normal.gdb`/`inspect_overflow.gdb`.
* Kết luận: `name` là local stack buffer; `strcpy` không nhận giới hạn nên có thể ghi qua ranh giới object.

**Bước 4 — Cùng input 64 byte qua bản secure length**

* Thao tác:
  1. Về trang chủ bằng cách bấm logo/đường dẫn trang chủ hoặc nhấn `Ctrl+L`, nhập `http://127.0.0.1:5002`, nhấn `Enter`.
  2. Bấm nút `Mở length check`; nếu đang ở trang so sánh, bấm đúng card `Length check`.
  3. Ở form `Trường name`, bấm mẫu `A × 64`; textarea được điền tự động, rồi bấm `Gửi đến tiến trình C`.
  4. Cuộn xuống Trace Panel và giữ nguyên trang kết quả để đối chiếu với request vulnerable.
* Nói: “Input giống Bước 2 để so sánh công bằng. Bản secure phải từ chối trước khi copy, không cắt im lặng.”
* Quan sát: trace/response kỳ vọng báo `Rejected: input exceeds 31 bytes`, exit code từ nhánh length check và không có `stack-buffer-overflow`; xác nhận bằng output live.
* F12 show: `Network → POST /secure/length/submit → Payload` để chỉ `name=A×64`; `Response` show reject/status; UI `Trace Panel` show length check và không có ASan overflow.
* Kết luận: primary fix là kiểm tra byte length trước thao tác copy và giữ invariant 31 byte dữ liệu + `null`.

**Bước 5 — Cùng input 64 byte qua `snprintf`**

* Thao tác:
  1. Nhấn `Ctrl+L`, nhập `http://127.0.0.1:5002`, nhấn `Enter`, rồi bấm nút `Mở snprintf`.
  2. Bấm mẫu `A × 64` trong `Input mẫu`; kiểm tra textarea `Trường name` đã được điền, rồi bấm `Gửi đến tiến trình C`.
  3. Cuộn tới Trace Panel và mở phần output để chỉ vào `written` và kết quả reject/truncate.
* Nói: “`snprintf` giới hạn kích thước vùng đích, nhưng bản lab vẫn kiểm tra `written` để không báo thành công sau khi bị truncate.”
* Quan sát: response kỳ vọng báo input vượt giới hạn/không chấp nhận kết quả bị cắt; không có ASan overflow, và trace phân biệt `written` với `sizeof(name)`.
* F12 show: `Network → POST /secure/snprintf/submit`, mở `Payload` và `Response`; UI trace show `written`, `sizeof(name)` và verdict reject/truncate thực tế.
* Kết luận: bounded formatting tốt hơn API không giới hạn, nhưng phải kiểm tra trạng thái truncate/error thay vì coi output cắt ngắn là thành công.

**Bước 6 — Tách primary fix khỏi hardening**

* Thao tác:
  1. Nhấn `Ctrl+L`, nhập `http://127.0.0.1:5002`, nhấn `Enter`, rồi bấm `Mở Hardening Inspector`.
  2. Cuộn tới khu vực build profile, bấm mẫu `A × 64` ở profile `secure_hardened`, rồi bấm `Chạy hardened`.
  3. Nếu cần quan sát GDB, mở WSL/terminal, đứng tại thư mục Lab02, chạy `make all`, rồi chạy `gdb -q -x gdb/inspect_hardened.gdb`.
  4. Phần compiler/loader flags lấy từ Hardening Inspector hoặc output WSL; không coi trang web là bằng chứng đã chạy GDB.
* Nói: “Compiler/loader hardening làm exploitation khó hơn hoặc phát hiện sớm hơn. Nó không biến `strcpy` không giới hạn thành API an toàn.”
* Quan sát: trang/trace nêu `-fstack-protector-strong`, `_FORTIFY_SOURCE`, PIE/ASLR, RELRO và NX/DEP; GDB hardened chỉ được gọi là observed khi command trả output thật.
* F12 show: `Network → GET /hardening → Response` chỉ dùng để chứng minh trang đã tải; phần flag phải show ở trang `Hardening`/source hoặc output WSL, không nói rằng F12 đã quan sát compiler flag.
* Kết luận: length validation/secure API là fix gốc; canary, ASLR, DEP/NX và RELRO là lớp giảm tác động.

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
**Trả lời khi demo:** Có thể nêu stack protector/canary, ASLR/PIE, DEP/NX, `_FORTIFY_SOURCE` và RELRO. Bản lab hiển thị các flag này trong `/hardening`; chúng là defense in depth sau khi code đã được sửa.

## Nếu demo lỗi

- Nếu WSL không có hoặc `make all` lỗi, ghi rõ native demo chưa chạy; không gọi ASan/GDB là observed, và dùng source/trace có sẵn để giải thích.
- Nếu `scripts\run_lab.bat` không khởi động được, kiểm tra `http://127.0.0.1:5002`, dừng phiên cũ rồi chạy lại script; không tự thay bằng binary chưa build.
- Nếu UI báo quá 256 byte, dùng đúng mẫu `A × 64`; giới hạn UI là 256 byte, còn invariant native là 31 byte dữ liệu.
- Nếu 32 byte không crash, vẫn kết luận đã vượt capacity; chỉ kết luận process crash khi response/exit code hoặc runtime log cho thấy.

## Chốt lab

Root cause: `strcpy` ghi input dài vào `char name[32]` không có giới hạn.
Primary fix: kiểm tra byte length hoặc dùng bounded API và kiểm tra truncate/error.
Defense in depth: ASan, stack canary, ASLR/PIE, DEP/NX, FORTIFY và RELRO.
