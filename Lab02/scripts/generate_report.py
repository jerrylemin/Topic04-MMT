"""Sinh báo cáo Lab02 ngắn gọn từ bằng chứng hiện có; không giả lập kết quả."""
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from screenshot_manifest import SCREENSHOTS
from PIL import Image as PILImage, UnidentifiedImageError
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

SHOT_DIR=ROOT/"evidence/screenshots"; REPORT_DIR=ROOT/"report"
DOCX_PATH=REPORT_DIR/"21127645_LeMinh_Lab02_BufferOverflow.docx"
PDF_PATH=REPORT_DIR/"21127645_LeMinh_Lab02_BufferOverflow.pdf"

SECTIONS=[
 ("1. Mục tiêu và môi trường thực hành",[
  "Mục tiêu là quan sát lỗi ghi vượt vùng nhớ trong backend native nhận input từ HTTP, dùng ASan/GDB để định vị, xác định các mốc độ dài và kiểm chứng hai bản vá cùng compiler hardening.",
  "Môi trường: Flask tại 127.0.0.1:5002 và GCC/GDB/binary Linux trong Ubuntu, WSL hoặc Docker local. Lab chỉ gây crash có kiểm soát; không có shellcode, ROP hay chiếm quyền."],[]),
 ("2. Kịch bản và các bước thực hiện",[
  "Gửi tên ngắn để tạo baseline; gửi 64 byte tới profile vulnerable và ghi nhận trạng thái tiến trình; đọc ASan; chạy GDB; kiểm tra nhiều độ dài; thử secure_length, secure_snprintf và kiểm tra hardening."],[0,1,3,4]),
 ("3. Nguyên nhân kỹ thuật",[
  "Trong process_name, name[32] là mảng local trên stack frame. strcpy sao chép tới byte null nhưng không biết kích thước đích. Input 32 byte đã cần byte null thứ 33; dữ liệu dài hơn có thể ghi đè biến lân cận, canary, saved frame pointer hoặc return address.",
  "strcpy và gets không nhận capacity đích; sprintf không tự giới hạn output. Memory corruption có thể làm hỏng luồng điều khiển và phụ thuộc layout bộ nhớ, nên nghiêm trọng hơn lỗi logic chỉ trả kết quả sai."],[2]),
 ("4. Kết quả và bằng chứng",[
  "Bản secure_length đo byte và từ chối trước copy. Bản secure_snprintf giới hạn output theo sizeof(name) và kiểm tra return value để từ chối truncation. Hardening được đọc từ binary thật, không suy diễn từ tên profile."],[5,6,7]),
 ("5. Mức độ ảnh hưởng",[
  "Input HTTP có thể đi qua Flask tới chương trình C, vì vậy lỗi native có thể bị kích hoạt từ xa đối với service đang phơi endpoint. Hậu quả tối thiểu là tiến trình dừng/DoS; memory corruption còn có thể ảnh hưởng tính toàn vẹn và luồng điều khiển. Lab không khai thác vượt quá crash local."],[]),
 ("6. Bản vá và cách phòng chống",[
  "Vulnerable tối thiểu: char name[32]; strcpy(name, user_input). Vá 1: dùng strnlen, yêu cầu độ dài <=31 rồi mới copy và thêm null. Vá 2: snprintf(name, sizeof name, \"%s\", user_input), sau đó từ chối nếu return value âm hoặc >= sizeof name.",
  "Giới hạn request ở tầng web; tránh parser C/C++ khi không cần; ưu tiên ngôn ngữ memory-safe. Bật stack protector/canary, PIE kết hợp ASLR, full RELRO, NX và FORTIFY. Đây là lớp giảm thiểu, không thay kiểm tra biên."],[]),
 ("7. Trả lời các câu hỏi báo cáo trong BaiTapTopic04.docx",[
  "Buffer Overflow là lỗi memory safety do ghi ngoài vùng cấp phát; Injection làm dữ liệu bị interpreter hiểu thành lệnh/cú pháp. Backend native bị kích hoạt qua HTTP vì server chuyển body request thành đối số cho chương trình C.",
  "Firewall không biết capacity của buffer và request hợp lệ về giao thức vẫn có thể chứa input quá dài. Cần sửa code, giới hạn input và hardening ở tiến trình.",
  "Bản vá length hiệu quả vì chặn trước mọi thao tác ghi; bản vá snprintf hiệu quả khi vừa giới hạn số byte vừa kiểm tra truncation. Ít nhất ba hardening: canary phát hiện stack bị sửa, ASLR/PIE ngẫu nhiên hóa địa chỉ, NX cấm thực thi vùng dữ liệu; RELRO làm vùng relocation chỉ đọc.",
  "ASLR là ngẫu nhiên hóa layout địa chỉ; DEP/NX ngăn thực thi mã ở vùng dữ liệu; Stack Canary là giá trị kiểm tra trước khi hàm return."],[]),
 ("8. Kết quả kiểm thử",[],[8]),
 ("9. Kết luận",[
  "Lỗi bắt nguồn từ copy không có giới hạn vào name[32]. Kiểm tra biên và xử lý truncation là bản vá chính; ASan/GDB giúp phát hiện và phân tích, còn hardening chỉ giảm khả năng/tác động khi lỗi vẫn tồn tại."],[]),
]

def valid_png(path):
 try:
  if not path.is_file() or not path.stat().st_size:return False
  with PILImage.open(path) as image:return image.format=="PNG" and image.width>0 and image.height>0
 except (OSError,UnidentifiedImageError):return False

def evidence_summary():
 out=[]; log=ROOT/"evidence/logs/pytest.txt"
 if log.exists() and log.stat().st_size:
  lines=[x.strip() for x in log.read_text(encoding="utf-8",errors="replace").splitlines() if x.strip()]
  out.append("Log pytest thật (dòng cuối): "+(lines[-1] if lines else "log rỗng"))
 else:out.append("Chưa có evidence/logs/pytest.txt; báo cáo không tuyên bố kiểm thử đạt.")
 length=ROOT/"evidence/logs/length_test.json"
 if length.exists():
  try:
   data=json.loads(length.read_text(encoding="utf-8")); rows=data if isinstance(data,list) else data.get("results",[])
   first_asan=next((r.get("length") for r in rows if r.get("asan_detected")),None); first_crash=next((r.get("length") for r in rows if r.get("crash_detected")),None)
   out.append(f"length_test.json thật: ASan đầu tiên={first_asan if first_asan is not None else 'chưa quan sát'}; crash đầu tiên={first_crash if first_crash is not None else 'chưa quan sát'}.")
  except (OSError,json.JSONDecodeError):out.append("length_test.json không đọc được; không suy diễn mốc độ dài.")
 else:out.append("Chưa có length_test.json; chưa kết luận mốc ASan/crash.")
 gdb=list((ROOT/"evidence/gdb").glob("*.txt")) if (ROOT/"evidence/gdb").exists() else []
 out.append("Log GDB thật: "+(", ".join(p.name for p in gdb) if gdb else "chưa có"))
 return out

def shade(cell,fill):
 shd=OxmlElement("w:shd");shd.set(qn("w:fill"),fill);cell._tc.get_or_add_tcPr().append(shd)

def configure_docx(doc):
 s=doc.sections[0];s.page_height,s.page_width=Cm(29.7),Cm(21);s.top_margin=s.bottom_margin=Cm(1.7);s.left_margin=s.right_margin=Cm(1.8)
 for name in ("Normal","Title","Heading 1","Heading 2","Caption"):
  st=doc.styles[name];st.font.name="Arial";st._element.rPr.rFonts.set(qn("w:ascii"),"Arial");st._element.rPr.rFonts.set(qn("w:hAnsi"),"Arial")
 doc.styles["Normal"].font.size=Pt(10.5);doc.styles["Normal"].paragraph_format.space_after=Pt(5)
 doc.styles["Heading 1"].font.size=Pt(15);doc.styles["Heading 1"].font.color.rgb=RGBColor(23,74,132)

def add_cover(doc):
 p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(110)
 r=p.add_run("BÁO CÁO THỰC HÀNH LAB 02");r.bold=True;r.font.name="Arial";r.font.size=Pt(25);r.font.color.rgb=RGBColor(23,74,132)
 for text in ("BUFFER OVERFLOW TRONG ỨNG DỤNG WEB LOCAL","HTTP - ASan - GDB - Bản vá - Hardening","MSSV: 21127645","Họ tên: Lê Minh"):
  p=doc.add_paragraph(text);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 doc.add_page_break()

def placeholder_lines(number,shot):
 return [f"ẢNH {number:02d}/{len(SCREENSHOTS):02d}",f"Tên file bắt buộc: {shot['filename']}",f"Tiêu đề ảnh: {shot['title']}","Chèn ảnh tại vị trí này.",f"URL hoặc lệnh: {shot['location']}",f"Thao tác: {shot['initial']} Nhập {shot['data']} {shot['button']}",f"Panel/DevTools: {shot['panel']}",f"Nội dung bắt buộc phải thấy: {shot['required']}",f"Kết quả mong đợi: {shot['expected']}",f"Caption: {shot['caption']}"]

def picture_inches(path,max_w=6.25,max_h=4.3):
 with PILImage.open(path) as im:
  scale=min(max_w/im.width,max_h/im.height);return im.width*scale,im.height*scale

def add_docx_shot(doc,index,missing):
 shot=SCREENSHOTS[index];number=index+1;path=SHOT_DIR/shot["filename"]
 if valid_png(path):
  w,h=picture_inches(path);p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True;p.add_run().add_picture(str(path),width=Inches(w),height=Inches(h))
 else:
  missing.append(shot["filename"]);table=doc.add_table(rows=1,cols=1);table.style="Table Grid";table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"));cell=table.cell(0,0);shade(cell,"FFF4D6");cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
  for i,line in enumerate(placeholder_lines(number,shot)):
   p=cell.paragraphs[0] if i==0 else cell.add_paragraph();p.paragraph_format.space_after=Pt(2);run=p.add_run(line);run.font.name="Arial";run.font.size=Pt(9);run.bold=i in (0,1,2,3)
 cap=doc.add_paragraph(f"Hình {number}. {shot['caption']}",style="Caption");cap.alignment=WD_ALIGN_PARAGRAPH.CENTER

def build_docx():
 doc=Document();configure_docx(doc);add_cover(doc);missing=[]
 for title,paras,indexes in SECTIONS:
  doc.add_heading(title,1)
  if title.startswith("8."):
   for line in evidence_summary():doc.add_paragraph(line)
  for text in paras:doc.add_paragraph(text)
  for index in indexes:add_docx_shot(doc,index,missing)
 REPORT_DIR.mkdir(exist_ok=True);doc.save(DOCX_PATH);return missing

def pdf_font():
 n=Path("C:/Windows/Fonts/arial.ttf");b=Path("C:/Windows/Fonts/arialbd.ttf")
 if n.exists() and b.exists():pdfmetrics.registerFont(TTFont("ArialVN",str(n)));pdfmetrics.registerFont(TTFont("ArialVN-B",str(b)));return "ArialVN","ArialVN-B"
 return "Helvetica","Helvetica-Bold"

def add_pdf_shot(story,index,body,bold,missing):
 shot=SCREENSHOTS[index];number=index+1;path=SHOT_DIR/shot["filename"]
 story.append(PageBreak())
 block=[]
 if valid_png(path):
  with PILImage.open(path) as im:
   scale=min(17*cm/im.width,11*cm/im.height);block.append(Image(str(path),width=im.width*scale,height=im.height*scale))
 else:
  if shot["filename"] not in missing:missing.append(shot["filename"])
  content="<br/><br/>".join(line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;") for line in placeholder_lines(number,shot))
  block.append(Table([[Paragraph(content,body)]],colWidths=[17*cm],splitInRow=0,style=TableStyle([("BOX",(0,0),(-1,-1),1,colors.HexColor("#D49A18")),("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#FFF4D6")),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),3)])))
 block.extend([Paragraph(f"Hình {number}. {shot['caption']}",body),Spacer(1,8)]);story.extend(block)

def build_pdf(missing):
 font,bold=pdf_font();samples=getSampleStyleSheet();body=ParagraphStyle("BodyVN",parent=samples["BodyText"],fontName=font,fontSize=9.5,leading=13,spaceAfter=5);h1=ParagraphStyle("H1VN",parent=samples["Heading1"],fontName=bold,fontSize=15,leading=18,textColor=colors.HexColor("#174A84"),spaceBefore=9,spaceAfter=6);title=ParagraphStyle("TitleVN",parent=samples["Title"],fontName=bold,fontSize=23,textColor=colors.HexColor("#174A84"),alignment=1)
 story=[Spacer(1,6*cm),Paragraph("BÁO CÁO THỰC HÀNH LAB 02",title),Paragraph("BUFFER OVERFLOW TRONG ỨNG DỤNG WEB LOCAL",title),Paragraph("MSSV: 21127645 - Họ tên: Lê Minh",body),PageBreak()]
 for section_title,paras,indexes in SECTIONS:
  story.append(Paragraph(section_title,h1))
  if section_title.startswith("8."):
   for line in evidence_summary():story.append(Paragraph(line,body))
  for text in paras:story.append(Paragraph(text,body))
  for index in indexes:add_pdf_shot(story,index,body,bold,missing)
 SimpleDocTemplate(str(PDF_PATH),pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=1.7*cm,bottomMargin=1.7*cm).build(story)

def main():
 SHOT_DIR.mkdir(parents=True,exist_ok=True);REPORT_DIR.mkdir(exist_ok=True);missing=build_docx();build_pdf(missing)
 missing=[item["filename"] for item in SCREENSHOTS if item["filename"] in missing]
 print(f"Đã tạo DOCX: {DOCX_PATH}");print(f"Đã tạo PDF:  {PDF_PATH}");print(f"Ảnh còn thiếu ({len(missing)}): {', '.join(missing) if missing else 'không'}");return 0

if __name__=="__main__":raise SystemExit(main())
