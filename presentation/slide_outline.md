# Slide outline — Nhóm Lê Minh 21127645 và Nguyễn Vũ Bách 21127224 / Topic04

Communication job: Sau 33 slide, người học phải hiểu sáu lỗ hổng như sáu cách phá vỡ trust boundary khác nhau, truy được dữ liệu từ source tới sink/quyết định, và biết bản vá nguyên nhân gốc cùng các lớp defense in depth.

| Slide | Lab | Takeaway và visual chính |
|---:|---|---|
| 01 | Tổng quan | Bìa Broadside cam; sáu đường tấn công hội tụ vào trust boundary; Lê Minh · 21127645 và Nguyễn Vũ Bách · 21127224 |
| 02 | Tổng quan | Bản đồ vòng đời dữ liệu từ Browser đến Response/Browser State; đặt 6 lab vào đúng boundary; bảng hậu quả–biện pháp |
| 03 | Lab01 | Ba XSS khác nhau ở source/storage/sink nhưng cùng biến dữ liệu thành mã |
| 04 | Lab01 | Reflected chạy qua request–response; Stored đi qua SQLite rồi phát lại; sequence kép + placeholder `29_reflected_network_request.png` |
| 05 | Lab01 | DOM XSS nằm hoàn toàn ở browser: `location.hash → innerHTML`; code thật và `textContent` |
| 06 | Lab01 | Root cause và patch: encode/sanitize/safe DOM API; CSP/cookie flags chỉ bổ sung; placeholder `41_secure_dom_textcontent.png` |
| 07 | Lab01 | Ma trận Reflected/Stored/DOM + 5 câu trả lời báo cáo + evidence checklist |
| 08 | Lab02 | HTTP vẫn có thể kích hoạt memory corruption trong process C; phạm vi crash local kiểm soát |
| 09 | Lab02 | `name[32]` chứa tối đa 31 byte dữ liệu; stack diagram normal/overflow |
| 10 | Lab02 | Quy trình 8 bước quan sát response/crash/GDB; hai placeholder cho ảnh người học tự chụp: `31_long_input_network_payload.png`, `34_secure_length_network_response.png` |
| 11 | Lab02 | `strcpy` không biết sức chứa; length check và `snprintf` chặn trước copy |
| 12 | Lab02 | Hardening nhiều lớp giảm khả năng khai thác nhưng không thay bản vá code; 5 câu trả lời |
| 13 | Lab03 | Mọi parameter phía browser là client-controlled; integer hợp lệ vẫn có thể trái policy |
| 14 | Lab03 | Giá phải được lấy từ DB; sequence vulnerable/secure + placeholder `45_checkout_tampered_payload.png` |
| 15 | Lab03 | IDOR là thiếu object-level authorization: invoice 1002 phải bị 403 với User A; placeholder `51_invoice_secure_403_response.png` |
| 16 | Lab03 | Mass assignment biến field profile thành privilege escalation; allowlist chỉ email |
| 17 | Lab03 | Ma trận Price/Invoice/Role + 5 câu trả lời và controls bắt buộc |
| 18 | Lab04 | CSRF cần session sống, cookie tự gửi, state change và thiếu token; tam giác 3 bên |
| 19 | Lab04 | Browser gửi form cross-origin tới target; SOP không ngăn request; sequence + placeholder `08_email_after_csrf.png` |
| 20 | Lab04 | Request anatomy cho thấy cookie có mặt nhưng token thiếu/origin sai vẫn được vulnerable route chấp nhận |
| 21 | Lab04 | Token theo session + Origin/Referer exact + SameSite + re-auth tạo luồng secure 403/allow; placeholder `13_secure_missing_token_403.png` |
| 22 | Lab04 | Bảng vulnerable/secure/attack request + 5 câu trả lời + evidence checklist |
| 23 | Lab05 | SQLi xảy ra tại ranh giới xây query, trước SQL parser |
| 24 | Lab05 | Payload local cố định làm thay logic WHERE; query transformation + placeholder `42_login_bypass_response.png` |
| 25 | Lab05 | Search concatenation mở rộng result set; request/query chạy song song; không payload phá dữ liệu |
| 26 | Lab05 | Parameter binding tách SQL code và data; code thật + PBKDF2/generic errors/least privilege; placeholder `43_secure_login_same_payload.png` |
| 27 | Lab05 | Defense in depth chỉ hiệu quả khi parameterized query là lớp gốc; 5 câu trả lời |
| 28 | Lab06 | Cookie vận chuyển state nhưng không tạo niềm tin; client sửa role rồi gửi lại |
| 29 | Lab06 | Quan sát flags và sửa `lab06_role`; placeholder `51_plain_cookie_modified_application.png`, bắt buộc che token/session dài |
| 30 | Lab06 | Base64 là encoding; Signed thêm integrity; Encrypted thêm confidentiality + integrity |
| 31 | Lab06 | Opaque session ID → server lookup → DB role → authorization; rotate/revoke; placeholder `56_signed_cookie_rejected_response.png` |
| 32 | Lab06 | Ma trận Plain/Base64/Signed/Encrypted/Server session + 5 câu trả lời |
| 33 | Tổng kết | Chu trình 7 bước và ma trận source–sink–patch cho 6 lab; nền cam Broadside |

Mỗi lab đúng 5 slide. Mỗi lab có đúng 2 placeholder ảnh, đều là shape PowerPoint có thể thay thủ công; không có ảnh giả, ảnh stock hoặc ảnh chụp tự động.
