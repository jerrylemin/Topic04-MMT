"""Sinh báo cáo Lab04 ngắn gọn, có placeholder ảnh đúng vị trí."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from screenshot_manifest import SCREENSHOTS  # noqa: E402

REPORT = ROOT / "report"
SHOTS = ROOT / "evidence" / "screenshots"
DOCX = REPORT / "21127645_LeMinh_Lab04_CSRF.docx"
PDF = REPORT / "21127645_LeMinh_Lab04_CSRF.pdf"
PYTEST_LOG = ROOT / "evidence" / "logs" / "pytest.txt"
COVERAGE_LOG = ROOT / "evidence" / "logs" / "coverage.txt"


def _fill(cell, color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd")) or OxmlElement("w:shd")
    if shd.getparent() is None:
        tc_pr.append(shd)
    shd.set(qn("w:fill"), color)


def _border(cell, color="2E74B5", size="14") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:color"), color)
        borders.append(node)


def _style(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(1.7)
    section.left_margin = section.right_margin = Cm(1.8)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "Arial", Pt(10.5)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08
    for name, size, color in (("Heading 1", 16, "1F4E79"), ("Heading 2", 12.5, "2E74B5"), ("Heading 3", 11, "1F4E79")):
        st = doc.styles[name]
        st.font.name, st.font.size, st.font.bold = "Arial", Pt(size), True
        st.font.color.rgb = RGBColor.from_string(color)
        st.paragraph_format.space_before, st.paragraph_format.space_after = Pt(9), Pt(4)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Lab04 - CSRF | 21127645 - Lê Minh")


def _valid_png(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size == 0:
        return False
    try:
        with PILImage.open(path) as image:
            image.verify()
        with PILImage.open(path) as image:
            return image.format == "PNG" and image.width >= 800 and image.height >= 450
    except OSError:
        return False


def image_size(path: Path, max_width=6.35, max_height=6.3):
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return width * scale, height * scale


def _evidence(doc: Document, index: int, item: dict, missing: list[str]) -> None:
    path = SHOTS / item["filename"]
    if _valid_png(path):
        width, height = image_size(path)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Inches(width), height=Inches(height))
    else:
        missing.append(item["filename"])
        table = doc.add_table(rows=1, cols=1)
        table.autofit = False
        cant_split = OxmlElement("w:cantSplit")
        table.rows[0]._tr.get_or_add_trPr().append(cant_split)
        cell = table.cell(0, 0)
        cell.width = Cm(16.8)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        _fill(cell, "EAF3F8")
        _border(cell)
        details = [
            f"ẢNH {index:02d}/{len(SCREENSHOTS):02d}", f"Tên file: {item['filename']}",
            f"Tiêu đề ảnh: {item['purpose']}", "Chèn ảnh tại vị trí này.",
            f"URL hoặc lệnh: {item['url_command']}", f"Thao tác: {item['input_data']} | {item['button']}",
            f"Panel hoặc DevTools tab: {item['panel']}", f"Nội dung bắt buộc phải thấy: {item['required']}",
            f"Kết quả mong đợi: {item['expected']}", f"Caption: {item['caption']}",
        ]
        for line_no, line in enumerate(details):
            p = cell.paragraphs[0] if line_no == 0 else cell.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(line)
            run.font.name, run.font.size = "Arial", Pt(12 if line_no == 0 else 10)
            run.bold = line_no in (0, 1, 3)
    caption = doc.add_paragraph(f"Hình {index}. {item['caption']}")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.italic, run.font.size = True, Pt(9)


def _code(doc: Document, source: str) -> None:
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.cell(0, 0)
    _fill(cell, "F3F5F7")
    run = cell.paragraphs[0].add_run(source)
    run.font.name, run.font.size = "Consolas", Pt(8.5)


def _log_summary(path: Path, limit=1000) -> str | None:
    if not path.is_file() or path.stat().st_size == 0:
        return None
    data = path.read_bytes()
    encoding = "utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    text = data.decode(encoding, errors="replace")
    return " ".join(text.split())[-limit:]


def build_docx(missing: list[str] | None = None) -> Path:
    missing = missing if missing is not None else []
    doc = Document()
    _style(doc)
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(100)
    run = title.add_run("BÁO CÁO THỰC HÀNH\nLAB04 - CROSS-SITE REQUEST FORGERY")
    run.bold, run.font.name, run.font.size = True, "Arial", Pt(23)
    run.font.color.rgb = RGBColor(31, 78, 121)
    for line in ("Môn: Mạng máy tính", "Sinh viên: Lê Minh", "MSSV: 21127645", "Môi trường: localhost - dữ liệu giả lập"):
        p = doc.add_paragraph(line)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    doc.add_heading("1. Mục tiêu và môi trường thực hành", 1)
    doc.add_paragraph("Mục tiêu là giải thích vì sao browser tự gửi session cookie, tái hiện đổi email thiếu CSRF token và kiểm chứng synchronizer token kết hợp exact Origin/Referer validation.")
    doc.add_paragraph("Victim Application chạy tại http://127.0.0.1:5004; Demo Page cố định tại http://127.0.0.1:9004. Tài khoản victim dùng dữ liệu SQLite giả lập. Không có website, email hay tài khoản thật.")

    doc.add_heading("2. Kịch bản và các bước thực hiện", 1)
    doc.add_heading("2.1 Request hợp lệ ban đầu", 2)
    doc.add_paragraph("Đăng nhập victim và gửi request đổi email cùng origin để xác nhận session và trạng thái ban đầu.")
    _evidence(doc, 1, SCREENSHOTS[0], missing)
    doc.add_heading("2.2 Form giả lập và vulnerable CSRF", 2)
    doc.add_paragraph("Demo Page chứa form POST local cố định đến /vulnerable/change-email, không biết password hoặc token của victim.")
    _evidence(doc, 2, SCREENSHOTS[1], missing)
    doc.add_paragraph("Khi victim còn đăng nhập và chủ động bấm gửi form demo, route vulnerable chỉ dựa vào session cookie nên email bị đổi.")
    _evidence(doc, 3, SCREENSHOTS[2], missing)
    doc.add_heading("2.3 Kiểm chứng bản secure", 2)
    doc.add_paragraph("Request thiếu hoặc sai token trả 403 và database không đổi.")
    _evidence(doc, 4, SCREENSHOTS[3], missing)
    doc.add_paragraph("Request từ Demo Page còn bị exact Origin/Referer validation từ chối trước mutation.")
    _evidence(doc, 5, SCREENSHOTS[4], missing)
    doc.add_paragraph("Request cùng origin có token hợp lệ cập nhật email; token được rotate sau thành công.")
    _evidence(doc, 6, SCREENSHOTS[5], missing)

    doc.add_heading("3. Nguyên nhân kỹ thuật", 1)
    doc.add_paragraph("Browser quản lý cookie và tự gắn cookie khi policy cho phép. Route vulnerable coi cookie xác thực là đủ bằng chứng về ý định, không yêu cầu token hoặc kiểm tra nguồn request. SOP thường ngăn trang khác đọc response nhưng không ngăn form HTML gửi request.")
    _code(doc, "# Vulnerable: chỉ dựa vào session\n@login_required\ndef vulnerable_change_email():\n    update_email(session['user_id'], request.form['email'])")

    doc.add_heading("4. Kết quả và bằng chứng", 1)
    doc.add_paragraph("Luồng vulnerable đổi state mà không có token. Luồng secure từ chối token thiếu/sai và Origin khác; chỉ request có session, Origin/Referer hợp lệ và token đúng mới cập nhật. Audit/trace ghi decision nhưng không lưu token/cookie đầy đủ.")
    _evidence(doc, 7, SCREENSHOTS[6], missing)

    doc.add_heading("5. Mức độ ảnh hưởng", 1)
    doc.add_paragraph("CSRF có thể làm sai tính toàn vẹn dữ liệu bằng quyền của victim. Đổi email trong hệ thống thật có thể hỗ trợ chiếm quyền; logout gây gián đoạn; thao tác tài chính có thể nghiêm trọng. Lab chỉ đổi dữ liệu giả lập local.")

    doc.add_heading("6. Bản vá và cách phòng chống", 1)
    doc.add_paragraph("Dùng token ngẫu nhiên duy nhất theo session, kiểm tra ở server trước mutation và rotate sau thành công. Kèm SameSite=Lax/Strict phù hợp, exact Origin/Referer, POST-only và re-authentication cho thao tác nhạy cảm. CAPTCHA và CORS không phải biện pháp chính.")
    _code(doc, "# Secure: kiểm tra trước UPDATE\nvalidate_origin_or_referer(request)\nvalidate_csrf_token(session['csrf_token'], request.form['csrf_token'])\nupdate_email(session['user_id'], validated_email)\nrotate_csrf_token(session)")

    doc.add_heading("7. Trả lời các câu hỏi báo cáo trong BaiTapTopic04.docx", 1)
    answers = [
        "Browser tự gửi cookie vì cookie jar và matching policy do browser quản lý; ứng dụng không cần tự thêm cookie vào từng form.",
        "CSRF không cần biết mật khẩu vì victim đã có session được xác thực; request lợi dụng credential đó.",
        "Trang tạo request cross-origin thường không đọc được response do SOP, nhưng request vẫn có thể thay đổi state.",
        "CSRF ép browser thực hiện hành động bằng credential sẵn có; XSS chạy script trong trusted origin và có thể đọc token trong DOM.",
        "Không dùng GET cho state change vì link, prefetch, cache hoặc crawler có thể kích hoạt ngoài ý muốn; thao tác phải dùng POST và kiểm tra token.",
    ]
    for i, answer in enumerate(answers, 1):
        doc.add_paragraph(f"{i}. {answer}")

    doc.add_heading("8. Kết quả kiểm thử", 1)
    pytest_summary = _log_summary(PYTEST_LOG)
    coverage_summary = _log_summary(COVERAGE_LOG)
    if pytest_summary:
        doc.add_paragraph("Pytest summary đọc từ evidence/logs/pytest.txt:")
        _code(doc, pytest_summary)
    else:
        doc.add_paragraph("Chưa có evidence/logs/pytest.txt; generator không tự ghi PASS.")
    if coverage_summary:
        doc.add_paragraph("Coverage summary đọc từ evidence/logs/coverage.txt:")
        _code(doc, coverage_summary)

    doc.add_heading("9. Kết luận", 1)
    doc.add_paragraph("CSRF tồn tại khi server nhầm credential tự động gửi với ý định của người dùng. Token server-side là lớp chính; Origin/Referer, SameSite, POST-only, re-authentication và audit là các lớp bổ sung.")

    REPORT.mkdir(parents=True, exist_ok=True)
    doc.save(DOCX)
    return DOCX


def build_pdf() -> Path | None:
    if PDF.exists():
        PDF.unlink()
    soffice = shutil.which("soffice")
    candidate = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
    if not soffice and candidate.exists():
        soffice = str(candidate)
    if not soffice:
        return None
    result = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(REPORT), str(DOCX)], capture_output=True, text=True, timeout=180)
    if result.returncode or not PDF.is_file():
        raise RuntimeError(result.stderr or result.stdout or "Không thể chuyển DOCX sang PDF.")
    return PDF


def main() -> int:
    missing: list[str] = []
    build_docx(missing)
    pdf = build_pdf()
    print(f"DOCX: {DOCX}")
    print(f"PDF: {pdf if pdf else 'chưa sinh - thiếu LibreOffice'}")
    print(f"Missing screenshots ({len(missing)}): {', '.join(missing) if missing else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
