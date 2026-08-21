# HƯỚNG DẪN CHỤP ẢNH TỐI GIẢN - LAB05 SQL INJECTION

Mục tiêu là chụp ít ảnh nhất nhưng vẫn đủ bằng chứng cho BaiTapTopic04.docx. Không chụp riêng từng tab DevTools nếu một ảnh tổng hợp đã chứng minh được cùng ý.

## Tổng số ảnh đề nghị: 3

Quy tắc chung: dùng đúng localhost của lab, dùng scenario/payload có sẵn trong repository, giữ URL/route và kết quả chính trong ảnh, che password, session ID, cookie/token/secret dài. Không chụp bước cài đặt, terminal khởi động, trang chủ hoặc ảnh lặp lại.

## Danh sách ảnh bắt buộc

### Ảnh 01. `01_login_injection.png`

- Caption: Login SQL Injection - vulnerable và secure.
- Phải thấy: Dùng scenario cố định admin_lab' --. Ảnh phải cho thấy vulnerable tạo session/bypass điều kiện password, còn secure với cùng input không đăng nhập.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 02. `02_search_injection.png`

- Caption: Search SQL Injection - result set bị mở rộng.
- Phải thấy: Dùng payload cố định %' OR 1=1 --. Ảnh phải thấy vulnerable trả nhiều/8 sản phẩm thay vì tập con mong đợi.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 03. `03_parameterized_query.png`

- Caption: Secure query - parameter binding.
- Phải thấy: Gửi cùng payload vào secure search/login. Chụp Query Construction hoặc log cho thấy SQL template có placeholder ? và payload nằm ở parameter, kết quả không bị mở rộng/bypass.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

## Map sang báo cáo

File báo cáo `21127645_LeMinh_21127224_NguyenVuBach_Lab05_SQLInjection.docx` đã có 3 placeholder tương ứng trong phụ lục cuối báo cáo. Thay placeholder theo đúng thứ tự, giữ caption và phần “Ảnh phải thể hiện”.

## Tiêu chí đủ

- Có bằng chứng vulnerable hoạt động đúng kịch bản của đề.
- Có bằng chứng secure chặn hoặc xử lý đúng cùng input khi đề yêu cầu so sánh.
- Có đủ thông tin để giải thích root cause và primary fix mà không cần ảnh bổ sung.
- Không có ảnh trang trí hoặc lặp lại trạng thái đã chứng minh.
