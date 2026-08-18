# Phân tích GDB an toàn cho Lab02

Các phiên dưới đây chỉ quan sát tiến trình local, không sửa thanh ghi, return address hay bộ nhớ. Build trước bằng `make all`, đứng tại thư mục `Lab02`, và không lưu core dump (`ulimit -c 0`).

## Chạy ba phiên

```bash
gdb -q -x gdb/inspect_normal.gdb
gdb -q -x gdb/inspect_overflow.gdb
gdb -q -x gdb/inspect_hardened.gdb
```

Muốn lưu log thật, dùng `tee` sau khi đã kiểm tra lệnh và môi trường:

```bash
gdb -q -x gdb/inspect_normal.gdb 2>&1 | tee evidence/gdb/normal_session.txt
gdb -q -x gdb/inspect_overflow.gdb 2>&1 | tee evidence/gdb/overflow_session.txt
gdb -q -x gdb/inspect_hardened.gdb 2>&1 | tee evidence/gdb/hardened_session.txt
```

`inspect_normal.gdb` dừng tại `process_name`, xem biến cục bộ, `sizeof(name)`, vùng byte quanh `name`, mã máy rồi tiếp tục với `Le Minh`. `inspect_overflow.gdb` dùng đúng 64 ký tự `A`, tiếp tục cho tới khi tiến trình dừng và in backtrace/signal. `inspect_hardened.gdb` quan sát bản vá hardened; input dài dự kiến bị từ chối, không phải kích hoạt canary.

Địa chỉ và stack layout chỉ có ý nghĩa trong phiên local hiện tại; kiến trúc, ABI, compiler và flags có thể làm kết quả khác nhau. Chỉ kết luận signal/crash sau khi GDB thật sự hiển thị chúng. Không tạo shellcode, ROP, reverse shell hay thao tác thay đổi luồng điều khiển.

## Docker profile dành riêng cho GDB

```bash
docker compose --profile gdb run --rm gdb
```

Chỉ service `gdb` có `SYS_PTRACE` và `seccomp=unconfined` để debugger theo dõi tiến trình trong container lab local. Service web thường không có quyền này; không service nào chạy `privileged`.
