# HƯỚNG DẪN CHỤP ẢNH TỐI GIẢN - LAB06 COOKIE POISONING

Mục tiêu là chụp ít ảnh nhất nhưng vẫn đủ bằng chứng cho BaiTapTopic04.docx. Không chụp riêng từng tab DevTools nếu một ảnh tổng hợp đã chứng minh được cùng ý.

## Tổng số ảnh đề nghị: 4

Quy tắc chung: dùng đúng localhost của lab, dùng scenario/payload có sẵn trong repository, giữ URL/route và kết quả chính trong ảnh, che password, session ID, cookie/token/secret dài. Không chụp bước cài đặt, terminal khởi động, trang chủ hoặc ảnh lặp lại.

## Danh sách ảnh bắt buộc

### Ảnh 01. `01_plain_cookie_tamper.png`

- Caption: Plain cookie - sửa role để vượt quyền.
- Phải thấy: Đăng nhập student ở Plain Cookie Demo, sửa lab06_role=user thành admin trong DevTools rồi reload admin route. Ảnh phải thấy cookie đã sửa và quyền truy cập vulnerable.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 02. `02_base64_tamper.png`

- Caption: Base64 không bảo vệ integrity.
- Phải thấy: Trong Base64 Demo, giải mã role=user, thay bằng giá trị demo role=admin và reload. Ảnh phải chứng minh encoding đảo ngược được và server vulnerable tin dữ liệu.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 03. `03_signed_cookie_rejected.png`

- Caption: Signed cookie - tamper bị phát hiện.
- Phải thấy: Sửa một ký tự signed cookie rồi reload. Ảnh phải thấy server từ chối/invalid signature trước khi dùng payload.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 04. `04_server_side_session.png`

- Caption: Server-side session - role lấy từ server.
- Phải thấy: Đăng nhập student rồi admin_lab ở Server-side Session Demo. Ảnh phải cho thấy client chỉ giữ opaque session ID, student bị từ chối admin route và admin hợp lệ được phép. Không chụp full token/secret.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

## Map sang báo cáo

File báo cáo `21127645_LeMinh_21127224_NguyenVuBach_Lab06_CookiePoisoning.docx` đã có 4 placeholder tương ứng trong phụ lục cuối báo cáo. Thay placeholder theo đúng thứ tự, giữ caption và phần “Ảnh phải thể hiện”.

## Tiêu chí đủ

- Có bằng chứng vulnerable hoạt động đúng kịch bản của đề.
- Có bằng chứng secure chặn hoặc xử lý đúng cùng input khi đề yêu cầu so sánh.
- Có đủ thông tin để giải thích root cause và primary fix mà không cần ảnh bổ sung.
- Không có ảnh trang trí hoặc lặp lại trạng thái đã chứng minh.
