# HƯỚNG DẪN CHỤP ẢNH TỐI GIẢN - LAB01 CROSS-SITE SCRIPTING (XSS)

Mục tiêu là chụp ít ảnh nhất nhưng vẫn đủ bằng chứng cho BaiTapTopic04.docx. Không chụp riêng từng tab DevTools nếu một ảnh tổng hợp đã chứng minh được cùng ý.

## Tổng số ảnh đề nghị: 5

Quy tắc chung: dùng đúng localhost của lab, dùng scenario/payload có sẵn trong repository, giữ URL/route và kết quả chính trong ảnh, che password, session ID, cookie/token/secret dài. Không chụp bước cài đặt, terminal khởi động, trang chủ hoặc ảnh lặp lại.

## Danh sách ảnh bắt buộc

### Ảnh 01. `01_reflected_vulnerable.png`

- Caption: Reflected XSS - bản vulnerable.
- Phải thấy: Hiển thị URL /vulnerable/search, payload đã nhập, alert hoặc DOM img/onerror và Network request q. Một ảnh phải chứng minh input bị phản chiếu thành HTML thực thi.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 02. `02_reflected_secure.png`

- Caption: Reflected XSS - bản secure.
- Phải thấy: Gửi đúng payload ở /secure/search. Ảnh phải thấy payload chỉ hiển thị như text/đã encode và không có alert.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 03. `03_stored_persistence.png`

- Caption: Stored XSS - lưu và tồn tại sau reload.
- Phải thấy: Ảnh sau khi đăng comment độc hại rồi reload. Phải thấy comment vẫn tồn tại và browser tiếp tục tạo/thi hành nội dung ở bản vulnerable. Nếu giao diện cho phép, mở Network/Response hoặc Database Inspector trong cùng ảnh.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 04. `04_stored_secure.png`

- Caption: Stored XSS - bản secure.
- Phải thấy: Gửi cùng nội dung ở /secure/post/1/comments. Ảnh phải thấy event handler/thẻ nguy hiểm bị loại hoặc encode và không có alert.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

### Ảnh 05. `05_dom_vulnerable_secure.png`

- Caption: DOM-based XSS - so sánh vulnerable và secure.
- Phải thấy: Xếp vulnerable và secure cạnh nhau trong một screenshot. Bên vulnerable dùng fragment và sinh DOM qua innerHTML. Bên secure hiển thị cùng fragment như textContent. Network không có request mới khi chỉ thay hash.
- Cách chụp: gom UI và vùng DevTools/terminal liên quan vào cùng khung. Khi cần đối chiếu vulnerable/secure, đặt hai cửa sổ cạnh nhau trong một screenshot nếu đọc được rõ.
- Không cần chụp thêm: request trung gian hoặc tab Headers/Payload/Response riêng nếu không bổ sung bằng chứng mới.

## Map sang báo cáo

File báo cáo `21127645_LeMinh_21127224_NguyenVuBach_Lab01_XSS.docx` đã có 5 placeholder tương ứng trong phụ lục cuối báo cáo. Thay placeholder theo đúng thứ tự, giữ caption và phần “Ảnh phải thể hiện”.

## Tiêu chí đủ

- Có bằng chứng vulnerable hoạt động đúng kịch bản của đề.
- Có bằng chứng secure chặn hoặc xử lý đúng cùng input khi đề yêu cầu so sánh.
- Có đủ thông tin để giải thích root cause và primary fix mà không cần ảnh bổ sung.
- Không có ảnh trang trí hoặc lặp lại trạng thái đã chứng minh.
