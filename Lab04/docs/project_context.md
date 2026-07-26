# Bối cảnh dự án Lab04

Lab04 là hai ứng dụng Flask chỉ chạy trên loopback để minh họa CSRF. Victim App cố định tại `http://127.0.0.1:5004`; Demo Page cố định tại `http://127.0.0.1:9004`. Luồng đổi email vulnerable cố ý bỏ qua xác thực CSRF. Các thao tác secure, logout và reset yêu cầu session hợp lệ, kiểm tra chính xác Origin/Referer và synchronizer token. Inspector và evidence phải che dữ liệu nhạy cảm.
