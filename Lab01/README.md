# Lab 01 - Cross-Site Scripting

Ứng dụng Flask offline minh họa Reflected, Stored và DOM-based XSS cùng bản vá. Chỉ dùng payload `alert()` trong lab tại `127.0.0.1`; không dùng website thật, browser automation hoặc ảnh giả.

## Chạy ứng dụng

- Windows: `scripts\run_lab.bat` hoặc `powershell -File scripts\run_lab.ps1`
- Linux: `sh scripts/run_lab.sh`
- Docker: `docker compose up --build`
- URL: `http://127.0.0.1:5000`

| Bài | Vulnerable | Secure |
|---|---|---|
| Reflected | `/vulnerable/search` | `/secure/search` |
| Stored | `/vulnerable/post/1/comments` | `/secure/post/1/comments` |
| DOM | `/vulnerable/dom-search` | `/secure/dom-search` |

Cookie demo: `/profile`; CSP/header: `/security-headers`. Khi cần làm lại Stored XSS, chạy `python scripts/reset_database.py`.

## Tài khoản và dữ liệu demo

Lab không cần đăng nhập. Dữ liệu bình luận nằm trong SQLite local. Trace/inspector đọc request, response, SQLite và DOM thật; không gửi dữ liệu ra ngoài.

## Ảnh bằng chứng và báo cáo

Lab yêu cầu đúng **10 ảnh** theo [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md), lưu thủ công vào `evidence/screenshots/`.

```powershell
python scripts/check_screenshots.py --list-required
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Checker kiểm tra đúng tên, thiếu/thừa, PNG hợp lệ, file rỗng/hỏng, kích thước tối thiểu 1024x600 và SHA-256 trùng; không OCR hay đánh giá nội dung. Generator luôn tạo:

- `report/21127645_LeMinh_Lab01_XSS.docx`
- `report/21127645_LeMinh_Lab01_XSS.pdf`

Thiếu ảnh thì report có placeholder chi tiết ngay sau kịch bản tương ứng và in danh sách còn thiếu. Đặt PNG đúng tên rồi chạy lại generator để tự thay bằng ảnh thật, giữ tỷ lệ và caption. Danh sách 28 tên cũ chỉ để tham khảo tại [LEGACY_SCREENSHOTS.md](LEGACY_SCREENSHOTS.md), không còn bắt buộc.

## Kiểm thử

```powershell
python -m compileall .
python -m pytest -q
```

Chỉ kết luận đạt theo exit code và log thực tế; generator không hard-code `PASS`.
