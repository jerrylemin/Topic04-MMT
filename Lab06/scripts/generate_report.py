"""Sinh báo cáo Lab06 ngắn gọn; ảnh thiếu được biểu diễn bằng placeholder chi tiết."""
from __future__ import annotations
import json,re
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches,Pt,RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image
try:
 from .screenshot_manifest import SCREENSHOTS,EXPECTED_FILES
 from .check_screenshots import png_dimensions,MIN_WIDTH,MIN_HEIGHT
except ImportError:
 from screenshot_manifest import SCREENSHOTS,EXPECTED_FILES
 from check_screenshots import png_dimensions,MIN_WIDTH,MIN_HEIGHT

ROOT=Path(__file__).resolve().parents[1]; SHOTS=ROOT/"evidence"/"screenshots"; REPORT=ROOT/"report"
DOCX_NAME="21127645_LeMinh_Lab06_CookiePoisoning.docx"; PDF_NAME="21127645_LeMinh_Lab06_CookiePoisoning.pdf"
REPORT_SECTIONS=("1. Mục tiêu và môi trường thực hành","2. Kịch bản và các bước thực hiện","3. Nguyên nhân kỹ thuật","4. Kết quả và bằng chứng","5. Mức độ ảnh hưởng","6. Bản vá và cách phòng chống","7. Trả lời các câu hỏi báo cáo trong BaiTapTopic04.docx","8. Kết quả kiểm thử","9. Kết luận")
QA_ANSWERS=(
 ("Vì sao cookie là dữ liệu không đáng tin cậy?","Cookie nằm ở client, người dùng có thể đọc, xóa hoặc sửa rồi gửi lại. Server phải xác minh toàn vẹn và phân quyền bằng dữ liệu server-side."),
 ("Cookie Poisoning khác Session Hijacking như thế nào?","Poisoning sửa nội dung cookie để thay đổi quyết định; hijacking chiếm một session/token hợp lệ của người khác để mạo danh."),
 ("Base64 có phải là mã hóa không?","Không. Base64 chỉ biểu diễn byte thành văn bản và có thể decode/encode lại mà không cần khóa."),
 ("Signed cookie giải quyết vấn đề gì?","Chữ ký phát hiện sửa đổi và xác thực nguồn tạo cookie; nó không tự che nội dung và không thay thế authorization."),
 ("Vì sao server-side authorization vẫn là bắt buộc?","Ngay cả cookie hợp lệ chỉ mô tả phiên. Mỗi request vẫn phải kiểm tra danh tính, role và quyền đối với tài nguyên hiện tại ở server."),
)
VULN_CODE="role = request.cookies.get(\"role\")\nif role == \"admin\":\n    return admin_page()"
FIX_CODE="session_id = request.cookies.get(\"session_id\")\nsession = load_active_session(session_id)\nuser = load_user(session.user_id)\nrequire_role(user, \"admin\")"

def _valid(path):
 try:w,h=png_dimensions(path);return path.stat().st_size>0 and w>=MIN_WIDTH and h>=MIN_HEIGHT
 except (OSError,ValueError):return False
def _pytest_summary():
 p=ROOT/"evidence/logs/pytest.txt"
 if not p.is_file():return "Chưa có log pytest; không tuyên bố kết quả."
 m=re.search(r"(\d+) passed(?:, (\d+) failed)?",p.read_text(encoding="utf-8",errors="replace"))
 return (f"Pytest ghi nhận: {m.group(1)} passed"+(f", {m.group(2)} failed" if m and m.group(2) else "")+".") if m else "Log pytest không có dòng tổng kết nhận diện được."
def _shade(cell):
 tc=cell._tc.get_or_add_tcPr(); shd=OxmlElement("w:shd");shd.set(qn("w:fill"),"FFF4CC");tc.append(shd);b=OxmlElement("w:tcBorders");tc.append(b)
 for edge in ("top","left","bottom","right"):
  e=OxmlElement(f"w:{edge}");e.set(qn("w:val"),"single");e.set(qn("w:sz"),"10");e.set(qn("w:color"),"D49A00");b.append(e)
def _ev_docx(doc,i,missing):
 item=SCREENSHOTS[i]; path=SHOTS/item["name"]
 if _valid(path):
  p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(path),width=Inches(6.1));c=doc.add_paragraph(f"Hình {i+1}. {item['caption']}");c.alignment=WD_ALIGN_PARAGRAPH.CENTER;return
 missing.append(item["name"]);cell=doc.add_table(rows=1,cols=1).cell(0,0);_shade(cell)
 lines=(f"ẢNH {i+1:02d}/{len(SCREENSHOTS):02d}",f"Tên file: {item['name']}",f"Tiêu đề ảnh: {item['title']}","Chèn ảnh tại vị trí này.",f"URL hoặc lệnh: {item['url']}",f"Thao tác: {item['action']}",f"Panel hoặc DevTools tab cần mở: {item['panel']}",f"Nội dung bắt buộc phải thấy: {item['must_show']}",f"Kết quả mong đợi: {item['expected']}",f"Caption: {item['caption']}")
 for n,line in enumerate(lines):
  p=cell.paragraphs[0] if n==0 else cell.add_paragraph();r=p.add_run(line);r.bold=n in (0,1);r.font.size=Pt(9)
def build_docx(path):
 d=Document();s=d.sections[0];s.page_width=Inches(8.27);s.page_height=Inches(11.69);s.top_margin=s.bottom_margin=Inches(.6);s.left_margin=s.right_margin=Inches(.7)
 d.styles["Normal"].font.name="Arial";d.styles["Normal"].font.size=Pt(10.2);d.styles["Normal"].paragraph_format.space_after=Pt(4)
 for name,size,color in (("Title",24,"17365D"),("Heading 1",15,"1F4E79"),("Heading 2",12,"2F5597")):
  st=d.styles[name];st.font.name="Arial";st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string(color);st.font.bold=True
 p=d.add_paragraph(style="Title");p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run("BÁO CÁO THỰC HÀNH LAB 6\nCOOKIE POISONING")
 for line in ("Sinh viên: Lê Minh - MSSV: 21127645","Môi trường: Flask/SQLite tại http://127.0.0.1:5006","Phạm vi: dữ liệu giả lập, hoàn toàn trên localhost"):
  x=d.add_paragraph(line);x.alignment=WD_ALIGN_PARAGRAPH.CENTER
 d.add_page_break();missing=[]
 d.add_heading(REPORT_SECTIONS[0],1);d.add_paragraph("Mục tiêu là nhận diện rủi ro khi server tin cookie client, phân biệt plain/Base64/signed/encrypted cookie và chứng minh server-side session. Mọi thao tác dùng Flask/SQLite và trình duyệt trên loopback.")
 d.add_heading(REPORT_SECTIONS[1],1)
 steps=(("2.1 Quan sát cookie","Đăng nhập user demo và ghi Name, Domain, Path, HttpOnly, Secure, SameSite.",[0]),("2.2 Plain Cookie","Sửa role user thành admin; bản vulnerable cấp quyền sai.",[1]),("2.3 Base64 Cookie","Decode JSON, sửa role, encode lại; server vulnerable vẫn chấp nhận.",[2]),("2.4 Signed Cookie hợp lệ","Giữ cookie nguyên vẹn và quan sát xác minh chữ ký.",[3]),("2.5 Signed Cookie bị sửa","Sửa một ký tự; chữ ký sai và request bị từ chối.",[4]),("2.6 Authenticated encryption","So sánh token hợp lệ với token bị sửa; kiểm tra toàn vẹn thất bại.",[5]),("2.7 Server-side authorization","Cookie chỉ giữ session ID; role lấy từ database và kiểm tra từng request.",[6]),("2.8 Vòng đời session","Session rotate sau login, bị hủy khi logout và token cũ bị từ chối.",[7]))
 for title,text,ids in steps:
  d.add_heading(title,2);d.add_paragraph(text)
  for i in ids:_ev_docx(d,i,missing)
 d.add_heading(REPORT_SECTIONS[2],1);d.add_paragraph("Root cause là coi cookie client-controlled như nguồn sự thật cho role. Plain và Base64 không có cơ chế toàn vẹn; Base64 không phải mã hóa. Signed/authenticated token phát hiện sửa đổi, nhưng authorization vẫn phải kiểm tra server-side.")
 d.add_heading(REPORT_SECTIONS[3],1);d.add_paragraph("Ảnh 01-03 thể hiện dữ liệu client và hai bypass; ảnh 04-06 thể hiện kiểm tra toàn vẹn; ảnh 07-08 chứng minh session ID, role server-side, rotation và logout invalidation. Audit/evidence JSON thật tiếp tục là nguồn đối chiếu.")
 d.add_heading(REPORT_SECTIONS[4],1);d.add_paragraph("Ảnh hưởng gồm leo thang đặc quyền, truy cập trang quản trị, mạo danh trạng thái và sai quyết định nghiệp vụ. Mức độ nghiêm trọng khi cookie điều khiển role/balance/permission; lab chỉ dùng tài khoản và dữ liệu local.")
 d.add_heading(REPORT_SECTIONS[5],1);d.add_paragraph("Không lưu role/is_admin/balance trực tiếp trong cookie. Ưu tiên session ID ngẫu nhiên và role trong database; kiểm tra quyền ở mỗi request. Nếu giữ dữ liệu client, dùng chữ ký hoặc authenticated encryption. Cookie bật HttpOnly, Secure trên HTTPS, SameSite; rotate sau login và hủy server-side khi logout.")
 d.add_heading("Đoạn vulnerable",2);d.add_paragraph(VULN_CODE);d.add_heading("Đoạn secure",2);d.add_paragraph(FIX_CODE)
 d.add_heading(REPORT_SECTIONS[6],1)
 for q,a in QA_ANSWERS:d.add_heading(q,2);d.add_paragraph(a)
 d.add_heading(REPORT_SECTIONS[7],1);d.add_paragraph(_pytest_summary());d.add_paragraph("Kết quả chỉ được đọc từ log hiện có; generator không hard-code PASS.");_ev_docx(d,8,missing)
 d.add_heading(REPORT_SECTIONS[8],1);d.add_paragraph("Cookie luôn là input không tin cậy. Kiểm tra toàn vẹn ngăn sửa token; server-side session, authorization theo request và quản lý vòng đời phiên mới tạo ranh giới tin cậy đầy đủ.")
 path.parent.mkdir(parents=True,exist_ok=True);d.save(path);return missing
def _font():
 for r,b in ((r"C:\Windows\Fonts\arial.ttf",r"C:\Windows\Fonts\arialbd.ttf"),("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
  if Path(r).is_file() and Path(b).is_file():pdfmetrics.registerFont(TTFont("Lab",r));pdfmetrics.registerFont(TTFont("LabB",b));return
 raise RuntimeError("Không tìm thấy font Unicode cho PDF")
def build_pdf(path):
 _font();ss=getSampleStyleSheet();body=ParagraphStyle("body",parent=ss["BodyText"],fontName="Lab",fontSize=9,leading=11,spaceAfter=5);h1=ParagraphStyle("h1",parent=ss["Heading1"],fontName="LabB",fontSize=14,textColor=colors.HexColor("#1F4E79"),spaceBefore=8,spaceAfter=5);h2=ParagraphStyle("h2",parent=ss["Heading2"],fontName="LabB",fontSize=11,textColor=colors.HexColor("#2F5597"),spaceBefore=5,spaceAfter=3);center=ParagraphStyle("center",parent=body,alignment=TA_CENTER)
 story=[Spacer(1,1.5*inch),Paragraph("BÁO CÁO THỰC HÀNH LAB 6",ParagraphStyle("title",parent=h1,fontSize=23,alignment=TA_CENTER)),Paragraph("COOKIE POISONING",ParagraphStyle("sub",parent=h1,fontSize=17,alignment=TA_CENTER)),Spacer(1,.4*inch),Paragraph("Sinh viên: Lê Minh - MSSV: 21127645",center),Paragraph("Flask/SQLite - http://127.0.0.1:5006 - localhost",center),PageBreak()];missing=[]
 def ev(i):
  item=SCREENSHOTS[i];img=SHOTS/item["name"]
  if _valid(img):
   x=Image(str(img));x._restrictSize(6.2*inch,4.4*inch);story.extend([x,Paragraph(f"Hình {i+1}. {item['caption']}",center)])
  else:
   missing.append(item["name"]);text="<br/>".join((f"<b>ẢNH {i+1:02d}/{len(SCREENSHOTS):02d}</b>",f"<b>Tên file:</b> {item['name']}",f"<b>Tiêu đề ảnh:</b> {item['title']}","Chèn ảnh tại vị trí này.",f"<b>URL hoặc lệnh:</b> {item['url']}",f"<b>Thao tác:</b> {item['action']}",f"<b>Panel:</b> {item['panel']}",f"<b>Phải thấy:</b> {item['must_show']}",f"<b>Kết quả:</b> {item['expected']}",f"<b>Caption:</b> {item['caption']}"));t=Table([[Paragraph(text,body)]],colWidths=[6.5*inch]);t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#FFF4CC")),("BOX",(0,0),(-1,-1),1,colors.HexColor("#D49A00")),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]));story.append(t)
 story += [Paragraph(REPORT_SECTIONS[0],h1),Paragraph("Nhận diện Cookie Poisoning và chứng minh server-side session trên localhost.",body),Paragraph(REPORT_SECTIONS[1],h1)]
 steps=(("2.1 Quan sát cookie","Ghi cookie và flags.",[0]),("2.2 Plain Cookie","Sửa role và quan sát cấp quyền sai.",[1]),("2.3 Base64 Cookie","Decode, sửa role và encode lại.",[2]),("2.4 Signed hợp lệ","Cookie nguyên vẹn được xác minh.",[3]),("2.5 Signed bị sửa","Một ký tự bị sửa làm chữ ký sai.",[4]),("2.6 Encrypted token","Authenticated encryption từ chối token sửa.",[5]),("2.7 Server session","Role lấy từ database.",[6]),("2.8 Vòng đời session","Rotation, logout và token cũ.",[7]))
 for title,text,ids in steps:story += [Paragraph(title,h2),Paragraph(text,body)];[ev(i) for i in ids]
 story += [Paragraph(REPORT_SECTIONS[2],h1),Paragraph("Root cause là tin role client-controlled. Base64 không bảo vệ toàn vẹn; signed/encrypted token vẫn cần authorization.",body),Paragraph(REPORT_SECTIONS[3],h1),Paragraph("Ảnh 01-08 đối chiếu vulnerable, kiểm tra toàn vẹn và session server-side.",body),Paragraph(REPORT_SECTIONS[4],h1),Paragraph("Rủi ro gồm leo thang đặc quyền và truy cập trái phép; lab giới hạn dữ liệu local.",body),Paragraph(REPORT_SECTIONS[5],h1),Paragraph("Dùng session ID ngẫu nhiên, role trong DB, authorization từng request, ký/mã hóa có xác thực, flags, rotation và logout invalidation.",body),Paragraph("Đoạn vulnerable",h2),Paragraph(VULN_CODE.replace("\n","<br/>"),body),Paragraph("Đoạn secure",h2),Paragraph(FIX_CODE.replace("\n","<br/>"),body),Paragraph(REPORT_SECTIONS[6],h1)]
 for q,a in QA_ANSWERS:story += [Paragraph(q,h2),Paragraph(a,body)]
 story += [Paragraph(REPORT_SECTIONS[7],h1),Paragraph(_pytest_summary(),body)];ev(8);story += [Paragraph(REPORT_SECTIONS[8],h1),Paragraph("Cookie là input; toàn vẹn, authorization và vòng đời phiên tạo ranh giới tin cậy.",body)]
 path.parent.mkdir(parents=True,exist_ok=True);SimpleDocTemplate(str(path),pagesize=A4,leftMargin=.7*inch,rightMargin=.7*inch,topMargin=.6*inch,bottomMargin=.6*inch).build(story);return missing
def main():
 REPORT.mkdir(exist_ok=True);missing=build_docx(REPORT/DOCX_NAME);pdf_missing=build_pdf(REPORT/PDF_NAME);assert missing==pdf_missing;print(json.dumps({"docx":str(REPORT/DOCX_NAME),"pdf":str(REPORT/PDF_NAME),"required":len(EXPECTED_FILES),"missing_screenshots":missing},ensure_ascii=False,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
