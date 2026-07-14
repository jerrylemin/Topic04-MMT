# Lab 01 — Cross-Site Scripting

Ứng dụng Flask offline minh họa Reflected, Stored và DOM-based XSS cùng bản vá. Mỗi thao tác tạo timeline và các inspector từ request, SQLite, response hoặc DOM thật. Chỉ chạy tại `127.0.0.1`; payload chỉ dùng `alert()` trong lab local.

## Chạy ứng dụng

- Windows: `scripts\run_lab.bat` hoặc `powershell -File scripts\run_lab.ps1`.
- Linux: `sh scripts/run_lab.sh`.
- Docker: `docker compose up --build`.
- URL: `http://127.0.0.1:5000`.

| Bài | Có lỗ hổng | Đã vá |
|---|---|---|
| Reflected | `/vulnerable/search` | `/secure/search` |
| Stored | `/vulnerable/post/1/comments` | `/secure/post/1/comments` |
| DOM | `/vulnerable/dom-search` | `/secure/dom-search` |

Cookie: `/profile`; CSP/header: `/security-headers`.

## Đọc trace

1. Thực hiện form hoặc thay fragment. Timeline ghi Browser UI → HTTP → Flask/SQLite/Jinja → Response/DOM → Verdict.
2. Bấm một bước để mở input, output, kỹ thuật, mã liên quan và ý nghĩa bảo mật. **Trước/Sau** chạy từng bước; **Auto Play/Tạm dừng** chỉ điều khiển phần trình bày.
3. **Request** dùng request Flask thật và che toàn bộ giá trị cookie. **Response** hiển thị header, vùng HTML liên quan, trước/sau escape và độ dài.
4. **Source → Sink** cho biết đường tainted data. **So sánh mã** khớp `Markup/autoescape`, `bleach.clean` và `innerHTML/textContent` đang chạy. **Database** đọc bảng comments thật.
5. **Presentation Mode** phóng to bước hiện tại và ẩn phần phụ. Bấm lại để thoát.
6. **Xuất JSON** tải trace hiện tại; **Sao chép trace**, **Xóa timeline**, **Chạy lại** làm đúng tên nút. Bản secure/vulnerable có nút so sánh chéo.

## Payload an toàn

```html
<img src=x onerror="alert('Reflected XSS')">
<img src=x onerror="alert('Stored XSS')"><strong>Xin chào</strong>
#<img src=x onerror="alert('DOM XSS')">
```

Input validation chỉ hỗ trợ; output encoding/sanitization sửa sink. CSP và HttpOnly là defense in depth, không thay việc sửa XSS. Production HTTPS phải đặt `SESSION_COOKIE_SECURE=true`.

## Ảnh thủ công và báo cáo

Không dùng Playwright, Selenium hoặc tự động chụp ảnh. Làm theo [HUONG_DAN_CHUP_ANH.md](HUONG_DAN_CHUP_ANH.md), đặt đúng 28 PNG vào `evidence/screenshots/`, rồi chạy:

```powershell
python scripts/check_screenshots.py
python scripts/generate_report.py
```

Checker chỉ kiểm tra file: tên, số lượng, PNG/rỗng/quá nhỏ, ảnh thiếu/thừa và hash trùng; không OCR. Report vẫn được tạo khi thiếu ảnh và dùng placeholder có tên, URL, thao tác, thành phần cần thấy. Chạy lại generator sau khi thêm ảnh để thay placeholder bằng ảnh thật, giữ đúng tỷ lệ.

## Database, trace và test

```powershell
python scripts/reset_database.py
python scripts/generate_trace_samples.py
pytest -q
```

Trace mẫu nằm trong `evidence/traces/`; log test nằm trong `evidence/logs/pytest.txt`. Nếu cổng 5000 bận, dừng tiến trình cũ. Nếu báo cáo thiếu ảnh, kiểm tra tên bằng checker; nếu PDF thiếu glyph, bảo đảm Windows có Arial hoặc cài font Unicode phù hợp.
