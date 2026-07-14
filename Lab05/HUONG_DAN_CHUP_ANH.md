# Hướng dẫn chụp ảnh thủ công LAB 5

Ảnh được chụp **thủ công**, lưu đúng tên trong `evidence/screenshots/`. Trước khi chụp, chạy app tại `http://127.0.0.1:5005`, đặt zoom trình duyệt 100%, mở rộng cửa sổ tối thiểu 1280×720 và reset lab khi hướng dẫn yêu cầu. Không dùng công cụ tự động điều khiển trình duyệt, không tạo ảnh giả. Ảnh terminal chỉ chụp kết quả lệnh đã chạy thật.

## 01_home_overview.png

**Tên file:** `01_home_overview.png` · **Mục đích:** Tổng quan phạm vi LAB 5. · **URL:** `/` · **Điều kiện ban đầu:** App đang chạy, chưa cần đăng nhập. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Mở trang chủ. · **Inspector cần mở:** Không. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Tiêu đề LAB 5, bốn phần học tập và nhãn local-only. · **Kết quả mong đợi:** Thấy rõ vulnerable/secure và địa chỉ 127.0.0.1:5005. · **Caption báo cáo:** Tổng quan ứng dụng học tập SQL Injection trong phạm vi local. · **Lỗi thường gặp:** Chụp thiếu scope card. · **Cách làm lại:** Cuộn lên đầu trang và chụp toàn bộ hero.

## 02_database_seed.png

**Tên file:** `02_database_seed.png` · **Mục đích:** Xác nhận dữ liệu giả lập đã seed. · **URL:** `/dashboard` · **Điều kiện ban đầu:** Bấm Reset dữ liệu lab một lần. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Reset dữ liệu lab. · **Inspector cần mở:** Database Inspector nếu dashboard có trace reset. · **Timeline step cần chọn:** Final Result. · **Nội dung bắt buộc:** 3 users, ít nhất 8 products và trạng thái local database. · **Kết quả mong đợi:** Seed hoàn tất, không có dữ liệu thật. · **Caption báo cáo:** Database SQLite local sau khi seed dữ liệu giả lập. · **Lỗi thường gặp:** Số liệu cũ do chưa reset. · **Cách làm lại:** Reset, xác nhận POST hoàn tất rồi tải lại dashboard.

## 03_vulnerable_login_normal.png

**Tên file:** `03_vulnerable_login_normal.png` · **Mục đích:** Login legacy với input hợp lệ. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Reset lab và chưa đăng nhập. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Dữ liệu bình thường, rồi Chạy vulnerable login. · **Inspector cần mở:** Final Security Verdict. · **Timeline step cần chọn:** Final verdict. · **Nội dung bắt buộc:** Decision authenticated và mode vulnerable. · **Kết quả mong đợi:** Session demo được tạo từ tài khoản hợp lệ. · **Caption báo cáo:** Vulnerable login bình thường trong database local. · **Lỗi thường gặp:** Session cũ còn tồn tại. · **Cách làm lại:** Đăng xuất, reset và chạy lại đúng tài khoản.

## 04_vulnerable_login_request.png

**Tên file:** `04_vulnerable_login_request.png` · **Mục đích:** Quan sát request login thật đã che password. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Vừa chạy normal vulnerable login. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Mở Request. · **Inspector cần mở:** Request Inspector. · **Timeline step cần chọn:** HTTP Request. · **Nội dung bắt buộc:** POST, path, form field names; password chỉ hiện metadata/giá trị che. · **Kết quả mong đợi:** Không thấy plaintext password. · **Caption báo cáo:** Request Inspector của vulnerable login với trường nhạy cảm đã che. · **Lỗi thường gặp:** Chụp form trước khi submit. · **Cách làm lại:** Submit lại rồi mở tab Request trong trace mới.

## 05_vulnerable_login_query.png

**Tên file:** `05_vulnerable_login_query.png` · **Mục đích:** Chứng minh phương thức nối chuỗi. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Có trace normal vulnerable login. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** Construction type, query template và final query masked. · **Kết quả mong đợi:** Thấy string concatenation, chưa dùng placeholder. · **Caption báo cáo:** Query vulnerable được tạo bằng nối chuỗi. · **Lỗi thường gặp:** Mở nhầm trace secure. · **Cách làm lại:** Kiểm tra badge vulnerable và chạy lại flow.

## 06_quote_login_input.png

**Tên file:** `06_quote_login_input.png` · **Mục đích:** Phát hiện ký tự đơn giản có nguy cơ. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Đăng xuất khỏi session trước. · **Dữ liệu cần nhập:** Username `'`, password `x`. · **Nút cần bấm:** Ký tự dấu nháy đơn, rồi Chạy vulnerable login. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Input Validation. · **Nội dung bắt buộc:** Raw input, độ dài và quote_detected=true. · **Kết quả mong đợi:** Scenario cố định được nhận diện. · **Caption báo cáo:** Input Inspector phát hiện dấu nháy đơn trong login. · **Lỗi thường gặp:** Gõ dấu nháy kiểu cong. · **Cách làm lại:** Dùng đúng nút scenario cố định.

## 07_quote_login_error.png

**Tên file:** `07_quote_login_error.png` · **Mục đích:** Quan sát lỗi query có kiểm soát. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Vừa submit quote login. · **Dữ liệu cần nhập:** Username `'`, password `x`. · **Nút cần bấm:** Mở tab Error. · **Inspector cần mở:** Error Inspector. · **Timeline step cần chọn:** Error Handling. · **Nội dung bắt buộc:** Category `sql_syntax_error`, handled status, không có traceback/absolute path. · **Kết quả mong đợi:** Diagnostic local đã che thông tin nhạy cảm. · **Caption báo cáo:** Quote input tạo lỗi cú pháp được phân loại an toàn. · **Lỗi thường gặp:** Chụp trang lỗi Flask debug. · **Cách làm lại:** Tắt debug, chạy lại app và scenario.

## 08_auth_logic_input.png

**Tên file:** `08_auth_logic_input.png` · **Mục đích:** Ghi nhận scenario authentication logic cố định. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Đã đăng xuất. · **Dữ liệu cần nhập:** Dùng nút Điều kiện đăng nhập local; password `wrong`. · **Nút cần bấm:** Điều kiện đăng nhập local, rồi submit. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Browser UI. · **Nội dung bắt buộc:** Boolean expression và comment marker của scenario cố định được nhận diện. · **Kết quả mong đợi:** Input category là local auth logic demo. · **Caption báo cáo:** Input cố định dùng minh họa authentication logic trong local lab. · **Lỗi thường gặp:** Tự sửa chuỗi scenario. · **Cách làm lại:** Reset form và dùng đúng nút được cung cấp.

## 09_auth_query_changed.png

**Tên file:** `09_auth_query_changed.png` · **Mục đích:** Cho thấy cấu trúc WHERE bị thay đổi. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Có trace auth logic vulnerable. · **Dữ liệu cần nhập:** Scenario Điều kiện đăng nhập local. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** SQLite Parser. · **Nội dung bắt buộc:** Final query masked và `sql_structure_changed=true`. · **Kết quả mong đợi:** Visualizer đánh dấu String Concatenation/Unexpected Result. · **Caption báo cáo:** Nối chuỗi làm thay đổi cấu trúc điều kiện xác thực. · **Lỗi thường gặp:** Chọn trace quote error. · **Cách làm lại:** Chạy đúng nút auth logic rồi mở trace mới nhất.

## 10_auth_decision_vulnerable.png

**Tên file:** `10_auth_decision_vulnerable.png` · **Mục đích:** Quan sát quyết định xác thực sai. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Auth logic scenario đã trả result set. · **Dữ liệu cần nhập:** Scenario auth logic, password `wrong`. · **Nút cần bấm:** Tab Authentication. · **Inspector cần mở:** Authentication Decision Inspector. · **Timeline step cần chọn:** Authentication Decision. · **Nội dung bắt buộc:** Decision local_demo_bypass, password không hợp lệ và authentication_bypassed=true. · **Kết quả mong đợi:** Server chọn user do WHERE đã đổi. · **Caption báo cáo:** Authentication decision vulnerable chấp nhận sai trong demo local. · **Lỗi thường gặp:** Password đúng làm mất ý nghĩa. · **Cách làm lại:** Đăng xuất và dùng password `wrong`.

## 11_auth_session_created.png

**Tên file:** `11_auth_session_created.png` · **Mục đích:** Chứng minh state change của bypass demo. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Auth logic vulnerable vừa hoàn tất. · **Dữ liệu cần nhập:** Scenario auth logic, password `wrong`. · **Nút cần bấm:** Mở Verdict. · **Inspector cần mở:** Final Security Verdict. · **Timeline step cần chọn:** Session Management. · **Nội dung bắt buộc:** `session_created=true` và `authenticated_via=vulnerable_local_demo`. · **Kết quả mong đợi:** UI cảnh báo session chỉ để minh họa. · **Caption báo cáo:** Session demo được tạo sau quyết định vulnerable. · **Lỗi thường gặp:** Đã mở trace khác sau đó. · **Cách làm lại:** Đăng xuất và chạy lại duy nhất scenario này.

## 12_secure_login_same_input.png

**Tên file:** `12_secure_login_same_input.png` · **Mục đích:** Dùng cùng input trên bản secure. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Đăng xuất khỏi vulnerable session. · **Dữ liệu cần nhập:** Nút Cùng input logic, password `wrong`. · **Nút cần bấm:** Cùng input logic, rồi Chạy secure login. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Input Validation. · **Nội dung bắt buộc:** Cùng raw input như ảnh 08, mode secure. · **Kết quả mong đợi:** Request được xử lý như dữ liệu, không chạy logic ngoài scenario. · **Caption báo cáo:** Cùng input authentication logic đi qua secure route. · **Lỗi thường gặp:** Chưa đăng xuất session vulnerable. · **Cách làm lại:** POST logout rồi submit lại secure flow.

## 13_secure_login_parameter_binding.png

**Tên file:** `13_secure_login_parameter_binding.png` · **Mục đích:** Chứng minh parameterized query. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Có trace secure same-input. · **Dữ liệu cần nhập:** Scenario Cùng input logic. · **Nút cần bấm:** Tab Parameters. · **Inspector cần mở:** Parameter Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** `WHERE username = ?`, parameter count và bound_by_driver=true. · **Kết quả mong đợi:** SQL structure preserved=true. · **Caption báo cáo:** Secure login bind username vào placeholder. · **Lỗi thường gặp:** Chụp Query tab nhưng thiếu parameter. · **Cách làm lại:** Mở riêng tab Parameters và chọn step binding.

## 14_secure_login_rejected.png

**Tên file:** `14_secure_login_rejected.png` · **Mục đích:** Xác nhận secure route từ chối cùng input. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Secure same-input đã chạy. · **Dữ liệu cần nhập:** Scenario auth logic, password `wrong`. · **Nút cần bấm:** Tab Authentication hoặc Verdict. · **Inspector cần mở:** Authentication Decision Inspector. · **Timeline step cần chọn:** Final Result. · **Nội dung bắt buộc:** Decision rejected, session_created=false và generic message. · **Kết quả mong đợi:** Không xác thực, không tiết lộ username tồn tại. · **Caption báo cáo:** Secure login từ chối input từng đổi logic ở bản vulnerable. · **Lỗi thường gặp:** Session cũ làm header vẫn hiện user. · **Cách làm lại:** Đăng xuất, reset và chạy secure flow trước.

## 15_secure_login_normal_success.png

**Tên file:** `15_secure_login_normal_success.png` · **Mục đích:** Xác nhận bản secure vẫn hỗ trợ login hợp lệ. · **URL:** `/secure/login` · **Điều kiện ban đầu:** Chưa đăng nhập. · **Dữ liệu cần nhập:** `admin_lab` / `AdminLab123!`. · **Nút cần bấm:** Dữ liệu bình thường, rồi Chạy secure login. · **Inspector cần mở:** Authentication Decision Inspector. · **Timeline step cần chọn:** Password Processing. · **Nội dung bắt buộc:** `check_password_hash`, authenticated, `authenticated_via=secure_pbkdf2`. · **Kết quả mong đợi:** Login thành công và session rotate. · **Caption báo cáo:** Secure normal login với PBKDF2 thành công. · **Lỗi thường gặp:** Nhập sai chữ hoa/thường password. · **Cách làm lại:** Đăng xuất và dùng nút tài khoản demo.

## 16_vulnerable_search_normal.png

**Tên file:** `16_vulnerable_search_normal.png` · **Mục đích:** Baseline tìm kiếm vulnerable. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Database đã reset. · **Dữ liệu cần nhập:** `USB`. · **Nút cần bấm:** Dữ liệu bình thường, rồi Chạy vulnerable search. · **Inspector cần mở:** Result Set Inspector. · **Timeline step cần chọn:** Result Set. · **Nội dung bắt buộc:** Các sản phẩm có USB và số rows baseline. · **Kết quả mong đợi:** Chỉ kết quả phù hợp từ products. · **Caption báo cáo:** Kết quả tìm kiếm bình thường ở vulnerable mode. · **Lỗi thường gặp:** Dùng từ khóa khác làm sai baseline. · **Cách làm lại:** Xóa ô và dùng nút USB.

## 17_vulnerable_search_query.png

**Tên file:** `17_vulnerable_search_query.png` · **Mục đích:** Quan sát keyword nối vào LIKE. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Có trace normal vulnerable search. · **Dữ liệu cần nhập:** `USB`. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** Final SQL masked và construction type concatenation. · **Kết quả mong đợi:** Keyword nằm trong SQL text, chưa dùng placeholder. · **Caption báo cáo:** Vulnerable search ghép keyword trực tiếp vào LIKE. · **Lỗi thường gặp:** Chụp trang secure search. · **Cách làm lại:** Kiểm tra badge vulnerable rồi chạy lại.

## 18_quote_search_error.png

**Tên file:** `18_quote_search_error.png` · **Mục đích:** Phát hiện lỗi search bằng dấu nháy đơn. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Database bình thường. · **Dữ liệu cần nhập:** `'`. · **Nút cần bấm:** Ký tự dấu nháy đơn, rồi submit. · **Inspector cần mở:** Error Inspector. · **Timeline step cần chọn:** Error Handling. · **Nội dung bắt buộc:** sql_syntax_error, rows_changed=0, không traceback. · **Kết quả mong đợi:** Lỗi được ghi audit và UI vẫn an toàn. · **Caption báo cáo:** Quote search tạo lỗi cú pháp trong query nối chuỗi. · **Lỗi thường gặp:** Chụp thông báo trình duyệt thay vì inspector. · **Cách làm lại:** Mở tab Error của trace mới nhất.

## 19_expanded_search_input.png

**Tên file:** `19_expanded_search_input.png` · **Mục đích:** Ghi nhận scenario mở rộng kết quả cố định. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Reset database nếu cần. · **Dữ liệu cần nhập:** Dùng nút Mở rộng kết quả local. · **Nút cần bấm:** Mở rộng kết quả local, rồi submit. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Browser UI. · **Nội dung bắt buộc:** Input category fixed expanded search; trust level untrusted. · **Kết quả mong đợi:** Scenario chỉ nhắm products local. · **Caption báo cáo:** Input cố định minh họa thay đổi điều kiện tìm kiếm. · **Lỗi thường gặp:** Tự tạo payload khác. · **Cách làm lại:** Dùng nút scenario, không sửa chuỗi.

## 20_expanded_search_query.png

**Tên file:** `20_expanded_search_query.png` · **Mục đích:** Cho thấy điều kiện search bị thay đổi. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Có trace expanded vulnerable search. · **Dữ liệu cần nhập:** Scenario mở rộng local. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** SQLite Parser. · **Nội dung bắt buộc:** sql_structure_changed=true, final query masked và visualizer vulnerable. · **Kết quả mong đợi:** SQLite parse điều kiện rộng hơn dự kiến. · **Caption báo cáo:** Cấu trúc LIKE bị thay đổi bởi phép nối chuỗi. · **Lỗi thường gặp:** Chọn quote-error trace. · **Cách làm lại:** Submit scenario expanded rồi mở trace mới.

## 21_expanded_search_results.png

**Tên file:** `21_expanded_search_results.png` · **Mục đích:** Chứng minh result set ngoài điều kiện mong muốn. · **URL:** `/vulnerable/search` · **Điều kiện ban đầu:** Expanded search đã chạy. · **Dữ liệu cần nhập:** Scenario mở rộng local. · **Nút cần bấm:** Tab Result Set. · **Inspector cần mở:** Result Set Inspector. · **Timeline step cần chọn:** Result Set. · **Nội dung bắt buộc:** Actual rows lớn hơn baseline, table=products, database_modified=false. · **Kết quả mong đợi:** Chỉ sản phẩm local được trả về; không đọc users. · **Caption báo cáo:** Vulnerable search trả thêm rows trong bảng products. · **Lỗi thường gặp:** Kết quả không lớn hơn do dùng sai input. · **Cách làm lại:** Reset và dùng nút expanded chính xác.

## 22_secure_search_same_input.png

**Tên file:** `22_secure_search_same_input.png` · **Mục đích:** Đối chiếu cùng input qua secure search. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Đã ghi nhận expanded vulnerable baseline. · **Dữ liệu cần nhập:** Nút Cùng input mở rộng. · **Nút cần bấm:** Cùng input mở rộng, rồi Chạy secure search. · **Inspector cần mở:** Input Inspector. · **Timeline step cần chọn:** Input Validation. · **Nội dung bắt buộc:** Cùng raw input, mode secure, validation pass. · **Kết quả mong đợi:** Input được coi là literal search value. · **Caption báo cáo:** Cùng input mở rộng được xử lý ở secure route. · **Lỗi thường gặp:** Nhập khác chuỗi vulnerable. · **Cách làm lại:** Dùng nút cố định ở secure search.

## 23_secure_search_binding.png

**Tên file:** `23_secure_search_binding.png` · **Mục đích:** Chứng minh `LIKE ?` và parameter tuple. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Có trace secure same-input. · **Dữ liệu cần nhập:** Cùng input mở rộng. · **Nút cần bấm:** Tab Parameters. · **Inspector cần mở:** Parameter Inspector. · **Timeline step cần chọn:** Query Construction. · **Nội dung bắt buộc:** Template có `LIKE ?`, parameter masked, bound_by_driver=true. · **Kết quả mong đợi:** sql_structure_preserved=true. · **Caption báo cáo:** Secure search bind `%keyword%` qua SQLite driver. · **Lỗi thường gặp:** Chụp final query nhưng thiếu placeholder. · **Cách làm lại:** Mở Parameter Inspector và chọn step binding.

## 24_secure_search_expected_results.png

**Tên file:** `24_secure_search_expected_results.png` · **Mục đích:** Xác nhận secure result set đúng điều kiện. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Secure same-input đã chạy. · **Dữ liệu cần nhập:** Cùng input mở rộng. · **Nút cần bấm:** Tab Result Set. · **Inspector cần mở:** Result Set Inspector. · **Timeline step cần chọn:** Final Result. · **Nội dung bắt buộc:** Unexpected rows=false, limit=50, actual rows theo literal input. · **Kết quả mong đợi:** Không mở rộng toàn bộ products. · **Caption báo cáo:** Parameter binding giữ kết quả search đúng ý nghĩa. · **Lỗi thường gặp:** Chụp normal `USB` thay vì same-input. · **Cách làm lại:** Dùng lại nút Cùng input mở rộng.

## 25_query_visualizer.png

**Tên file:** `25_query_visualizer.png` · **Mục đích:** So sánh data flow vulnerable/secure. · **URL:** `/secure/search` · **Điều kiện ban đầu:** Có trace secure search. · **Dữ liệu cần nhập:** `USB`. · **Nút cần bấm:** Mở Query. · **Inspector cần mở:** Query Construction Inspector. · **Timeline step cần chọn:** Parameter Binding. · **Nội dung bắt buộc:** User Input → Python Value → SQL Template → Binding → SQLite Parser → Expected Result. · **Kết quả mong đợi:** Sơ đồ có placeholder và structure preserved. · **Caption báo cáo:** Query visualizer của secure parameter binding. · **Lỗi thường gặp:** Sơ đồ nằm dưới fold. · **Cách làm lại:** Cuộn trong Query Inspector đến toàn bộ flow.

## 26_code_comparison_login.png

**Tên file:** `26_code_comparison_login.png` · **Mục đích:** So sánh source login thật. · **URL:** `/comparison#login-code` · **Điều kiện ban đầu:** Source backend đã có line markers. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Login trong subnav. · **Inspector cần mở:** Code Comparison. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** File/function/line range, nối chuỗi đối chiếu placeholder + check_password_hash. · **Kết quả mong đợi:** Hai cột source thật hiển thị đầy đủ. · **Caption báo cáo:** So sánh code vulnerable và secure login. · **Lỗi thường gặp:** Source excerpt chưa được backend cung cấp. · **Cách làm lại:** Chạy lại app sau khi source hoàn tất rồi tải trang.

## 27_code_comparison_search.png

**Tên file:** `27_code_comparison_search.png` · **Mục đích:** So sánh source search thật. · **URL:** `/comparison#search-code` · **Điều kiện ban đầu:** Trang comparison đã tải. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Search trong subnav. · **Inspector cần mở:** Code Comparison. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Keyword nối LIKE đối chiếu `LIKE ?` và parameter tuple. · **Kết quả mong đợi:** Line reference khớp source. · **Caption báo cáo:** So sánh code vulnerable và secure product search. · **Lỗi thường gặp:** Chụp nhầm section login. · **Cách làm lại:** Dùng anchor Search và kiểm tra heading.

## 28_error_comparison.png

**Tên file:** `28_error_comparison.png` · **Mục đích:** So sánh xử lý error. · **URL:** `/comparison#error-code` · **Điều kiện ban đầu:** Trang comparison đã tải. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Error handling trong subnav. · **Inspector cần mở:** Code Comparison. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Vulnerable diagnostic local đối chiếu generic message + internal error ID. · **Kết quả mong đợi:** Không cột nào chứa traceback/path tuyệt đối. · **Caption báo cáo:** So sánh error handling trước và sau vá. · **Lỗi thường gặp:** Source excerpt trống. · **Cách làm lại:** Tải lại sau khi backend hoàn tất comparison data.

## 29_password_hashing.png

**Tên file:** `29_password_hashing.png` · **Mục đích:** Giải thích lưu trữ mật khẩu. · **URL:** `/comparison#storage` · **Điều kiện ban đầu:** Database đã seed. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Password storage. · **Inspector cần mở:** Database Inspector nếu có trace secure login. · **Timeline step cần chọn:** Password Processing. · **Nội dung bắt buộc:** Legacy SHA-256 unsalted đối chiếu PBKDF2-SHA256 600000 + unique salt; không full hash. · **Kết quả mong đợi:** Secure route chỉ dùng PBKDF2/check_password_hash. · **Caption báo cáo:** Password hashing legacy và PBKDF2 trong LAB 5. · **Lỗi thường gặp:** Chụp lộ full hash trong terminal. · **Cách làm lại:** Chỉ chụp UI metadata/fingerprint ngắn.

## 30_security_controls.png

**Tên file:** `30_security_controls.png` · **Mục đích:** Tổng hợp defense in depth runtime. · **URL:** `/security-controls` · **Điều kiện ban đầu:** App chạy với config cuối. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Kiểm soát trên nav. · **Inspector cần mở:** Security Control Panel. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Prepared statement, PBKDF2, validation, limit, session, CSP, audit, least privilege và WAF limitation. · **Kết quả mong đợi:** Mỗi control có status/source/route/risk/limit. · **Caption báo cáo:** Security controls phản ánh cấu hình runtime thật. · **Lỗi thường gặp:** Chụp thiếu cột do cửa sổ hẹp. · **Cách làm lại:** Mở rộng cửa sổ hoặc cuộn ngang và ghép trong báo cáo thủ công nếu cần.

## 31_audit_logs.png

**Tên file:** `31_audit_logs.png` · **Mục đích:** Chứng minh logging và monitoring. · **URL:** `/audit-logs` · **Điều kiện ban đầu:** Đã chạy normal, quote, auth logic và expanded search. · **Dữ liệu cần nhập:** Không. · **Nút cần bấm:** Audit trên nav. · **Inspector cần mở:** Bảng Audit Logs. · **Timeline step cần chọn:** Audit Logging nếu mở trace. · **Nội dung bắt buộc:** Action, route, decision, error category, result count và trace ID. · **Kết quả mong đợi:** Không chứa password, cookie hoặc full hash. · **Caption báo cáo:** Audit events đã che dữ liệu nhạy cảm từ các flow thật. · **Lỗi thường gặp:** Bảng trống vì chưa chạy demo flows. · **Cách làm lại:** Chạy các scenario yêu cầu rồi tải lại audit log.

## 32_trace_timeline.png

**Tên file:** `32_trace_timeline.png` · **Mục đích:** Trình bày Action Timeline chi tiết. · **URL:** `/vulnerable/login` · **Điều kiện ban đầu:** Có trace auth logic vulnerable. · **Dữ liệu cần nhập:** Scenario auth logic. · **Nút cần bấm:** Chọn một timeline summary. · **Inspector cần mở:** Timeline. · **Timeline step cần chọn:** Query Construction hoặc Authentication Decision. · **Nội dung bắt buộc:** Step number, timestamp, layer, technique, input/output, code reference, security meaning, status. · **Kết quả mong đợi:** Step mở rộng và progress phản ánh vị trí. · **Caption báo cáo:** Action Timeline từ request đến final verdict. · **Lỗi thường gặp:** Step đang đóng. · **Cách làm lại:** Bấm đúng step để mở chi tiết trước khi chụp.

## 33_presentation_mode.png

**Tên file:** `33_presentation_mode.png` · **Mục đích:** Minh họa chế độ trình chiếu trace hiện có. · **URL:** Trang kết quả có trace. · **Điều kiện ban đầu:** Trace có nhiều steps. · **Dữ liệu cần nhập:** Không thêm input. · **Nút cần bấm:** Presentation Mode, rồi bước sau nếu cần. · **Inspector cần mở:** Timeline. · **Timeline step cần chọn:** Authentication Decision hoặc Result Set. · **Nội dung bắt buộc:** Một step cỡ chữ lớn, progress, nút trước/sau, Auto Play và Chạy lại trace. · **Kết quả mong đợi:** Điều khiển chỉ đổi step, không gửi request. · **Caption báo cáo:** Presentation Mode trình bày một bước của trace thật. · **Lỗi thường gặp:** Nhấn Escape làm thoát trước khi chụp. · **Cách làm lại:** Bật lại mode và chọn step bằng phím mũi tên.

## 34_pytest_passed.png

**Tên file:** `34_pytest_passed.png` · **Mục đích:** Bằng chứng test tự động. · **URL:** Terminal local. · **Điều kiện ban đầu:** Môi trường ảo đã cài requirements. · **Dữ liệu cần nhập:** Lệnh `pytest`. · **Nút cần bấm:** Enter trong terminal. · **Inspector cần mở:** Không. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Lệnh thật, số test collected/passed và không có failure. · **Kết quả mong đợi:** Pytest exit code 0. · **Caption báo cáo:** Kết quả pytest của LAB 5. · **Lỗi thường gặp:** Chụp log cũ hoặc bị cắt dòng summary. · **Cách làm lại:** Chạy lại `pytest` và chụp sau khi lệnh kết thúc.

## 35_coverage.png

**Tên file:** `35_coverage.png` · **Mục đích:** Bằng chứng coverage module lõi. · **URL:** Terminal local. · **Điều kiện ban đầu:** Pytest chạy được. · **Dữ liệu cần nhập:** `pytest --cov=. --cov-report=term-missing`. · **Nút cần bấm:** Enter trong terminal. · **Inspector cần mở:** Không. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** Bảng coverage thật cho các module lõi và dòng TOTAL. · **Kết quả mong đợi:** Các module yêu cầu đạt ngưỡng đề bài. · **Caption báo cáo:** Coverage đo từ test suite LAB 5. · **Lỗi thường gặp:** Chụp con số ghi tay hoặc log chưa hoàn tất. · **Cách làm lại:** Chạy đúng lệnh coverage và chụp output cuối.

## 36_report_files.png

**Tên file:** `36_report_files.png` · **Mục đích:** Xác nhận artifact báo cáo. · **URL:** Thư mục `Lab05/report/`. · **Điều kiện ban đầu:** `scripts/generate_report.py` đã chạy thành công. · **Dữ liệu cần nhập:** Lệnh `python scripts/generate_report.py`. · **Nút cần bấm:** Mở thư mục report sau khi script kết thúc. · **Inspector cần mở:** Không. · **Timeline step cần chọn:** Không. · **Nội dung bắt buộc:** `21127645_LeMinh_Lab05_SQLInjection.docx` và `.pdf`, kích thước file khác 0. · **Kết quả mong đợi:** Cả hai artifact đúng tên và mở được. · **Caption báo cáo:** DOCX và PDF hoàn chỉnh của LAB 5. · **Lỗi thường gặp:** PDF chưa tạo nhưng vẫn chụp tên placeholder. · **Cách làm lại:** Đọc lỗi script, sửa nguyên nhân, tạo lại và mở kiểm tra thật.

## Kiểm tra bộ ảnh

Sau khi chụp đủ ảnh, chạy:

```text
python scripts/check_screenshots.py
```

Checker chỉ kiểm tra tên, PNG signature/IHDR, file rỗng, kích thước, ảnh thiếu/thừa và hash trùng. Checker không dùng OCR, không phân tích nội dung và không tạo ảnh.
