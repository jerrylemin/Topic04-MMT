# Feature progress - Lab02

| Hạng mục | Trạng thái | Bằng chứng |
|---|---|---|
| Launcher WSL/Docker trên Windows | Hoàn tất | WSL preflight exit 0; Docker launcher tự mở engine và `/health` trả HTTP 200 |
| Build 5 binary | Hoàn tất | `make all`, `build/*` |
| README và quick-run scripts | Hoàn tất | Syntax PowerShell/sh/bash đạt |
| GDB scripts/hướng dẫn | Hoàn tất mã; chưa chạy session | `gdb/*.gdb`, `gdb/README_GDB.md` |
| Docker/Compose | Hoàn tất và đã chạy thử | `docker compose config --quiet`; container healthy; `/health` trả HTTP 200 |
| Hướng dẫn 28 ảnh | Hoàn tất | `HUONG_DAN_CHUP_ANH.md` |
| Ảnh thủ công | Chưa có | Checker báo thiếu 28/28 |
| DOCX | Đã sinh, kiểm tra cấu trúc đạt | `report/21127645_LeMinh_21127224_NguyenVuBach_Lab02_BufferOverflow.docx` |
| PDF | Đã sinh, visual QA đạt | 19 trang, Poppler render sạch |
| Pytest | Đạt tại thời điểm handoff | 14 passed; `evidence/logs/pytest.txt` |
