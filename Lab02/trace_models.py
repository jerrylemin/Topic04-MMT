from datetime import datetime, timezone

from security_utils import utf8_length


BUFFER_SIZE = 32
SAFE_CAPACITY = 31


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _step(number: int, layer: str, title: str, description: str, **details) -> dict:
    return {
        "step_number": number,
        "timestamp": _now(),
        "layer": layer,
        "title": title,
        "description": description,
        "technique": details.get("technique", "Quan sát luồng dữ liệu"),
        "input_data": details.get("input_data", {}),
        "output_data": details.get("output_data", {}),
        "code_reference": details.get("code_reference", ""),
        "security_meaning": details.get("security_meaning", ""),
        "status": details.get("status", "completed"),
    }


def build_trace(
    trace_id: str,
    mode: str,
    name: str,
    request_summary: dict,
    native_result: dict,
    mode_info: dict,
) -> dict:
    started_at = request_summary["timestamp"]
    completed_at = _now()
    name_bytes = utf8_length(name)
    overflow_bytes = max(0, name_bytes + 1 - BUFFER_SIZE)
    preview = name if len(name) <= 64 else f"{name[:64]}…"
    asan = native_result.get("asan", {"detected": False})
    rejected = native_result.get("exit_code") in {65, 66, 67}
    crashed = native_result.get("crash_detected", False)
    actual_overflow = mode.startswith("vulnerable") and bool(overflow_bytes)
    if asan.get("detected"):
        verdict, verdict_status = "ASan phát hiện stack-buffer-overflow.", "danger"
    elif rejected:
        verdict, verdict_status = "Input bị từ chối trước khi gây memory corruption.", "safe"
    elif native_result.get("status") != "completed":
        verdict, verdict_status = "Tiến trình native chưa hoàn tất.", "warning"
    elif overflow_bytes:
        verdict, verdict_status = "Đã vượt ranh giới name[32].", "danger"
    else:
        verdict, verdict_status = "Input nằm trong sức chứa chuỗi C an toàn.", "safe"

    common = [
        ("Browser", "Browser nhận input", "Trình duyệt ghi nhận ký tự và byte UTF-8."),
        ("HTTP", "Browser tạo HTTP request", f"POST {request_summary['path']} dùng form URL encoded."),
        ("Flask", "Flask định tuyến", "Gateway áp dụng giới hạn request và allowlist mode."),
        ("Flask", "Flask chuẩn bị subprocess", "Binary cố định, argument list, shell=False và timeout ngắn."),
        ("OS", "Hệ điều hành tạo tiến trình C", f"Chạy profile {mode_info['profile']}."),
        ("C", "process_name tạo stack frame", "Biến cục bộ name[32] nằm trong stack frame theo mô hình giáo dục."),
    ]
    if mode.startswith("vulnerable"):
        native_steps = [
            ("C", "strcpy bắt đầu copy", "strcpy copy đến null terminator mà không biết kích thước đích."),
            ("Memory", "Kiểm tra ranh giới bộ nhớ", f"Số byte ghi vượt theo mô hình: {overflow_bytes}."),
        ]
    elif mode == "secure_length":
        native_steps = [
            ("C", "strnlen đo input", f"So sánh {name_bytes} byte với sức chứa 31 byte."),
            ("Memory", "Kiểm tra trước copy", "Input quá dài bị từ chối; input hợp lệ mới được copy và thêm null."),
        ]
    else:
        native_steps = [
            ("C", "snprintf giới hạn ghi", "sizeof(name) giới hạn số byte được ghi vào buffer."),
            ("Memory", "Kiểm tra return value", "Return value phát hiện truncate và từ chối input quá dài."),
        ]
    tail = [
        ("Native", "Kết quả native", f"Trạng thái: {native_result.get('status')}; exit: {native_result.get('exit_code')}."),
        ("Flask", "Flask thu kết quả", "stdout và stderr được giới hạn, chuẩn hóa và che đường dẫn."),
        ("HTTP", "Flask tạo HTTP response", "Response chứa Trace ID và X-Lab-Mode."),
        ("Verdict", "Final Security Verdict", verdict),
    ]
    steps = []
    for number, (layer, title, description) in enumerate(common + native_steps + tail, 1):
        steps.append(
            _step(
                number,
                layer,
                title,
                description,
                input_data={"preview": preview, "chars": len(name), "bytes": name_bytes}
                if number == 1
                else {},
                output_data=native_result if title == "Kết quả native" else {},
                code_reference=("native/vulnerable_processor.c:process_name" if mode.startswith("vulnerable") else "native processor"),
                security_meaning=verdict if title == "Final Security Verdict" else description,
                status=verdict_status if title == "Final Security Verdict" else "completed",
            )
        )

    return {
        "trace_id": trace_id,
        "lab_type": "buffer_overflow_local",
        "mode": mode,
        "started_at": started_at,
        "completed_at": completed_at,
        "input_value": preview,
        "input_length_chars": len(name),
        "input_length_bytes": name_bytes,
        "buffer_size": BUFFER_SIZE,
        "safe_capacity": SAFE_CAPACITY,
        "overflow_bytes": overflow_bytes,
        "request_summary": request_summary,
        "native_binary": native_result.get("binary"),
        "build_profile": mode_info["profile"],
        "compiler_flags": mode_info["flags"],
        "steps": steps,
        "exit_code": native_result.get("exit_code"),
        "signal": native_result.get("signal"),
        "asan_detected": bool(asan.get("detected")),
        "asan": asan,
        "crash_detected": crashed,
        "native_result": native_result,
        "hardening": {"verification": "collected separately from the binary"},
        "security_controls": [
            {
                "name": "Request body và name limit",
                "enabled": True,
                "file": "config.py / app.py",
                "risk": "Giới hạn tài nguyên và payload của lab.",
                "limit": "C vẫn phải tự kiểm tra lại input.",
            },
            {
                "name": "Mode và binary allowlist",
                "enabled": True,
                "file": "config.py / native_runner.py",
                "risk": "Ngăn client chọn command hoặc đường dẫn tùy ý.",
                "limit": "Chỉ bảo vệ biên subprocess.",
            },
            {
                "name": "Validation trong native C",
                "enabled": not mode.startswith("vulnerable"),
                "file": "native/secure_*_processor.c",
                "risk": "Ngăn copy vượt name[32].",
                "limit": "Compiler hardening vẫn cần cho defense in depth.",
            },
        ],
        "final_result": {
            "verdict": verdict,
            "status": verdict_status,
            "overflow": actual_overflow,
            "would_overflow_without_validation": bool(overflow_bytes),
            "crash": crashed,
            "asan": bool(asan.get("detected")),
            "asan_detected": bool(asan.get("detected")),
            "rejected": rejected,
            "exit_code": native_result.get("exit_code"),
            "cause": verdict,
            "impact": "Crash/DoS cục bộ" if crashed else "Không quan sát memory corruption.",
        },
    }
