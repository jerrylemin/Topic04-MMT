# Bối cảnh dự án Lab05

Lab05 là ứng dụng Flask/SQLite học tập về SQL Injection, chỉ chạy tại `http://127.0.0.1:5005`. Các kịch bản injection dùng chuỗi cố định, chỉ tác động database giả lập trong Lab05 và chỉ thực hiện `SELECT`. Bản secure dùng parameter binding, PBKDF2 qua Werkzeug, generic error, redaction, audit và trace từ request/SQLite thật.
