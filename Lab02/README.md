# Lab02 - Buffer Overflow trong ứng dụng web local

Ứng dụng minh họa luồng dữ liệu `Browser -> HTTP POST -> Flask -> subprocess -> chương trình C -> exit/signal -> HTTP response`. Bản lỗi dùng `char name[32]` và `strcpy`; hai bản vá kiểm tra tối đa 31 byte hoặc dùng `snprintf` kèm kiểm tra return value. AddressSanitizer, GDB và compiler hardening hỗ trợ quan sát/phòng thủ nhưng không thay secure coding.

Thông tin bài: **MSSV 21127645 - Lê Minh - LAB 2, BUFFER OVERFLOW TRONG ỨNG DỤNG WEB LOCAL**.

## Phạm vi an toàn

- Chỉ chạy tại `127.0.0.1` trong Linux VM, WSL hoặc Docker local; app không bind `0.0.0.0`.
- Chỉ dùng chuỗi văn bản bình thường hoặc `A`/`B` lặp, tối đa 256 byte theo cấu hình lab.
- Không gửi request ra Internet, không quét host khác, không shellcode/ROP/reverse shell/persistence/malware và không sửa return address.
- `vulnerable_debug` dành cho GDB local. Giao diện dùng `vulnerable_asan` cho input dài để tiến trình dừng và có log rõ; core dump nên tắt bằng `ulimit -c 0`.
- Địa chỉ memory chỉ quan sát thủ công trong GDB, không hiển thị trên UI chính.

## Kiến trúc và route

1. Browser UI gửi form và hiển thị timeline, request/native/ASan/memory/hardening inspector.
2. Flask áp request limit, validation UTF-8 byte, allowlist mode, timeout và gọi `subprocess.run([...], shell=False)` trong working directory cố định.
3. Binary C xử lý input, in PID/độ dài/buffer size; hệ điều hành trả exit code hoặc signal để Flask chuẩn hóa thành trace.

| Route | Chức năng |
|---|---|
| `GET /` | Tổng quan lab |
| `GET /vulnerable`, `POST /submit` | Bản vulnerable debug/ASan/hardened |
| `GET /secure/length`, `POST /secure/length/submit` | Bản vá kiểm tra 31 byte |
| `GET /secure/snprintf`, `POST /secure/snprintf/submit` | Bản vá `snprintf` |
| `GET /hardening` | So sánh build/hardening |
| `GET /gdb-guide` | Hướng dẫn GDB |
| `GET /comparison` | So sánh mã nguồn |
| `GET /api/trace/<trace_id>`, `POST /api/trace/clear` | Đọc/xóa trace local |
| `GET /health` | Healthcheck |

## Cấu trúc chính

```text
Lab02/
├── app.py, config.py, native_runner.py, trace_models.py, trace_service.py
├── native/                 # Ba chương trình C và header dùng chung
├── build/                  # 5 binary do Makefile sinh
├── templates/, static/     # UI, timeline, visualizer, Presentation Mode
├── scripts/                # build/run/client/test/report/screenshot/cleanup
├── gdb/                    # Ba script quan sát và README_GDB.md
├── tests/                  # pytest
├── evidence/               # log/trace/request/response/ASan/GDB/ảnh thật
└── report/                 # DOCX/PDF sinh từ generate_report.py
```

## Yêu cầu hệ thống

- Python 3.11+, GCC, Make, GDB và binutils trên Linux/WSL; Docker là lựa chọn tái lập.
- Python packages trong `requirements.txt`: Flask, requests, pytest, Pillow, python-docx và ReportLab.
- Không có Playwright/Selenium/CDN. Ảnh được chụp thủ công.

Trên Windows, dùng WSL hoặc Docker cho GCC/GDB; tài liệu không giả định GDB native Windows hoạt động.

## Chạy trên Linux

```bash
cd Lab02
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make all
python app.py
```

Mở `http://127.0.0.1:5002`. Dừng bằng `Ctrl+C`; không chạy script bằng root.

Script gộp:

```bash
sh scripts/run_lab.sh
```

## Chạy trên WSL

Mở Ubuntu bằng user thường, chuyển tới thư mục mount Windows rồi chạy cùng quy trình Linux. Từ PowerShell user thường:

```powershell
.\scripts\build_all.ps1
.\scripts\run_lab.ps1
```

Hai script PowerShell chuyển sang distro `Ubuntu`; nếu máy dùng tên distro khác, chạy trực tiếp trong distro đó. Không chạy PowerShell Administrator.

Từ File Explorer hoặc Command Prompt, có thể dùng hai launcher riêng:

```bat
scripts\run_lab_wsl.bat
scripts\run_lab_docker.bat
```

`run_lab_wsl.bat` tự khởi động distro `Ubuntu` rồi gọi launcher WSL hiện có. `run_lab_docker.bat` tự mở Docker Desktop khi cần, chờ Docker Engine sẵn sàng và chạy `docker compose up --build`.

## Chạy bằng Docker

```bash
docker compose up --build
```

Compose chỉ publish `127.0.0.1:5002:5002`, mount `evidence/` và `report/`, có healthcheck, không dùng `network_mode: host` hoặc `privileged`. App vẫn bind loopback trong container; `socat` chuyển tiếp từ địa chỉ nội bộ của container tới `127.0.0.1:5002` để port mapping hoạt động mà không đổi bind của Flask. Service web không có `SYS_PTRACE`.

Profile GDB local:

```bash
docker compose --profile gdb run --rm gdb
```

Chỉ service `gdb` có `SYS_PTRACE` và `seccomp=unconfined`, cần thiết để debugger theo dõi tiến trình trong container local. Profile này không có network và không dùng cho web thường.

## Build binary

```bash
make all
# hoặc
sh scripts/build_all.sh
```

| Binary | Mục đích | Nhóm flags chính |
|---|---|---|
| `build/vulnerable_debug` | GDB | `-O0 -g -fno-omit-frame-pointer -fno-stack-protector` |
| `build/vulnerable_asan` | Phát hiện overflow | debug flags + `-fsanitize=address,undefined` |
| `build/secure_length` | Bản vá length | `-O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie`, Full RELRO, NX |
| `build/secure_snprintf` | Bản vá `snprintf` | Cùng nhóm hardening |
| `build/secure_hardened` | So sánh hardened | Cùng nhóm hardening, profile riêng |

Tên/flags không chứng minh trạng thái binary. Dùng `file`, `readelf`, `objdump` hoặc script thu thập build info và chỉ báo kết quả đã đo thật.

## Gửi request local

Trên UI, chọn mẫu `Le Minh`, 31, 32, 64 hoặc 128 byte. Client script luôn cố định host local:

```bash
python scripts/send_request.py --mode vulnerable_asan --text "Le Minh"
python scripts/send_request.py --mode vulnerable_asan --length 64
python scripts/send_request.py --mode secure_length --length 64
python scripts/send_request.py --mode secure_snprintf --length 64
```

Không dùng URL/host bên ngoài. Input 32 byte đã vượt khả năng chứa chuỗi C vì còn cần null terminator, nhưng không được khẳng định luôn crash tại 32 byte.

## Kiểm thử độ dài

Khi app đang chạy:

```bash
python scripts/test_lengths.py
```

Kết quả thật được lưu trong `evidence/logs/length_test.csv`, `.json` và `.txt`. Phân biệt: mốc đầu tiên ghi vượt theo capacity, mốc đầu tiên ASan phát hiện và mốc đầu tiên tiến trình crash/dừng.

## Dùng GDB

```bash
ulimit -c 0
gdb -q -x gdb/inspect_normal.gdb
gdb -q -x gdb/inspect_overflow.gdb
gdb -q -x gdb/inspect_hardened.gdb
```

Xem [gdb/README_GDB.md](gdb/README_GDB.md) để lưu log thật. Script chỉ break/run/frame/info/x/disassemble/backtrace; không sửa thanh ghi hoặc luồng điều khiển.

## Đọc AddressSanitizer

Chọn `vulnerable_asan`, gửi 64 ký tự `A`, rồi mở ASan Inspector. Đối chiếu loại lỗi, file, hàm, dòng `strcpy`, write size, buffer, input length, stack trace và exit code. Đường dẫn home được che. ASan là công cụ kiểm thử; không phải cơ chế production chính và kết quả phải lấy từ stderr thật.

## Xem hardening

Build đủ binary, mở `http://127.0.0.1:5002/hardening`, rồi đối chiếu Canary, PIE, RELRO, NX, FORTIFY, ASan, optimization và frame pointer. Stack Canary phát hiện thay đổi; PIE hỗ trợ ASLR; NX ngăn thực thi data; RELRO bảo vệ relocation; FORTIFY tăng kiểm tra thư viện. Tất cả chỉ là lớp bổ sung cho bản vá code.

## Presentation Mode

Chạy một trace, bấm **Presentation Mode**, dùng Previous/Next hoặc Auto Play để trình bày từng bước có sẵn. Auto Play không tạo request/crash mới. Có thể mở visualizer, source và comparison từ các nút điều hướng.

## Chụp và kiểm tra ảnh

Làm đúng 28 kịch bản trong [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md), lưu PNG thủ công vào `evidence/screenshots/`, rồi chạy:

```bash
python scripts/check_screenshots.py
```

Script kiểm tra tên, PNG, file rỗng/hỏng, kích thước, ảnh thiếu/thừa và hash trùng; không OCR hoặc tạo/phân tích nội dung ảnh.

## Tạo báo cáo DOCX và PDF

```bash
python scripts/generate_report.py
```

Kết quả:

- `report/21127645_LeMinh_Lab02_BufferOverflow.docx`
- `report/21127645_LeMinh_Lab02_BufferOverflow.pdf`

Script dùng python-docx và ReportLab, có bìa editorial, mục lục, số trang, 17 chương, phụ lục, caption hình/bảng. Ảnh thật được giữ tỷ lệ; ảnh chưa có trở thành placeholder chi tiết gồm tên, URL/lệnh, thao tác và nội dung bắt buộc. Chạy lại sẽ tự thay placeholder bằng ảnh thật. Script chỉ đọc bằng chứng hiện có và ghi rõ phần chưa thu thập, không tạo log/GDB/ASan giả.

## Chạy pytest

```bash
pytest
# build trước và lưu log thật
bash scripts/run_tests.sh
```

Chỉ kết luận pass khi lệnh trả exit code 0. Log được ghi vào `evidence/logs/pytest.txt`.

## Lỗi thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| Thiếu GCC/GDB trên Windows | Dùng Ubuntu/WSL hoặc Docker; không cố chạy binary Linux trực tiếp |
| `ModuleNotFoundError` | Kích hoạt `.venv`, chạy `python -m pip install -r requirements.txt` |
| Binary unavailable | `make all`, kiểm tra quyền thực thi và đứng đúng thư mục `Lab02` |
| Port 5002 bận | Dừng phiên lab cũ; không đổi sang host/port bên ngoài phạm vi |
| ASan không hiện lỗi | Xác nhận chọn `vulnerable_asan`, binary build bằng sanitizer và dùng 64 byte ASCII |
| GDB không attach trong Docker | Chạy đúng profile `gdb`; không thêm ptrace vào service web |
| Screenshot checker trả 1 | Đọc danh sách thiếu/thừa/hỏng/kích thước/hash; chụp lại thủ công |
| Báo cáo còn placeholder | Bổ sung đúng PNG rồi chạy lại `generate_report.py` |
| DOCX chưa cập nhật TOC | Mở bằng Word/LibreOffice và cập nhật fields; PDF có mục lục/số trang được dựng trực tiếp |

## Dọn file sinh ra

Mặc định chỉ liệt kê, không xóa:

```bash
python scripts/clean_generated_files.py
python scripts/clean_generated_files.py --yes
```

Lệnh xác nhận chỉ dọn build, report và evidence sinh tự động; luôn giữ `evidence/screenshots/` để không xóa ảnh thủ công của người dùng.
