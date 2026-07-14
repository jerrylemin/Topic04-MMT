# Hướng dẫn chụp ảnh Lab02

## 1. Chuẩn bị

Build/chạy binary Linux trong Ubuntu/WSL hoặc Docker; không chạy binary Linux bằng Windows Python. Chỉ dùng `http://127.0.0.1:5002`, input kiểm thử local và chụp thủ công. Lưu PNG tối thiểu 1024x600 vào `evidence/screenshots/`. Có thể ghép UI với inspector/terminal nếu chữ đọc được. Trước mỗi ảnh chọn đúng profile; GDB phải chạy trong phiên local mới.

## 2. Danh sách ảnh cần chụp

`01_normal_input.png`, `02_overflow_http_crash.png`, `03_asan_log.png`, `04_gdb_backtrace.png`, `05_length_thresholds.png`, `06_length_fix.png`, `07_snprintf_fix.png`, `08_hardening.png`, `09_tests_reports.png`.

## 3. Cách chụp từng ảnh

### 01_normal_input.png
- **Tên file:** `01_normal_input.png`
- **Mục đích:** Chứng minh input ngắn qua HTTP và native thành công.
- **Trạng thái ban đầu:** Đã build và chạy app; chọn `vulnerable_debug`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu cần nhập:** `Le Minh`.
- **Nút cần bấm:** Submit/Gửi.
- **Tab DevTools hoặc inspector cần mở:** Request và Native Process Inspector.
- **Nội dung bắt buộc phải xuất hiện:** POST, input ngắn, exit/stdout thật, không overflow.
- **Kết quả đúng:** Tiến trình xử lý thành công và không crash.
- **Caption dùng trong báo cáo:** Input bình thường đi qua HTTP và tiến trình native thành công.

Bước 1. Mở URL. Bước 2. Nhập `Le Minh`. Bước 3. Bấm **Submit**. Bước 4. Mở hai inspector. Bước 5. Chụp UI và kết quả. Bước 6. Lưu đúng tên.

### 02_overflow_http_crash.png
- **Tên file:** `02_overflow_http_crash.png`
- **Mục đích:** Chứng minh input dài làm bản vulnerable dừng/crash có kiểm soát.
- **Trạng thái ban đầu:** Chọn `vulnerable_asan` hoặc `vulnerable_debug`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/vulnerable`
- **Dữ liệu cần nhập:** 64 ký tự `A`.
- **Nút cần bấm:** Submit/Gửi.
- **Tab DevTools hoặc inspector cần mở:** Request và Native Process/Final Verdict.
- **Nội dung bắt buộc phải xuất hiện:** POST length=64 và exit/signal/crash thực tế.
- **Kết quả đúng:** Tiến trình vulnerable bị dừng; Flask vẫn hoạt động.
- **Caption dùng trong báo cáo:** Input 64 byte qua HTTP kích hoạt lỗi trong backend native vulnerable.

Bước 1. Chọn profile. Bước 2. Nhập 64 `A`. Bước 3. Bấm **Submit**. Bước 4. Mở Request/Native. Bước 5. Chụp length và trạng thái dừng. Bước 6. Lưu đúng tên.

### 03_asan_log.png
- **Tên file:** `03_asan_log.png`
- **Mục đích:** Định vị ghi vượt buffer bằng stderr thật.
- **Trạng thái ban đầu:** Vừa chạy ảnh 02 bằng `vulnerable_asan`.
- **URL hoặc lệnh:** ASan Inspector/evidence ASan từ lần chạy thật.
- **Dữ liệu cần nhập:** Trace 64 ký tự `A`.
- **Nút cần bấm:** Mở ASan Inspector/stack trace.
- **Tab DevTools hoặc inspector cần mở:** ASan Inspector.
- **Nội dung bắt buộc phải xuất hiện:** `stack-buffer-overflow`, WRITE, `process_name/strcpy`, file và dòng.
- **Kết quả đúng:** ASan báo ghi vượt `name[32]`.
- **Caption dùng trong báo cáo:** ASan phát hiện stack-buffer-overflow tại thao tác strcpy.

Bước 1. Giữ trace ảnh 02. Bước 2. Không nhập lại. Bước 3. Bấm mở ASan. Bước 4. Mở stack trace. Bước 5. Chụp loại lỗi/hàm/dòng. Bước 6. Lưu đúng tên.

### 04_gdb_backtrace.png
- **Tên file:** `04_gdb_backtrace.png`
- **Mục đích:** Chứng minh stack frame/backtrace từ binary debug.
- **Trạng thái ban đầu:** Mở WSL/Docker tại Lab02, đã `make all`.
- **URL hoặc lệnh:** `gdb -q -x gdb/inspect_overflow.gdb`
- **Dữ liệu cần nhập:** Input local do script GDB cung cấp.
- **Nút cần bấm:** Enter/continue theo script.
- **Tab DevTools hoặc inspector cần mở:** Terminal GDB.
- **Nội dung bắt buộc phải xuất hiện:** Điểm dừng/signal, frame `process_name`, `name[32]` hoặc backtrace.
- **Kết quả đúng:** GDB định vị lỗi mà không sửa thanh ghi/luồng điều khiển.
- **Caption dùng trong báo cáo:** GDB xác nhận vị trí lỗi và backtrace của phiên overflow local.

Bước 1. Mở terminal WSL. Bước 2. Nhập lệnh GDB. Bước 3. Chạy/continue. Bước 4. Hiện frame/backtrace. Bước 5. Chụp terminal. Bước 6. Lưu đúng tên.

### 05_length_thresholds.png
- **Tên file:** `05_length_thresholds.png`
- **Mục đích:** Xác định capacity, mốc ASan và mốc crash qua nhiều độ dài.
- **Trạng thái ban đầu:** Đã build binary trong WSL/Docker.
- **URL hoặc lệnh:** `python scripts/test_lengths.py` nếu có, hoặc bảng kiểm tra độ dài tích hợp.
- **Dữ liệu cần nhập:** Các mốc quanh 31, 32, 40, 64 byte.
- **Nút cần bấm:** Chạy test/mở bảng.
- **Tab DevTools hoặc inspector cần mở:** Terminal hoặc Length Test table.
- **Nội dung bắt buộc phải xuất hiện:** Capacity 31, ASan đầu tiên, crash đầu tiên từ kết quả thật.
- **Kết quả đúng:** Không đánh đồng ranh giới buffer với mốc crash.
- **Caption dùng trong báo cáo:** Kiểm tra nhiều độ dài xác định capacity, mốc ASan và mốc crash.

Bước 1. Mở terminal/bảng. Bước 2. Chọn các độ dài. Bước 3. Chạy test. Bước 4. Hiện toàn bảng. Bước 5. Chụp các mốc đọc được. Bước 6. Lưu đúng tên.

### 06_length_fix.png
- **Tên file:** `06_length_fix.png`
- **Mục đích:** Chứng minh từ chối input trước copy.
- **Trạng thái ban đầu:** Chọn `secure_length`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/length`
- **Dữ liệu cần nhập:** 64 ký tự `A`.
- **Nút cần bấm:** Submit/Gửi.
- **Tab DevTools hoặc inspector cần mở:** Native/Code Inspector và Final Verdict.
- **Nội dung bắt buộc phải xuất hiện:** `strnlen`, giới hạn 31, reject trước copy, status thật.
- **Kết quả đúng:** Không ghi buffer khi input quá dài.
- **Caption dùng trong báo cáo:** Bản vá kiểm tra độ dài từ chối input trước thao tác copy.

Bước 1. Mở URL. Bước 2. Nhập 64 `A`. Bước 3. Bấm **Submit**. Bước 4. Mở code/verdict. Bước 5. Chụp bước reject. Bước 6. Lưu đúng tên.

### 07_snprintf_fix.png
- **Tên file:** `07_snprintf_fix.png`
- **Mục đích:** Chứng minh `snprintf` có giới hạn và kiểm tra truncation.
- **Trạng thái ban đầu:** Chọn `secure_snprintf`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/secure/snprintf`
- **Dữ liệu cần nhập:** 64 ký tự `A`.
- **Nút cần bấm:** Submit/Gửi.
- **Tab DevTools hoặc inspector cần mở:** Native/Code Inspector và Final Verdict.
- **Nội dung bắt buộc phải xuất hiện:** `snprintf`, `sizeof(name)`, return value và reject truncation.
- **Kết quả đúng:** Input bị cắt không được coi là thành công.
- **Caption dùng trong báo cáo:** Bản vá snprintf phát hiện và từ chối kết quả bị cắt ngắn.

Bước 1. Mở URL. Bước 2. Nhập 64 `A`. Bước 3. Bấm **Submit**. Bước 4. Mở code/verdict. Bước 5. Chụp return value/reject. Bước 6. Lưu đúng tên.

### 08_hardening.png
- **Tên file:** `08_hardening.png`
- **Mục đích:** Chứng minh Canary, PIE, RELRO và NX từ binary thật.
- **Trạng thái ban đầu:** Đã `make all`, gồm `secure_hardened`.
- **URL hoặc lệnh:** `http://127.0.0.1:5002/hardening`
- **Dữ liệu cần nhập:** Không nhập.
- **Nút cần bấm:** Refresh Hardening Inspector.
- **Tab DevTools hoặc inspector cần mở:** Hardening Inspector.
- **Nội dung bắt buộc phải xuất hiện:** Canary, PIE, RELRO, NX và nguồn lệnh kiểm tra.
- **Kết quả đúng:** Trạng thái lấy từ binary thật, chỉ là lớp bổ sung.
- **Caption dùng trong báo cáo:** Canary, PIE, RELRO và NX tăng chiều sâu bảo vệ cho binary.

Bước 1. Build trong Linux. Bước 2. Mở URL. Bước 3. Bấm refresh. Bước 4. Mở inspector. Bước 5. Chụp bốn cơ chế. Bước 6. Lưu đúng tên.

### 09_tests_reports.png
- **Tên file:** `09_tests_reports.png`
- **Mục đích:** Chứng minh pytest thật và report artifacts.
- **Trạng thái ban đầu:** Dùng WSL/Docker nếu test cần binary Linux.
- **URL hoặc lệnh:** `python -m pytest -q`; `python scripts/generate_report.py`; `ls -lh report/`.
- **Dữ liệu cần nhập:** Ba lệnh trên.
- **Nút cần bấm:** Enter sau mỗi lệnh.
- **Tab DevTools hoặc inspector cần mở:** Terminal.
- **Nội dung bắt buộc phải xuất hiện:** Tổng kết pytest thực tế, DOCX/PDF và kích thước khác 0.
- **Kết quả đúng:** Chỉ ghi đạt khi pytest exit 0.
- **Caption dùng trong báo cáo:** Kết quả pytest thực tế và report artifacts của Lab02.

Bước 1. Mở terminal đúng môi trường. Bước 2. Chạy pytest. Bước 3. Chạy generator/liệt kê report. Bước 4. Cuộn thấy tổng kết. Bước 5. Chụp terminal. Bước 6. Lưu đúng tên.

## 4. Cách kiểm tra và sinh báo cáo

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Thiếu ảnh vẫn sinh DOCX/PDF với placeholder đúng vị trí. Sau khi thêm đủ PNG đúng tên, chạy lại generator để tự thay ảnh thật.
