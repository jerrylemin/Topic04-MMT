from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from screenshot_manifest import SCREENSHOTS  # noqa: E402

OUT = ROOT / "report"
SHOTS = ROOT / "evidence" / "screenshots"
DOCX_PATH = OUT / "21127645_LeMinh_Lab03_ParameterTampering.docx"
PDF_PATH = OUT / "21127645_LeMinh_Lab03_ParameterTampering.pdf"
PYTEST_LOG = ROOT / "evidence" / "logs" / "pytest.txt"

ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def clean_text(value: str) -> str:
    value = ANSI_ESCAPE.sub("", value)
    return "".join(ch for ch in value if ch in "\n\r\t" or ord(ch) >= 32)


def read_log(path: Path) -> str:
    data = path.read_bytes()
    encoding = "utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return clean_text(data.decode(encoding, errors="replace"))


def pytest_summary(path: Path, max_lines: int = 4) -> str:
    """Return concise pytest result lines without embedding a traceback."""
    lines = [line.strip() for line in read_log(path).splitlines() if line.strip()]
    result_lines = [
        line for line in lines
        if line.startswith(("FAILED ", "ERROR "))
        or (" passed" in line and " in " in line)
        or (" failed" in line and " in " in line)
    ]
    if not result_lines:
        result_lines = lines[-max_lines:]
    return "\n".join(result_lines[-max_lines:])


def _set_cell_fill(cell, color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = tc_pr.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        tc_pr.append(shading)
    shading.set(qn("w:fill"), color)


def _set_cell_border(cell, color="2E74B5", size="14") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)
        borders.append(element)


def _style_document(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(1.7)
    section.left_margin = section.right_margin = Cm(1.8)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08
    for name, size, color in (("Heading 1", 16, "1F4E79"), ("Heading 2", 12.5, "2E74B5"), ("Heading 3", 11, "1F4E79")):
        style = doc.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(9)
        style.paragraph_format.space_after = Pt(4)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Lab03 - Parameter Tampering | 21127645 - Lê Minh")


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


def image_size(path: Path, max_width: float = 6.35, max_height: float = 6.3) -> tuple[float, float]:
    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return width * scale, height * scale


def _add_caption(doc: Document, text: str) -> None:
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = False
    for run in p.runs:
        run.italic = True
        run.font.size = Pt(9)


def _add_evidence(doc: Document, index: int, item: dict, missing: list[str]) -> None:
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
        _set_cell_fill(cell, "EAF3F8")
        _set_cell_border(cell)
        details = [
            f"ẢNH {index:02d}/{len(SCREENSHOTS):02d}",
            f"Tên file: {item['filename']}",
            f"Tiêu đề ảnh: {item['purpose']}",
            "Chèn ảnh tại vị trí này.",
            f"URL hoặc lệnh: {item['url_command']}",
            f"Thao tác: {item['input']} | {item['button']}",
            f"Panel hoặc DevTools tab: {item['panel']}",
            f"Nội dung bắt buộc phải thấy: {item['required']}",
            f"Kết quả mong đợi: {item['expected']}",
            f"Caption: {item['caption']}",
        ]
        for line_no, line in enumerate(details):
            p = cell.paragraphs[0] if line_no == 0 else cell.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_together = True
            p.paragraph_format.keep_with_next = line_no < len(details) - 1
            run = p.add_run(line)
            run.font.name = "Arial"
            run.font.size = Pt(10 if line_no else 12)
            run.bold = line_no in (0, 1, 3)
    _add_caption(doc, f"Hình {index}. {item['caption']}")


def _code(doc: Document, text: str) -> None:
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.cell(0, 0)
    _set_cell_fill(cell, "F3F5F7")
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)


def build_docx(missing: list[str] | None = None) -> Path:
    missing = missing if missing is not None else []
    doc = Document()
    _style_document(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(100)
    r = p.add_run("BÁO CÁO THỰC HÀNH\nLAB03 - PARAMETER TAMPERING")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor(31, 78, 121)
    for line in ("Môn: Mạng máy tính", "Sinh viên: Lê Minh", "MSSV: 21127645", "Môi trường: localhost - dữ liệu giả lập"):
        q = doc.add_paragraph(line)
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    doc.add_heading("1. Mục tiêu và môi trường thực hành", 1)
    doc.add_paragraph("Mục tiêu là nhận biết thao túng tham số phía client, phân biệt validation với authorization và kiểm chứng ba bản vá: lấy giá từ database, kiểm tra quyền sở hữu hóa đơn, và chỉ cho phép cập nhật field an toàn.")
    doc.add_paragraph("Ứng dụng Flask/SQLite chạy tại http://127.0.0.1:5003. Tài khoản dùng trong ảnh là user_a; product 5 có giá 100000 VND, invoice 1001 thuộc User A và invoice 1002 thuộc User B. Phạm vi chỉ là dữ liệu lab local.")

    doc.add_heading("2. Kịch bản và các bước thực hiện", 1)
    doc.add_heading("2.1 Checkout bình thường", 2)
    doc.add_paragraph("User A thêm product 5, quantity 1 và gửi checkout với price=100000 để xác nhận luồng ban đầu.")
    _add_evidence(doc, 1, SCREENSHOTS[0], missing)
    doc.add_heading("2.2 Thay đổi giá", 2)
    doc.add_paragraph("Trên bản vulnerable, sửa hidden price thành 1; server dùng giá client và tạo invoice 1 VND.")
    _add_evidence(doc, 2, SCREENSHOTS[1], missing)
    doc.add_paragraph("Gửi cùng price=1 vào bản secure. Server truy vấn products.price_vnd=100000, bỏ qua giá client và ghi audit mismatch.")
    _add_evidence(doc, 3, SCREENSHOTS[2], missing)
    doc.add_heading("2.3 IDOR hóa đơn", 2)
    doc.add_paragraph("User A đổi id=1001 thành id=1002. Bản vulnerable trả hóa đơn User B vì chỉ truy vấn theo ID.")
    _add_evidence(doc, 4, SCREENSHOTS[3], missing)
    doc.add_paragraph("Bản secure lấy user_id từ session, áp dụng policy owner-or-admin và trả 403 trước khi render dữ liệu.")
    _add_evidence(doc, 5, SCREENSHOTS[4], missing)
    doc.add_heading("2.4 Thay đổi quyền", 2)
    doc.add_paragraph("Bản vulnerable nhận role=admin từ hidden field và cập nhật trực tiếp database/session.")
    # LibreOffice có thể đặt một row không tách ngay sát đáy trang nhưng vẫn cắt
    # phần đầu khi chuyển trang. Page break rõ ràng giữ trọn placeholder 06.
    doc.add_page_break()
    _add_evidence(doc, 6, SCREENSHOTS[5], missing)
    doc.add_paragraph("Sau reset, bản secure chỉ allowlist email, lấy identity từ session và giữ role=user dù client gửi role/user_id.")
    _add_evidence(doc, 7, SCREENSHOTS[6], missing)

    doc.add_heading("3. Nguyên nhân kỹ thuật", 1)
    doc.add_paragraph("Cả ba lỗi có cùng trust-boundary sai: server dùng dữ liệu do client kiểm soát để quyết định giá, object hoặc quyền. Hidden field không bí mật; integer hợp lệ vẫn có thể trỏ đến object trái quyền; parameterized SQL không sửa được lỗi business logic.")
    _code(doc, "# Vulnerable - dữ liệu client quyết định\nsubmitted_price = int(request.form['price'])\ninvoice = get_invoice(request.args['id'])\nrole = request.form['role']")

    doc.add_heading("4. Kết quả và bằng chứng", 1)
    doc.add_paragraph("Bản vulnerable lần lượt chấp nhận giá 1 VND, trả invoice 1002 cho User A và đổi role thành admin. Bản secure giữ giá database, trả 403 cho IDOR và loại field role/user_id. Audit liên kết các quyết định với trace thật.")
    # Tránh LibreOffice tự đẩy row từ cuối trang rồi cắt các dòng đầu.
    evidence_heading = doc.add_heading("4.1 Audit, pytest và report artifacts", 2)
    evidence_heading.paragraph_format.page_break_before = True
    evidence_heading.paragraph_format.keep_with_next = True
    _add_evidence(doc, 8, SCREENSHOTS[7], missing)

    doc.add_heading("5. Mức độ ảnh hưởng", 1)
    doc.add_paragraph("Sửa giá gây sai lệch tài chính; IDOR làm lộ dữ liệu người khác; mass assignment có thể nâng quyền. Trong hệ thống thật, mức ảnh hưởng có thể cao đến nghiêm trọng. Lab chỉ dùng dữ liệu giả lập và không thực hiện giao dịch thật.")

    doc.add_heading("6. Bản vá và cách phòng chống", 1)
    doc.add_paragraph("Giá phải lấy từ database; danh tính phải lấy từ session; mỗi invoice phải kiểm tra owner hoặc quyền admin; self-service profile chỉ nhận allowlist field. Kèm validation kiểu/phạm vi, transaction, audit, least privilege và kiểm thử hồi quy.")
    _code(doc, "# Secure - quyết định ở server\nproduct = get_product(product_id)\ntotal = product['price_vnd'] * quantity\ninvoice = get_invoice_for_owner(invoice_id, session['user_id'])\nallowed = {'email': request.form.get('email')}")

    doc.add_heading("7. Trả lời các câu hỏi báo cáo trong BaiTapTopic04.docx", 1)
    answers = [
        "Parameter Tampering sửa giá trị request hợp lệ để làm sai logic/quyền; SQL Injection chèn cú pháp làm đổi cấu trúc câu SQL.",
        "Hidden field không phải cơ chế bảo mật vì người dùng kiểm soát DOM và request.",
        "IDOR thuộc Broken Access Control trong OWASP Top 10, cụ thể là thiếu object-level authorization.",
        "Trước khi trả invoice, server phải xác thực session, validate ID, tìm object và kiểm tra owner hoặc quyền admin.",
        "Không nên truyền giá sản phẩm từ client như nguồn quyết định vì client sửa được; server phải lấy giá hiện hành từ database.",
    ]
    for index, answer in enumerate(answers, 1):
        doc.add_paragraph(f"{index}. {answer}")

    doc.add_heading("8. Kết quả kiểm thử", 1)
    if PYTEST_LOG.is_file() and PYTEST_LOG.stat().st_size:
        summary = pytest_summary(PYTEST_LOG)
        doc.add_paragraph("Kết quả được đọc từ evidence/logs/pytest.txt, không ghi cứng:")
        _code(doc, summary)
    else:
        doc.add_paragraph("Chưa có evidence/logs/pytest.txt. Chạy `python -m pytest -q` và lưu output thật trước khi nộp; generator không tự ghi PASS.")

    doc.add_heading("9. Kết luận", 1)
    doc.add_paragraph("Lab chứng minh client không phải vùng tin cậy. Bản vá hiệu quả khi mọi quyết định giá, danh tính và quyền được thực hiện ở server, còn audit/trace chỉ hỗ trợ quan sát và phát hiện bất thường.")

    OUT.mkdir(parents=True, exist_ok=True)
    doc.save(DOCX_PATH)
    return DOCX_PATH


def build_pdf() -> Path | None:
    if PDF_PATH.exists():
        PDF_PATH.unlink()
    soffice = shutil.which("soffice")
    windows_soffice = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
    if not soffice and windows_soffice.exists():
        soffice = str(windows_soffice)
    if not soffice:
        return None
    result = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(DOCX_PATH)], capture_output=True, text=True, timeout=180)
    if result.returncode != 0 or not PDF_PATH.is_file():
        raise RuntimeError(result.stderr or result.stdout or "Không thể chuyển DOCX sang PDF.")
    return PDF_PATH


def main() -> int:
    missing: list[str] = []
    build_docx(missing)
    pdf = build_pdf()
    print(f"DOCX: {DOCX_PATH}")
    print(f"PDF: {pdf if pdf else 'chưa sinh - thiếu LibreOffice'}")
    print(f"Missing screenshots ({len(missing)}): {', '.join(missing) if missing else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
