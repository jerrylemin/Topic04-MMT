import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from screenshot_manifest import SCREENSHOTS
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT=Path(__file__).parents[1]; SHOTS=ROOT/"evidence/screenshots"; OUT=ROOT/"report"; OUT.mkdir(exist_ok=True)
DOCX=OUT/"21127645_LeMinh_Lab01_XSS.docx"; PDF=OUT/"21127645_LeMinh_Lab01_XSS.pdf"
LABS=[
 ("Reflected XSS",'request.args["q"]',"Markup(q) trong HTML","Jinja autoescape",[
  ("Browser UI","Nhập payload","Raw input","HTML form","Dữ liệu tainted"),("HTTP Request","Tạo GET","URL encoded","Percent encoding","Query string"),("Flask Router","Đọc q","request.args","URL decode","Python string"),("Server Validation","Giới hạn 200","q","Length check","q hợp lệ"),("Template Engine","Render q","q","Markup hoặc autoescape","HTML unsafe/text"),("HTTP Response","Trả HTML","Rendered template","HTTP","Response body"),("Browser Parser","Parse response","HTML","HTML parser","Element hoặc text node"),("Final Result","Kết luận","DOM","Event/text","Executed hoặc blocked")]),
 ("Stored XSS",'request.form["body"] → comments.body',"Markup(row[body])","Bleach allowlist + Jinja",[
  ("Browser UI","Nhập comment","Author/body","HTML form","Form data"),("HTTP Request","POST","Form data","urlencoded body","request.form"),("Flask Router","Đọc form","request.form","Flask","Python string"),("Validation","Kiểm tra rỗng/độ dài","Body","Length check","Hợp lệ"),("SQLite","INSERT","Body","Parameterized SQL","Stored row"),("SQLite","SELECT","post_id=1","Parameterized SQL","Rows"),("Template Engine","Render body","DB value","Markup/Bleach","Unsafe/sanitized HTML"),("Browser Parser","Parse comment","HTML","Parser","Event/text"),("Final Result","Reload","Stored payload","Repeat render","Executed hoặc blocked")]),
 ("DOM-based XSS","location.hash","innerHTML","textContent",[
  ("Browser UI","Đổi fragment","URL fragment","hashchange","Client state"),("HTTP Request","Gửi path","URL","HTTP semantics","Không có fragment"),("Browser JavaScript","Đọc hash","location.hash","slice/decodeURIComponent","Decoded value"),("DOM","Gán sink","Decoded value","innerHTML/textContent","Element/text node"),("DOM Inspector","Đọc outerHTML","DOM hiện tại","DOM API","Tag/event count"),("Final Result","Kết luận","DOM","Browser event","Executed hoặc blocked")])]

def fit(path: Path, max_w: float, max_h: float):
    with PILImage.open(path) as image: w,h=image.size
    scale=min(max_w/w,max_h/h); return w*scale,h*scale

doc=Document(); section=doc.sections[0]; section.top_margin=section.bottom_margin=Inches(.75); section.left_margin=section.right_margin=Inches(.8)
for style in ["Normal","Title","Heading 1","Heading 2"]:
    doc.styles[style].font.name="Arial"
doc.styles["Normal"].font.size=Pt(10.5); doc.styles["Heading 1"].font.color.rgb=RGBColor(23,74,132)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; run=p.add_run("LAB 01 — CROSS-SITE SCRIPTING"); run.bold=True; run.font.size=Pt(26); run.font.color.rgb=RGBColor(23,74,132)
for text in ["BÁO CÁO TRỰC QUAN HÓA LUỒNG XỬ LÝ", "MSSV: 21127645", "Họ tên: Lê Minh"]:
    p=doc.add_paragraph(text); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_page_break(); doc.add_heading("Mục lục",0)
for text in ["1. Mục tiêu và an toàn","2. Kiến thức nền","3. Reflected XSS","4. Stored XSS","5. DOM-based XSS","6. CSP và cookie","7. Kiểm thử","8. Phụ lục 28 ảnh"]: doc.add_paragraph(text)
doc.add_page_break(); doc.add_heading("1. Mục tiêu và an toàn",1); doc.add_paragraph("Theo dõi dữ liệu thật từ thao tác người dùng qua request, Flask, SQLite/Jinja, response và browser; so sánh bản có lỗ hổng với bản đã vá. Lab chỉ bind 127.0.0.1, không gửi trace hay payload ra Internet.")
doc.add_heading("2. Kiến thức nền",1); doc.add_paragraph("Source là nơi dữ liệu không tin cậy đi vào. Transform là các bước decode, validation, lưu trữ hoặc sanitization. Sink quyết định dữ liệu được xem là text hay mã. Input validation không thay output encoding; CSP và HttpOnly là defense in depth.")
for index,(name,source,sink,fix,rows) in enumerate(LABS,3):
    doc.add_heading(f"{index}. {name}",1); doc.add_paragraph(f"Mục tiêu: truy vết source `{source}` tới sink `{sink}` và kiểm chứng bản vá `{fix}`.")
    doc.add_heading("Sequence / data flow",2); doc.add_paragraph(" → ".join(row[0] for row in rows)); doc.add_paragraph(f"Source: {source} → Transform → Sink: {sink} → Result. Bản vá thay sink/transform bằng {fix}.")
    table=doc.add_table(rows=1,cols=7); table.style="Table Grid"
    for cell,text in zip(table.rows[0].cells,["STT","Layer","Hành động","Input","Kỹ thuật","Output","Ý nghĩa"]): cell.text=text
    for i,row in enumerate(rows,1):
        cells=table.add_row().cells
        values=[str(i),*row]
        for cell,text in zip(cells,values): cell.text=text
    doc.add_heading("Phân tích thực nghiệm",2); doc.add_paragraph(f"Request và route được lấy từ thao tác thật. Phiên bản lỗi đưa dữ liệu tới {sink}, khiến browser có thể diễn giải payload thành mã. Phiên bản secure dùng {fix}; dữ liệu trở thành text hoặc HTML trong allowlist. Mức ảnh hưởng: {'mọi người xem và nhiều lần reload' if name.startswith('Stored') else 'người mở URL/fragment'}.")
doc.add_heading("6. CSP và cookie",1); doc.add_paragraph("Flask after_request thêm CSP: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src/base-uri/frame-ancestors 'none'; form-action 'self'. Cookie dùng HttpOnly và SameSite=Lax; Secure=False cho local HTTP, production HTTPS phải True. HttpOnly không vá XSS.")
doc.add_heading("7. Kiểm thử",1); log=ROOT/"evidence/logs/pytest.txt"; doc.add_paragraph(log.read_text(encoding="utf-8",errors="replace") if log.exists() else "Chưa có log pytest.")
doc.add_heading("8. Phụ lục ảnh từng bước",1); missing=[]
for filename,url,action,required in SCREENSHOTS:
    path=SHOTS/filename; doc.add_heading(filename,2)
    if path.exists() and path.stat().st_size:
        w,h=fit(path,6.5,8.2); doc.add_picture(str(path),width=Inches(w),height=Inches(h)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    else:
        missing.append(filename); table=doc.add_table(rows=4,cols=1); table.style="Table Grid"
        for cell,text in zip([row.cells[0] for row in table.rows],[f"ẢNH CẦN BỔ SUNG: {filename}",f"URL: {url}",f"Thao tác: {action}",f"Phải xuất hiện: {required}"]): cell.text=text
    doc.add_paragraph(f"Caption: {required}")
doc.save(DOCX)

font_path=Path("C:/Windows/Fonts/arial.ttf"); font="ArialVN" if font_path.exists() else "Helvetica"
if font_path.exists(): pdfmetrics.registerFont(TTFont(font,str(font_path)))
styles=getSampleStyleSheet(); body=ParagraphStyle("VN",parent=styles["BodyText"],fontName=font,fontSize=9,leading=13); heading=ParagraphStyle("HVN",parent=styles["Heading1"],fontName=font,textColor=colors.HexColor("#174a84")); title=ParagraphStyle("TVN",parent=styles["Title"],fontName=font)
story=[Paragraph("LAB 01 — CROSS-SITE SCRIPTING",title),Paragraph("MSSV: 21127645 — Họ tên: Lê Minh",body),PageBreak(),Paragraph("Mục tiêu và an toàn",heading),Paragraph("Trace dữ liệu thật qua Browser → HTTP → Flask → SQLite/Jinja → Response → DOM. Chỉ chạy tại 127.0.0.1.",body)]
for name,source,sink,fix,rows in LABS:
    story += [PageBreak(),Paragraph(name,heading),Paragraph(f"Source: {source} → Transform → Sink: {sink} → Result. Bản vá: {fix}.",body)]
    data=[["STT","Layer","Hành động","Kỹ thuật","Output"]]+[[str(i),r[0],r[1],r[3],r[4]] for i,r in enumerate(rows,1)]
    story.append(Table(data,colWidths=[.7*cm,3.2*cm,4.2*cm,4*cm,5*cm],repeatRows=1,style=TableStyle([("GRID",(0,0),(-1,-1),.35,colors.grey),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#dceafa")),("FONTNAME",(0,0),(-1,-1),font),("FONTSIZE",(0,0),(-1,-1),7)])))
story += [PageBreak(),Paragraph("CSP, cookie và kiểm thử",heading),Paragraph("CSP là lớp bổ sung; HttpOnly không vá XSS; production HTTPS phải bật Secure cookie.",body),Paragraph(log.read_text(encoding="utf-8",errors="replace") if log.exists() else "Chưa có log pytest.",body)]
for filename,url,action,required in SCREENSHOTS:
    path=SHOTS/filename; story += [PageBreak(),Paragraph(filename,heading)]
    if path.exists() and path.stat().st_size:
        w,h=fit(path,17*cm,22*cm); story.append(Image(str(path),width=w,height=h))
    else:
        story.append(Table([[f"ẢNH CẦN BỔ SUNG: {filename}"],[f"URL: {url}"],[f"Thao tác: {action}"],[f"Phải xuất hiện: {required}"]],colWidths=[17*cm],style=TableStyle([("BOX",(0,0),(-1,-1),1,colors.HexColor("#c9363e")),("INNERGRID",(0,0),(-1,-1),.4,colors.grey),("FONTNAME",(0,0),(-1,-1),font),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ffe2e2")),("PADDING",(0,0),(-1,-1),10)])))
    story.append(Paragraph(f"Caption: {required}",body))
SimpleDocTemplate(str(PDF),pagesize=A4,rightMargin=1.5*cm,leftMargin=1.5*cm,topMargin=1.5*cm,bottomMargin=1.5*cm).build(story)
print(f"Đã tạo: {DOCX}\nĐã tạo: {PDF}\nẢnh còn thiếu ({len(missing)}): {', '.join(missing) or 'không'}")
