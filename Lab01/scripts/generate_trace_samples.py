import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from app import create_app
from database import reset_db

ROOT=Path(__file__).parents[1]; OUT=ROOT/"evidence/traces"; OUT.mkdir(parents=True,exist_ok=True)
REQUESTS=ROOT/"evidence/requests"; RESPONSES=ROOT/"evidence/responses"; REQUESTS.mkdir(parents=True,exist_ok=True); RESPONSES.mkdir(parents=True,exist_ok=True)
app=create_app({"TESTING":True,"DATABASE":"trace-samples.db"})
with app.app_context(): reset_db()
client=app.test_client()
cases={
 "reflected_vulnerable":("get","/vulnerable/search?q=%3Cimg%20src=x%20onerror%3Dalert(1)%3E",None),
 "reflected_secure":("get","/secure/search?q=%3Cimg%20src=x%20onerror%3Dalert(1)%3E",None),
 "stored_vulnerable":("post","/vulnerable/post/1/comments",{"author":"Kiểm thử","body":"<img src=x onerror=alert(1)>"}),
 "stored_secure":("post","/secure/post/1/comments",{"author":"Kiểm thử","body":"<img src=x onerror=alert(1)><strong>Xin chào</strong>"}),
 "dom_vulnerable":("get","/vulnerable/dom-search",None),
 "dom_secure":("get","/secure/dom-search",None),
}
for name,(method,url,data) in cases.items():
    response=getattr(client,method)(url,data=data)
    match=re.search(r'<pre class="trace-json" hidden>(.*?)</pre>',response.text,re.S)
    if not match: raise RuntimeError(f"Không tìm thấy trace trong {url}")
    trace=json.loads(html.unescape(match.group(1)))
    (OUT/f"{name}.json").write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding="utf-8")
    (REQUESTS/f"{name}.json").write_text(json.dumps(trace["request_summary"],ensure_ascii=False,indent=2),encoding="utf-8")
    (RESPONSES/f"{name}.json").write_text(json.dumps({"status":response.status_code,"headers":dict(response.headers),"summary":trace["response_summary"]},ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"evidence/security_headers.json").write_text(json.dumps(dict(client.get("/security-headers").headers),ensure_ascii=False,indent=2),encoding="utf-8")
(ROOT/"trace-samples.db").unlink(missing_ok=True)
print(f"Đã tạo {len(cases)} trace JSON mẫu tại {OUT}")
