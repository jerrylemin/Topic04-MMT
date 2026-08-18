from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from urllib.parse import quote
from uuid import uuid4

from flask import Request


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _short(value: object, limit: int = 240) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[:limit] + "…"


def _mask_cookie(value: str) -> str:
    if not value:
        return "(không có)"
    return "; ".join(f"{part.split('=', 1)[0]}=***" for part in value.split("; "))


def _step(number: int, layer: str, title: str, description: str, technique: str,
          input_data: object, output_data: object, code: str, meaning: str,
          status: str = "normal") -> dict:
    return {"step_number": number, "timestamp": _now(), "layer": layer,
            "title": title, "description": description, "technique": technique,
            "input_data": _short(input_data), "output_data": _short(output_data),
            "code_reference": code, "security_meaning": meaning, "status": status}


def _request_summary(req: Request, route: str) -> dict:
    return {"method": req.method, "url": req.url, "path": req.path,
            "query_string": req.query_string.decode("utf-8", "replace"),
            "headers": {"Host": req.host, "Content-Type": req.content_type or "(không có)",
                        "User-Agent": _short(req.user_agent.string, 100)},
            "form_body": {k: _short(v) for k, v in req.form.items()},
            "cookie": _mask_cookie(req.headers.get("Cookie", "")),
            "sent_at": _now(), "flask_route": route}


def _base(lab_type: str, mode: str, action: str, req: Request, route: str) -> dict:
    return {"trace_id": uuid4().hex, "lab_type": lab_type, "mode": mode,
            "started_at": _now(), "completed_at": _now(), "user_action": action,
            "input_source": "", "steps": [], "request_summary": _request_summary(req, route),
            "response_summary": {"status": 200, "content_type": "text/html; charset=utf-8",
                                 "headers": {}, "html_snippet": "", "before_escape": "",
                                 "after_escape": "", "length": 0},
            "security_controls": [], "source_to_sink": [], "code_comparison": {},
            "transformations": [], "database_inspector": None, "final_result": {}}


def reflected_trace(req: Request, raw: str, mode: str, results: list[str], error: str) -> dict:
    secure = mode == "secure"; route = f"/{mode}/search"; encoded = quote(raw, safe="")
    escaped = html.escape(raw, quote=True); special = re.findall(r"[<>'\"]", raw)
    tags = re.findall(r"<\s*([a-zA-Z0-9]+)", raw); handlers = re.findall(r"\bon\w+\s*=", raw, re.I)
    t = _base("reflected", mode, "Gửi biểu mẫu tìm kiếm" if raw else "Mở trang tìm kiếm", req, route)
    t["input_source"] = 'request.args["q"]'
    t["steps"] = [
        _step(1,"Browser UI","Nhập dữ liệu",f"{len(raw)} ký tự; ký tự đặc biệt: {special}; thẻ: {tags}; event handler: {handlers}","HTML form",raw,raw,"<input name=\"q\">","Dữ liệu từ người dùng là không tin cậy","warning" if raw else "idle"),
        _step(2,"HTTP Request","Tạo URL","Trình duyệt percent-encode dữ liệu vào query string.","URL encoding",raw,encoded,"GET /search?q=...","Encoding URL không phải output encoding."),
        _step(3,"Flask Router","Định tuyến request",f"Flask khớp method GET với {route}.","Route matching",req.path,route,"app.add_url_rule(...) ","Request đi vào đúng bài thử."),
        _step(4,"Server Validation","Đọc và kiểm tra q","request.args đã URL-decode; giới hạn 200 ký tự.","request.args + length check",encoded,raw[:200],'request.args.get("q", "")',"Validation chỉ hỗ trợ, không thay output encoding.","safe" if not error else "warning"),
        _step(5,"Template Engine","Render template","Jinja nhận dữ liệu tìm kiếm và danh sách kết quả.","Jinja autoescape" if secure else "Markup bypass",raw,escaped if secure else raw,"{{ q }}" if secure else "Markup(q)","Ký tự được escape." if secure else "Markup vô hiệu hóa autoescape cho q.","safe" if secure else "danger"),
        _step(6,"HTTP Response","Trả HTML","Response chứa vùng kết quả tìm kiếm.","HTTP response",raw,escaped if secure else raw,"render_template(...) ","Dữ liệu đi tới browser dưới dạng text đã escape." if secure else "Payload còn nguyên trong HTML.","safe" if secure else "danger"),
        _step(7,"Browser HTML Parser","Phân tích HTML","Browser tạo text node." if secure else "Browser có thể tạo element và đăng ký event handler.","HTML parser",escaped if secure else raw,"Text node" if secure else (tags or ["HTML element"]),"HTML parser","Không có JavaScript chạy." if secure else "onerror có thể chạy khi tài nguyên lỗi.","safe" if secure else "danger"),
        _step(8,"Final Result","Kết luận","Payload hiển thị dạng văn bản." if secure else "Payload an toàn có thể thực thi trong lab.","Security verdict",raw,"rendered_as_text" if secure else "payload_executed",route,"Bản vá chặn XSS." if secure else "Reflected XSS được chứng minh.","safe" if secure else "danger")]
    t["source_to_sink"] = [{"name":'request.args["q"]',"value":_short(raw),"file":"app.py","line":"search()","trust":"Không tin cậy","risk":"Source"},{"name":"Python string","value":_short(raw),"file":"app.py","line":"validation","trust":"Không tin cậy","risk":"Tainted"},{"name":"Jinja template","value":_short(escaped if secure else raw),"file":f"templates/reflected_{mode}.html","line":"{{ q }}","trust":"Đã encode" if secure else "Không encode","risk":"Safe" if secure else "Sink"},{"name":"Browser result","value":"Text" if secure else "HTML element/event","file":"Browser","line":"HTML parser","trust":"Safe" if secure else "Executable","risk":"Blocked" if secure else "XSS"}]
    t["code_comparison"]={"vulnerable":"q = Markup(q)\n{{ q }}","secure":"q = q\n{{ q }}","explanation":"Markup bỏ qua autoescape; giá trị thường được Jinja encode theo ngữ cảnh HTML."}
    t["transformations"]=[{"label":"Raw input","value":raw},{"label":"URL encoded","value":encoded},{"label":"Server decoded","value":raw},{"label":"HTML output","value":escaped if secure else raw},{"label":"Browser interpretation","value":"Text node" if secure else "HTML element / event handler"}]
    t["security_controls"]=[{"name":"Input validation","enabled":True,"file":"app.py","risk":"Giới hạn độ dài","limit":"Không chống XSS một mình"},{"name":"Jinja autoescape","enabled":secure,"file":f"templates/reflected_{mode}.html","risk":"Ngăn HTML injection","limit":"Phải đúng ngữ cảnh"},{"name":"CSP","enabled":secure,"file":"app.py headers()","risk":"Giảm thực thi script","limit":"Không thay sửa sink"},{"name":"External network blocked","enabled":True,"file":"Thiết kế local","risk":"Không exfiltration","limit":"Chỉ là phạm vi lab"}]
    t["final_result"]={"verdict":"Payload không thực thi" if secure else "Payload đã thực thi (khi là payload img/onerror)","stored":False,"escaped":secure,"sanitized":False,"csp_blocked":secure,"remaining_risk":"Thấp trong ngữ cảnh HTML" if secure else "Cao","impact":"Người mở URL"}
    return t


def stored_trace(req: Request, mode: str, rows: list[dict], body: str = "", inserted: bool = False, error: str = "") -> dict:
    secure = mode == "secure"; route=f"/{mode}/post/1/comments"; sanitized = html.escape(body)
    t=_base("stored",mode,"Gửi bình luận" if req.method=="POST" else "Tải trang bình luận",req,route); t["input_source"]='request.form["body"] / SQLite comments.body'
    t["steps"]=[
        _step(1,"Browser UI","Nhập bình luận","Form nhận author và body.","HTML form",body,body,"<textarea name=\"body\">","Body là dữ liệu không tin cậy","warning" if body else "idle"),
        _step(2,"HTTP Request","Gửi POST" if req.method=="POST" else "Gửi GET","Browser tạo request body application/x-www-form-urlencoded.","Form encoding",body,req.form.to_dict(),"POST /comments","Request thật được Request Inspector ghi lại."),
        _step(3,"Flask Router","Đọc request.form","Route chấp nhận GET và POST.","request.form",req.form.to_dict(),body,'request.form.get("body")',"Dữ liệu vẫn tainted."),
        _step(4,"Server Validation","Kiểm tra dữ liệu",error or "Không rỗng; author ≤60, body ≤2000.","Length validation",body,"Hợp lệ" if not error else error,"if not author or not body","Không thay output encoding.","safe" if not error else "warning"),
        _step(5,"SQLite Database","SQLite INSERT","Truy vấn tham số tách mã SQL khỏi dữ liệu.","Parameterized SQL",body,"Đã lưu" if inserted else "Không INSERT trong GET",'INSERT ... VALUES(1,?,?)',"Chống SQLi nhưng không chống Stored XSS.","safe" if inserted else "idle"),
        _step(6,"SQLite Database","SQLite SELECT",f"Đọc {len(rows)} bản ghi thật từ comments.","Parameterized SQL",1,[r.get("id") for r in rows],"SELECT ... WHERE post_id=?","Payload lưu được phát lại khi render."),
        _step(7,"Template Engine","Render comments","Bleach allowlist rồi render." if secure else "Body được Markup và đưa thẳng vào HTML.","Bleach + Jinja" if secure else "Markup bypass",body,sanitized if secure else body,"bleach.clean(...)" if secure else 'Markup(row["body"])',"Thuộc tính sự kiện bị loại." if secure else "Sink giữ HTML nguy hiểm.","safe" if secure else "danger"),
        _step(8,"HTTP Response","Trả danh sách bình luận","Response chứa dữ liệu đọc từ SQLite.","HTTP response",body,sanitized if secure else body,"render_template(...) ","Dữ liệu phát tới mọi người xem."),
        _step(9,"Browser HTML Parser","Parse comment","Tạo text/HTML allowlist." if secure else "Tạo element và event handler từ payload.","HTML parser",sanitized if secure else body,"Không script" if secure else "Event handler có thể chạy","Browser parser","Reload lặp lại cùng kết quả.","safe" if secure else "danger"),
        _step(10,"Final Result","Kết luận","Dữ liệu vẫn ở DB nhưng không thực thi." if secure else "Payload có thể chạy lại sau reload.","Security verdict",body,"sanitized" if secure else "payload_executed",route,"Stored XSS bị chặn khi hiển thị." if secure else "Phạm vi ảnh hưởng gồm mọi người xem.","safe" if secure else "danger")]
    t["source_to_sink"]=[{"name":'request.form["body"]',"value":_short(body),"file":"app.py","line":"comments()","trust":"Không tin cậy","risk":"Source"},{"name":"SQLite comments.body","value":_short(body),"file":"lab01.db","line":"comments","trust":"Tainted at rest","risk":"Stored"},{"name":"Jinja output","value":_short(sanitized if secure else body),"file":f"templates/stored_{mode}.html","line":"comment body","trust":"Sanitized" if secure else "Unsafe","risk":"Safe" if secure else "Sink"},{"name":"Browser result","value":"Allowed HTML/text" if secure else "HTML event","file":"Browser","line":"HTML parser","trust":"Safe" if secure else "Executable","risk":"Blocked" if secure else "XSS"}]
    t["code_comparison"]={"vulnerable":'row["body"] = Markup(row["body"])','secure':'bleach.clean(row["body"], tags=ALLOWED_TAGS, attributes={})',"explanation":"SQL tham số bảo vệ câu SQL; Bleach mới giới hạn HTML trước khi hiển thị."}
    t["transformations"]=[{"label":"Trước sanitization","value":body},{"label":"Thẻ phát hiện","value":str(re.findall(r"<\s*/?\s*([\w-]+)",body))},{"label":"Thuộc tính sự kiện","value":str(re.findall(r"\bon\w+",body,re.I))},{"label":"Sau sanitization/escape","value":sanitized if secure else body}]
    t["database_inspector"]={"table":"comments","columns":["id","post_id","author","body","created_at"],"row_count":len(rows),"latest":rows[-1] if rows else {},"raw_value":body,"rendered_value":sanitized if secure else body}
    t["security_controls"]=[{"name":"Parameterized SQL","enabled":True,"file":"app.py","risk":"SQL Injection","limit":"Không chống XSS"},{"name":"Bleach sanitization","enabled":secure,"file":"app.py","risk":"HTML/event nguy hiểm","limit":"Allowlist phải duy trì"},{"name":"Jinja autoescape","enabled":secure,"file":f"templates/stored_{mode}.html","risk":"HTML injection","limit":"Markup có thể bypass"},{"name":"CSP","enabled":secure,"file":"app.py","risk":"Script ngoài policy","limit":"Defense in depth"}]
    t["final_result"]={"verdict":"Payload không thực thi" if secure else "Payload có thể thực thi và lặp lại","stored":inserted or bool(rows),"escaped":secure,"sanitized":secure,"csp_blocked":secure,"remaining_risk":"HTML trong allowlist" if secure else "Cao","impact":"Mọi người xem bài viết"}
    return t


def simple_trace(req: Request, kind: str, mode: str = "secure") -> dict:
    route=req.path; t=_base(kind,mode,"Mở trang",req,route)
    if kind=="dom":
        sink="textContent" if mode=="secure" else "innerHTML"
        t["input_source"]="location.hash"; t["steps"]=[
            _step(1,"Browser UI","Thay đổi fragment","Browser giữ fragment phía client.","hashchange","#payload","location.hash","URL fragment","Không gửi lên server."),
            _step(2,"HTTP Request","Server nhận path","Request HTTP không chứa fragment.","HTTP semantics",req.url,req.path,"request.path","Server không thể đọc fragment."),
            _step(3,"Browser JavaScript","Đọc location.hash","Script chạy khi load/hashchange.","slice + decodeURIComponent","location.hash","decoded value","location.hash.slice(1)","Dữ liệu vẫn không tin cậy."),
            _step(4,"DOM","Gán dữ liệu vào sink",f"Bản {mode} dùng {sink}.",sink,"decoded value","DOM",f"result.{sink} = value", "Tạo text node." if mode=="secure" else "Parse chuỗi thành HTML.","safe" if mode=="secure" else "danger"),
            _step(5,"Browser HTML Parser","Diễn giải DOM","DOM Inspector đọc outerHTML thật.","DOM API","DOM trước","DOM sau","result.outerHTML","Không tạo event handler." if mode=="secure" else "Có thể tạo img/onerror.","safe" if mode=="secure" else "danger"),
            _step(6,"Final Result","Kết luận","Client trace thay giá trị mẫu bằng DOM hiện tại.","Security verdict",sink,"payload_rendered_as_text" if mode=="secure" else "payload_executed",req.path,"Payload bị chặn." if mode=="secure" else "Payload có thể chạy.","safe" if mode=="secure" else "danger")]
        t["code_comparison"]={"vulnerable":"result.innerHTML = value;","secure":"result.textContent = value;","explanation":"innerHTML parse chuỗi thành node; textContent tạo text node."}
        t["source_to_sink"]=[{"name":"location.hash","value":"#payload","file":f"static/js/dom_{mode}.js","line":"location.hash.slice(1)","trust":"Không tin cậy","risk":"Source"},{"name":"decodeURIComponent","value":"decoded value","file":f"static/js/dom_{mode}.js","line":"try/catch","trust":"Không tin cậy","risk":"Transform"},{"name":sink,"value":"decoded value","file":f"static/js/dom_{mode}.js","line":f"result.{sink}","trust":"Safe" if mode=="secure" else "Unsafe","risk":"Text" if mode=="secure" else "Sink"},{"name":"DOM result","value":"Text node" if mode=="secure" else "Element/event","file":"Browser","line":"DOM parser","trust":"Safe" if mode=="secure" else "Executable","risk":"Blocked" if mode=="secure" else "XSS"}]
        t["transformations"]=[{"label":"Server path","value":req.path},{"label":"Fragment","value":"chỉ browser biết"},{"label":"Sink","value":sink}]
    elif kind=="headers":
        directives=["default-src 'self'","script-src 'self'","style-src 'self'","img-src 'self' data:","object-src 'none'","base-uri 'none'","frame-ancestors 'none'","form-action 'self'"]
        t["steps"]=[_step(i+1,layer,title,desc,tech,inp,out,code,meaning,status) for i,(layer,title,desc,tech,inp,out,code,meaning,status) in enumerate([
            ("Flask Router","Hoàn thành response","View đã render HTML.","Flask response",route,"Response object","render_template","Chuẩn bị thêm header","normal"),("Security Headers","after_request chạy","Middleware áp dụng cho route secure.","Flask hook",route,"secure=True","@app.after_request","Một điểm cấu hình chung","safe"),("Security Headers","Thêm CSP","Ghép policy từ các directive.","CSP",route,"; ".join(directives),"response.headers.update","Defense in depth","safe"),("Browser HTML Parser","Phân tích policy","Browser so resource với policy.","CSP enforcement","resource","allow/block","script-src 'self'","Không cho inline/external ngoài origin","safe"),("Final Result","Kết luận","Resource hợp lệ được phép; resource lệch policy bị chặn.","Security verdict","policy","enforced",route,"CSP không thay sửa code","safe")])]
        t["transformations"]=[{"label":d.split()[0],"value":d} for d in directives]
    else:
        t["steps"]=[_step(1,"HTTP Request","Mở profile","Request thật đi vào /profile.","GET",req.url,route,"@app.route('/profile')","Session mẫu local."),_step(2,"Security Headers","Thiết lập cookie","Flask thêm cookie flags.","Set-Cookie","session=***","HttpOnly; SameSite=Lax","Config","HttpOnly không vá XSS.","safe"),_step(3,"Final Result","Kết luận","Cookie chỉ chứa dữ liệu mẫu.","Cookie security","local HTTP","Secure=False",route,"Production HTTPS phải Secure=True.","safe")]
    t["security_controls"]=[{"name":"CSP","enabled":True,"file":"app.py","risk":"Script/resource ngoài policy","limit":"Không sửa sink"},{"name":"HttpOnly","enabled":True,"file":"config.py","risk":"JavaScript đọc cookie","limit":"Không vá XSS"},{"name":"Secure","enabled":False,"file":"config.py","risk":"Cookie qua HTTP","limit":"Local HTTP; production bật True"},{"name":"SameSite=Lax","enabled":True,"file":"config.py","risk":"Request cross-site","limit":"Không thay CSRF token"}]
    t["final_result"]={"verdict":"Đã áp dụng lớp phòng thủ","stored":False,"escaped":True,"sanitized":False,"csp_blocked":True,"remaining_risk":"Cấu hình production","impact":"Giảm rủi ro"}
    return t
