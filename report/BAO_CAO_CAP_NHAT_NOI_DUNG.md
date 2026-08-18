# Báo cáo cập nhật nội dung Topic04

## Báo cáo đã sửa
- `Lab01/report/21127645_LeMinh_21127224_NguyenVuBach_Lab01_XSS.docx`
- `Lab02/report/21127645_LeMinh_21127224_NguyenVuBach_Lab02_BufferOverflow.docx`
- `Lab03/report/21127645_LeMinh_21127224_NguyenVuBach_Lab03_ParameterTampering.docx`
- `Lab04/report/21127645_LeMinh_21127224_NguyenVuBach_Lab04_CSRF.docx`
- `Lab05/report/21127645_LeMinh_21127224_NguyenVuBach_Lab05_SQLInjection.docx`
- `Lab06/report/21127645_LeMinh_21127224_NguyenVuBach_Lab06_CookiePoisoning.docx`

## Chương được bổ sung/chuẩn hóa
- Sáu báo cáo dùng cùng 14 mục: tên/phạm vi, mục tiêu, môi trường, kiến trúc, bước thực hiện, kết quả, nguyên nhân, ảnh hưởng, phòng chống, bản vá, câu hỏi, bài học, phân công và phụ lục evidence.
- Thông tin hai thành viên được đồng bộ ở bìa, header, metadata và phân công.

## Nội dung thừa đã xóa
- Các chương kiểm tra ngoài phạm vi, quy trình sinh tệp trung gian và nội dung không trực tiếp phục vụ yêu cầu của lab.
- Các ô ảnh legacy/test lặp lại hoặc không phải bằng chứng thật; báo cáo chỉ giữ bảng yêu cầu ảnh F12 cần thiết.

## Ảnh đã giữ
- Không có ảnh bitmap thật trong sáu DOCX đầu vào. Danh sách ảnh F12 cần chụp được giữ trong phụ lục và đồng bộ với `HUONG_DAN_CHUP_ANH.md`/manifest.

## Ảnh đã xóa khỏi báo cáo
- Không xóa file ảnh thật. Chỉ loại các ô hướng dẫn legacy/test khỏi DOCX; không xóa file vật lý trong `evidence`.

## Hướng dẫn ảnh đã cập nhật
- Không sửa thêm trong lượt chuẩn hóa này; sáu file hướng dẫn hiện tại đã có danh sách F12 tương ứng với manifest.

## Bằng chứng thật còn thiếu
- Lab01: Ảnh browser/DevTools cho normal input, reflected/stored/DOM vulnerable và secure retest.
- Lab02: Toàn bộ ảnh browser; request-response; log GDB/ASan/crash, vị trí crash, stack overwrite và ngưỡng input.
- Lab03: Ảnh checkout/IDOR/role tampering vulnerable và secure.
- Lab04: Ảnh email trước/sau, request hợp lệ/CSRF, secure 403 và email không đổi; source hiện không auto-submit.
- Lab05: Ảnh normal/quote/auth bypass/search expanded và secure retest.
- Lab06: Ảnh cookie fields, plain/Base64 tampering, signed rejection và server-session authorization.

## PPTX
- Trạng thái: Chưa đối chiếu.
- Chưa có file PPTX cuối.
- Tổng số slide cuối: 0.

## Xác nhận phạm vi
- Không tạo hoặc cập nhật PDF.
- Không chạy test, pytest hoặc smoke test.
- Không chạy lab, Docker hoặc kịch bản khai thác.
- Không tạo screenshot giả.
- Không sửa logic vulnerable/secure, route, database schema hoặc payload kỹ thuật.
