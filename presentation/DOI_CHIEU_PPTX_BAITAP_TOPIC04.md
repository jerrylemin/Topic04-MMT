# Đối chiếu PPTX với BaiTapTopic04

PPTX đã đối chiếu: `21127645_LeMinh_21127224_NguyenVuBach_Topic04_6Labs_final.pptx` (33 slide). Đối tượng trình bày là lớp học; mục tiêu là giải thích chu trình nhận diện -> thử nghiệm local -> phân tích -> vá, không trình bày ô ảnh như kết quả thật.

| Slide | Lab | Yêu cầu DOCX được trình bày | Đầy đủ | Thiếu | Sai hoặc chưa sát | Đề xuất sửa |
| ----: | --- | --- | --- | --- | --- | --- |
| 1 | Tổng quan | Tên chủ đề, sáu lab, hai thành viên | Có | Không | Không | Không cần sửa |
| 2 | Tổng quan | Quy định an toàn; không website/hệ thống thật; không đánh cắp dữ liệu/cookie; không malware/reverse shell/persistence | Có | Không | Không | Không cần sửa |
| 3 | Lab01 | So sánh Reflected/Stored/DOM theo source, trung gian và sink | Có | Ảnh thật | Không | Chèn ảnh thật sau khi sinh viên thực hành |
| 4 | Lab01 | Normal input trước payload; Reflected và Stored; vị trí phản chiếu/nơi lưu; reload/user khác | Có về nội dung | Ảnh request/response/reload thật | Không | Giữ ô ảnh, chèn ảnh thật theo guide |
| 5 | Lab01 | DOM source/sink; location.hash; innerHTML/document.write/eval/setTimeout; fragment không gửi server; textContent | Có | Ảnh Network/Elements thật | Không | Chèn ảnh thật sau khi thực hành |
| 6 | Lab01 | Bốn ngữ cảnh output encoding; sanitization; textContent; CSP; cookie flags | Có | Ảnh secure thật | Không | Chèn ảnh thật sau khi thực hành |
| 7 | Lab01 | Năm câu trả lời, bản vá và checklist bằng chứng | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 8 | Lab02 | Linux/GCC/GDB/Python; HTTP -> Flask -> native; giới hạn crash local, không shellcode/ROP | Có | Log/ảnh thật | Không | Chèn evidence thật |
| 9 | Lab02 | Buffer stack, 32 byte, strcpy, overflow và khác Injection | Có | Kết quả runtime | Không | Không suy diễn crash từ sơ đồ |
| 10 | Lab02 | Chuỗi thực hành input thường/dài, crash, GDB/ASan, patch, retest | Có về nội dung | Toàn bộ log GDB/ASan/crash và ảnh thật | Không | Bổ sung sau khi sinh viên chạy lab |
| 11 | Lab02 | Hai bản vá: kiểm độ dài và snprintf; request limit | Có | Response retest thật | Không | Chèn ảnh response thật |
| 12 | Lab02 | Canary, ASLR, NX/DEP, PIE, RELRO, memory-safe language; năm câu hỏi | Có | Log hardening/runtime | Không | Không cần sửa nội dung |
| 13 | Lab03 | Trust boundary của form/URL/hidden/cookie; validation khác authorization | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 14 | Lab03 | Sửa giá, vulnerable chấp nhận và secure lấy giá DB | Có về nội dung | Payload/response ảnh thật | Không | Chèn ảnh thật theo guide |
| 15 | Lab03 | User A -> invoice A -> invoice B; IDOR; Broken Access Control; secure 403 | Có | Ảnh 403 thật | Không | Chèn ảnh thật |
| 16 | Lab03 | Role tampering, privilege escalation, field allowlist, identity từ session | Có | Ảnh request/response thật | Không | Chèn ảnh thật |
| 17 | Lab03 | Bảng ba tampering, năm câu trả lời và chuỗi thao tác | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 18 | Lab04 | Victim login; cookie tự gửi; attacker local; điều kiện CSRF | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 19 | Lab04 | Form attacker và email trước/sau | Có, có giải thích khác biệt | Ảnh trước/sau thật | Đề yêu cầu auto-submit nhưng source dùng nút submit có xác nhận | Đã sửa slide để ghi submit thủ công; không khẳng định auto-submit |
| 20 | Lab04 | Request hợp lệ ban đầu; request CSRF; cookie; token/Origin/Referer | Có | Ảnh request thật | Không | Không cần sửa nội dung |
| 21 | Lab04 | Token theo session, Origin/Referer, SameSite, re-auth, secure 403 và email không đổi | Có | Ảnh 403/email không đổi thật | Không | Chèn ảnh thật |
| 22 | Lab04 | Năm câu trả lời; phân biệt CSRF/XSS; GET state change; evidence checklist | Có | Ảnh thật | Không | Đã đổi checklist từ auto-submit sang submit thủ công |
| 23 | Lab05 | Normal input, dấu nháy đơn, error-based detection | Có | Ảnh thật | Không | Chèn ảnh thật |
| 24 | Lab05 | Query trước/sau; WHERE thay đổi; authentication bypass local | Có | Response ảnh thật | Không | Chèn ảnh thật |
| 25 | Lab05 | Search baseline; expanded result; data extraction cơ bản | Có | Result-set ảnh thật | Không | Chèn ảnh thật |
| 26 | Lab05 | Parameter binding; PBKDF2; secure retest login/search | Có | Hai ảnh secure thật | Không | Chèn ảnh thật |
| 27 | Lab05 | ORM/raw SQL; generic error; least privilege; validation/logging/WAF; năm câu hỏi | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 28 | Lab06 | Cookie là client-controlled; poisoning khác hijacking | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 29 | Lab06 | Name/Value/Domain/Path/flags; plain role user -> admin; access control | Có | Ảnh Application/response thật | Không | Chèn ảnh thật |
| 30 | Lab06 | Base64 decode -> JSON -> sửa -> encode -> gửi lại; confidentiality/integrity; AEAD/MAC | Có | Ảnh chuỗi Base64 thật | Không | Chèn ảnh thật |
| 31 | Lab06 | Signed cookie rejection; server session; DB role; rotate/revoke; cookie flags | Có | Ảnh signed/session thật | Không | Chèn ảnh thật |
| 32 | Lab06 | So sánh plain/Base64/signed/encrypted/server session; năm câu trả lời; server authorization | Có | Ảnh thật | Không | Không cần sửa nội dung |
| 33 | Tổng kết | Chu trình bảy bước và cấu trúc báo cáo 11 mục của đề | Có | Không | Không | Không cần sửa |

## Kết luận

- PPTX đã sửa bìa để có đủ hai thành viên và sửa slide 19/22 cho đúng source Lab04.
- Mỗi lab giữ đúng 5 slide; tổng số slide là 33; không thêm slide.
- Các ô `CHÈN ẢNH THẬT` được giữ làm vị trí chờ, không được gọi là kết quả quan sát.
- Không có nhãn nguồn kiểu `P103-P108`, không có nội dung tự chấm điểm và không tạo PDF.
