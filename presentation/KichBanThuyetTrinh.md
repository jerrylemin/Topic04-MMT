# Kịch bản thuyết trình chi tiết Topic04

**Chủ đề:** Sáu lỗ hổng, một ranh giới niềm tin  
**Thành viên:** Lê Minh — 21127645; Nguyễn Vũ Bách — 21127224  
**Số slide:** 18  
**Nguồn trình bày:** `21127645_LeMinh_21127224_NguyenVuBach_Topic04_6Labs_short.pptx`

## Cách sử dụng kịch bản

- Mỗi mục tương ứng với đúng một slide trong PowerPoint.
- Các bullet trong phần **Kịch bản trình bày** có thể đọc lần lượt khi thuyết trình.
- Không cần đọc nguyên văn toàn bộ phần **Giải thích thuật ngữ**. Phần này dùng để tra cứu và giải thích khi giảng viên hỏi.
- Thời lượng gợi ý:
  - Slide mở đầu và chuyển chương: khoảng 30–45 giây.
  - Slide kỹ thuật: khoảng 1,5–2,5 phút.
  - Tổng thời lượng: khoảng 25–35 phút tùy mức độ giải thích.

---

# Slide 01 — Sáu lỗ hổng, một ranh giới niềm tin

## Mục tiêu của slide

- Giới thiệu chủ đề chung.
- Nêu phạm vi an toàn của bài thực hành.
- Giới thiệu hai thành viên thực hiện.

## Kịch bản trình bày

- Kính chào thầy/cô và các bạn. Nhóm em gồm **Lê Minh, mã số sinh viên 21127645**, và **Nguyễn Vũ Bách, mã số sinh viên 21127224**.
- Chủ đề nhóm em trình bày là **“Sáu lỗ hổng, một ranh giới niềm tin”**.
- Sáu lỗ hổng được nghiên cứu gồm:
  - Cross-Site Scripting, hay XSS.
  - Buffer Overflow.
  - Parameter Tampering.
  - Cross-Site Request Forgery, hay CSRF.
  - SQL Injection.
  - Cookie Poisoning.
- Sáu lỗi này khác nhau về kỹ thuật, nhưng có một điểm chung:
  - Ứng dụng đã tin dữ liệu hoặc quyết định tại một vị trí không an toàn.
  - Dữ liệu từ client được sử dụng mà chưa được kiểm tra theo đúng ngữ cảnh.
- Mục tiêu của bài không chỉ là biết một payload có thể làm gì.
- Mục tiêu quan trọng hơn là:
  - Xác định dữ liệu đi từ đâu.
  - Xác định nơi dữ liệu được xử lý hoặc diễn giải.
  - Xác định thành phần nào đưa ra quyết định cuối cùng.
  - Đặt bản vá tại đúng ranh giới bị phá vỡ.
- Toàn bộ thử nghiệm chỉ được thực hiện trong môi trường local có kiểm soát.
- Nhóm không thực hiện trên website thật, không đánh cắp dữ liệu thật và không chiếm quyền hệ thống.

## Câu chuyển sang slide tiếp theo

- Để phân tích thống nhất cả sáu lỗ hổng, nhóm sử dụng một khung gồm ba câu hỏi: **source ở đâu, sink ở đâu và ai giữ quyết định cuối cùng**.

## Giải thích thuật ngữ và từ chuyên ngành

- **Lỗ hổng bảo mật:** Điểm yếu trong thiết kế, mã nguồn, cấu hình hoặc quy trình, có thể khiến hệ thống hoạt động ngoài ý muốn.
- **Khai thác lỗ hổng:** Quá trình tạo điều kiện để điểm yếu biểu hiện thành hành vi sai, ví dụ chạy script, đọc dữ liệu trái quyền hoặc làm chương trình crash.
- **Ranh giới niềm tin — Trust boundary:** Điểm chuyển tiếp giữa hai vùng có mức độ tin cậy khác nhau, ví dụ từ browser sang server hoặc từ ứng dụng web sang chương trình C.
- **Client:** Phía gửi request đến server, thường là trình duyệt hoặc ứng dụng của người dùng.
- **Server:** Phía tiếp nhận request, xử lý nghiệp vụ, truy cập dữ liệu và trả response.
- **Local:** Môi trường chạy trên máy cá nhân hoặc máy ảo, không phải hệ thống công khai.
- **Môi trường có kiểm soát:** Môi trường được thiết kế cho mục đích học tập, có dữ liệu giả lập và không ảnh hưởng hệ thống thật.
- **Payload:** Dữ liệu kiểm thử được đưa vào ứng dụng để quan sát cách hệ thống xử lý.
- **Root cause:** Nguyên nhân gốc tạo ra lỗ hổng.
- **Root fix:** Bản vá trực tiếp loại bỏ nguyên nhân gốc.

---

# Slide 02 — Đọc mọi lỗi qua ba câu hỏi

## Mục tiêu của slide

- Giới thiệu khung phân tích dùng cho toàn bộ bài.
- Nhấn mạnh phạm vi thực hành an toàn.

## Kịch bản trình bày

- Nhóm đọc mỗi lỗ hổng thông qua ba câu hỏi.
- Câu hỏi thứ nhất là **Source: Dữ liệu đến từ đâu?**
  - Dữ liệu có thể đến từ URL, form, cookie, HTTP body, database hoặc bộ nhớ.
  - Việc xác định source giúp biết điểm bắt đầu của luồng dữ liệu không đáng tin cậy.
- Câu hỏi thứ hai là **Sink: Dữ liệu được diễn giải ở đâu?**
  - Ví dụ browser diễn giải dữ liệu thành HTML.
  - SQL parser diễn giải chuỗi thành truy vấn.
  - Hàm `strcpy` ghi dữ liệu vào vùng nhớ cố định.
- Câu hỏi thứ ba là **Decision: Ai giữ quyết định cuối cùng?**
  - Server hay client quyết định giá sản phẩm?
  - Session cookie chỉ chứng minh người dùng đã đăng nhập, hay có chứng minh ý định đổi email không?
  - Role trong cookie hay role trong database mới là nguồn quyết định quyền truy cập?
- Ba câu hỏi này giúp nhóm tránh chỉ tập trung vào payload.
- Payload có thể thay đổi, nhưng ranh giới tin cậy và nguyên nhân gốc thường ổn định hơn.
- Phạm vi an toàn của bài gồm:
  - Chỉ chạy local.
  - Chỉ dùng dữ liệu giả lập.
  - Không thử trên website thật.
  - Không chiếm quyền hệ thống.
  - Không tạo reverse shell, malware hoặc persistence.
- Trong các slide sau, nhóm sẽ áp dụng cùng một cách đọc cho từng lab.

## Câu chuyển sang slide tiếp theo

- Lab đầu tiên là XSS, nơi dữ liệu không tin cậy đi từ một source đến một sink có khả năng diễn giải dữ liệu thành HTML hoặc JavaScript.

## Giải thích thuật ngữ và từ chuyên ngành

- **Source:** Nguồn đưa dữ liệu vào luồng xử lý, ví dụ query parameter, form field, cookie hoặc URL fragment.
- **Sink:** Điểm tiếp nhận và diễn giải dữ liệu, có thể biến dữ liệu thành mã, truy vấn, đường dẫn hoặc thao tác bộ nhớ.
- **Decision:** Quyết định bảo mật cuối cùng, ví dụ cho phép truy cập, cập nhật dữ liệu hoặc chạy một thao tác.
- **Data flow:** Luồng di chuyển và biến đổi của dữ liệu qua các thành phần.
- **Input:** Dữ liệu đầu vào do người dùng hoặc hệ thống khác cung cấp.
- **Output:** Dữ liệu ứng dụng trả về hoặc đưa sang thành phần khác.
- **Dữ liệu giả lập:** Dữ liệu được tạo riêng cho bài lab, không phải thông tin cá nhân hoặc dữ liệu thật.
- **Website thật:** Website công khai hoặc hệ thống không được cấp quyền kiểm thử.
- **Chiếm quyền hệ thống:** Đạt được quyền điều khiển hoặc thực thi trái phép trên hệ thống.
- **Reverse shell:** Kết nối dòng lệnh từ máy mục tiêu quay về máy điều khiển.
- **Malware:** Phần mềm được tạo với mục đích gây hại, đánh cắp dữ liệu hoặc kiểm soát hệ thống.
- **Persistence:** Kỹ thuật duy trì quyền truy cập sau khi hệ thống khởi động lại hoặc phiên kết thúc.

---

# Slide 03 — XSS là đường đi từ source đến sink

## Mục tiêu của slide

- Phân biệt Reflected XSS, Stored XSS và DOM-based XSS.
- Giải thích luồng source → storage → sink.

## Kịch bản trình bày

- XSS xảy ra khi dữ liệu không đáng tin cậy được browser diễn giải thành HTML hoặc JavaScript có thể thực thi.
- Với **Reflected XSS**:
  - Source là tham số query trong URL, ví dụ giá trị `q`.
  - Server đưa dữ liệu đó vào HTML response mà không encode đúng.
  - Browser parser đọc response và diễn giải payload.
  - Payload chỉ xuất hiện trong một request cụ thể.
  - Nạn nhân thường phải mở URL đã được tạo sẵn.
- Với **Stored XSS**:
  - Source là form bình luận.
  - Payload được lưu vào SQLite hoặc một nơi lưu trữ khác.
  - Khi server render template, dữ liệu được phát lại.
  - Mọi người mở trang chứa dữ liệu đó đều có thể bị ảnh hưởng.
  - Việc tải lại trang có thể làm payload chạy lại.
- Với **DOM-based XSS**:
  - Source nằm ở phía browser, ví dụ `location.hash`.
  - JavaScript phía client đọc fragment.
  - Dữ liệu được đưa vào `innerHTML`.
  - Browser tạo DOM mới và có thể kích hoạt event handler.
- Điểm đáng chú ý là fragment sau dấu `#` thường không được gửi trong HTTP request.
- Vì vậy server có thể không nhìn thấy payload, nhưng browser vẫn chạm vào sink nguy hiểm.
- Ba loại XSS khác nhau về đường đi, nhưng cùng nguyên nhân:
  - Dữ liệu bị biến từ data thành code hoặc markup.

## Câu chuyển sang slide tiếp theo

- Vì lỗi xuất hiện tại điểm dữ liệu được diễn giải, bản vá XSS phải đặt tại sink, không thể chỉ dừng ở validation đầu vào.

## Giải thích thuật ngữ và từ chuyên ngành

- **XSS — Cross-Site Scripting:** Lỗ hổng cho phép dữ liệu không tin cậy được browser diễn giải thành script hoặc HTML có khả năng gây hại.
- **Reflected XSS:** Payload đi vào request và được phản chiếu ngay trong response.
- **Stored XSS:** Payload được lưu bền vững rồi phát lại cho người dùng khi xem dữ liệu.
- **DOM-based XSS:** XSS phát sinh do JavaScript phía client đọc source và ghi vào DOM sink nguy hiểm.
- **URL query:** Phần tham số sau dấu `?` trong URL, ví dụ `?q=test`.
- **HTML response:** Nội dung HTML server trả về cho browser.
- **Browser parser:** Thành phần của trình duyệt phân tích HTML, CSS và JavaScript để tạo trang.
- **Comment form:** Biểu mẫu cho phép người dùng gửi bình luận.
- **SQLite:** Hệ quản trị cơ sở dữ liệu nhúng, lưu dữ liệu trong một file local.
- **Payload:** Chuỗi kiểm thử dùng để quan sát liệu dữ liệu có bị thực thi hoặc diễn giải sai không.
- **Template render:** Quá trình ghép dữ liệu vào mẫu HTML để tạo response.
- **Viewer:** Người dùng mở và xem nội dung.
- **DOM — Document Object Model:** Mô hình đối tượng biểu diễn cấu trúc tài liệu HTML trong browser.
- **`location.hash`:** Phần fragment của URL bắt đầu bằng dấu `#`.
- **Fragment:** Phần URL thường dùng để trỏ tới vị trí trong trang và không được gửi lên server trong request thông thường.
- **`innerHTML`:** Thuộc tính DOM cho phép đọc hoặc ghi chuỗi dưới dạng HTML.
- **Event handler:** Đoạn mã chạy khi một sự kiện xảy ra, ví dụ click, load hoặc error.
- **Storage:** Nơi lưu dữ liệu, ví dụ database, file, session hoặc cache.
- **Markup:** Cấu trúc đánh dấu như HTML, được browser phân tích để tạo giao diện.

---

# Slide 04 — Vá tại sink, không dừng ở validation

## Mục tiêu của slide

- Trình bày bản vá nguyên nhân gốc cho ba loại XSS.
- Phân biệt root fix với defense in depth.

## Kịch bản trình bày

- Trước tiên, nhóm so sánh phiên bản vulnerable và secure của từng loại XSS.
- Với Reflected XSS:
  - Phiên bản lỗi sử dụng dữ liệu theo dạng `Markup(q)`.
  - Cách này nói với template rằng chuỗi đã an toàn, nên dữ liệu có thể được đưa thẳng vào HTML.
  - Phiên bản secure sử dụng cơ chế autoescape của Jinja.
- Với Stored XSS:
  - Phiên bản lỗi đưa nội dung bình luận vào `Markup(body)`.
  - Phiên bản an toàn sử dụng sanitization theo allowlist.
  - Chỉ các thẻ và thuộc tính được phép mới được giữ lại.
- Với DOM-based XSS:
  - Phiên bản lỗi ghi chuỗi vào `innerHTML`.
  - Phiên bản an toàn dùng `textContent` khi chỉ cần hiển thị văn bản.
- Root fix của XSS gồm ba nhóm:
  - Encode dữ liệu đúng theo ngữ cảnh.
  - Sanitize khi thật sự cần cho phép rich text.
  - Sử dụng DOM API an toàn.
- Contextual encoding phải phụ thuộc nơi dữ liệu xuất hiện:
  - HTML text.
  - JavaScript.
  - URL.
  - HTML attribute.
- Validation vẫn hữu ích, nhưng không đủ:
  - Một chuỗi hợp lệ trong ngữ cảnh này có thể nguy hiểm trong ngữ cảnh khác.
  - Validation không thay thế output encoding.
- CSP, HttpOnly, Secure và SameSite là defense in depth:
  - Chúng giảm khả năng khai thác hoặc giảm hậu quả.
  - Chúng không làm một sink nguy hiểm trở thành an toàn.
- Stored XSS có phạm vi rộng vì payload có thể ảnh hưởng mọi viewer.
- HttpOnly chỉ giảm khả năng JavaScript đọc cookie, không ngăn script thực hiện mọi hành động khác.

## Câu chuyển sang slide tiếp theo

- Lab tiếp theo chuyển từ việc browser diễn giải dữ liệu sang một loại ranh giới khác: dữ liệu HTTP đi vào chương trình C và chạm tới vùng nhớ stack.

## Giải thích thuật ngữ và từ chuyên ngành

- **Vulnerable:** Trạng thái hoặc phiên bản có lỗ hổng.
- **Secure:** Trạng thái hoặc phiên bản đã áp dụng biện pháp bảo vệ phù hợp.
- **Validation:** Kiểm tra định dạng, kiểu, độ dài hoặc miền giá trị của input.
- **Output encoding:** Chuyển ký tự đặc biệt thành biểu diễn an toàn để dữ liệu không bị hiểu là mã.
- **Contextual encoding:** Encoding phù hợp với đúng ngữ cảnh đích, ví dụ HTML, JavaScript, URL hoặc attribute.
- **HTML context:** Vị trí dữ liệu nằm trong nội dung HTML.
- **JavaScript context:** Vị trí dữ liệu nằm trong chuỗi hoặc biểu thức JavaScript.
- **URL context:** Vị trí dữ liệu nằm trong URL và cần URL encoding.
- **Attribute context:** Vị trí dữ liệu nằm trong thuộc tính HTML như `href`, `src` hoặc `value`.
- **Jinja:** Template engine thường dùng với Flask.
- **Autoescape:** Cơ chế tự động escape ký tự đặc biệt khi render template.
- **`Markup`:** Kiểu dữ liệu đánh dấu chuỗi là HTML an toàn, có thể làm mất tác dụng autoescape nếu dùng sai.
- **Sanitization:** Làm sạch nội dung bằng cách loại bỏ thành phần nguy hiểm.
- **Allowlist:** Danh sách những giá trị được phép, mọi giá trị khác bị loại bỏ hoặc từ chối.
- **Rich text:** Nội dung có định dạng như in đậm, liên kết hoặc danh sách.
- **Safe DOM API:** API thao tác DOM không diễn giải dữ liệu thành HTML khi không cần thiết.
- **`textContent`:** Thuộc tính đặt nội dung dưới dạng văn bản thuần.
- **Defense in depth:** Nhiều lớp phòng thủ bổ sung, để một lớp thất bại không dẫn ngay đến hậu quả nghiêm trọng.
- **CSP — Content Security Policy:** Chính sách giới hạn nguồn và loại nội dung mà browser được phép thực thi.
- **HttpOnly:** Cờ cookie ngăn JavaScript phía client đọc cookie qua `document.cookie`.
- **Secure cookie:** Cookie chỉ được gửi qua kết nối HTTPS.
- **SameSite:** Cờ kiểm soát việc gửi cookie trong các request cross-site.
- **Root fix:** Biện pháp sửa trực tiếp nguyên nhân gốc.
- **Blast radius:** Phạm vi ảnh hưởng khi sự cố hoặc khai thác xảy ra.

---

# Slide 05 — HTTP có thể chạm vùng nhớ stack

## Mục tiêu của slide

- Giải thích Buffer Overflow trong backend native.
- Mô tả sự khác nhau giữa input ngắn và input vượt capacity.

## Kịch bản trình bày

- Buffer Overflow không nhất thiết bắt đầu từ một chương trình dòng lệnh.
- Trong lab này, dữ liệu đi theo chuỗi:
  - Browser gửi input local.
  - Request `POST /submit` được gửi đến Flask.
  - Flask áp dụng một số giới hạn request.
  - Ứng dụng gọi chương trình native bằng `subprocess`.
  - Chương trình C sử dụng `strcpy` để copy dữ liệu vào `name[32]`.
- `name[32]` có tổng capacity là 32 byte.
- Để lưu một chuỗi C hợp lệ:
  - Tối đa 31 byte dành cho dữ liệu.
  - 1 byte dành cho ký tự kết thúc null.
- Khi input nằm trong capacity:
  - Dữ liệu được ghi trong buffer.
  - Canary, saved frame và return address không bị thay đổi.
- Khi input quá dài:
  - `strcpy` tiếp tục copy vì hàm này không biết kích thước buffer đích.
  - Dữ liệu có thể ghi sang vùng nhớ lân cận.
  - Canary có thể bị đổi.
  - Stack frame có thể bị hỏng.
  - Chương trình rơi vào undefined behavior hoặc crash.
- Firewall vẫn có thể thấy đây là một HTTP request hợp lệ.
- Lỗi chỉ biểu hiện khi dữ liệu đã đi sâu tới code C và vượt capacity nội bộ.
- Phạm vi bài lab chỉ là:
  - Quan sát crash có kiểm soát.
  - Xác định nguyên nhân.
  - Không viết shellcode.
  - Không xây ROP chain.
  - Không chiếm quyền hệ thống.

## Câu chuyển sang slide tiếp theo

- Vì lỗi nằm ở thao tác copy trong mã nguồn C, bước đầu tiên phải là sửa source; các cơ chế hardening chỉ được đặt sau đó.

## Giải thích thuật ngữ và từ chuyên ngành

- **Buffer Overflow:** Lỗi ghi dữ liệu vượt quá vùng nhớ đã cấp cho buffer.
- **HTTP:** Giao thức truyền request và response giữa client với server.
- **POST:** HTTP method thường dùng để gửi dữ liệu hoặc tạo thay đổi trạng thái.
- **`/submit`:** Endpoint nhận dữ liệu trong kịch bản lab.
- **Flask:** Web framework Python dùng để xây dựng ứng dụng server.
- **Request limit:** Giới hạn kích thước request mà server chấp nhận.
- **Native code:** Mã được biên dịch trực tiếp thành mã máy, ví dụ C hoặc C++.
- **`subprocess`:** Cơ chế cho phép chương trình Python chạy một process bên ngoài.
- **`shell=False`:** Chạy process trực tiếp mà không thông qua command shell, giúp tránh một số rủi ro shell injection.
- **C:** Ngôn ngữ lập trình cho phép quản lý bộ nhớ ở mức thấp.
- **`strcpy`:** Hàm copy chuỗi C nhưng không nhận kích thước buffer đích.
- **`name[32]`:** Mảng ký tự gồm 32 byte.
- **Capacity:** Dung lượng tối đa của vùng chứa.
- **Byte:** Đơn vị dữ liệu gồm 8 bit.
- **Null terminator:** Byte `\0` đánh dấu kết thúc chuỗi C.
- **Stack:** Vùng nhớ dùng cho biến local, thông tin gọi hàm và địa chỉ trở về.
- **Stack grows down:** Trên nhiều kiến trúc, stack phát triển từ địa chỉ cao xuống địa chỉ thấp.
- **Stack Canary:** Giá trị kiểm tra đặt gần dữ liệu điều khiển để phát hiện ghi tràn.
- **Saved frame:** Thông tin lưu lại để phục hồi stack frame của hàm gọi.
- **Return address:** Địa chỉ lệnh mà chương trình quay lại sau khi hàm kết thúc.
- **Control data:** Dữ liệu ảnh hưởng trực tiếp đến luồng điều khiển chương trình.
- **Undefined behavior:** Hành vi không được ngôn ngữ đảm bảo, có thể dẫn đến crash hoặc kết quả không dự đoán được.
- **Crash:** Chương trình dừng bất thường.
- **Shellcode:** Mã máy nhỏ thường dùng làm payload để thực hiện hành động sau khi khai thác lỗi bộ nhớ.
- **ROP — Return-Oriented Programming:** Kỹ thuật ghép các đoạn mã có sẵn để điều khiển luồng thực thi.
- **Firewall:** Thành phần lọc hoặc kiểm soát lưu lượng mạng theo rule.
- **Backend:** Thành phần phía server xử lý logic và dữ liệu.

---

# Slide 06 — Source fix trước, hardening sau

## Mục tiêu của slide

- Trình bày hai cách vá Buffer Overflow.
- Giải thích các lớp hardening.
- Nhấn mạnh vai trò của bằng chứng GDB hoặc ASan.

## Kịch bản trình bày

- Phiên bản vulnerable có hai dòng chính:
  - Khai báo `char name[32]`.
  - Gọi `strcpy(name, input)`.
- Vấn đề là `strcpy` không biết capacity của `name`.
- Cách sửa thứ nhất là kiểm tra độ dài:
  - Dùng `strnlen(input, 33)` để phát hiện chuỗi dài hơn giới hạn.
  - Nếu độ dài lớn hơn 31 byte thì từ chối trước khi copy.
- Cách sửa thứ hai là ghi có giới hạn:
  - Dùng `snprintf(name, 32, "%s", input)`.
  - Kiểm tra giá trị trả về.
  - Nếu số ký tự cần ghi lớn hơn hoặc bằng 32 thì từ chối.
- Invariant của chương trình là:
  - Tối đa 31 byte dữ liệu.
  - Byte thứ 32 dành cho null terminator.
- Sau source fix, có thể bổ sung các lớp hardening:
  - Ở HTTP: giới hạn request quá lớn.
  - Ở compiler: stack protector, FORTIFY và PIE.
  - Ở loader: RELRO và ASLR.
  - Ở hệ điều hành: NX hoặc DEP.
  - Ở kiến trúc dài hạn: ưu tiên ngôn ngữ memory-safe khi phù hợp.
- Buffer Overflow khác Injection:
  - Overflow phá vỡ ranh giới vùng nhớ.
  - Injection thay đổi cú pháp hoặc ý nghĩa của lệnh hay truy vấn.
- Firewall không đủ vì request có thể hợp lệ về mạng nhưng vẫn quá lớn so với buffer nội bộ.
- Không được suy kết luận crash chỉ từ việc nhìn source.
- Mốc crash, vùng overwrite và độ dài gây lỗi phải được quan sát bằng bằng chứng thật:
  - GDB.
  - AddressSanitizer.
  - Crash log.
- Hardening giúp giảm khả năng khai thác, nhưng không sửa `strcpy`.
- Thứ tự đúng là:
  - Sửa source.
  - Bật hardening.
  - Kiểm thử lại cùng input.

## Câu chuyển sang slide tiếp theo

- Sang Lab03, vùng bị phá không phải bộ nhớ mà là chính sách nghiệp vụ: client gửi tham số, nhưng server phải giữ quyền quyết định.

## Giải thích thuật ngữ và từ chuyên ngành

- **Source fix:** Sửa lỗi trực tiếp trong mã nguồn gây ra lỗ hổng.
- **Hardening:** Tăng cường bảo vệ để giảm khả năng khai thác hoặc giảm hậu quả.
- **`strnlen`:** Hàm đo độ dài chuỗi nhưng dừng ở giới hạn chỉ định.
- **`snprintf`:** Hàm ghi chuỗi có giới hạn kích thước buffer.
- **Bounded write:** Thao tác ghi có ràng buộc số byte tối đa.
- **Reject:** Từ chối input hoặc request trước khi thực hiện thao tác nguy hiểm.
- **Invariant:** Điều kiện luôn phải đúng trong suốt quá trình xử lý.
- **Stack protector:** Cơ chế compiler chèn canary và kiểm tra trước khi hàm trả về.
- **FORTIFY:** Nhóm kiểm tra bổ sung của thư viện/compiler để phát hiện một số thao tác bộ nhớ không an toàn.
- **PIE — Position Independent Executable:** Kiểu binary có thể được nạp ở địa chỉ khác nhau.
- **Loader:** Thành phần hệ thống nạp chương trình và thư viện vào bộ nhớ.
- **RELRO — Relocation Read-Only:** Cơ chế bảo vệ một số vùng relocation khỏi bị ghi sau khi nạp.
- **ASLR — Address Space Layout Randomization:** Ngẫu nhiên hóa vị trí các vùng nhớ.
- **OS — Operating System:** Hệ điều hành.
- **NX — No-eXecute:** Đánh dấu vùng dữ liệu là không được phép thực thi mã.
- **DEP — Data Execution Prevention:** Cơ chế ngăn thực thi mã ở vùng dữ liệu, tương đương mục tiêu với NX.
- **Memory-safe language:** Ngôn ngữ hoặc runtime giảm mạnh các lỗi truy cập bộ nhớ sai, ví dụ Rust, Java hoặc C#.
- **Injection:** Nhóm lỗi làm input được diễn giải như một phần của lệnh hoặc truy vấn.
- **GDB — GNU Debugger:** Trình gỡ lỗi dùng để quan sát stack, register và điểm crash.
- **ASan — AddressSanitizer:** Công cụ runtime phát hiện lỗi truy cập bộ nhớ như buffer overflow.
- **Overwrite:** Ghi đè lên dữ liệu đã tồn tại.
- **Evidence:** Bằng chứng quan sát được, như log, trace, screenshot hoặc response thực tế.

---

# Slide 07 — Client gửi tham số, server giữ quyền quyết định

## Mục tiêu của slide

- Giới thiệu ba kịch bản Parameter Tampering.
- Phân biệt validation với authorization.
- Xác định nguồn dữ liệu authoritative.

## Kịch bản trình bày

- Parameter Tampering là việc người dùng sửa tham số của request để thay đổi kết quả xử lý.
- Kịch bản thứ nhất là sửa giá checkout:
  - Client gửi `price=1`.
  - Dù giá nằm trong hidden field, người dùng vẫn có thể sửa request.
  - Server không được dùng giá do client gửi làm giá trị quyết định.
- Nguồn giá authoritative phải là database hiện tại:
  - Client chỉ gửi `product_id` và `quantity`.
  - Server đọc `products.price_vnd`.
  - Server tự tính lại tổng tiền.
- Kịch bản thứ hai là IDOR hóa đơn:
  - Người dùng đổi `id=1001` thành `id=1002`.
  - ID hợp lệ về kiểu dữ liệu nhưng có thể trỏ tới hóa đơn của người khác.
  - Server phải kiểm tra owner hoặc quyền admin trước khi trả dữ liệu.
- Kịch bản thứ ba là role tampering:
  - Client thêm hoặc sửa `role=admin`.
  - Nếu server bind toàn bộ field, role có thể bị cập nhật trái phép.
  - Đây là một dạng mass assignment.
- Field policy phải dùng allowlist:
  - Ví dụ chỉ cho phép cập nhật email.
  - Không nhận role, `user_id`, `balance` hoặc field nhạy cảm từ client.
- Identity phải lấy từ session đã xác thực.
- Điểm quan trọng:
  - Validation kiểu và range chỉ cho biết dữ liệu có đúng định dạng.
  - Authorization mới trả lời người dùng có quyền thực hiện hành động đó không.
- Chính sách nghiệp vụ phải thuộc về server.

## Câu chuyển sang slide tiếp theo

- Ba kịch bản có dữ liệu bị sửa khác nhau, nhưng đều cần một nguồn authoritative phía server để đưa ra quyết định.

## Giải thích thuật ngữ và từ chuyên ngành

- **Parameter Tampering:** Thao túng giá trị tham số trong URL, form, request body, cookie hoặc storage.
- **Checkout:** Quy trình xác nhận và tạo đơn hàng.
- **`price`:** Tham số giá sản phẩm.
- **Hidden field:** Trường form không hiển thị trực tiếp trên UI nhưng vẫn được gửi từ client.
- **Invoice:** Hóa đơn hoặc đối tượng ghi nhận giao dịch.
- **ID:** Mã định danh của một đối tượng.
- **Object:** Tài nguyên cụ thể như hóa đơn, tài khoản hoặc đơn hàng.
- **Profile:** Dữ liệu hồ sơ người dùng.
- **Role:** Vai trò quyền hạn, ví dụ user hoặc admin.
- **Mass assignment:** Cập nhật hàng loạt field từ request vào model mà không giới hạn field nhạy cảm.
- **Trust boundary:** Ranh giới giữa dữ liệu client kiểm soát và quyết định server phải xác minh.
- **Authoritative source:** Nguồn được coi là chính thức để đưa ra quyết định.
- **Database hiện tại:** Dữ liệu mới nhất do server quản lý.
- **Object policy:** Chính sách xác định ai được phép thao tác trên một object.
- **Owner:** Người sở hữu tài nguyên.
- **Admin:** Vai trò quản trị có quyền rộng hơn.
- **Field policy:** Chính sách xác định field nào được phép đọc hoặc cập nhật.
- **Allowlist:** Chỉ cho phép danh sách field đã xác định trước.
- **Identity:** Danh tính người dùng đã được xác thực.
- **Session:** Trạng thái đăng nhập do server quản lý hoặc xác minh.
- **`user_id`:** Mã định danh người dùng.
- **`balance`:** Số dư tài khoản.
- **Validation kiểu/range:** Kiểm tra kiểu dữ liệu và miền giá trị.
- **Authorization:** Kiểm tra quyền thực hiện hành động hoặc truy cập tài nguyên.
- **Business policy:** Quy tắc nghiệp vụ, ví dụ giá phải lấy từ database và hóa đơn chỉ trả cho chủ sở hữu.

---

# Slide 08 — Ba tampering, ba nguồn authoritative

## Mục tiêu của slide

- Tổng hợp cách vá ba kịch bản Parameter Tampering.
- Giải thích IDOR, Broken Access Control và khác biệt với SQL Injection.

## Kịch bản trình bày

- Bảng trên slide gồm năm cột:
  - Kịch bản.
  - Tham số client sửa.
  - Kiểm tra bị thiếu.
  - Nguồn authoritative.
  - Kết quả secure.
- Với giá checkout:
  - Client sửa `price`.
  - Kiểm tra bị thiếu là đối chiếu giá phía server.
  - Nguồn authoritative là sản phẩm trong database.
  - Kết quả secure là server tính lại tổng tiền đúng.
- Với IDOR invoice:
  - Client sửa `id`.
  - Kiểm tra bị thiếu là object-level authorization.
  - Nguồn authoritative là session kết hợp owner của invoice.
  - Nếu người dùng không sở hữu tài nguyên thì server trả 403.
- Với role tampering:
  - Client sửa `role`.
  - Kiểm tra bị thiếu là field allowlist.
  - Nguồn authoritative là session và role hiện tại trong database.
  - Kết quả secure là giữ role hiện tại, không nhận role mới từ client.
- Hidden field không phải cơ chế bảo mật:
  - Nó chỉ ẩn khỏi giao diện.
  - Người dùng vẫn có thể sửa qua DevTools hoặc proxy.
- IDOR thuộc nhóm Broken Access Control:
  - Lỗi không nằm ở việc ID có hợp lệ hay không.
  - Lỗi nằm ở việc server không xác minh quyền trên object cụ thể.
- Parameter Tampering khác SQL Injection:
  - Tampering thay đổi giá trị hoặc policy mà server tin.
  - SQL Injection làm thay đổi cấu trúc truy vấn.
- Kết luận của lab:
  - Identity từ session.
  - Giá từ database.
  - Owner từ object.
  - Role từ server.
  - Không lấy các quyết định này từ client.

## Câu chuyển sang slide tiếp theo

- Lab04 tiếp tục cho thấy session chỉ chứng minh danh tính, nhưng chưa chứng minh người dùng thật sự có ý định thực hiện một thao tác thay đổi dữ liệu.

## Giải thích thuật ngữ và từ chuyên ngành

- **Scenario:** Kịch bản kiểm thử cụ thể.
- **Secure result:** Kết quả mong đợi sau khi áp dụng kiểm tra an toàn.
- **Object-level authorization:** Kiểm tra quyền trên từng đối tượng cụ thể.
- **Authz:** Viết tắt của authorization.
- **HTTP 403 Forbidden:** Server hiểu request nhưng từ chối vì người dùng không có quyền.
- **IDOR — Insecure Direct Object Reference:** Lỗi cho phép đổi ID để truy cập object không thuộc quyền.
- **Broken Access Control:** Nhóm lỗ hổng kiểm soát truy cập, khi người dùng thực hiện hành động ngoài quyền được cấp.
- **Access control:** Cơ chế xác định ai được phép làm gì trên tài nguyên nào.
- **SQLi — SQL Injection:** Lỗi làm dữ liệu người dùng được SQL parser hiểu như cú pháp truy vấn.
- **Policy:** Quy tắc quyết định hành động có được phép hay không.
- **Field allowlist:** Danh sách field được phép cập nhật.
- **Owner check:** Kiểm tra người yêu cầu có phải chủ sở hữu tài nguyên.
- **Session identity:** Danh tính lấy từ session, không lấy từ tham số `user_id` do client gửi.
- **Authoritative:** Có thẩm quyền làm nguồn sự thật cho quyết định.
- **DevTools:** Bộ công cụ phát triển tích hợp trong browser.
- **Proxy:** Công cụ trung gian để quan sát hoặc thay đổi HTTP request trong môi trường lab.

---

# Slide 09 — Session chứng minh danh tính, không chứng minh ý định

## Mục tiêu của slide

- Giải thích cơ chế CSRF.
- Phân biệt credential với intent.
- Làm rõ vai trò của SOP và CORS.

## Kịch bản trình bày

- CSRF xảy ra khi trình duyệt của nạn nhân gửi một request ngoài ý muốn đến ứng dụng mà nạn nhân đang đăng nhập.
- Trong sơ đồ có ba thành phần:
  - Trang giả lập attacker chạy ở một origin local.
  - Victim browser đã có session cookie.
  - Target application có endpoint thay đổi trạng thái.
- Bước một:
  - Nạn nhân mở trang giả lập.
  - Trang đó chứa form gửi request đến target.
- Bước hai:
  - Browser gửi `POST change-email`.
  - Cookie của target được browser tự động gắn vào request.
- Bước ba:
  - Request đến từ origin khác.
  - Request không có CSRF token.
- Bước bốn:
  - Phiên bản vulnerable chỉ kiểm tra session.
  - Server cho phép cập nhật email.
- Session cookie trả lời câu hỏi:
  - Request thuộc phiên đăng nhập của ai?
- Nhưng session không trả lời:
  - Người dùng có chủ động muốn đổi email hay không?
- Attacker không cần biết mật khẩu của nạn nhân.
- Attacker cũng không nhất thiết phải đọc được response.
- Same-Origin Policy thường ngăn script của attacker đọc response từ origin khác.
- Tuy nhiên SOP không luôn ngăn browser gửi một form cross-origin.
- Vì thay đổi trạng thái đã xảy ra, việc không đọc được response không ngăn được CSRF.
- CORS không phải bản vá CSRF:
  - CORS chủ yếu kiểm soát việc script cross-origin đọc response.
  - CSRF lợi dụng credential tự động gửi và endpoint thiếu kiểm tra intent.

## Câu chuyển sang slide tiếp theo

- Vì vậy bản vá phải từ chối request trước khi mutation nếu thiếu token hoặc origin không hợp lệ.

## Giải thích thuật ngữ và từ chuyên ngành

- **CSRF — Cross-Site Request Forgery:** Tấn công ép browser của nạn nhân gửi request ngoài ý muốn đến ứng dụng đã đăng nhập.
- **Session:** Trạng thái liên kết request với người dùng đã đăng nhập.
- **Session cookie:** Cookie mang mã phiên hoặc thông tin cần thiết để server nhận diện phiên.
- **Credential:** Bằng chứng danh tính, ví dụ cookie phiên hoặc token đăng nhập.
- **Intent:** Ý định chủ động của người dùng đối với một thao tác.
- **Attacker page:** Trang do bên tấn công kiểm soát, trong lab được chạy local.
- **Victim browser:** Trình duyệt của người dùng đang có phiên đăng nhập hợp lệ.
- **Target application:** Ứng dụng đích mà request được gửi tới.
- **State-changing endpoint:** Endpoint làm thay đổi dữ liệu hoặc trạng thái, ví dụ đổi email.
- **Cross-origin:** Giữa hai origin khác nhau.
- **Origin:** Tổ hợp scheme, host và port, ví dụ `http://127.0.0.1:5004`.
- **POST request:** Request dùng HTTP method POST.
- **CSRF token:** Giá trị ngẫu nhiên liên kết với phiên, dùng để chứng minh request đến từ form hợp lệ.
- **Vulnerable:** Phiên bản thiếu kiểm tra chống CSRF.
- **SOP — Same-Origin Policy:** Chính sách trình duyệt hạn chế một origin đọc dữ liệu của origin khác.
- **CORS — Cross-Origin Resource Sharing:** Cơ chế server cho phép một số origin đọc response cross-origin.
- **Response:** Dữ liệu server trả lại sau request.
- **Mutation:** Thao tác làm thay đổi trạng thái hoặc dữ liệu.
- **Credential khác intent:** Có thông tin đăng nhập không đồng nghĩa request phản ánh ý muốn thật của người dùng.

---

# Slide 10 — Deny trước mutation

## Mục tiêu của slide

- Trình bày luồng kiểm tra CSRF an toàn.
- Giải thích các lớp token, Origin/Referer, SameSite và re-authentication.

## Kịch bản trình bày

- Nguyên tắc của slide là **deny trước mutation**:
  - Mọi kiểm tra phải hoàn tất trước khi cập nhật dữ liệu.
- Luồng an toàn gồm các gate:
  - Xác định session.
  - Kiểm tra Origin hoặc Referer theo exact allowlist.
  - Kiểm tra CSRF token duy nhất theo session.
  - Chỉ nhận method POST và validate input.
  - Chỉ thực hiện mutation sau khi toàn bộ gate đều hợp lệ.
- Ở request vulnerable:
  - Cookie có vì browser tự gửi.
  - Token bị thiếu.
  - Origin khác với target.
  - Server vẫn allow chỉ vì session hợp lệ.
  - Kết quả là email bị đổi.
- Ở secure policy:
  - Token phải đủ ngẫu nhiên.
  - Token được so sánh phía server.
  - Origin phải exact match.
  - SameSite hỗ trợ giảm một số trường hợp cookie cross-site.
  - Hành động nhạy cảm có thể yêu cầu re-authentication.
- Nếu sai bất kỳ gate nào:
  - Server trả 403.
  - Trạng thái phải giữ nguyên.
- Không nên dùng GET cho thao tác thay đổi trạng thái.
- GET dễ bị kích hoạt ngoài ý muốn qua link, ảnh, prefetch hoặc cache.
- CAPTCHA chỉ là lớp hỗ trợ:
  - Không thay thế token.
  - Không thay thế Origin/Referer.
  - Không phải bản vá nguyên nhân gốc.

## Câu chuyển sang slide tiếp theo

- Trong Lab05, thay vì lợi dụng cookie tự gửi, attacker làm input được SQL parser hiểu như một phần của cú pháp truy vấn.

## Giải thích thuật ngữ và từ chuyên ngành

- **Deny:** Từ chối request.
- **Deny before mutation:** Từ chối trước khi bất kỳ thay đổi dữ liệu nào xảy ra.
- **Gate:** Một điều kiện kiểm tra bắt buộc trong luồng xử lý.
- **Origin header:** Header cho biết origin đã tạo request.
- **Referer header:** Header thường cho biết URL trang trước đó tạo request.
- **Exact allowlist:** Chỉ chấp nhận chính xác các origin đã cấu hình.
- **Unique per session:** Mỗi phiên có token riêng.
- **Random token:** Token được sinh bằng nguồn ngẫu nhiên đủ mạnh.
- **Compare server-side:** Server tự so sánh token nhận được với token của phiên.
- **POST-only:** Endpoint thay đổi trạng thái chỉ chấp nhận POST hoặc method phù hợp, không dùng GET.
- **Input validation:** Kiểm tra dữ liệu trước khi cập nhật.
- **SameSite cookie:** Cờ hạn chế cookie trong một số request cross-site.
- **Re-authentication:** Yêu cầu người dùng xác thực lại trước hành động nhạy cảm.
- **Sensitive action:** Hành động có rủi ro cao như đổi mật khẩu, chuyển tiền hoặc đổi email quan trọng.
- **HTTP 403:** Mã phản hồi từ chối quyền thực hiện request.
- **State:** Trạng thái dữ liệu hiện tại.
- **CAPTCHA:** Cơ chế phân biệt người dùng với tự động hóa, nhưng không chứng minh nguồn và intent của request.
- **Mutation:** Thay đổi dữ liệu, ví dụ cập nhật email trong database.
- **Prefetch:** Trình duyệt tải trước tài nguyên, có thể vô tình kích hoạt GET nếu thiết kế endpoint sai.
- **Cache:** Cơ chế lưu tạm response hoặc tài nguyên.

---

# Slide 11 — Nối chuỗi trộn code và dữ liệu

## Mục tiêu của slide

- Giải thích nguyên nhân SQL Injection.
- Minh họa authentication bypass và expanded search.

## Kịch bản trình bày

- SQL Injection xảy ra khi ứng dụng nối input người dùng trực tiếp vào chuỗi SQL.
- Luồng lỗi gồm:
  - Nhận input.
  - Nối chuỗi.
  - Gửi câu lệnh cho SQL parser.
  - Parser đọc một phần input như syntax.
  - Logic của mệnh đề WHERE bị thay đổi.
  - Kết quả xác thực hoặc tập bản ghi bị thay đổi.
- Ví dụ authentication bypass:
  - Input username chứa phần comment SQL.
  - Sau khi nối chuỗi, phần kiểm tra password nằm sau ký hiệu comment.
  - Điều kiện password không còn tham gia vào logic truy vấn.
  - Ứng dụng có thể xác thực sai mà không biết mật khẩu.
- Ví dụ expanded search:
  - Input làm xuất hiện điều kiện `OR 1=1`.
  - Điều kiện này luôn đúng.
  - Query trả nhiều dòng hơn baseline dự kiến.
- Điểm quan trọng:
  - Lỗi không phải do dấu nháy đơn tự nó nguy hiểm.
  - Lỗi do ứng dụng trộn code và data trước khi SQL parser xử lý.
- Trong phạm vi lab:
  - Chỉ dùng SQLite local.
  - Chỉ thực hiện SELECT.
  - Không dùng UNION.
  - Không thực hiện blind injection.
  - Không dùng stacked query.
  - Không sửa hoặc phá dữ liệu.
- Phần phát hiện lỗi có thể bắt đầu bằng:
  - Input bình thường.
  - Dấu nháy đơn.
  - Quan sát lỗi SQL hoặc hành vi bất thường.
- Mục tiêu là chứng minh thay đổi logic, không mở rộng sang khai thác hệ thống thật.

## Câu chuyển sang slide tiếp theo

- Bản vá chính là tách cấu trúc SQL khỏi dữ liệu bằng prepared statement và parameter binding.

## Giải thích thuật ngữ và từ chuyên ngành

- **SQL Injection — SQLi:** Lỗ hổng khi input được SQL parser diễn giải như cú pháp truy vấn.
- **Concatenation:** Nối nhiều chuỗi thành một chuỗi lớn.
- **SQL parser:** Thành phần phân tích câu SQL thành cấu trúc mà database thực thi.
- **Syntax:** Cú pháp của ngôn ngữ SQL.
- **Logic:** Điều kiện quyết định query trả dữ liệu nào.
- **WHERE:** Mệnh đề SQL lọc các bản ghi.
- **Authentication bypass:** Vượt qua kiểm tra đăng nhập mà không có credential đúng.
- **`password_digest`:** Giá trị đại diện cho mật khẩu đã được băm.
- **SQL comment:** Cú pháp làm phần còn lại của dòng không được parser xử lý như điều kiện.
- **Expanded search:** Kết quả tìm kiếm được mở rộng ngoài phạm vi dự kiến.
- **LIKE:** Toán tử SQL tìm chuỗi theo mẫu.
- **`OR 1=1`:** Điều kiện logic luôn đúng.
- **Baseline:** Kết quả chuẩn khi dùng input bình thường.
- **Result set:** Tập các hàng query trả về.
- **SQLite:** Database nhúng dùng trong lab local.
- **SELECT-only:** Chỉ chạy truy vấn đọc dữ liệu.
- **UNION-based SQLi:** Kỹ thuật ghép kết quả từ truy vấn khác bằng `UNION`.
- **Blind SQLi:** SQL Injection không thấy trực tiếp dữ liệu hoặc lỗi, phải suy luận qua phản hồi.
- **Stacked query:** Gửi nhiều câu SQL liên tiếp trong một input.
- **Data extraction:** Lấy dữ liệu ngoài phạm vi ứng dụng dự kiến.
- **Error-based detection:** Phát hiện SQLi thông qua lỗi SQL hoặc hành vi response bất thường.
- **Query:** Câu lệnh truy vấn database.
- **Rows:** Các dòng dữ liệu database trả về.

---

# Slide 12 — Parameter binding khóa cấu trúc SQL

## Mục tiêu của slide

- Trình bày bản vá SQL Injection.
- Phân biệt parameterized query với nối chuỗi.
- Giải thích các lớp phòng thủ hỗ trợ.

## Kịch bản trình bày

- Ở cách nối chuỗi:
  - Ứng dụng ghép `username` trực tiếp vào SQL.
  - Input có thể trở thành syntax.
- Ở cách bind tham số:
  - Câu SQL dùng placeholder `?`.
  - Giá trị username được truyền riêng cho driver.
  - Cấu trúc SQL được giữ cố định.
  - Input luôn được xử lý như data.
- Đây là primary fix của SQL Injection:
  - Prepared statement.
  - Parameterized query.
- Password phải được lưu bằng hàm băm phù hợp:
  - PBKDF2.
  - bcrypt.
  - Argon2.
- Tuy nhiên password hashing không thay thế parameter binding:
  - Hash bảo vệ mật khẩu lưu trữ.
  - Parameter binding bảo vệ cấu trúc query.
- Thông báo lỗi cho người dùng nên là generic:
  - Không lộ schema.
  - Không lộ nội dung query.
  - Chi tiết kỹ thuật được ghi vào log phía server.
- Database account nên tuân theo least privilege.
- Có thể giới hạn số lượng kết quả để giảm ảnh hưởng.
- Validation, logging và WAF là lớp hỗ trợ.
- Escaping thủ công dễ sai:
  - Phụ thuộc dialect SQL.
  - Phụ thuộc vị trí dữ liệu.
- ORM không tự động an toàn trong mọi trường hợp:
  - Raw SQL.
  - String interpolation.
  - Nối chuỗi trong ORM vẫn có thể tái tạo lỗi.
- Retest phải dùng cùng input:
  - Ở phiên bản secure, input được bind như literal.
  - Logic query không thay đổi.
- WAF không thay thế sửa code.

## Câu chuyển sang slide tiếp theo

- Lab06 quay lại một dạng dữ liệu client khác: cookie do server tạo nhưng sau đó được lưu, sửa và gửi lại từ phía client.

## Giải thích thuật ngữ và từ chuyên ngành

- **Parameter binding:** Gắn giá trị input vào placeholder của query thay vì nối vào chuỗi SQL.
- **Prepared statement:** Câu SQL có cấu trúc được chuẩn bị riêng, dữ liệu truyền dưới dạng tham số.
- **Parameterized query:** Query dùng tham số do database driver xử lý.
- **Placeholder:** Vị trí đại diện cho giá trị, ví dụ `?`.
- **Primary fix:** Biện pháp sửa chính loại bỏ nguyên nhân gốc.
- **PBKDF2:** Hàm dẫn xuất khóa dựa trên mật khẩu, dùng nhiều vòng lặp để làm chậm dò mật khẩu.
- **bcrypt:** Thuật toán băm mật khẩu có cost điều chỉnh được.
- **Argon2:** Thuật toán băm mật khẩu hiện đại, có khả năng chống tấn công dùng phần cứng tốt hơn khi cấu hình đúng.
- **Password hashing:** Biến mật khẩu thành giá trị một chiều để lưu trữ an toàn hơn.
- **Generic error message:** Thông báo lỗi chung, không tiết lộ chi tiết nội bộ.
- **Schema:** Cấu trúc database gồm bảng, cột và quan hệ.
- **Least privilege:** Tài khoản chỉ có quyền tối thiểu cần cho nhiệm vụ.
- **Result limit:** Giới hạn số dòng trả về.
- **Logging:** Ghi sự kiện để theo dõi và điều tra.
- **WAF — Web Application Firewall:** Lớp lọc request web để phát hiện hoặc chặn mẫu tấn công.
- **Data-access layer:** Lớp mã nguồn chịu trách nhiệm truy cập database.
- **Query construction:** Quá trình xây dựng câu SQL.
- **Escaping:** Thêm ký tự hoặc biến đổi input để giảm khả năng được hiểu như cú pháp.
- **ORM — Object-Relational Mapping:** Lớp ánh xạ object trong mã nguồn với bảng database.
- **Raw SQL:** Câu SQL viết trực tiếp thay vì dùng API abstraction.
- **String interpolation:** Chèn giá trị vào chuỗi bằng cú pháp định dạng.
- **Literal:** Giá trị dữ liệu được parser coi là dữ liệu, không phải cú pháp.
- **Retest:** Kiểm thử lại sau bản vá bằng cùng điều kiện hoặc input.
- **Database driver:** Thư viện trung gian gửi query và tham số đến database.

---

# Slide 13 — Cookie quay lại server như dữ liệu client

## Mục tiêu của slide

- Giải thích Cookie Poisoning.
- Chứng minh Base64 không tạo ra tính toàn vẹn.
- Nhấn mạnh cookie flags không thay authorization.

## Kịch bản trình bày

- Cookie thường được server tạo, nhưng sau đó được lưu ở client.
- Khi request tiếp theo được gửi:
  - Cookie quay lại server từ phía client.
  - Vì vậy server không được mặc định tin nội dung cookie.
- Luồng plain cookie:
  - Server đặt `role=user`.
  - Browser lưu Name, Value và các flags.
  - Người dùng sửa thành `role=admin`.
  - Server tin role và đưa ra quyết định sai.
- Đây là Cookie Poisoning:
  - Nội dung cookie bị sửa để làm thay đổi hành vi ứng dụng.
- Base64 không giải quyết vấn đề:
  - Người dùng decode Base64.
  - Đọc được JSON.
  - Sửa role.
  - Encode lại.
  - Gửi cookie mới về server.
- Base64 không cần secret.
- Base64 chỉ thay đổi cách biểu diễn bytes.
- Nếu không có chữ ký hoặc MAC:
  - Server không phát hiện nội dung đã bị sửa.
  - Cookie không có integrity.
- Cookie flags như HttpOnly, Secure và SameSite vẫn cần thiết.
- Tuy nhiên các flags này bảo vệ những rủi ro khác:
  - Không biến role phía client thành nguồn authorization hợp lệ.
- Quyền truy cập phải được server quyết định dựa trên dữ liệu phía server.

## Câu chuyển sang slide tiếp theo

- Để chọn cách lưu state phù hợp, cần phân biệt khả năng đọc, phát hiện sửa, bảo mật nội dung và khả năng thu hồi.

## Giải thích thuật ngữ và từ chuyên ngành

- **Cookie:** Dữ liệu nhỏ browser lưu và gửi kèm các request phù hợp.
- **Cookie Poisoning:** Sửa nội dung cookie để làm server xử lý sai.
- **Name:** Tên cookie.
- **Value:** Giá trị cookie.
- **Cookie flags:** Các thuộc tính kiểm soát hành vi cookie.
- **`role=user`:** Ví dụ role người dùng thường.
- **`role=admin`:** Ví dụ role quản trị.
- **Client-controlled:** Dữ liệu mà người dùng có khả năng quan sát hoặc thay đổi.
- **Base64:** Cách mã hóa biểu diễn bytes thành chuỗi ký tự, không phải mã hóa bảo mật.
- **Decode:** Chuyển Base64 trở lại bytes hoặc chuỗi gốc.
- **JSON — JavaScript Object Notation:** Định dạng dữ liệu dạng cặp key-value.
- **Encode:** Chuyển dữ liệu sang một biểu diễn khác.
- **Secret:** Giá trị bí mật dùng trong ký hoặc mã hóa.
- **Bytes:** Dữ liệu nhị phân.
- **Integrity:** Khả năng phát hiện dữ liệu đã bị thay đổi.
- **Authorization:** Quyết định quyền truy cập hoặc hành động.
- **Server decision:** Quyết định do server thực hiện sau khi kiểm tra nguồn dữ liệu.
- **Plain cookie:** Cookie chứa giá trị đọc được trực tiếp, không ký hoặc mã hóa.
- **Cookie flags không thay authorization:** Dù cookie được bảo vệ khi truyền hoặc khỏi JavaScript, role trong cookie vẫn không nên là nguồn quyền authoritative.

---

# Slide 14 — Chọn state model theo thuộc tính cần bảo vệ

## Mục tiêu của slide

- So sánh plain, Base64, signed, encrypted cookie và server session.
- Phân biệt confidentiality, integrity và revocation.
- Phân biệt Cookie Poisoning với Session Hijacking.

## Kịch bản trình bày

- Không có một state model phù hợp cho mọi mục tiêu.
- Cần xác định thuộc tính cần bảo vệ:
  - Client có đọc được không?
  - Server có phát hiện sửa đổi không?
  - Nội dung có được giữ bí mật không?
  - Có thể revoke ngay không?
  - Role authoritative nằm ở đâu?
- Với plain cookie:
  - Client đọc được.
  - Không phát hiện sửa.
  - Không có confidentiality.
  - Khó revoke tức thời.
  - Không nên dùng role phía client.
- Với Base64:
  - Client vẫn đọc được sau khi decode.
  - Không phát hiện sửa.
  - Không có confidentiality.
  - Chỉ thay đổi cách biểu diễn.
- Với signed cookie:
  - Payload vẫn có thể đọc được.
  - Chữ ký giúp server phát hiện sửa đổi.
  - Có integrity và authenticity nếu triển khai đúng.
  - Khả năng revoke vẫn hạn chế nếu cookie tự chứa state.
- Với encrypted cookie:
  - Client không đọc được nội dung.
  - Có confidentiality.
  - Chỉ có integrity khi dùng AEAD hoặc encryption kèm MAC.
  - Không nên mang role động làm nguồn authoritative.
- Với server session:
  - Browser chỉ giữ opaque ID.
  - Server lookup session.
  - Trạng thái và role nằm ở server hoặc database.
  - Có thể revoke phiên tức thời.
- Session lifecycle nên gồm:
  - Sinh ID ngẫu nhiên.
  - Lưu hash hoặc mapping phía server.
  - Kiểm tra active và expiry.
  - Rotate khi login hoặc thay đổi quyền.
  - Revoke khi logout.
- Authorization phải kiểm tra policy và role hiện tại trên từng request.
- Cookie Poisoning khác Session Hijacking:
  - Poisoning là sửa state trong cookie.
  - Hijacking là lấy token hoặc session ID hợp lệ của người khác.
- Kết luận:
  - Base64 không phải encryption.
  - Signed không đồng nghĩa encrypted.
  - Encrypted không tự động có integrity nếu không dùng AEAD hoặc MAC.
  - Server session thường phù hợp hơn cho role và quyền động.

## Câu chuyển sang slide tiếp theo

- Sau khi đi qua sáu lab, chúng ta có thể tổng hợp lại bằng một câu hỏi chung: ứng dụng đã đặt niềm tin ở đâu?

## Giải thích thuật ngữ và từ chuyên ngành

- **State model:** Cách hệ thống lưu và quản lý trạng thái giữa các request.
- **Plain:** Dữ liệu không ký và không mã hóa.
- **Signed cookie:** Cookie có chữ ký số hoặc MAC để phát hiện sửa đổi.
- **Encrypted cookie:** Cookie có nội dung được mã hóa để bảo vệ bí mật.
- **Server session:** Trạng thái phiên được lưu phía server, client chỉ giữ mã định danh.
- **Confidentiality:** Tính bí mật, ngăn bên không được phép đọc nội dung.
- **Integrity:** Tính toàn vẹn, phát hiện dữ liệu bị sửa.
- **Authenticity:** Khả năng xác minh dữ liệu do bên có secret hợp lệ tạo ra.
- **Detect modification:** Phát hiện nội dung đã thay đổi.
- **Revoke:** Thu hồi hiệu lực của token hoặc session.
- **Immediate revocation:** Thu hồi có tác dụng ngay trên server.
- **Payload:** Phần dữ liệu chính bên trong cookie hoặc token.
- **AEAD — Authenticated Encryption with Associated Data:** Chế độ mã hóa cung cấp cả confidentiality và integrity.
- **MAC — Message Authentication Code:** Mã kiểm tra dùng secret để xác minh integrity và authenticity.
- **Opaque ID:** Mã định danh ngẫu nhiên không chứa ý nghĩa nghiệp vụ mà client có thể khai thác.
- **Lookup server:** Server tra cứu trạng thái dựa trên ID.
- **Hash lookup:** Lưu hoặc tra cứu dạng hash của session ID để giảm rủi ro lộ token gốc.
- **Active:** Trạng thái phiên còn hiệu lực.
- **Expiry:** Thời điểm phiên hết hạn.
- **Rotate session:** Đổi session ID mới, thường sau login hoặc thay đổi quyền.
- **Session lifecycle:** Toàn bộ vòng đời từ tạo, sử dụng, rotate, hết hạn đến revoke.
- **Current DB role:** Role mới nhất trong database.
- **Cookie Poisoning:** Sửa state trong cookie.
- **Session Hijacking:** Chiếm token hoặc session ID hợp lệ của người khác.
- **Dynamic role:** Role có thể thay đổi trong thời gian cookie còn hiệu lực.
- **Authorization source:** Nguồn dữ liệu server dùng để quyết định quyền.

---

# Slide 15 — Sáu lỗi khác tên, cùng một câu hỏi

## Mục tiêu của slide

- Chuyển từ phân tích từng lab sang tổng hợp.
- Nhấn mạnh câu hỏi trung tâm về vị trí đặt niềm tin.

## Kịch bản trình bày

- Đến đây, nhóm đã trình bày sáu lỗ hổng với sáu cơ chế khác nhau.
- XSS liên quan đến browser diễn giải dữ liệu thành markup hoặc script.
- Buffer Overflow liên quan đến dữ liệu vượt capacity vùng nhớ.
- Parameter Tampering liên quan đến server tin tham số nghiệp vụ từ client.
- CSRF liên quan đến server tin credential nhưng không kiểm tra intent.
- SQL Injection liên quan đến SQL parser nhận input như syntax.
- Cookie Poisoning liên quan đến server tin state hoặc role từ cookie.
- Dù tên gọi khác nhau, câu hỏi chung vẫn là:
  - Ứng dụng đã đặt niềm tin ở đâu?
  - Dữ liệu nào bị xem là đáng tin khi thực tế vẫn do client kiểm soát?
  - Quyết định nào đáng lẽ phải thuộc về server?
- Khi trả lời đúng các câu hỏi này, nhóm có thể tìm được root cause.
- Khi tìm đúng root cause, bản vá sẽ ngắn gọn và chính xác hơn.
- Slide tiếp theo tổng hợp điểm gãy và root fix của cả sáu lab.

## Câu chuyển sang slide tiếp theo

- Ma trận sau đặt sáu lỗi cạnh nhau để thấy rõ dữ liệu bị tin sai, điểm gãy và bản vá nguyên nhân gốc.

## Giải thích thuật ngữ và từ chuyên ngành

- **Tổng hợp:** Kết nối các kết quả riêng lẻ thành nguyên tắc chung.
- **Niềm tin:** Mức độ hệ thống chấp nhận dữ liệu hoặc quyết định mà không cần kiểm tra thêm.
- **Điểm gãy:** Vị trí ranh giới bảo mật bị phá vỡ.
- **Root cause:** Nguyên nhân gốc.
- **Root fix:** Bản vá trực tiếp tại nguyên nhân gốc.
- **Client-controlled data:** Dữ liệu phía client có thể sửa.
- **Server-side decision:** Quyết định được xác minh và thực hiện phía server.
- **Security invariant:** Điều kiện bảo mật phải luôn đúng.
- **Trust model:** Cách hệ thống xác định thành phần và dữ liệu nào được tin cậy.

---

# Slide 16 — Điểm gãy khác nhau; root fix luôn ở ranh giới

## Mục tiêu của slide

- So sánh root cause và root fix của sáu lab.
- Rút ra nguyên tắc “client không phải vùng an toàn”.

## Kịch bản trình bày

- Hàng thứ nhất là XSS:
  - Dữ liệu bị tin sai đến từ URL, form hoặc storage.
  - Điểm gãy là HTML hoặc DOM sink.
  - Root fix là encode hoặc sanitize đúng context và dùng safe DOM API.
- Hàng thứ hai là Buffer Overflow:
  - Input HTTP đi tới chương trình C.
  - Điểm gãy là capacity của buffer.
  - Root fix là length invariant và bounded write.
- Hàng thứ ba là Parameter Tampering:
  - Dữ liệu bị tin sai là giá, ID và role.
  - Điểm gãy là business policy hoặc access policy.
  - Root fix là database, session, object authorization và allowlist.
- Hàng thứ tư là CSRF:
  - Request có cookie nên server nghĩ là hợp lệ.
  - Điểm gãy là thiếu bằng chứng ý định trước mutation.
  - Root fix là token, Origin hoặc Referer và deny trước write.
- Hàng thứ năm là SQL Injection:
  - Input bị ghép vào query.
  - Điểm gãy là SQL parser.
  - Root fix là parameterized query và tách code khỏi data.
- Hàng thứ sáu là Cookie Poisoning:
  - Role hoặc state nằm ở client.
  - Điểm gãy là nguồn authorization.
  - Root fix là server session, current database role và revoke.
- Điểm chung:
  - Client không phải vùng an toàn.
  - Validation không phải lúc nào cũng đủ.
  - Bản vá phải gần nơi quyết định hoặc diễn giải nhất.
- Defense in depth vẫn quan trọng.
- Nhưng defense in depth không được dùng để thay root fix.

## Câu chuyển sang slide tiếp theo

- Để chứng minh các kết luận này, quy trình thực hành phải đặt bằng chứng trước kết luận và luôn retest phiên bản secure.

## Giải thích thuật ngữ và từ chuyên ngành

- **Ma trận root cause:** Bảng đối chiếu nguyên nhân gốc và bản vá của nhiều lỗ hổng.
- **Dữ liệu bị tin sai:** Dữ liệu được ứng dụng xem là đáng tin dù chưa đủ kiểm chứng.
- **HTML sink:** Điểm dữ liệu được đưa vào HTML và có thể bị parser diễn giải.
- **DOM sink:** API DOM có khả năng diễn giải dữ liệu thành cấu trúc hoặc mã.
- **Safe DOM API:** API không biến text thành HTML khi không cần thiết.
- **Context:** Ngữ cảnh dữ liệu được sử dụng.
- **Length invariant:** Giới hạn độ dài luôn phải đúng.
- **Bounded write:** Ghi dữ liệu với kích thước tối đa xác định.
- **Business policy:** Quy tắc nghiệp vụ như tính giá.
- **Access policy:** Quy tắc truy cập và phân quyền.
- **Object authorization:** Kiểm tra quyền trên từng object.
- **Intent proof:** Bằng chứng request phản ánh ý định hợp lệ của người dùng.
- **Deny before write:** Từ chối trước khi ghi hoặc thay đổi dữ liệu.
- **Parameterized query:** Query tách cấu trúc SQL khỏi tham số.
- **Code/data separation:** Tách mã lệnh khỏi dữ liệu.
- **Authorization source:** Nguồn dùng để xác định quyền.
- **Current database role:** Role hiện tại được đọc từ database.
- **Revoke:** Thu hồi phiên hoặc token.
- **Client không phải vùng an toàn:** Mọi dữ liệu client gửi cần được kiểm tra lại phía server.
- **Decision boundary:** Ranh giới nơi hệ thống đưa ra quyết định bảo mật cuối cùng.

---

# Slide 17 — Bằng chứng đi trước kết luận

## Mục tiêu của slide

- Trình bày chu trình thực hành bảy bước.
- Nêu cấu trúc báo cáo và loại bằng chứng tối thiểu.

## Kịch bản trình bày

- Chu trình thực hành của nhóm gồm bảy bước.
- Bước một, **Nhận diện**:
  - Xác định chức năng, input và ranh giới có nguy cơ.
- Bước hai, **Khai thác local**:
  - Dùng payload hoặc input an toàn trong môi trường được cấp quyền.
- Bước ba, **Quan sát**:
  - Ghi nhận response, trạng thái, log hoặc debugger.
- Bước bốn, **Phân tích**:
  - Xác định source, sink, root cause và control bị thiếu.
- Bước năm, **Đánh giá**:
  - Xác định phạm vi và mức độ ảnh hưởng.
- Bước sáu, **Vá lỗi**:
  - Sửa tại nguyên nhân gốc.
- Bước bảy, **Retest secure**:
  - Dùng lại cùng input để chứng minh bản vá có hiệu quả.
- Báo cáo có thể được đọc theo bốn khối:
  - Bối cảnh.
  - Thực hành.
  - Phân tích.
  - Kết luận.
- Phần bối cảnh gồm:
  - Tên lab.
  - Mục tiêu.
  - Môi trường.
  - Phạm vi an toàn.
- Phần thực hành gồm:
  - Các bước.
  - Kết quả quan sát.
  - Request và response.
- Phần phân tích gồm:
  - Nguyên nhân.
  - Ảnh hưởng.
  - Phòng chống.
  - Bản vá.
- Phần kết luận gồm:
  - Bài học.
  - Retest.
  - Phụ lục ảnh, log hoặc trace.
- Evidence tối thiểu phải là bằng chứng thật:
  - Ảnh từng bước và trạng thái trước/sau.
  - Request, response, log, trace hoặc debugger.
  - Before/after code.
  - Retest cùng input.
- Không được biến việc “source có vẻ đúng” thành kết luận runtime.
- Ví dụ:
  - Nhìn thấy `strcpy` cho phép dự đoán rủi ro.
  - Nhưng điểm crash và byte overwrite phải được xác nhận bằng GDB hoặc ASan.
- Kết luận chỉ được đưa ra sau bằng chứng.

## Câu chuyển sang slide tiếp theo

- Từ toàn bộ sáu lab, nhóm rút ra ba nguyên tắc cuối cùng về dữ liệu, quyết định và bằng chứng.

## Giải thích thuật ngữ và từ chuyên ngành

- **Evidence:** Bằng chứng quan sát được hỗ trợ cho kết luận.
- **Nhận diện:** Xác định dấu hiệu và vị trí có khả năng tồn tại lỗ hổng.
- **Khai thác local:** Làm lỗ hổng biểu hiện trong môi trường local có kiểm soát.
- **Quan sát:** Ghi nhận hành vi thực tế của hệ thống.
- **Phân tích:** Giải thích nguyên nhân kỹ thuật.
- **Đánh giá:** Xác định ảnh hưởng, phạm vi và mức độ rủi ro.
- **Vá lỗi:** Thay đổi mã nguồn hoặc cấu hình để loại bỏ nguyên nhân.
- **Retest secure:** Kiểm thử lại phiên bản secure.
- **Request:** Dữ liệu client gửi tới server.
- **Response:** Dữ liệu server trả về.
- **Log:** Bản ghi sự kiện.
- **Trace:** Chuỗi thông tin cho thấy luồng thực thi hoặc lỗi.
- **Debugger:** Công cụ quan sát chương trình khi chạy.
- **Before/after code:** Đoạn mã trước và sau bản vá.
- **Runtime:** Thời điểm chương trình đang thực thi.
- **Source code:** Mã nguồn của chương trình.
- **Phụ lục:** Phần đính kèm ảnh, log, request-response hoặc đoạn mã.
- **Bối cảnh:** Mục tiêu, môi trường và phạm vi.
- **Kết quả quan sát:** Hành vi đã thực sự thấy khi chạy lab.
- **Phòng chống:** Các biện pháp ngăn lỗi hoặc giảm ảnh hưởng.
- **Chu trình bảy bước:** Nhận diện → khai thác local → quan sát → phân tích → đánh giá → vá → retest.
- **Cùng input:** Dùng lại dữ liệu kiểm thử ban đầu để so sánh vulnerable và secure.

---

# Slide 18 — Đặt niềm tin đúng chỗ

## Mục tiêu của slide

- Kết luận toàn bộ bài trình bày.
- Tóm tắt ba nguyên tắc: Data, Decision và Evidence.

## Kịch bản trình bày

- Nhóm kết luận bài bằng thông điệp: **Đặt niềm tin đúng chỗ**.
- Nguyên tắc thứ nhất là **Data**:
  - Mọi dữ liệu từ client đều không đáng tin cậy cho đến khi được kiểm tra đúng mục đích.
  - Dữ liệu từ URL, form, cookie, localStorage hoặc HTTP body đều có thể bị sửa.
- Nguyên tắc thứ hai là **Decision**:
  - Xác thực phải do server xác minh.
  - Phân quyền phải do server quyết định.
  - Tính toàn vẹn phải được kiểm tra bằng cơ chế phù hợp.
  - Giá, role, ownership và quyền truy cập không được lấy trực tiếp từ client.
- Nguyên tắc thứ ba là **Evidence**:
  - Chỉ kết luận những gì đã được quan sát.
  - Bằng chứng phải thể hiện trạng thái vulnerable, bản vá và retest.
- Sáu bài lab cho thấy:
  - XSS cần vá tại output hoặc DOM sink.
  - Buffer Overflow cần giới hạn bộ nhớ và bounded write.
  - Parameter Tampering cần nguồn authoritative phía server.
  - CSRF cần chứng minh intent trước mutation.
  - SQL Injection cần parameterized query.
  - Cookie Poisoning cần server-side authorization và session phù hợp.
- Defense in depth giúp giảm rủi ro, nhưng không thay thế root fix.
- Client không phải vùng an toàn.
- Server phải là nơi giữ các quyết định bảo mật cuối cùng.
- Nhóm em xin kết thúc phần trình bày và sẵn sàng trả lời câu hỏi.

## Giải thích thuật ngữ và từ chuyên ngành

- **Data:** Dữ liệu được hệ thống tiếp nhận, lưu trữ hoặc xử lý.
- **Untrusted data:** Dữ liệu chưa được xác minh và có thể bị sửa.
- **Decision:** Quyết định cho phép, từ chối hoặc thay đổi trạng thái.
- **Authentication — Xác thực:** Xác minh người dùng là ai.
- **Authorization — Phân quyền:** Xác minh người dùng được phép làm gì.
- **Integrity — Toàn vẹn:** Bảo đảm dữ liệu không bị sửa mà không bị phát hiện.
- **Ownership:** Quan hệ sở hữu giữa người dùng và tài nguyên.
- **Evidence:** Bằng chứng thực tế cho kết luận.
- **Retest:** Kiểm thử lại sau bản vá.
- **Root fix:** Sửa tại nguyên nhân gốc.
- **Defense in depth:** Các lớp phòng thủ bổ sung.
- **Server-side authorization:** Phân quyền được kiểm tra tại server trên từng request.
- **Authoritative source:** Nguồn chính thức dùng cho quyết định.
- **Output sink:** Nơi dữ liệu được đưa ra và diễn giải.
- **Mutation:** Thao tác thay đổi trạng thái.
- **Parameterized query:** Query giữ cấu trúc cố định và bind dữ liệu riêng.
- **Bounded write:** Ghi có giới hạn kích thước.
- **Client không phải vùng an toàn:** Không được xem dữ liệu client là đáng tin chỉ vì dữ liệu đến từ UI hoặc cookie.
- **Đặt niềm tin đúng chỗ:** Chỉ tin dữ liệu sau khi server xác minh tại đúng ranh giới và đúng ngữ cảnh.

---

# Phần câu hỏi nhanh có thể được giảng viên đặt ra

## 1. Vì sao validation không đủ chống XSS?

- Validation chỉ kiểm tra input theo một tập quy tắc.
- Dữ liệu có thể hợp lệ ở ngữ cảnh này nhưng nguy hiểm ở ngữ cảnh khác.
- Bản vá chính vẫn là output encoding, sanitization hoặc safe DOM API tại sink.

## 2. Vì sao firewall không chặn được Buffer Overflow?

- HTTP request có thể hợp lệ theo rule mạng.
- Firewall không biết capacity của biến `name[32]` trong chương trình C.
- Root cause nằm ở thao tác bộ nhớ nội bộ.

## 3. Parameter Tampering khác SQL Injection thế nào?

- Parameter Tampering làm server tin sai giá trị hoặc policy.
- SQL Injection làm input trở thành một phần cú pháp SQL.
- Một bên phá business/access policy, một bên phá ranh giới code/data.

## 4. CSRF có cần đọc response không?

- Không.
- CSRF chỉ cần request làm thay đổi trạng thái được gửi với credential của nạn nhân.
- SOP có thể ngăn đọc response nhưng thay đổi đã xảy ra.

## 5. Base64 có phải mã hóa không?

- Không.
- Base64 chỉ là encoding.
- Không có secret, không có confidentiality và không có integrity.

## 6. Signed cookie và encrypted cookie khác nhau thế nào?

- Signed cookie giúp phát hiện sửa đổi, nhưng payload thường vẫn đọc được.
- Encrypted cookie bảo vệ confidentiality.
- Integrity của encrypted cookie chỉ được bảo đảm khi dùng AEAD hoặc encryption kèm MAC.

## 7. Vì sao phải retest cùng input?

- Để so sánh trực tiếp vulnerable và secure.
- Chứng minh bản vá chặn đúng hành vi cũ.
- Tránh kết luận dựa trên một input khác hoặc điều kiện khác.

## 8. Root fix và defense in depth khác nhau thế nào?

- Root fix loại bỏ nguyên nhân gốc.
- Defense in depth giảm khả năng khai thác hoặc giảm hậu quả.
- Không nên dùng hardening, WAF, CSP hoặc cookie flags để thay thế sửa code.
