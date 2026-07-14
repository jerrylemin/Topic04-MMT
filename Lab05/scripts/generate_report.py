"""Sinh báo cáo Lab05 ngắn gọn; dùng ảnh thật nếu hợp lệ, nếu không dùng placeholder."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
try:
    from .screenshot_manifest import SCREENSHOTS, EXPECTED_FILES
    from .check_screenshots import png_dimensions, MIN_WIDTH, MIN_HEIGHT
except ImportError:
    from screenshot_manifest import SCREENSHOTS, EXPECTED_FILES
    from check_screenshots import png_dimensions, MIN_WIDTH, MIN_HEIGHT

ROOT=Path(__file__).resolve().parents[1]; SHOTS=ROOT/"evidence"/"screenshots"; REPORT=ROOT/"report"
DOCX_NAME="21127645_LeMinh_Lab05_SQLInjection.docx"; PDF_NAME="21127645_LeMinh_Lab05_SQLInjection.pdf"
REPORT_SECTIONS=("1. Mục tiêu và môi trường thực hành","2. Kịch bản và các bước thực hiện","3. Nguyên nhân kỹ thuật","4. Kết quả và bằng chứng","5. Mức độ ảnh hưởng","6. Bản vá và cách phòng chống","7. Trả lời các câu hỏi báo cáo trong BaiTapTopic04.docx","8. Kết quả kiểm thử","9. Kết luận")
QA_ANSWERS=(
 ("SQL Injection xảy ra ở tầng nào của ứng dụng?","Lỗi xuất hiện ở tầng truy cập dữ liệu khi ứng dụng ghép input vào câu SQL; input đi từ HTTP nhưng được SQLite diễn giải thành cú pháp."),
 ("Vì sao escaping thủ công dễ sai?","Quy tắc phụ thuộc DB, encoding và ngữ cảnh. Chỉ cần bỏ sót một nhánh hoặc ký tự là dữ liệu lại có thể trở thành mã SQL."),
 ("Prepared statement khác nối chuỗi SQL như thế nào?","Prepared statement giữ cấu trúc SQL cố định và truyền input như tham số; nối chuỗi trộn mã với dữ liệu trước khi DB phân tích."),
 ("ORM có tự động chống SQL Injection trong mọi trường hợp không?","Không. ORM an toàn khi dùng API bind tham số; raw SQL, biểu thức ghép chuỗi hoặc API dùng sai vẫn có thể gây injection."),
 ("Vì sao không nên hiển thị lỗi SQL chi tiết?","Thông tin về cú pháp, bảng và driver giúp suy đoán backend. Người dùng chỉ nên nhận thông báo chung; chi tiết được ghi log nội bộ đã redaction."),
)
VULN_CODE="sql = \"SELECT * FROM users WHERE username = '%s' AND password = '%s'\" % (username, digest)\nrow = conn.execute(sql).fetchone()"
FIX_CODE="row = conn.execute(\"SELECT * FROM users WHERE username = ?\", (username,)).fetchone()\nvalid = row and check_password_hash(row[\"password_hash\"], password)"

def _valid_image(path: Path)->bool:
    try: w,h=png_dimensions(path); return path.stat().st_size>0 and w>=MIN_WIDTH and h>=MIN_HEIGHT
    except (OSError,ValueError): return False
def _summary(path: Path, kind: str)->str:
    if not path.is_file(): return f"Chưa có log {kind}; không tuyên bố kết quả."
    text=path.read_text(encoding="utf-8",errors="replace")
    if kind=="pytest":
        m=re.search(r"(?P<p>\d+) passed(?:, (?P<f>\d+) failed)?",text)
        return (f"Pytest ghi nhận: {m.group('p')} passed"+(f", {m.group('f')} failed" if m and m.group('f') else "")+".") if m else "Log pytest không có dòng tổng kết nhận diện được."
    m=re.search(r"^TOTAL\s+.*?(\d+)%\s*$",text,re.M)
    return f"Coverage tổng ghi nhận: {m.group(1)}%." if m else "Log coverage không có dòng TOTAL nhận diện được."

def _shade(cell,fill="FFF4CC"):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement("w:shd"); shd.set(qn("w:fill"),fill); tcPr.append(shd)
    borders=tcPr.first_child_found_in("w:tcBorders")
    if borders is None: borders=OxmlElement("w:tcBorders"); tcPr.append(borders)
    for edge in ("top","left","bottom","right"):
        node=OxmlElement(f"w:{edge}"); node.set(qn("w:val"),"single"); node.set(qn("w:sz"),"10"); node.set(qn("w:color"),"D49A00"); borders.append(node)
def _add_evidence_docx(doc:Document,index:int,item:dict,missing:list[str]):
    path=SHOTS/item["name"]
    if _valid_image(path):
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(path),width=Inches(6.1))
        c=doc.add_paragraph(f"Hình {index}. {item['caption']}"); c.alignment=WD_ALIGN_PARAGRAPH.CENTER
        return
    missing.append(item["name"]); table=doc.add_table(rows=1,cols=1); cell=table.cell(0,0); _shade(cell); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    lines=(f"ẢNH {index:02d}/{len(SCREENSHOTS):02d}",f"Tên file: {item['name']}",f"Tiêu đề ảnh: {item['title']}","Chèn ảnh tại vị trí này.",f"URL hoặc lệnh: {item['url']}",f"Thao tác: {item['action']}",f"Panel hoặc DevTools tab cần mở: {item['panel']}",f"Nội dung bắt buộc phải thấy: {item['must_show']}",f"Kết quả mong đợi: {item['expected']}",f"Caption: {item['caption']}")
    for n,line in enumerate(lines):
        p=cell.paragraphs[0] if n==0 else cell.add_paragraph(); r=p.add_run(line); r.bold=n in (0,1); r.font.size=Pt(9)
def _styles(doc:Document):
    sec=doc.sections[0]; sec.page_width=Inches(8.27); sec.page_height=Inches(11.69); sec.top_margin=sec.bottom_margin=Inches(.65); sec.left_margin=sec.right_margin=Inches(.7)
    normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(10.5); normal.paragraph_format.space_after=Pt(4)
    for name,size,color in (("Title",24,"17365D"),("Heading 1",15,"1F4E79"),("Heading 2",12,"2F5597")):
        s=doc.styles[name]; s.font.name="Arial"; s.font.size=Pt(size); s.font.color.rgb=RGBColor.from_string(color); s.font.bold=True
def build_docx(path:Path)->list[str]:
    doc=Document(); _styles(doc); missing=[]
    p=doc.add_paragraph(style="Title"); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run("BÁO CÁO THỰC HÀNH LAB 5\nSQL INJECTION")
    for line in ("Sinh viên: Lê Minh - MSSV: 21127645","Môi trường: Flask/SQLite tại http://127.0.0.1:5005","Phạm vi: dữ liệu giả lập, hoàn toàn trên localhost"):
        x=doc.add_paragraph(line); x.alignment=WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()
    doc.add_heading(REPORT_SECTIONS[0],1); doc.add_paragraph("Mục tiêu là nhận diện SQL Injection do nối chuỗi, quan sát login/search trong lab và chứng minh bản vá parameterized query. Môi trường dùng Python, Flask, SQLite và trình duyệt trên loopback; không kết nối website thật.")
    doc.add_heading(REPORT_SECTIONS[1],1)
    steps=(
      ("2.1 Luồng bình thường","Reset database, đăng nhập tài khoản demo và tìm USB để có mốc đối chiếu.",[0]),
      ("2.2 Phát hiện bằng dấu nháy đơn","Gửi kịch bản dấu nháy cố định. Câu SQL ghép chuỗi lỗi; ứng dụng chỉ trả lỗi chung.",[1]),
      ("2.3 Authentication bypass local","Gửi kịch bản cố định làm thay đổi điều kiện WHERE; bản vulnerable tạo phiên dù không biết mật khẩu.",[2]),
      ("2.4 Injection tại search","Gửi kịch bản cố định làm điều kiện đúng rộng hơn và trả thêm sản phẩm local.",[3]),
      ("2.5 Secure login","Gửi lại cùng chuỗi. Placeholder tách SQL khỏi dữ liệu nên username literal không khớp.",[4]),
      ("2.6 Secure search","Gửi lại cùng keyword. LIKE ? giữ cấu trúc query và không mở rộng tập kết quả.",[5]),)
    for title,text,ids in steps:
        doc.add_heading(title,2); doc.add_paragraph(text)
        for i in ids:_add_evidence_docx(doc,i+1,SCREENSHOTS[i],missing)
    doc.add_heading(REPORT_SECTIONS[2],1); doc.add_paragraph("Root cause là dữ liệu HTTP được ghép trực tiếp vào chuỗi SQL trước khi SQLite phân tích. Dấu nháy đóng literal; phần còn lại thay đổi cú pháp hoặc logic WHERE. Ở search, input nằm trong LIKE nên có thể mở rộng điều kiện. Lỗi thuộc tầng truy cập dữ liệu, không phải do HTTP tự thân.")
    doc.add_heading(REPORT_SECTIONS[3],1); doc.add_paragraph("Bằng chứng 01-04 thể hiện baseline, lỗi, bypass và mở rộng kết quả; ảnh 05-06 dùng cùng input để chứng minh bản secure giữ nguyên cấu trúc SQL. Trace, query event và audit thật được generator giữ làm nguồn đối chiếu, không thay bằng kết quả giả.")
    doc.add_heading(REPORT_SECTIONS[4],1); doc.add_paragraph("Ảnh hưởng gồm vượt xác thực, đọc dữ liệu ngoài dự kiến, suy đoán cấu trúc backend qua lỗi và làm sai quyết định nghiệp vụ. Trong hệ thống thật, mức độ có thể nghiêm trọng nếu tài khoản DB có quyền rộng; lab giới hạn SELECT và dữ liệu giả lập local.")
    doc.add_heading(REPORT_SECTIONS[5],1); doc.add_paragraph("Bản vá chính là prepared statement/parameterized query. Mật khẩu dùng PBKDF2 thay plaintext; lỗi trả thông báo chung; input được kiểm tra kiểu/độ dài; tài khoản DB cần least privilege; audit/monitoring và WAF chỉ là lớp bổ sung.")
    doc.add_heading("Đoạn vulnerable",2); doc.add_paragraph(VULN_CODE,style="Normal"); doc.add_heading("Đoạn secure",2); doc.add_paragraph(FIX_CODE,style="Normal"); _add_evidence_docx(doc,7,SCREENSHOTS[6],missing)
    doc.add_heading(REPORT_SECTIONS[6],1)
    for q,a in QA_ANSWERS: doc.add_heading(q,2); doc.add_paragraph(a)
    doc.add_heading(REPORT_SECTIONS[7],1); doc.add_paragraph(_summary(ROOT/"evidence/logs/pytest.txt","pytest")); doc.add_paragraph(_summary(ROOT/"evidence/logs/coverage.txt","coverage")); doc.add_paragraph("Các con số trên được đọc từ log hiện có; nếu log không nhận diện được, báo cáo ghi rõ thay vì hard-code PASS."); _add_evidence_docx(doc,8,SCREENSHOTS[7],missing)
    doc.add_heading(REPORT_SECTIONS[8],1); doc.add_paragraph("Thực nghiệm cho thấy ranh giới mã SQL và dữ liệu phải được duy trì bằng binding. Validation, generic error, hashing, least privilege và monitoring tăng chiều sâu phòng thủ nhưng không thay thế sửa câu query.")
    path.parent.mkdir(parents=True,exist_ok=True); doc.save(path); return missing

def _pdf_font():
    for regular,bold in ((r"C:\Windows\Fonts\arial.ttf",r"C:\Windows\Fonts\arialbd.ttf"),("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if Path(regular).is_file() and Path(bold).is_file(): pdfmetrics.registerFont(TTFont("Lab",regular)); pdfmetrics.registerFont(TTFont("LabB",bold)); return
    raise RuntimeError("Không tìm thấy font Unicode cho PDF")
def build_pdf(path:Path)->list[str]:
    _pdf_font(); styles=getSampleStyleSheet(); body=ParagraphStyle("body",parent=styles["BodyText"],fontName="Lab",fontSize=9.2,leading=11.2,spaceAfter=5); h1=ParagraphStyle("h1",parent=styles["Heading1"],fontName="LabB",fontSize=14,textColor=colors.HexColor("#1F4E79"),spaceBefore=9,spaceAfter=5); h2=ParagraphStyle("h2",parent=styles["Heading2"],fontName="LabB",fontSize=11,textColor=colors.HexColor("#2F5597"),spaceBefore=6,spaceAfter=3); center=ParagraphStyle("center",parent=body,alignment=TA_CENTER); story=[Spacer(1,1.5*inch),Paragraph("BÁO CÁO THỰC HÀNH LAB 5",ParagraphStyle("title",parent=h1,fontSize=23,alignment=TA_CENTER)),Paragraph("SQL INJECTION",ParagraphStyle("sub",parent=h1,fontSize=17,alignment=TA_CENTER)),Spacer(1,.4*inch),Paragraph("Sinh viên: Lê Minh - MSSV: 21127645",center),Paragraph("Flask/SQLite - http://127.0.0.1:5005 - localhost",center),PageBreak()]; missing=[]
    def ev(i):
        item=SCREENSHOTS[i]; img=SHOTS/item["name"]
        if _valid_image(img):
            figure=Image(str(img)); figure._restrictSize(6.2*inch,4.4*inch)
            story.extend([figure,Paragraph(f"Hình {i+1}. {item['caption']}",center)])
        else:
            missing.append(item["name"]); text="<br/>".join((f"<b>ẢNH {i+1:02d}/{len(SCREENSHOTS):02d}</b>",f"<b>Tên file:</b> {item['name']}",f"<b>Tiêu đề ảnh:</b> {item['title']}","Chèn ảnh tại vị trí này.",f"<b>URL hoặc lệnh:</b> {item['url']}",f"<b>Thao tác:</b> {item['action']}",f"<b>Panel:</b> {item['panel']}",f"<b>Phải thấy:</b> {item['must_show']}",f"<b>Kết quả:</b> {item['expected']}",f"<b>Caption:</b> {item['caption']}")); t=Table([[Paragraph(text,body)]],colWidths=[6.5*inch]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#FFF4CC")),("BOX",(0,0),(-1,-1),1,colors.HexColor("#D49A00")),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])); story.append(t)
    story += [Paragraph(REPORT_SECTIONS[0],h1),Paragraph("Mục tiêu là nhận diện SQL Injection do nối chuỗi và chứng minh parameterized query trên Flask/SQLite local.",body),Paragraph(REPORT_SECTIONS[1],h1)]
    for title,text,ids in (("2.1 Luồng bình thường","Đăng nhập demo và tìm USB để có mốc đối chiếu.",[0]),("2.2 Dấu nháy đơn","Bản vulnerable có lỗi query đã xử lý.",[1]),("2.3 Authentication bypass","Điều kiện WHERE bị thay đổi trong lab local.",[2]),("2.4 Search mở rộng","Điều kiện LIKE trả thêm sản phẩm.",[3]),("2.5 Secure login","Placeholder tách dữ liệu và SQL.",[4]),("2.6 Secure search","LIKE ? giữ nguyên cấu trúc query.",[5])): story += [Paragraph(title,h2),Paragraph(text,body)]; [ev(i) for i in ids]
    story += [Paragraph(REPORT_SECTIONS[2],h1),Paragraph("Input HTTP bị ghép vào SQL trước khi SQLite phân tích; dấu nháy và phần sau trở thành cú pháp thay vì dữ liệu.",body),Paragraph(REPORT_SECTIONS[3],h1),Paragraph("Ảnh 01-06 đối chiếu cùng kịch bản ở vulnerable và secure; trace/audit thật là nguồn hỗ trợ.",body),Paragraph(REPORT_SECTIONS[4],h1),Paragraph("Ảnh hưởng gồm vượt xác thực, đọc dữ liệu ngoài dự kiến và rò rỉ chi tiết backend. Lab giới hạn SELECT và dữ liệu local.",body),Paragraph(REPORT_SECTIONS[5],h1),Paragraph("Dùng parameter binding, PBKDF2, generic error, validation, least privilege và monitoring.",body),Paragraph("Đoạn vulnerable",h2),Paragraph(VULN_CODE.replace("\n","<br/>"),body),Paragraph("Đoạn secure",h2),Paragraph(FIX_CODE.replace("\n","<br/>"),body)]; ev(6); story.append(Paragraph(REPORT_SECTIONS[6],h1))
    for q,a in QA_ANSWERS: story += [Paragraph(q,h2),Paragraph(a,body)]
    story += [Paragraph(REPORT_SECTIONS[7],h1),Paragraph(_summary(ROOT/"evidence/logs/pytest.txt","pytest"),body),Paragraph(_summary(ROOT/"evidence/logs/coverage.txt","coverage"),body)]; ev(7); story += [Paragraph(REPORT_SECTIONS[8],h1),Paragraph("Binding duy trì ranh giới mã/dữ liệu; các control khác tạo phòng thủ nhiều lớp.",body)]
    path.parent.mkdir(parents=True,exist_ok=True); SimpleDocTemplate(str(path),pagesize=A4,leftMargin=.7*inch,rightMargin=.7*inch,topMargin=.6*inch,bottomMargin=.6*inch).build(story); return missing
def main()->int:
    REPORT.mkdir(exist_ok=True); missing=build_docx(REPORT/DOCX_NAME); pdf_missing=build_pdf(REPORT/PDF_NAME); assert missing==pdf_missing
    print(json.dumps({"docx":str(REPORT/DOCX_NAME),"pdf":str(REPORT/PDF_NAME),"required":len(EXPECTED_FILES),"missing_screenshots":missing},ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
