# HƯỚNG DẪN CHỤP ẢNH TỐI GIẢN - LAB02 BUFFER OVERFLOW

Mục tiêu là chụp ít ảnh nhất nhưng vẫn đủ bằng chứng cho BaiTapTopic04.docx. Không chụp riêng từng tab DevTools nếu một ảnh tổng hợp đã chứng minh được cùng ý.

## Tổng số ảnh đề nghị: 3

Quy tắc chung: dùng đúng localhost của lab, dùng scenario/payload có sẵn trong repository, giữ URL/route và kết quả chính trong ảnh, che password, session ID, cookie/token/secret dài. Không chụp bước cài đặt, terminal khởi động, trang chủ hoặc ảnh lặp lại.

## Danh sách ảnh bắt buộc

### Ảnh 01. `01_boundary_and_overflow.png`

- Caption: Ranh giới buffer và input gây overflow.
- Phải thấy: Hiển thị UI/Memory Visualizer với buffer 32 byte, input bình thường hoặc 31 byte và input dài 64 byte. Ảnh phải làm rõ dữ liệu dài hơn capacity.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 02. `02_asan_evidence.png`

- Caption: ASan phát hiện stack-buffer-overflow.
- Phải thấy: Chạy vulnerable_asan với input 64 byte. Chụp terminal hoặc ASan Inspector thấy stack-buffer-overflow và exit khác 0. Không cần chụp nhiều trang log.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 03. `03_secure_and_hardening.png`

- Caption: Bản secure và hardening.
- Phải thấy: Trong một ảnh, chứng minh secure_length hoặc secure_snprintf từ chối/truncate input dài. Nếu có Hardening Inspector, mở kèm để thấy canary/PIE/NX/RELRO là defense in depth.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

## Map sang báo cáo

File báo cáo `21127645_LeMinh_21127224_NguyenVuBach_Lab02_BufferOverflow.docx` đã có 3 placeholder tương ứng trong phụ lục cuối báo cáo. Thay placeholder theo đúng thứ tự, giữ caption và phần “Ảnh phải thể hiện”.

## Tiêu chí đủ

- Có bằng chứng vulnerable hoạt động đúng kịch bản của đề.
- Có bằng chứng secure chặn hoặc xử lý đúng cùng input khi đề yêu cầu so sánh.
- Có đủ thông tin để giải thích root cause và primary fix mà không cần ảnh bổ sung.
- Không có ảnh trang trí hoặc lặp lại trạng thái đã chứng minh.
