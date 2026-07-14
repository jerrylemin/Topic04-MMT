# Session handoff - Lab02

## Đã hoàn tất

- Bổ sung `scripts/run_lab_wsl.bat` và `scripts/run_lab_docker.bat`; hai launcher lần lượt tự khởi động Ubuntu WSL hoặc Docker Desktop rồi chạy lab.
- Tài liệu vận hành: `README.md`, `HUONG_DAN_CHUP_ANH.md` mô tả 9 ảnh bằng chứng tối thiểu, theo các bước chụp ngắn và rõ.
- Script build/run/test/cleanup cho Linux/WSL/Windows; checker PNG/hash; ba script GDB an toàn.
- Dockerfile/Compose với web không có ptrace, profile GDB riêng có `SYS_PTRACE`, `seccomp=unconfined`, `network_mode: none`, không privileged.
- `scripts/generate_report.py` sinh DOCX/PDF tiếng Việt gồm 9 mục bám đề bài, caption và placeholder chi tiết đặt ngay sau kịch bản tương ứng.
- Artifact: `report/21127645_LeMinh_Lab02_BufferOverflow.docx` và `.pdf`.

## Xác minh đã chạy

- WSL: `sh scripts/build_all.sh` - 5 binary ELF hiện có.
- WSL: `bash scripts/run_tests.sh` - `14 passed in 1.45s`, log thật ở `evidence/logs/pytest.txt`.
- `python scripts/check_screenshots.py` - hiện thiếu toàn bộ 9 ảnh thủ công; checker không tạo ảnh thay thế.
- `python scripts/generate_report.py` - tạo thành công DOCX/PDF với 9 placeholder.
- Poppler: PDF 19 trang Letter; đã render và kiểm tra toàn bộ trang, không thấy clipping/overlap.
- DOCX structural QA: đủ 17 chương, phụ lục, 28 caption, trường PAGE và bảng fixed-width.
- `docker compose config --quiet` đạt; `scripts/run_lab_docker.bat` đã tự mở Docker Desktop, build image, đưa container tới trạng thái healthy và nhận HTTP 200 từ `/health`. Container thử nghiệm đã được `docker compose down` sau khi xác minh.

## Việc còn lại

- Chụp thủ công 9 PNG theo `HUONG_DAN_CHUP_ANH.md`, chạy lại checker và report generator.
- GDB chưa có trong Ubuntu WSL hiện tại, vì vậy chưa có session/log GDB thật. Chạy theo `gdb/README_GDB.md` sau khi có GDB hoặc dùng Docker profile.
- LibreOffice/`soffice` không có, nên DOCX chưa qua render PNG trực quan; chỉ structural QA. PDF đã qua Poppler visual QA.
- Nếu test suite tiếp tục được bổ sung, chạy lại `bash scripts/run_tests.sh`, sau đó chạy lại `generate_report.py` để báo cáo lấy dòng tổng kết mới.
