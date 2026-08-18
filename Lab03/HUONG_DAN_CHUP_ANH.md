# HƯỚNG DẪN CHỤP ẢNH TỐI GIẢN - LAB03 PARAMETER TAMPERING

Mục tiêu là chụp ít ảnh nhất nhưng vẫn đủ bằng chứng cho BaiTapTopic04.docx. Không chụp riêng từng tab DevTools nếu một ảnh tổng hợp đã chứng minh được cùng ý.

## Tổng số ảnh đề nghị: 4

Quy tắc chung: dùng đúng localhost của lab, dùng scenario/payload có sẵn trong repository, giữ URL/route và kết quả chính trong ảnh, che password, session ID, cookie/token/secret dài. Không chụp bước cài đặt, terminal khởi động, trang chủ hoặc ảnh lặp lại.

## Danh sách ảnh bắt buộc

### Ảnh 01. `01_price_tampering.png`

- Caption: Price tampering - vulnerable và secure.
- Phải thấy: Chụp request sửa price của product 5 từ 100000 thành 1 và kết quả vulnerable chấp nhận. Trong cùng ảnh hoặc bố cục cạnh nhau, thể hiện secure checkout lấy lại giá 100000 từ server/database.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 02. `02_idor.png`

- Caption: IDOR - Broken Access Control.
- Phải thấy: Đăng nhập user_a, đổi invoice từ 1001 sang 1002. Ảnh phải chứng minh vulnerable xem được invoice người khác và secure trả 403 hoặc không render dữ liệu.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 03. `03_role_tampering.png`

- Caption: Role tampering / mass assignment.
- Phải thấy: Sửa hidden role=user thành admin ở vulnerable và cho thấy role bị thay đổi. Bản secure phải bỏ qua trường role và giữ user.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 04. `04_audit_evidence.png`

- Caption: Audit log cho hành vi tampering.
- Phải thấy: Chụp audit/log của secure route có ít nhất một sự kiện price mismatch, invoice_access_denied hoặc sensitive_field_submitted. Một ảnh log đủ cho phần phát hiện và điều tra.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

## Map sang báo cáo

File báo cáo `21127645_LeMinh_21127224_NguyenVuBach_Lab03_ParameterTampering.docx` đã có 4 placeholder tương ứng trong phụ lục cuối báo cáo. Thay placeholder theo đúng thứ tự, giữ caption và phần “Ảnh phải thể hiện”.

## Tiêu chí đủ

- Có bằng chứng vulnerable hoạt động đúng kịch bản của đề.
- Có bằng chứng secure chặn hoặc xử lý đúng cùng input khi đề yêu cầu so sánh.
- Có đủ thông tin để giải thích root cause và primary fix mà không cần ảnh bổ sung.
- Không có ảnh trang trí hoặc lặp lại trạng thái đã chứng minh.
