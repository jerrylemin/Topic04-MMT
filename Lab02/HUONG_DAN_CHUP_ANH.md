# Hướng dẫn chụp ảnh thủ công - Lab02 Buffer Overflow

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

## 27_pytest_passed.png

- **Tên file:** `27_pytest_passed.png`
- **Mục đích:** Ghi nhận kết quả kiểm thử tự động thật.
- **Điều kiện ban đầu:** Môi trường WSL đã cài requirements; binary build được.
- **URL hoặc lệnh:** `sh scripts/run_tests.sh` hoặc `pytest`.
- **Dữ liệu nhập:** Bộ test của repo.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** Dòng tổng kết pytest của lần chạy hiện tại; không ghi cứng số test.
- **Kết quả mong đợi:** Chỉ chụp trạng thái pass nếu lệnh thật sự trả exit code 0.
- **Caption báo cáo:** Hình 27. Kết quả pytest của Lab02 trong môi trường WSL.
- **Lỗi thường gặp:** Chụp log cũ hoặc che mất lỗi/exit code.
- **Cách làm lại:** Chạy lại `sh scripts/run_tests.sh`, sửa lỗi nếu có, chỉ chụp khi toàn bộ pass.

## 28_report_files.png

- **Tên file:** `28_report_files.png`
- **Mục đích:** Chứng minh hai artifact báo cáo đã được sinh.
- **Điều kiện ban đầu:** Đã chạy trình tạo báo cáo.
- **URL hoặc lệnh:** `python scripts/generate_report.py` rồi `ls -lh report/`.
- **Dữ liệu nhập:** Ảnh hiện có trong `evidence/screenshots/`; thiếu ảnh dùng placeholder mô tả.
- **Nút cần bấm:** Không.
- **Panel cần mở:** Terminal/file manager local.
- **Bước timeline cần chọn:** Không.
- **Nội dung bắt buộc:** `21127645_LeMinh_Lab02_BufferOverflow.docx` và `.pdf`, kích thước khác 0.
- **Kết quả mong đợi:** Hai file mở được; báo cáo in danh sách ảnh còn thiếu.
- **Caption báo cáo:** Hình 28. Hai file DOCX và PDF được tạo từ cùng dữ liệu báo cáo.
- **Lỗi thường gặp:** Chụp trước khi generation hoàn tất hoặc chỉ có một định dạng.
- **Cách làm lại:** Chạy lại script, đọc lỗi dependency nếu có, xác nhận cả hai file khác 0 rồi chụp.

## Kiểm tra sau khi chụp

```bash
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Script kiểm tra chỉ đọc metadata/PNG/hash, không OCR và không phân tích nội dung. Sau khi thay ảnh, chạy lại trình tạo báo cáo để placeholder được thay bằng ảnh thật.
