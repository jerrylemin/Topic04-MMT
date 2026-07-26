# HƯỚNG DẪN CHỤP ẢNH THỦ CÔNG - LAB02 BUFFER OVERFLOW LOCAL

## 1. Mục đích tài liệu

Tài liệu giúp sinh viên tự cài môi trường, tự chạy lab, tự thực hiện kịch bản và tự chụp bằng chứng thật. Chỉ thao tác trên localhost của repository; không thử trên website/hệ thống thật, không dùng ảnh dựng, Playwright, Selenium, extension/macro chụp tự động hoặc công cụ chỉnh DOM để giả kết quả. Đóng tab riêng tư, không để lộ cookie/token thật, dữ liệu cá nhân, password, session ID hay chữ ký dài.

## 2. Chuẩn bị môi trường từ đầu

Mở Command Prompt tại thư mục repository, vào `Topic04\Lab02`, rồi chạy `scripts\run_lab.bat`. Wrapper gọi PowerShell và WSL Ubuntu để chạy `scripts/run_lab.sh`; terminal Administrator bị từ chối theo source. Trong WSL có thể chạy `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, `make all`, `python app.py`. Khi thấy server tại `http://127.0.0.1:5002`, mở URL đó; dừng bằng `Ctrl+C`. Docker chỉ là phương án phụ trong README và không cần dùng để chụp bộ ảnh này.

### Tài khoản và dữ liệu cố định

Không có đăng nhập. Input bình thường là `Le Minh`; input dài dùng ký tự `A` lặp 64, mode `vulnerable_asan`, `secure_length` hoặc `secure_snprintf`.

## 3. Chuẩn bị trình duyệt và F12

1. Mở Chrome hoặc Microsoft Edge và truy cập đúng URL `127.0.0.1`/`localhost` nêu trong từng ảnh.
2. Nhấn `F12`, chọn menu DevTools > Dock side > Dock to right. Đặt browser zoom 80-100% và kéo vách ngăn để cùng thấy thanh địa chỉ, UI và DevTools.
3. Mở **Network**; bật **Preserve log** khi thao tác có redirect/reload; bật **Disable cache** trong lúc DevTools mở nếu cache làm sai nội dung.
4. Bấm Clear để xóa request cũ trước mỗi kịch bản. Lọc theo route như `login`, `search`, `checkout`, `invoice`, `change-email`, `admin` hoặc `submit`.
5. Chọn đúng request, lần lượt mở **Headers**, **Payload**, **Response** hoặc **Preview**. Mở **Cookies**, **Initiator** hay **Timing** chỉ khi mục ảnh yêu cầu.
6. Dùng **Application/Storage > Cookies** cho cookie; **Elements** cho DOM/form/hidden field; **Console** chỉ quan sát lỗi/trạng thái được yêu cầu, không chạy lệnh đọc cookie; **Sources** chỉ khi cần chứng minh JavaScript client-side.
7. Kéo rộng cột/khung chi tiết, thu gọn panel không liên quan và che value nhạy cảm; không cắt mất URL, status, tên request, tab đang mở hoặc kết quả UI.

## 4. Luồng thao tác theo kịch bản F12

Trước mỗi nhóm: reset đúng cách, đăng nhập đúng tài khoản, chụp trạng thái trước, thực hiện request vulnerable, chụp request/payload/response/trạng thái sau, rồi reset và chạy cùng dữ liệu ở bản secure. Không giả định bước trước còn hiệu lực; kiểm tra lại URL, account và cookie trước từng ảnh.

### F12-01. `29_normal_network_payload.png`

- **Mục tiêu:** Chứng minh request bình thường từ browser tới backend
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `name=Le Minh; mode=vulnerable_asan`
- **Thao tác/nút:** Bấm Gửi dữ liệu
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /submit`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** name `Le Minh`, mode `vulnerable_asan`, Content-Type form
- **Kết quả mong đợi:** Request bình thường được backend nhận
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload HTTP bình thường tới chương trình C
- **Mục báo cáo:** F12 / Normal / Request

### F12-02. `30_normal_network_response.png`

- **Mục tiêu:** Chứng minh response thành công
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `Le Minh`
- **Thao tác/nút:** Chọn POST vừa gửi
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Preview
- **Request cần chọn:** `POST /submit`
- **Trường cần mở:** Response và status
- **Nội dung bắt buộc:** HTTP thành công; trace/HTML có native exit code 0 hoặc trạng thái thực
- **Kết quả mong đợi:** UI hiển thị kết quả xử lý bình thường
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response bình thường từ backend native
- **Mục báo cáo:** F12 / Normal / Response

### F12-03. `31_long_input_network_payload.png`

- **Mục tiêu:** Chứng minh request input dài
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `A lặp 64; mode=vulnerable_asan`
- **Thao tác/nút:** Submit input dài
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload
- **Request cần chọn:** `POST /submit`
- **Trường cần mở:** Form Data
- **Nội dung bắt buộc:** Chuỗi A dài và mode; độ dài 64 thể hiện trong UI/trace
- **Kết quả mong đợi:** Backend nhận input dài có kiểm soát
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Payload 64 byte gửi tới bản vulnerable
- **Mục báo cáo:** F12 / Long input / Request

### F12-04. `32_long_input_network_response.png`

- **Mục tiêu:** Ghi response lỗi hoặc trạng thái backend thực
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `A lặp 64`
- **Thao tác/nút:** Chọn request 64 byte
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Response/Timing
- **Request cần chọn:** `POST /submit`
- **Trường cần mở:** Status, Response, Timing
- **Nội dung bắt buộc:** Response lỗi/ASan/exit/signal/connection state đúng quan sát; không khẳng định crash nếu không thấy
- **Kết quả mong đợi:** Kết quả phản ánh tiến trình C thực
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response của input dài ở bản vulnerable
- **Mục báo cáo:** F12 / Long input / Response

### F12-05. `33_browser_to_c_trace.png`

- **Mục tiêu:** Chứng minh luồng browser → Flask → subprocess → C
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `Trace 64 byte đã có`
- **Thao tác/nút:** Mở Request Inspector và Native Inspector cạnh Network
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Headers; UI Trace
- **Request cần chọn:** `POST /submit`
- **Trường cần mở:** Request URL, mode, trace id và native result
- **Nội dung bắt buộc:** Cùng trace nối request browser với binary/process/exit
- **Kết quả mong đợi:** Luồng web-to-native được đối chiếu
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** UI trace đối chiếu request tới chương trình C
- **Mục báo cáo:** F12 / Trace

### F12-06. `34_secure_length_network_response.png`

- **Mục tiêu:** Chứng minh bản vá length từ chối input dài
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/length`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `A lặp 64; mode=secure_length`
- **Thao tác/nút:** Submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload và Response
- **Request cần chọn:** `POST /secure/length/submit`
- **Trường cần mở:** Form Data; Response
- **Nội dung bắt buộc:** Input length 64; response từ chối/giới hạn trước copy
- **Kết quả mong đợi:** Không overflow ở bản length check
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure_length từ chối input dài
- **Mục báo cáo:** F12 / Secure length

### F12-07. `35_secure_snprintf_network_response.png`

- **Mục tiêu:** Chứng minh bản snprintf xử lý giới hạn
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/snprintf`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `A lặp 64; mode=secure_snprintf`
- **Thao tác/nút:** Submit
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload và Response
- **Request cần chọn:** `POST /secure/snprintf/submit`
- **Trường cần mở:** Form Data; Response
- **Nội dung bắt buộc:** Input dài; response báo reject/truncation theo source
- **Kết quả mong đợi:** Bản vá không ghi vượt buffer
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Response secure_snprintf kiểm soát input dài
- **Mục báo cáo:** F12 / Secure snprintf

### F12-08. `36_patched_request_comparison.png`

- **Mục tiêu:** So sánh cùng input giữa vulnerable và secure
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/comparison`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `A lặp 64`
- **Thao tác/nút:** Giữ Preserve log; gửi lần lượt vulnerable và secure
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network
- **Request cần chọn:** `Ba POST tương ứng`
- **Trường cần mở:** Headers/Payload/Response
- **Nội dung bắt buộc:** Cùng độ dài input; route và response khác nhau
- **Kết quả mong đợi:** Bản vá từ chối hoặc giới hạn có chủ đích
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** So sánh HTTP vulnerable và secure
- **Mục báo cáo:** F12 / Comparison

### F12-09. `37_backend_unavailable_timing.png`

- **Mục tiêu:** Ghi trạng thái nếu backend native không khả dụng
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `Input 64 byte`
- **Thao tác/nút:** Chỉ dùng khi request thực sự lỗi/reset
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Timing/Response
- **Request cần chọn:** `POST /submit`
- **Trường cần mở:** Timing và status
- **Nội dung bắt buộc:** Failed/connection reset/5xx hoặc thông báo binary unavailable đúng thực tế
- **Kết quả mong đợi:** Không diễn giải lỗi giả thành crash
- **Nếu không thấy:** Nếu request trả bình thường, không tạo ảnh giả; dùng ảnh response thực và ghi trạng thái quan sát được.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Trạng thái Network khi backend không trả bình thường
- **Mục báo cáo:** F12 / Error handling

### F12-10. `38_secure_payload_limit.png`

- **Mục tiêu:** Chứng minh giới hạn input ở response secure
- **Trạng thái ban đầu:** Server local đang chạy; xóa request cũ trong Network.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/length`
- **Tài khoản:** N/A
- **Dữ liệu nhập:** `A lặp 256 là tối đa cấu hình; không vượt giới hạn lab`
- **Thao tác/nút:** Submit và chọn request
- **Tab UI:** Trang chức năng tương ứng.
- **Tab F12:** Network > Payload/Response
- **Request cần chọn:** `POST /secure/length/submit`
- **Trường cần mở:** Form Data và Response
- **Nội dung bắt buộc:** Độ dài input; thông báo giới hạn/từ chối; không shellcode
- **Kết quả mong đợi:** Server áp chính sách độ dài
- **Nếu không thấy:** Bật Preserve log, bỏ bộ lọc sai, thực hiện lại thao tác rồi chọn đúng request.
- **Phạm vi ảnh:** Giữ thanh địa chỉ, UI kết quả và vùng DevTools liên quan trong cùng ảnh.
- **Caption:** Giới hạn input của bản vá
- **Mục báo cáo:** F12 / Secure / Limit

## 5. Bảng mô tả ảnh F12

| STT | Tên file | Mục tiêu | Chuẩn bị | URL/lệnh | Dữ liệu và thao tác | F12 cần mở | Nội dung bắt buộc | Kết quả | Caption | Mục báo cáo |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `29_normal_network_payload.png` | Chứng minh request bình thường từ browser tới backend | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/vulnerable` | name=Le Minh; mode=vulnerable_asan; Bấm Gửi dữ liệu | Network > Payload; Form Data | name `Le Minh`, mode `vulnerable_asan`, Content-Type form | Request bình thường được backend nhận | Payload HTTP bình thường tới chương trình C | F12 / Normal / Request |
| 2 | `30_normal_network_response.png` | Chứng minh response thành công | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/vulnerable` | Le Minh; Chọn POST vừa gửi | Network > Response/Preview; Response và status | HTTP thành công; trace/HTML có native exit code 0 hoặc trạng thái thực | UI hiển thị kết quả xử lý bình thường | Response bình thường từ backend native | F12 / Normal / Response |
| 3 | `31_long_input_network_payload.png` | Chứng minh request input dài | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/vulnerable` | A lặp 64; mode=vulnerable_asan; Submit input dài | Network > Payload; Form Data | Chuỗi A dài và mode; độ dài 64 thể hiện trong UI/trace | Backend nhận input dài có kiểm soát | Payload 64 byte gửi tới bản vulnerable | F12 / Long input / Request |
| 4 | `32_long_input_network_response.png` | Ghi response lỗi hoặc trạng thái backend thực | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/vulnerable` | A lặp 64; Chọn request 64 byte | Network > Response/Timing; Status, Response, Timing | Response lỗi/ASan/exit/signal/connection state đúng quan sát; không khẳng định crash nếu không thấy | Kết quả phản ánh tiến trình C thực | Response của input dài ở bản vulnerable | F12 / Long input / Response |
| 5 | `33_browser_to_c_trace.png` | Chứng minh luồng browser → Flask → subprocess → C | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/vulnerable` | Trace 64 byte đã có; Mở Request Inspector và Native Inspector cạnh Network | Network > Headers; UI Trace; Request URL, mode, trace id và native result | Cùng trace nối request browser với binary/process/exit | Luồng web-to-native được đối chiếu | UI trace đối chiếu request tới chương trình C | F12 / Trace |
| 6 | `34_secure_length_network_response.png` | Chứng minh bản vá length từ chối input dài | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/secure/length` | A lặp 64; mode=secure_length; Submit | Network > Payload và Response; Form Data; Response | Input length 64; response từ chối/giới hạn trước copy | Không overflow ở bản length check | Response secure_length từ chối input dài | F12 / Secure length |
| 7 | `35_secure_snprintf_network_response.png` | Chứng minh bản snprintf xử lý giới hạn | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/secure/snprintf` | A lặp 64; mode=secure_snprintf; Submit | Network > Payload và Response; Form Data; Response | Input dài; response báo reject/truncation theo source | Bản vá không ghi vượt buffer | Response secure_snprintf kiểm soát input dài | F12 / Secure snprintf |
| 8 | `36_patched_request_comparison.png` | So sánh cùng input giữa vulnerable và secure | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/comparison` | A lặp 64; Giữ Preserve log; gửi lần lượt vulnerable và secure | Network; Headers/Payload/Response | Cùng độ dài input; route và response khác nhau | Bản vá từ chối hoặc giới hạn có chủ đích | So sánh HTTP vulnerable và secure | F12 / Comparison |
| 9 | `37_backend_unavailable_timing.png` | Ghi trạng thái nếu backend native không khả dụng | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/vulnerable` | Input 64 byte; Chỉ dùng khi request thực sự lỗi/reset | Network > Timing/Response; Timing và status | Failed/connection reset/5xx hoặc thông báo binary unavailable đúng thực tế | Không diễn giải lỗi giả thành crash | Trạng thái Network khi backend không trả bình thường | F12 / Error handling |
| 10 | `38_secure_payload_limit.png` | Chứng minh giới hạn input ở response secure | Server local đang chạy; xóa request cũ trong Network. | `http://127.0.0.1:5002/secure/length` | A lặp 256 là tối đa cấu hình; không vượt giới hạn lab; Submit và chọn request | Network > Payload/Response; Form Data và Response | Độ dài input; thông báo giới hạn/từ chối; không shellcode | Server áp chính sách độ dài | Giới hạn input của bản vá | F12 / Secure / Limit |

## 6. Xử lý lỗi thường gặp

- **Port 5002 bị chiếm:** dừng server lab cũ bằng `Ctrl+C`; dùng `Get-NetTCPConnection -LocalPort 5002 -ErrorAction SilentlyContinue` để xác định tiến trình, không tự đổi port tài liệu.
- **Virtual environment chưa kích hoạt/thiếu dependency:** dùng đúng Python trong `.venv\Scripts\python.exe` và chạy `-m pip install -r requirements.txt`.
- **Database chưa seed/state cũ:** chạy script reset nêu ở mục 2, restart server rồi đăng nhập lại.
- **Cookie/session cũ hoặc sai tài khoản:** logout/reset, chỉ xóa cookie của đúng origin local, mở cửa sổ mới rồi đăng nhập lại.
- **Network không thấy request/bị lọc mất:** bỏ filter, bật Preserve log, bấm Clear rồi thực hiện lại; lưu ý đổi `location.hash` không phát sinh request mới.
- **Payload chưa URL encode:** nhập payload qua form; kiểm tra Request URL encoded và Query String Parameters decoded, không sửa payload sang chuỗi khác.
- **Alert không xuất hiện/redirect làm mất request/cache cũ:** bật Preserve log và Disable cache, reload, reset state rồi lặp lại đúng mode.
- **Server chưa nhận biến môi trường mới:** dừng bằng `Ctrl+C`, chạy lại script; không sửa source để làm khớp ảnh.
- **Ảnh nhỏ/bị cắt:** dock phải, giảm zoom, mở rộng trường cần đọc; giữ URL, request, status và UI kết quả.

## 7. Checklist cuối lab

- [ ] Server chạy đúng localhost và port.
- [ ] Đúng tài khoản/dữ liệu local; đủ ảnh theo manifest và đúng tên file.
- [ ] Ảnh có URL/lệnh, kết quả UI và đúng request/tab/field F12.
- [ ] Cookie/token/session/chữ ký dài đã che; vulnerable và secure tách biệt.
- [ ] Caption khớp báo cáo; không có ảnh trùng/ảnh giả/ảnh chụp tự động.
- [ ] Không chạy lại pytest/smoke test/Docker để tạo ảnh; ảnh test cũ (nếu có) chỉ là bằng chứng tùy chọn.
- [ ] Chỉ tạo DOCX; không tạo, cập nhật, mở hoặc render PDF.
- [ ] Chạy `python scripts/check_screenshots.py` khi sinh viên đã tự chụp đủ ảnh, rồi `python scripts/generate_report.py` để tạo DOCX.

## 8. Phụ lục hướng dẫn bộ ảnh hiện có

Các tên ảnh cũ được giữ để không phá vỡ quy trình hiện có. Thực hiện theo mô tả dưới đây; ảnh test cũ là tùy chọn và ảnh report chỉ cần chứng minh DOCX.

Chỉ chụp thủ công trong lab local. Lưu PNG vào `evidence/screenshots/`, tên không dấu/không khoảng trắng, kích thước tối thiểu 1024x600, chữ đọc được, không có cookie/secret/dữ liệu cá nhân. Thanh địa chỉ phải là `http://127.0.0.1:5002`; không chụp website hay IP bên ngoài. Không dùng Playwright, Selenium, OCR hoặc ảnh giả.

Trước mỗi ảnh UI: chạy app, mở đúng URL, thu gọn dữ liệu không liên quan, đặt zoom 100%, rồi chỉ chụp vùng đủ chứng minh yêu cầu. Trước ảnh terminal: đứng tại `Lab02`, dùng cửa sổ đủ rộng và không hiển thị đường dẫn home nếu không cần thiết.

## 01_home_overview.png

- **Tên file:** `01_home_overview.png`
- **Mục đích:** Tổng quan mục tiêu, kiến trúc ba tầng và các mode.
- **Điều kiện ban đầu:** App đang chạy, chưa cần trace.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/`
- **Dữ liệu nhập:** Không.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Khối kiến trúc/chế độ thực hành.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Mục tiêu lab; Browser -> Flask -> C; vulnerable, ASan, hai bản vá, hardened.
- **Kết quả mong đợi:** Trang chủ hiển thị đầy đủ và không lỗi.
- **Caption báo cáo:** Hình 1. Tổng quan kiến trúc và các chế độ thực hành của Lab02.
- **Lỗi thường gặp:** Chụp thiếu danh sách mode hoặc URL dùng `localhost`.
- **Cách làm lại:** Tải lại `/`, cuộn tới vị trí thấy cả mục tiêu và kiến trúc, xác nhận URL `127.0.0.1`.

## 02_normal_input_before_submit.png

- **Tên file:** `02_normal_input_before_submit.png`
- **Mục đích:** Ghi nhận input bình thường trước khi gửi.
- **Điều kiện ban đầu:** Mở trang vulnerable, chọn `vulnerable_asan`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `Le Minh`.
- **Nút cần bấm:** Chưa bấm Gửi.
- **Panel cần mở:** Form nhập liệu.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** `Le Minh`, mode, giới hạn input và nút gửi.
- **Kết quả mong đợi:** Form sẵn sàng, chưa có kết quả native mới.
- **Caption báo cáo:** Hình 2. Input bình thường trước khi gửi tới backend native.
- **Lỗi thường gặp:** Gửi form trước khi chụp hoặc lộ dữ liệu khác.
- **Cách làm lại:** Tải lại `/vulnerable`, nhập lại đúng chuỗi rồi chụp trước khi bấm.

## 03_normal_http_request.png

- **Tên file:** `03_normal_http_request.png`
- **Mục đích:** Chứng minh request POST local.
- **Điều kiện ban đầu:** Đã gửi `Le Minh` thành công.
- **URL hoặc lệnh:** `POST http://127.0.0.1:5002/submit`
- **Dữ liệu nhập:** `Le Minh`, mode `vulnerable_asan`.
- **Nút cần bấm:** Gửi; mở Request Inspector.
- **Panel cần mở:** Request Inspector.
- **Bước timeline cần chọn:** Bước Browser tạo HTTP request.
- **Nội dung bắt buộc:** Method POST, path `/submit`, Content-Type, name length, mode.
- **Kết quả mong đợi:** Inspector chỉ ra request local đúng route.
- **Caption báo cáo:** Hình 3. HTTP POST `/submit` với input bình thường.
- **Lỗi thường gặp:** Panel đóng hoặc ảnh chứa cookie đầy đủ.
- **Cách làm lại:** Chạy lại `Le Minh`, mở inspector, che thông tin không thuộc bài.

## 04_normal_native_process.png

- **Tên file:** `04_normal_native_process.png`
- **Mục đích:** Chứng minh tiến trình C kết thúc bình thường.
- **Điều kiện ban đầu:** Trace `Le Minh` đã hoàn tất.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `Le Minh`.
- **Nút cần bấm:** Mở Native Process Inspector.
- **Panel cần mở:** Native Process Inspector.
- **Bước timeline cần chọn:** Kết quả native.
- **Nội dung bắt buộc:** Binary/profile, PID, exit code 0, stdout `Processed name: Le Minh`, ASan false.
- **Kết quả mong đợi:** Không signal, không crash.
- **Caption báo cáo:** Hình 4. Tiến trình native xử lý input bình thường với exit code 0.
- **Lỗi thường gặp:** Dùng kết quả cũ hoặc không thấy exit code.
- **Cách làm lại:** Gửi lại `Le Minh`, chờ trace hoàn tất rồi mở panel.

## 05_normal_memory_visualizer.png

- **Tên file:** `05_normal_memory_visualizer.png`
- **Mục đích:** Minh họa dữ liệu nằm trong `name[32]`.
- **Điều kiện ban đầu:** Có trace input `Le Minh`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `Le Minh` (7 byte ASCII).
- **Nút cần bấm:** Mở Memory Visualizer.
- **Panel cần mở:** Memory Visualizer.
- **Bước timeline cần chọn:** Memory boundary.
- **Nội dung bắt buộc:** 7 byte dữ liệu, null terminator, buffer 32 byte, overflow 0.
- **Kết quả mong đợi:** Không ô đỏ ngoài buffer.
- **Caption báo cáo:** Hình 5. Mô hình bộ nhớ với input bình thường, không overflow.
- **Lỗi thường gặp:** Visualizer đang hiển thị trace 64 byte.
- **Cách làm lại:** Chọn đúng trace `Le Minh` hoặc gửi lại rồi mở visualizer.

## 06_overflow_32_input.png

- **Tên file:** `06_overflow_32_input.png`
- **Mục đích:** Chứng minh ranh giới chuỗi C 32 byte.
- **Điều kiện ban đầu:** Trang vulnerable, chưa gửi.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (32 ký tự ASCII).
- **Nút cần bấm:** Có thể chọn mẫu 32; chưa cần gửi khi chụp form.
- **Panel cần mở:** Giải thích giới hạn/null terminator.
- **Bước timeline cần chọn:** Browser nhận input nếu đã gửi.
- **Nội dung bắt buộc:** 32 ký tự/32 byte, safe capacity 31, cần thêm null terminator.
- **Kết quả mong đợi:** UI cảnh báo đã vượt khả năng chứa chuỗi an toàn.
- **Caption báo cáo:** Hình 6. Input 32 byte chạm buffer nhưng còn cần một byte null.
- **Lỗi thường gặp:** Chuỗi không đủ 32 hoặc dùng Unicode làm số byte khác số ký tự.
- **Cách làm lại:** Dùng nút mẫu 32 ký tự `A`, kiểm tra bộ đếm byte.

## 07_overflow_32_memory_boundary.png

- **Tên file:** `07_overflow_32_memory_boundary.png`
- **Mục đích:** Thể hiện ít nhất một byte ghi vượt vì null terminator.
- **Điều kiện ban đầu:** Đã gửi 32 ký tự ASCII ở mode ASan.
- **URL hoặc lệnh:** `POST http://127.0.0.1:5002/submit`
- **Dữ liệu nhập:** `A` lặp 32.
- **Nút cần bấm:** Gửi; mở Memory Visualizer.
- **Panel cần mở:** Memory Visualizer.
- **Bước timeline cần chọn:** Memory boundary.
- **Nội dung bắt buộc:** 32 byte trong buffer, null terminator ngoài biên, overflow tối thiểu 1 byte.
- **Kết quả mong đợi:** Có vùng đỏ ngoài `name[32]`; không khẳng định luôn crash.
- **Caption báo cáo:** Hình 7. Ghi vượt tối thiểu một byte tại ranh giới 32 byte.
- **Lỗi thường gặp:** Caption nói 32 byte luôn crash.
- **Cách làm lại:** Gửi đúng 32 byte, mở đúng bước boundary và giữ phần chú thích phụ thuộc môi trường.

## 08_overflow_64_request.png

- **Tên file:** `08_overflow_64_request.png`
- **Mục đích:** Ghi nhận request dài có kiểm soát.
- **Điều kiện ban đầu:** Chọn `vulnerable_asan`.
- **URL hoặc lệnh:** `POST http://127.0.0.1:5002/submit`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Chọn mẫu 64; Gửi; mở Request Inspector.
- **Panel cần mở:** Request Inspector.
- **Bước timeline cần chọn:** Browser tạo HTTP request.
- **Nội dung bắt buộc:** POST `/submit`, mode ASan, 64 ký tự và 64 byte.
- **Kết quả mong đợi:** Request được gateway nhận trong giới hạn lab.
- **Caption báo cáo:** Hình 8. Request 64 byte gửi tới binary AddressSanitizer.
- **Lỗi thường gặp:** Chọn `vulnerable_debug` hoặc input không đủ 64.
- **Cách làm lại:** Chọn lại mode ASan, dùng preset 64 và gửi một lần.

## 09_overflow_64_strcpy_step.png

- **Tên file:** `09_overflow_64_strcpy_step.png`
- **Mục đích:** Chỉ ra nguyên nhân ở `strcpy`.
- **Điều kiện ban đầu:** Trace 64 byte đã có.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Chọn bước `strcpy` trong timeline.
- **Panel cần mở:** Timeline/code reference.
- **Bước timeline cần chọn:** `strcpy bắt đầu copy`.
- **Nội dung bắt buộc:** `strcpy` không nhận kích thước đích, copy tới null, buffer 32 byte.
- **Kết quả mong đợi:** Giải thích nguyên nhân, không có hướng dẫn khai thác.
- **Caption báo cáo:** Hình 9. Bước `strcpy` sao chép không biết kích thước buffer đích.
- **Lỗi thường gặp:** Chụp bước HTTP thay vì bước copy.
- **Cách làm lại:** Dùng điều hướng timeline tới đúng tiêu đề `strcpy`.

## 10_overflow_64_memory_visualizer.png

- **Tên file:** `10_overflow_64_memory_visualizer.png`
- **Mục đích:** So sánh 32 byte buffer với vùng overflow.
- **Điều kiện ban đầu:** Trace 64 byte đã hoàn tất.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Mở Memory Visualizer.
- **Panel cần mở:** Memory Visualizer.
- **Bước timeline cần chọn:** Memory boundary.
- **Nội dung bắt buộc:** 32 byte trong buffer, 32 byte dữ liệu vượt tiếp theo, null sau chuỗi, chú thích mô hình giáo dục.
- **Kết quả mong đợi:** Vùng overflow màu đỏ rõ ràng.
- **Caption báo cáo:** Hình 10. Mô hình buffer 32 byte và vùng ghi vượt với input 64 byte.
- **Lỗi thường gặp:** Cắt mất legend hoặc khẳng định layout tuyệt đối.
- **Cách làm lại:** Mở rộng panel, chụp cả legend và ghi chú phụ thuộc compiler/ABI.

## 11_asan_detected.png

- **Tên file:** `11_asan_detected.png`
- **Mục đích:** Chứng minh sanitizer phát hiện lỗi thật.
- **Điều kiện ban đầu:** Đã chạy 64 byte bằng `vulnerable_asan`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Mở ASan Inspector.
- **Panel cần mở:** ASan Inspector.
- **Bước timeline cần chọn:** Kết quả native.
- **Nội dung bắt buộc:** `stack-buffer-overflow`, detected true, buffer `name`, input 64 byte.
- **Kết quả mong đợi:** ASan dừng tiến trình với lỗi đã parse.
- **Caption báo cáo:** Hình 11. AddressSanitizer phát hiện stack-buffer-overflow.
- **Lỗi thường gặp:** Binary chưa build ASan hoặc panel không có báo cáo.
- **Cách làm lại:** `make vulnerable_asan`, gửi lại 64 byte, chỉ chụp khi log thật xuất hiện.

## 12_asan_stack_trace.png

- **Tên file:** `12_asan_stack_trace.png`
- **Mục đích:** Gắn lỗi với file, hàm và dòng mã.
- **Điều kiện ban đầu:** ASan Inspector có log 64 byte.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Mở chi tiết stack trace.
- **Panel cần mở:** ASan Inspector.
- **Bước timeline cần chọn:** ASan abort/native result.
- **Nội dung bắt buộc:** `native/vulnerable_processor.c`, `process_name`, dòng chứa `strcpy`; đường dẫn home đã che.
- **Kết quả mong đợi:** Trace đủ định vị nguồn, không lộ đường dẫn cá nhân.
- **Caption báo cáo:** Hình 12. Stack trace ASan định vị lệnh `strcpy` trong `process_name`.
- **Lỗi thường gặp:** Chụp log có đường dẫn home đầy đủ.
- **Cách làm lại:** Dùng panel đã redact hoặc cắt phần đường dẫn ngoài Lab02.

## 13_native_crash_result.png

- **Tên file:** `13_native_crash_result.png`
- **Mục đích:** Ghi nhận trạng thái dừng của native process.
- **Điều kiện ban đầu:** Trace ASan 64 byte hoàn tất.
- **URL hoặc lệnh:** `POST http://127.0.0.1:5002/submit`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Mở Native Process Inspector.
- **Panel cần mở:** Native Process Inspector.
- **Bước timeline cần chọn:** Kết quả native.
- **Nội dung bắt buộc:** Exit code khác 0 hoặc signal thực tế, ASan status, timeout false.
- **Kết quả mong đợi:** UI mô tả dừng có kiểm soát, không bịa signal.
- **Caption báo cáo:** Hình 13. Kết quả tiến trình native dừng sau phát hiện lỗi.
- **Lỗi thường gặp:** Ghi signal dự đoán thay vì giá trị inspector.
- **Cách làm lại:** Chạy lại và chụp đúng giá trị native trả về trong phiên đó.

## 14_final_vulnerable_verdict.png

- **Tên file:** `14_final_vulnerable_verdict.png`
- **Mục đích:** Tổng kết overflow, phát hiện và nguyên nhân.
- **Điều kiện ban đầu:** Có trace 64 byte.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Mở Final Security Verdict.
- **Panel cần mở:** Final Security Verdict.
- **Bước timeline cần chọn:** Bước cuối.
- **Nội dung bắt buộc:** Overflow có, ASan có, crash/dừng theo kết quả thật, nguyên nhân `strcpy`, gợi ý hai bản vá.
- **Kết quả mong đợi:** Kết luận không mô tả khai thác thực thi mã.
- **Caption báo cáo:** Hình 14. Kết luận bảo mật cho phiên bản vulnerable với input 64 byte.
- **Lỗi thường gặp:** Chỉ có màu trạng thái nhưng thiếu nguyên nhân.
- **Cách làm lại:** Mở toàn bộ verdict và chụp đủ phần nguyên nhân/khuyến nghị.

## 15_length_test_table.png

- **Tên file:** `15_length_test_table.png`
- **Mục đích:** Ghi nhận nhiều độ dài thử và phân biệt các ngưỡng.
- **Điều kiện ban đầu:** App đang chạy; binary đã build.
- **URL hoặc lệnh:** `python scripts/test_lengths.py`
- **Dữ liệu nhập:** Các độ dài 1, 8, 16, 24, 31, 32, 33, 40, 48, 56, 64, 80, 96, 128, 192, 256.
- **Nút cần bấm:** Không; chạy lệnh trong terminal.
- **Panel cần mở:** Bảng UI nếu có hoặc terminal output thật.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Length, HTTP status, exit/signal, ASan/crash; không suy diễn ngưỡng chưa quan sát.
- **Kết quả mong đợi:** Có bảng kết quả từ lần chạy hiện tại.
- **Caption báo cáo:** Hình 15. Kết quả kiểm thử có kiểm soát theo độ dài input.
- **Lỗi thường gặp:** App chưa chạy hoặc terminal cắt mất cột.
- **Cách làm lại:** Khởi động app, mở rộng terminal, chạy lại script rồi chụp kết quả đầy đủ.

## 16_gdb_breakpoint.png

- **Tên file:** `16_gdb_breakpoint.png`
- **Mục đích:** Chứng minh GDB dừng tại `process_name`.
- **Điều kiện ban đầu:** WSL/Docker có GDB; `make vulnerable_debug`; `ulimit -c 0`.
- **URL hoặc lệnh:** `gdb -q -x gdb/inspect_normal.gdb`
- **Dữ liệu nhập:** `Le Minh`.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal GDB.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Breakpoint tại `process_name`, file/dòng nguồn và trạng thái stopped.
- **Kết quả mong đợi:** GDB dừng trước copy trong binary debug.
- **Caption báo cáo:** Hình 16. GDB dừng tại breakpoint của hàm `process_name`.
- **Lỗi thường gặp:** Chạy binary ASan hoặc không đứng tại Lab02.
- **Cách làm lại:** Build `vulnerable_debug`, `cd Lab02`, chạy lại script GDB.

## 17_gdb_local_buffer.png

- **Tên file:** `17_gdb_local_buffer.png`
- **Mục đích:** Quan sát buffer local và kích thước.
- **Điều kiện ban đầu:** Đang dừng ở breakpoint phiên normal.
- **URL hoặc lệnh:** `info locals`, `p sizeof(name)`, `x/64bx &name`.
- **Dữ liệu nhập:** `Le Minh`.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal GDB.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Local `name`, `sizeof(name) = 32` hoặc vùng byte quanh `name`; địa chỉ chỉ ở terminal local.
- **Kết quả mong đợi:** Xác nhận buffer cục bộ 32 byte.
- **Caption báo cáo:** Hình 17. Biến local `name[32]` trong stack frame quan sát bằng GDB.
- **Lỗi thường gặp:** Chụp địa chỉ ngoài GDB vào giao diện web.
- **Cách làm lại:** Chỉ chụp terminal GDB local, không sao chép địa chỉ vào UI/report text.

## 18_gdb_overflow_stop.png

- **Tên file:** `18_gdb_overflow_stop.png`
- **Mục đích:** Ghi nhận signal/backtrace thực tế với 64 byte.
- **Điều kiện ban đầu:** `make vulnerable_debug`; core dump tắt.
- **URL hoặc lệnh:** `gdb -q -x gdb/inspect_overflow.gdb`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal GDB.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Signal hoặc trạng thái dừng thật và `backtrace`; không sửa thanh ghi.
- **Kết quả mong đợi:** Có bằng chứng quan sát; nếu môi trường không crash phải ghi đúng như vậy.
- **Caption báo cáo:** Hình 18. Trạng thái dừng và backtrace của phiên overflow trong GDB.
- **Lỗi thường gặp:** Dùng log cũ hoặc tự ghi signal dự đoán.
- **Cách làm lại:** Xóa màn hình, chạy đúng script và chụp kết quả phiên mới.

## 19_secure_length_reject.png

- **Tên file:** `19_secure_length_reject.png`
- **Mục đích:** Chứng minh bản vá từ chối trước copy.
- **Điều kiện ban đầu:** Binary `secure_length` đã build.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/length`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Gửi.
- **Panel cần mở:** Native result/final verdict.
- **Bước timeline cần chọn:** Validation rejected.
- **Nội dung bắt buộc:** Giới hạn 31 byte, exit code 65, không copy, không memory corruption.
- **Kết quả mong đợi:** Request được xử lý có kiểm soát, native không crash.
- **Caption báo cáo:** Hình 19. Bản vá kiểm tra độ dài từ chối input 64 byte trước copy.
- **Lỗi thường gặp:** Chụp route vulnerable hoặc input 31 byte.
- **Cách làm lại:** Mở đúng route secure length, dùng preset 64 rồi gửi lại.

## 20_secure_length_timeline.png

- **Tên file:** `20_secure_length_timeline.png`
- **Mục đích:** Minh họa defense in depth tại C.
- **Điều kiện ban đầu:** Trace secure length 64 byte đã có.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/length`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Điều hướng timeline.
- **Panel cần mở:** Timeline.
- **Bước timeline cần chọn:** `strnlen`/so sánh với 31/reject.
- **Nội dung bắt buộc:** Đo byte, so sánh safe capacity, từ chối trước `memcpy`, không ghi buffer.
- **Kết quả mong đợi:** Luồng vá rõ ràng độc lập với validation Flask.
- **Caption báo cáo:** Hình 20. Timeline bản vá kiểm tra độ dài trước thao tác copy.
- **Lỗi thường gặp:** Chụp bước sau copy hoặc chỉ có giới hạn frontend.
- **Cách làm lại:** Chọn đúng bước native validation và mở phần kỹ thuật/ý nghĩa bảo mật.

## 21_secure_snprintf_reject.png

- **Tên file:** `21_secure_snprintf_reject.png`
- **Mục đích:** Chứng minh phát hiện truncate qua return value.
- **Điều kiện ban đầu:** Binary `secure_snprintf` đã build.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/snprintf`
- **Dữ liệu nhập:** `A` lặp 64.
- **Nút cần bấm:** Gửi; mở timeline/result.
- **Panel cần mở:** Native Inspector hoặc Final Verdict.
- **Bước timeline cần chọn:** Kiểm tra return value `snprintf`.
- **Nội dung bắt buộc:** `sizeof(name)=32`, phát hiện truncate, exit code 67, không chấp nhận truncate âm thầm.
- **Kết quả mong đợi:** Input bị từ chối, không overflow/crash.
- **Caption báo cáo:** Hình 21. Bản vá `snprintf` phát hiện và từ chối dữ liệu bị truncate.
- **Lỗi thường gặp:** Chỉ nói `snprintf` an toàn mà thiếu return value.
- **Cách làm lại:** Mở đúng bước kiểm tra `written >= sizeof(name)` và chụp cả kết quả.

## 22_code_comparison.png

- **Tên file:** `22_code_comparison.png`
- **Mục đích:** So sánh ba chiến lược xử lý chuỗi.
- **Điều kiện ban đầu:** App đang chạy.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/comparison`
- **Dữ liệu nhập:** Không.
- **Nút cần bấm:** Mở So sánh mã nguồn nếu đi từ workbench.
- **Panel cần mở:** Code Comparison.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** `strcpy`, `strnlen` + giới hạn 31, `snprintf` + kiểm tra return value.
- **Kết quả mong đợi:** Ba cột đọc được, nêu null terminator và byte UTF-8.
- **Caption báo cáo:** Hình 22. So sánh mã nguồn vulnerable và hai bản vá.
- **Lỗi thường gặp:** Cắt mất điều kiện return của `snprintf`.
- **Cách làm lại:** Giảm zoom vừa đủ để thấy trọn ba cột nhưng chữ vẫn đọc được.

## 23_hardening_comparison.png

- **Tên file:** `23_hardening_comparison.png`
- **Mục đích:** So sánh thuộc tính binary lấy từ công cụ thật.
- **Điều kiện ban đầu:** `make all`; công cụ `file/readelf/objdump` có sẵn.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/hardening`
- **Dữ liệu nhập:** Không.
- **Nút cần bấm:** Làm mới build info nếu có.
- **Panel cần mở:** Hardening Inspector.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Canary, PIE, RELRO, NX, FORTIFY cho các binary; trạng thái từ kiểm tra thật.
- **Kết quả mong đợi:** Có bảng so sánh, không ghi cứng.
- **Caption báo cáo:** Hình 23. So sánh thuộc tính hardening của các binary đã build.
- **Lỗi thường gặp:** Binary chưa build nên toàn bộ trạng thái unknown.
- **Cách làm lại:** Chạy `make all`, reload trang hardening và chụp lại kết quả thu thập mới.

## 24_stack_canary_explanation.png

- **Tên file:** `24_stack_canary_explanation.png`
- **Mục đích:** Giải thích vị trí khái niệm và vai trò canary.
- **Điều kiện ban đầu:** Trang hardening mở.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/hardening`
- **Dữ liệu nhập:** Không.
- **Nút cần bấm:** Mở giải thích Stack Canary.
- **Panel cần mở:** Stack/Hardening explanation.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Canary giữa local data và control data ở mức khái niệm; kiểm tra trước return; cảnh báo layout phụ thuộc compiler.
- **Kết quả mong đợi:** Không mô tả cách vượt qua canary.
- **Caption báo cáo:** Hình 24. Vị trí khái niệm và cơ chế phát hiện của Stack Canary.
- **Lỗi thường gặp:** Sơ đồ được mô tả như layout tuyệt đối.
- **Cách làm lại:** Chụp cả ghi chú mô hình giáo dục/phụ thuộc ABI và compiler.

## 25_asan_vs_hardening.png

- **Tên file:** `25_asan_vs_hardening.png`
- **Mục đích:** Phân biệt công cụ kiểm thử với cơ chế production.
- **Điều kiện ban đầu:** Trang hardening mở.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/hardening`
- **Dữ liệu nhập:** Không.
- **Nút cần bấm:** Mở bảng ASan vs Hardening.
- **Panel cần mở:** Bảng so sánh.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** ASan dùng phát hiện trong test; canary/PIE/RELRO/NX/FORTIFY giảm rủi ro; không thay secure coding.
- **Kết quả mong đợi:** Hai vai trò được phân biệt rõ.
- **Caption báo cáo:** Hình 25. Phân biệt AddressSanitizer và compiler/OS hardening.
- **Lỗi thường gặp:** Gọi ASan là biện pháp production hoặc hardening là bản vá `strcpy`.
- **Cách làm lại:** Mở đúng bảng so sánh và chụp cả dòng giới hạn.

## 26_presentation_mode.png

- **Tên file:** `26_presentation_mode.png`
- **Mục đích:** Minh họa chế độ trình bày từng bước.
- **Điều kiện ban đầu:** Có một trace; ưu tiên `Le Minh` để tránh lặp crash.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu nhập:** Trace `Le Minh` đã có.
- **Nút cần bấm:** Bật Presentation Mode; Next/Previous nếu cần.
- **Panel cần mở:** Timeline toàn màn hình.
- **Bước timeline cần chọn:** Một bước bất kỳ có chữ lớn, ví dụ Flask chuẩn bị subprocess.
- **Nội dung bắt buộc:** Một bước duy nhất, progress bar, Previous/Next/Replay và chữ lớn.
- **Kết quả mong đợi:** Auto Play chỉ phát trace hiện có, không gửi request mới.
- **Caption báo cáo:** Hình 26. Presentation Mode trình bày một bước của trace với chữ lớn.
- **Lỗi thường gặp:** Auto Play gửi lại request hoặc chụp nhiều bước chồng nhau.
- **Cách làm lại:** Dừng Auto Play, chọn một trace có sẵn và chụp một bước rõ ràng.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.

> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
- **Mục đích:** Ghi nhận kết quả kiểm thử tự động thật.
- **Điều kiện ban đầu:** Môi trường WSL đã cài requirements; binary build được.
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
- **Dữ liệu nhập:** Bộ test của repo.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal.
- **Bước timeline cần chọn:** Không.
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
- **Kết quả mong đợi:** Chỉ chụp trạng thái pass nếu lệnh thật sự trả exit code 0.
> Bằng chứng test/coverage cũ là tùy chọn; không chạy lại để phục vụ nhiệm vụ cập nhật tài liệu này.
- **Lỗi thường gặp:** Chụp log cũ hoặc che mất lỗi/exit code.
- **Cách làm lại:** Chạy lại `sh scripts/run_tests.sh`, sửa lỗi nếu có, chỉ chụp khi toàn bộ pass.

## 28_report_files.png

- **Tên file:** `28_report_files.png`
- **Mục đích:** Chứng minh artifact DOCX báo cáo đã được sinh.
- **Điều kiện ban đầu:** Đã chạy trình tạo báo cáo.
- **URL hoặc lệnh:** `python scripts/generate_report.py` rồi `ls -lh report/`.
- **Dữ liệu nhập:** Ảnh hiện có trong `evidence/screenshots/`; thiếu ảnh dùng placeholder mô tả.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal/file manager local.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** `21127645_LeMinh_21127224_NguyenVuBach_Lab02_BufferOverflow.docx`, kích thước khác 0.
- **Kết quả mong đợi:** File DOCX mở được; báo cáo in danh sách ảnh còn thiếu.
- **Caption báo cáo:** Hình 28. Hai file DOCX được tạo từ cùng dữ liệu báo cáo.
- **Lỗi thường gặp:** Chụp trước khi generation hoàn tất hoặc chỉ có một định dạng.
- **Cách làm lại:** Chạy lại script, đọc lỗi dependency nếu có, xác nhận cả hai file khác 0 rồi chụp.

## Kiểm tra sau khi chụp

```bash
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Script kiểm tra chỉ đọc metadata/PNG/hash, không OCR và không phân tích nội dung. Sau khi thay ảnh, chạy lại trình tạo báo cáo để placeholder được thay bằng ảnh thật.
### Bằng chứng cũ tùy chọn

- `27_pytest_passed.png`: giữ tên để tương thích manifest cũ; không chạy lại pytest cho nhiệm vụ này. Chỉ dùng nếu ảnh thật đã có từ trước.
