# Content matrix — Topic04 / 6 lab bảo mật ứng dụng web

Deck đích: `Topic04_6Labs_short.html` và PPTX 18 slide. Mỗi dòng dưới đây ánh xạ một nhóm yêu cầu bắt buộc trong `BaiTapTopic04.docx` tới ít nhất một slide. Nội dung được đối chiếu thêm với README, báo cáo DOCX và source vulnerable/secure của từng lab; slide không dùng ảnh chụp dự án hay placeholder ảnh.

| Yêu cầu BaiTapTopic04.docx | Lab | Slide trình bày | Nội dung rút gọn | Visual |
|---|---|---:|---|---|
| Chỉ thực hành trong VM/Docker/ứng dụng cố ý có lỗi; không thử website thật, không đánh cắp dữ liệu, không tạo shell/malware/persistence. | Chung | 02, 17 | Phạm vi local, dữ liệu giả lập, chu trình kiểm chứng có kiểm soát. | Ranh giới local + vòng đời 7 bước |
| Mỗi lab phải có bước thực hiện, kết quả, nguyên nhân, ảnh hưởng, phòng chống và bản vá. | Chung | 03–14, 17 | Mỗi cặp slide lab đi từ luồng lỗi đến root fix; slide 17 chuẩn hóa evidence và cấu trúc báo cáo. | Cặp flow/matrix + checklist bằng chứng |
| Phân biệt Reflected, Stored và DOM-based XSS. | Lab01 | 03 | So sánh source, nơi lưu, sink, thời điểm chạy và phạm vi nạn nhân. | Ba luồng source → storage → sink |
| Reflected XSS: dữ liệu query phản chiếu vào HTML; kiểm tra escape `< > " '`; nạn nhân mở URL có payload. | Lab01 | 03, 04 | Query hiện tại → HTML response → browser; bản secure giữ autoescape/contextual encoding. | Sequence ngắn + hàng so sánh vulnerable/secure |
| Stored XSS: payload được lưu, phát lại khi reload/người khác xem; thiếu HttpOnly làm tăng rủi ro. | Lab01 | 03, 04 | Form → SQLite → template → mọi lượt xem; sanitization/encoding tại render, cookie flags chỉ giảm hậu quả. | Flow có storage + defense layers |
| DOM XSS: kiểm tra `location.hash`, `innerHTML`, `document.write`, `eval`, `setTimeout(string)`; lỗi xảy ra ở browser. | Lab01 | 03, 04 | Source DOM không qua server; sink `innerHTML` parse thành node/handler; `textContent` tạo text node. | Browser-side source → sink + before/after code |
| Phòng chống XSS: contextual encoding, `textContent`, sanitization tin cậy, CSP, HttpOnly/Secure/SameSite, validation và không tin URL/form/cookie/localStorage. | Lab01 | 04 | Root fix ở sink; CSP/cookie flags/validation là defense in depth. | Ma trận 3 biến thể + lớp phòng thủ |
| Câu hỏi XSS: validation chưa đủ, cần output encoding, CSP không thay sửa code, cách vá từng lỗi. | Lab01 | 04 | Năm kết luận ngắn trả lời trực tiếp câu hỏi báo cáo. | Key-takeaway strip |
| Buffer Overflow có thể nằm sau HTTP trong web server/CGI/module/parser/backend native; lab chỉ gây crash có kiểm soát. | Lab02 | 05 | Browser → HTTP POST → Flask → subprocess → C → exit/signal; không shellcode/ROP/chiếm quyền. | HTTP → native backend |
| `char name[32]` + `strcpy`; gửi input ngắn/dài; dùng GDB/ASan để xác định crash, stack overwrite và ngưỡng lỗi từ evidence thật. | Lab02 | 05 | Capacity an toàn 31 byte + null; mô tả điều cần quan sát, không khẳng định mốc crash khi thiếu log runtime. | Stack memory normal/overflow |
| Phân tích buffer ở đâu, input vượt kích thước gây gì, vì sao `strcpy/gets/sprintf` nguy hiểm, memory corruption nghiêm trọng. | Lab02 | 05, 06 | Ghi vượt stack có thể phá dữ liệu lân cận/control data và tạo undefined behavior. | Stack frame có buffer/canary/frame pointer/return address |
| Vá ít nhất hai cách: kiểm tra độ dài; `fgets`/`snprintf`/`strncpy` cẩn thận; request limit. | Lab02 | 06 | `strnlen` + reject và `snprintf` + kiểm return; HTTP request limit chặn sớm. | Before/after code + invariant 31 byte |
| Hardening: stack protector, PIE/ASLR, RELRO, NX/DEP; ưu tiên thư viện/ngôn ngữ memory-safe. | Lab02 | 06 | Source fix là chính; compiler/loader/OS thu hẹp khả năng khai thác. | Defense-in-depth layers |
| Câu hỏi Buffer Overflow: khác Injection; HTTP kích hoạt native bug; firewall không đủ; vì sao bản vá hiệu quả; ít nhất 3 hardening. | Lab02 | 06 | Bảng 5 câu hỏi/kết luận. | Answer matrix |
| Parameter Tampering: không tin form, URL, hidden field, cookie; phân biệt validation và authorization. | Lab03 | 07 | Client parameter đi qua trust boundary tới quyết định policy server. | Client parameter → server policy decision |
| Thay đổi giá checkout; server phải lấy giá từ database. | Lab03 | 07, 08 | Vulnerable dùng `request.form.price`; secure dùng `products.price_vnd` tại thời điểm tính tổng. | Nhánh price + authoritative-source matrix |
| IDOR: đổi invoice ID; server kiểm owner/admin trên chính object; thuộc Broken Access Control. | Lab03 | 07, 08 | Authentication chưa đủ; object-level authorization trả allow/403. | Nhánh invoice + policy gate |
| Mass assignment/role tampering; không cho client gửi `role`, `is_admin`, `balance`, `user_id`. | Lab03 | 07, 08 | Identity lấy từ session; chỉ allowlist `email`; audit field nhạy cảm. | Nhánh profile + field allowlist |
| Câu hỏi Parameter Tampering: khác SQLi, hidden field không bảo mật, IDOR thuộc nhóm nào, kiểm gì trước khi trả invoice, vì sao giá phải ở server. | Lab03 | 08 | Năm câu trả lời được gắn với nguồn authoritative tương ứng. | Bảng scenario → lỗi → policy → kết quả |
| CSRF: victim đã đăng nhập, cookie tự gửi, endpoint đổi trạng thái thiếu token; phân biệt với XSS. | Lab04 | 09 | Trang giả lập local → victim browser → target; project hiện gửi form sau thao tác xác nhận của người dùng. | Attacker → browser → target sequence |
| Phân tích request CSRF: cookie có, token thiếu, Origin/Referer cross-origin; SOP không cần cho phép đọc response để state change xảy ra. | Lab04 | 09, 10 | Cookie chứng minh session, không chứng minh intent; SOP/CORS không phải bản vá CSRF. | Request anatomy + vulnerable/secure split |
| Secure: token ngẫu nhiên theo session, kiểm server, rotate; SameSite, Origin/Referer exact allowlist, POST-only, re-auth; CAPTCHA không phải lớp chính. | Lab04 | 10 | Deny trước mutation; các lớp phối hợp nhưng token/policy server là trọng tâm. | Defense pipeline có nhánh 403 |
| Câu hỏi CSRF: browser gửi cookie, không cần mật khẩu, thường không đọc response, khác XSS, không dùng GET cho state change. | Lab04 | 10 | Bảng năm câu hỏi/kết luận và evidence cần chứng minh trước/sau/403. | Answer matrix |
| SQLi do nối input vào SQL; phát hiện bằng input thường/dấu nháy; phân biệt auth bypass, expanded result và error-based detection cơ bản. | Lab05 | 11 | Input → concatenation → SQL parser → logic/result bị đổi trong SQLite local, SELECT-only. | Data-flow pipeline |
| Authentication bypass và search injection chỉ trong lab; ghi query bị biến đổi và retest cùng input ở bản secure. | Lab05 | 11, 12 | Login làm điều kiện mật khẩu mất tác dụng; search mở rộng tập kết quả; secure giữ cấu trúc SQL. | Hai nhánh login/search + before/after query |
| Vá bằng prepared/parameterized query; không nối chuỗi; hash mật khẩu; lỗi chung; least privilege. | Lab05 | 12 | SQL structure cố định, input bind như data; PBKDF2; generic error; quyền DB tối thiểu. | Code/data separation + defense layers |
| Câu hỏi SQLi: xảy ra ở tầng data access, escaping thủ công dễ sai, prepared khác concat, ORM không luôn an toàn, không lộ lỗi chi tiết. | Lab05 | 12 | Năm kết luận ngắn; WAF/validation/logging chỉ hỗ trợ. | Answer matrix |
| Cookie Poisoning: cookie là client-controlled; quan sát Name/Value/Domain/Path/HttpOnly/Secure/SameSite; sửa `role=user` thành `admin`. | Lab06 | 13 | Server phát cookie → client sửa → browser gửi lại → server vulnerable tin role. | Server cookie → client edit → server decision |
| Base64: decode JSON, sửa role, encode lại; Base64 chỉ encoding, không confidentiality/integrity. | Lab06 | 13, 14 | Plain và Base64 đều không có kiểm tra toàn vẹn. | Plain/Base64 parallel flows |
| Phân biệt plain, Base64, signed, encrypted và server-side session; signed bảo vệ integrity, encryption bảo vệ confidentiality + integrity khi authenticated. | Lab06 | 14 | Ma trận 5 mô hình theo readable/tamper detection/revocation/role source. | Capability matrix |
| Server-side session: opaque ID, hash lookup, active/expiry/revocation, role từ DB; rotate sau login, logout hủy server-side, authz mỗi request. | Lab06 | 14 | Quyết định quyền luôn dựa vào policy và state hiện tại phía server; cookie flags không thay authz. | Server-session flow + allow/deny branch |
| Câu hỏi Cookie Poisoning: cookie không đáng tin, khác hijacking, Base64 không mã hóa, signed cookie giải quyết integrity, server-side authorization bắt buộc. | Lab06 | 14 | Năm câu trả lời tích hợp trong ma trận kết luận. | Key-takeaway strip |
| Tổng hợp sáu lỗi: điểm gãy, nguồn dữ liệu bị tin sai và root fix. | Chung | 15, 16 | Sáu tên lỗi khác nhau nhưng cùng thất bại tại trust boundary. | Slide chuyển chương + ma trận 6 lab |
| Chu trình học tập: nhận diện → khai thác local → quan sát → phân tích → đánh giá → vá → kiểm tra secure. | Chung | 17 | Quy trình bảy bước, không lấy payload làm trọng tâm. | Vòng đời 7 bước |
| Cấu trúc báo cáo 11 mục và phụ lục ảnh/log/request-response. | Chung | 17 | Nén thành bốn khối: bối cảnh, thực hành, phân tích/vá, evidence; vẫn bao phủ đủ 11 mục. | Evidence stack + report map |
| Bài học: client không an toàn; server kiểm tra xác thực, phân quyền, toàn vẹn; secure-by-design. | Chung | 18 | Đặt niềm tin đúng chỗ: dữ liệu, quyết định, bằng chứng. | Kết luận nền cam với ba nguyên tắc |

## Phân bổ slide

| Slide | Vai trò | Lab/Phần | Thông điệp chính |
|---:|---|---|---|
| 01 | Bìa | Chung | Sáu lỗ hổng, một ranh giới niềm tin |
| 02 | Chuyển chương | Chung | Chỉ thực hành local; đọc mọi lỗi qua source → sink → decision |
| 03–04 | Kỹ thuật + kết luận | Lab01 | XSS là lỗi source-to-sink; vá tại đúng output context |
| 05–06 | Kỹ thuật + kết luận | Lab02 | HTTP có thể chạm code native; source fix trước hardening |
| 07–08 | Kỹ thuật + kết luận | Lab03 | Client gửi dữ liệu, server sở hữu quyết định policy |
| 09–10 | Kỹ thuật + kết luận | Lab04 | Session không chứng minh intent; deny trước mutation |
| 11–12 | Kỹ thuật + kết luận | Lab05 | Nối chuỗi trộn code/data; parameter binding tách chúng |
| 13–14 | Kỹ thuật + kết luận | Lab06 | Cookie không phải nguồn quyền; state authoritative ở server |
| 15 | Chuyển chương | Chung | Từ sáu lỗi đến một mô hình phòng thủ |
| 16 | Ma trận | Chung | Điểm gãy và root fix của sáu lab |
| 17 | Quy trình | Chung | Chu trình 7 bước và cấu trúc evidence/báo cáo |
| 18 | Kết luận | Chung | Đặt niềm tin đúng chỗ |
