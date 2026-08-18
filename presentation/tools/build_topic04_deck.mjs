import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = path.resolve(process.argv[2] ?? "21127645_LeMinh_21127224_NguyenVuBach_Topic04_6Labs_final.pptx");
const QA = path.resolve(process.argv[3] ?? "qa-structure");
const RENDER = process.argv[4] ? path.resolve(process.argv[4]) : null;

const W = 1280;
const H = 720;
const C = {
  dark: "#111111",
  panel: "#1A1A18",
  panel2: "#242420",
  orange: "#E85D26",
  cream: "#F0ECE5",
  muted: "#888880",
  rule: "#505048",
  black: "#111111",
  white: "#FFFFFF",
  green: "#71B48D",
  red: "#D96C5F",
};
const FONT = "Bahnschrift"; // closest installed fallback for Barlow
const MONO = "Consolas"; // closest installed fallback for IBM Plex Mono
const presentation = Presentation.create({ slideSize: { width: W, height: H } });
const qaSlides = [];
const placeholderManifest = [];

function pos(left, top, width, height) {
  return { left, top, width, height };
}

function shape(slide, name, geometry, position, fill = "none", lineFill = "none", lineWidth = 0) {
  return slide.shapes.add({
    geometry,
    name,
    position,
    fill,
    line: { style: "solid", fill: lineFill, width: lineWidth },
  });
}

function text(slide, name, value, position, options = {}) {
  const box = shape(slide, name, "textbox", position, "none", "none", 0);
  box.text = value;
  box.text.style = {
    typeface: options.mono ? MONO : FONT,
    fontSize: options.size ?? 20,
    bold: options.bold ?? false,
    color: options.color ?? C.cream,
    alignment: options.align ?? "left",
    verticalAlignment: options.valign ?? "top",
    autoFit: options.autoFit ?? "none",
    wrap: "square",
    insets: options.insets ?? { top: 2, right: 4, bottom: 2, left: 4 },
    lineSpacing: options.lineSpacing ?? 1.0,
  };
  return box;
}

function box(slide, name, value, position, options = {}) {
  const b = shape(
    slide,
    name,
    options.geometry ?? "rect",
    position,
    options.fill ?? C.panel,
    options.line ?? C.rule,
    options.lineWidth ?? 1,
  );
  b.text = value;
  b.text.style = {
    typeface: options.mono ? MONO : FONT,
    fontSize: options.size ?? 20,
    bold: options.bold ?? false,
    color: options.color ?? C.cream,
    alignment: options.align ?? "left",
    verticalAlignment: options.valign ?? "top",
    autoFit: options.autoFit ?? "none",
    wrap: "square",
    insets: options.insets ?? { top: 12, right: 14, bottom: 10, left: 14 },
    lineSpacing: options.lineSpacing ?? 1.0,
  };
  return b;
}

function addRule(slide, name, left, top, width, color = C.rule, height = 1) {
  return shape(slide, name, "rect", pos(left, top, width, height), color, "none", 0);
}

function label(slide, name, value, left, top, width, options = {}) {
  return text(slide, name, value.toUpperCase(), pos(left, top, width, options.height ?? 24), {
    mono: true,
    size: options.size ?? 19,
    bold: true,
    color: options.color ?? C.orange,
    align: options.align ?? "left",
    valign: "middle",
    insets: { top: 0, right: 2, bottom: 0, left: 2 },
  });
}

function chrome(slide, index, lab, titleValue, subtitle = "", options = {}) {
  slide.background.fill = options.orange ? C.orange : C.dark;
  if (!options.orange) {
    label(slide, `S${index}_EYEBROW`, lab, 56, 24, 460);
    text(slide, `S${index}_TITLE`, titleValue, pos(54, 52, 1170, 56), {
      size: 40,
      bold: true,
      color: C.cream,
      valign: "middle",
      insets: { top: 0, right: 0, bottom: 0, left: 0 },
    });
    if (subtitle) {
      text(slide, `S${index}_SUBTITLE`, subtitle, pos(56, 111, 1168, 35), {
        size: 19,
        color: C.muted,
        valign: "middle",
        insets: { top: 0, right: 0, bottom: 0, left: 0 },
      });
    }
    addRule(slide, `S${index}_TITLE_RULE`, 56, 150, 1168, C.rule, 1);
  }
}

function footer(slide, index, source, orange = false) {
  const fg = orange ? C.black : C.muted;
  addRule(slide, `S${index}_FOOTER_RULE`, 56, 674, 1168, orange ? C.black : C.rule, 1);
  text(slide, `S${index}_SOURCE`, `NGUỒN  ${source}`, pos(56, 681, 1050, 24), {
    mono: true,
    size: 19,
    color: fg,
    valign: "middle",
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  text(slide, `S${index}_NUMBER`, String(index).padStart(2, "0"), pos(1140, 681, 84, 24), {
    mono: true,
    size: 19,
    bold: true,
    color: fg,
    align: "right",
    valign: "middle",
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
  });
}

function notes(slide, index, lab, sources, narration) {
  slide.speakerNotes.textFrame.setText(
    `SLIDE ${String(index).padStart(2, "0")} — ${lab}\n\nNGUỒN ĐỐI CHIẾU\n${sources}\n\nGỢI Ý THUYẾT TRÌNH\n${narration}\n\nPHẠM VI\nChỉ trình diễn trên ứng dụng localhost cố ý có lỗi trong repository Topic04.`,
  );
}

function beginSlide(index, lab, titleValue, subtitle, source, options = {}) {
  const slide = presentation.slides.add();
  chrome(slide, index, lab, titleValue, subtitle, options);
  footer(slide, index, source, options.orange ?? false);
  qaSlides.push({ index, zones: [], minFontPx: 19 });
  return slide;
}

function zone(index, name, left, top, width, height) {
  qaSlides[index - 1].zones.push({ name, left, top, width, height });
}

function flow(slide, index, name, items, position, options = {}) {
  zone(index, name, position.left, position.top, position.width, position.height);
  const gap = options.gap ?? 14;
  const arrowW = options.arrowW ?? 28;
  const n = items.length;
  const nodeW = (position.width - (n - 1) * (gap + arrowW)) / n;
  for (let i = 0; i < n - 1; i += 1) {
    const x = position.left + (i + 1) * nodeW + i * (gap + arrowW) + gap;
    shape(slide, `${name}_ARROW_${i + 1}`, "rightArrow", pos(x, position.top + position.height / 2 - 9, arrowW, 18), options.arrowColor ?? C.orange, "none", 0);
  }
  items.forEach((item, i) => {
    const x = position.left + i * (nodeW + gap + arrowW);
    box(slide, `${name}_NODE_${i + 1}`, item, pos(x, position.top, nodeW, position.height), {
      fill: options.fill ?? C.panel,
      line: options.line ?? C.rule,
      size: options.size ?? 19,
      bold: options.bold ?? true,
      align: "center",
      valign: "middle",
      insets: { top: 6, right: 7, bottom: 6, left: 7 },
    });
  });
}

function twoCards(slide, index, name, leftCard, rightCard, options = {}) {
  const top = options.top ?? 178;
  const height = options.height ?? 430;
  const gap = 24;
  const width = (1168 - gap) / 2;
  zone(index, `${name}_LEFT`, 56, top, width, height);
  zone(index, `${name}_RIGHT`, 56 + width + gap, top, width, height);
  box(slide, `${name}_LEFT`, leftCard, pos(56, top, width, height), {
    fill: options.leftFill ?? C.panel,
    line: options.leftLine ?? C.red,
    size: options.size ?? 20,
    color: options.leftColor ?? C.cream,
  });
  box(slide, `${name}_RIGHT`, rightCard, pos(56 + width + gap, top, width, height), {
    fill: options.rightFill ?? C.panel,
    line: options.rightLine ?? C.green,
    size: options.size ?? 20,
    color: options.rightColor ?? C.cream,
  });
}

function codeBlock(slide, index, name, code, position, accent = C.orange) {
  zone(index, name, position.left, position.top, position.width, position.height);
  box(slide, name, code, position, {
    fill: "#0B0B0B",
    line: accent,
    size: 19,
    mono: true,
    color: C.cream,
    insets: { top: 13, right: 14, bottom: 12, left: 14 },
  });
}

function callout(slide, index, name, titleValue, body, position, color = C.orange) {
  zone(index, name, position.left, position.top, position.width, position.height);
  addRule(slide, `${name}_BAR`, position.left, position.top, 8, position.height, color, 8);
  if (position.height <= 100) {
    label(slide, `${name}_LABEL`, titleValue, position.left + 18, position.top, 172, { color, size: 19, height: position.height });
    text(slide, `${name}_BODY`, body, pos(position.left + 200, position.top, position.width - 202, position.height), {
      size: 19,
      color: C.cream,
      valign: "middle",
      insets: { top: 2, right: 4, bottom: 2, left: 4 },
    });
    return;
  }
  label(slide, `${name}_LABEL`, titleValue, position.left + 18, position.top + 2, position.width - 20, { color, size: 19 });
  text(slide, `${name}_BODY`, body, pos(position.left + 18, position.top + 34, position.width - 20, position.height - 36), {
    size: 20,
    color: C.cream,
  });
}

function placeholder(slide, index, lab, filename, position, caption, displayFilename = filename) {
  const base = `PH_S${String(index).padStart(2, "0")}_${lab}_${filename.replace(/[^a-zA-Z0-9]+/g, "_")}`;
  zone(index, base, position.left, position.top, position.width, position.height);
  shape(slide, `${base}_FRAME`, "rect", pos(position.left - 3, position.top - 3, position.width + 6, position.height + 6), "none", C.orange, 2);
  shape(slide, `${base}_IMAGE`, "rect", position, C.panel2, C.rule, 1);
  text(slide, `${base}_ICON`, "▣", pos(position.left + 16, position.top + 15, 48, 42), {
    mono: true,
    size: 30,
    bold: true,
    color: C.orange,
    valign: "middle",
  });
  text(slide, `${base}_INSTRUCTION`, `CHÈN ẢNH THẬT\n${displayFilename}\n16:9 · CROP → FILL\nXEM GUIDE`, pos(position.left + 70, position.top + 18, position.width - 88, position.height - 72), {
    mono: true,
    size: 19,
    bold: true,
    color: C.cream,
    valign: "middle",
  });
  text(slide, `${base}_CAPTION`, caption, pos(position.left, position.top + position.height - 43, position.width, 38), {
    mono: true,
    size: 19,
    color: C.muted,
    valign: "middle",
    insets: { top: 2, right: 8, bottom: 2, left: 8 },
  });
  placeholderManifest.push({ slide: index, lab, filename, shape: `${base}_IMAGE` });
}

function matrix(slide, index, name, headers, rows, position, widths, options = {}) {
  zone(index, name, position.left, position.top, position.width, position.height);
  const rowH = position.height / (rows.length + 1);
  let x = position.left;
  headers.forEach((h, c) => {
    box(slide, `${name}_H${c}`, h, pos(x, position.top, widths[c], rowH), {
      fill: C.orange,
      line: C.dark,
      size: options.headerSize ?? 19,
      bold: true,
      color: C.black,
      align: c === 0 ? "left" : "center",
      valign: "middle",
      insets: { top: 2, right: 7, bottom: 2, left: 7 },
    });
    x += widths[c];
  });
  rows.forEach((row, r) => {
    let cx = position.left;
    row.forEach((value, c) => {
      box(slide, `${name}_R${r}C${c}`, value, pos(cx, position.top + rowH * (r + 1), widths[c], rowH), {
        fill: r % 2 ? C.panel2 : C.panel,
        line: C.rule,
        size: options.size ?? 19,
        bold: c === 0,
        color: c === 0 ? C.cream : C.muted,
        valign: "middle",
        insets: { top: 2, right: 7, bottom: 2, left: 7 },
      });
      cx += widths[c];
    });
  });
}

function qaGrid(slide, index, name, items, position) {
  zone(index, name, position.left, position.top, position.width, position.height);
  const cols = 2;
  const gap = 16;
  const w = (position.width - gap) / cols;
  const h = (position.height - gap * 2) / 3;
  items.forEach((item, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    box(slide, `${name}_${i + 1}`, `${String(i + 1).padStart(2, "0")}  ${item}`, pos(position.left + col * (w + gap), position.top + row * (h + gap), w, h), {
      fill: C.panel,
      line: i === items.length - 1 ? C.orange : C.rule,
      size: 19,
      color: C.cream,
      valign: "middle",
      insets: { top: 8, right: 10, bottom: 8, left: 10 },
    });
  });
}

// 01 — Cover
{
  const s = beginSlide(1, "TOPIC 04", "", "", "BaiTapTopic04.docx · Lab01–Lab06", { orange: true });
  label(s, "S1_KICKER", "WEB APPLICATION SECURITY / 06 LABS", 56, 42, 720, { color: C.black });
  text(s, "S1_TITLE", "SÁU CÁCH\nPHÁ VỠ\nTRUST BOUNDARY", pos(52, 120, 780, 330), { size: 64, bold: true, color: C.black, insets: { top: 0, right: 0, bottom: 0, left: 0 } });
  addRule(s, "S1_VERTICAL", 888, 86, 2, C.black, 520);
  text(s, "S1_LABS", "01  XSS\n02  BUFFER OVERFLOW\n03  PARAMETER TAMPERING\n04  CSRF\n05  SQL INJECTION\n06  COOKIE POISONING", pos(930, 128, 280, 330), { mono: true, size: 22, bold: true, color: C.black, lineSpacing: 1.08 });
  text(s, "S1_ID", "LÊ MINH · 21127645\nNGUYỄN VŨ BÁCH · 21127224", pos(902, 510, 308, 100), { mono: true, size: 19, bold: true, color: C.black, align: "right" });
  zone(1, "cover-title", 52, 120, 780, 330);
  zone(1, "cover-labs", 930, 128, 280, 330);
  notes(s, 1, "Tổng quan", "BaiTapTopic04.docx; README và báo cáo Lab01–Lab06", "Mở đầu bằng luận điểm: sáu lỗi khác tên nhưng đều xuất hiện khi ứng dụng đặt niềm tin sai chỗ ở một ranh giới dữ liệu.");
}

// 02 — Overview
{
  const s = beginSlide(2, "BẢN ĐỒ", "Một vòng đời dữ liệu — sáu điểm gãy", "Theo dấu dữ liệu từ browser tới quyết định cuối cùng của server hoặc DOM.", "BaiTapTopic04.docx · source Lab01–Lab06");
  flow(s, 2, "S2_LIFECYCLE", ["BROWSER\nINPUT", "HTTP\nREQUEST", "APP /\nNATIVE", "DB /\nSESSION", "RESPONSE /\nDOM"], pos(56, 178, 1168, 92), { size: 19 });
  const attacks = [
    ["XSS", "output / DOM sink", "mã chạy trong browser"],
    ["BUFFER", "native memory", "crash / corruption"],
    ["PARAMETER", "policy decision", "giá / object / role"],
    ["CSRF", "browser credential", "state change ngoài ý muốn"],
    ["SQLi", "query construction", "logic SQL bị thay"],
    ["COOKIE", "client state", "quyền bị giả mạo"],
  ];
  attacks.forEach((a, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    box(s, `S2_ATTACK_${i + 1}`, `${a[0]}\n${a[1]}\n→ ${a[2]}`, pos(56 + col * 397, 304 + row * 150, 374, 126), { fill: C.panel, line: i === 0 ? C.orange : C.rule, size: 19, bold: i === 0 });
  });
  zone(2, "attack-grid", 56, 304, 1168, 276);
  callout(s, 2, "S2_THESIS", "QUY ĐỊNH AN TOÀN", "✓ Chỉ VM/Docker local, app cố tình có lỗi hoặc nền tảng học tập hợp pháp.\n✕ Không thử payload hay tấn công hệ thống thật; không đánh cắp cookie/tài khoản/dữ liệu; không reverse shell, malware, persistence, botnet, keylogger.", pos(56, 588, 1168, 66), C.orange);
  notes(s, 2, "Tổng quan", "BaiTapTopic04.docx · quy định an toàn chung; app/source của sáu lab", "Dùng vòng đời dữ liệu làm khung đọc. Mọi thực hành chỉ diễn ra trong môi trường local hoặc nền tảng học tập hợp pháp; tuyệt đối không thử trên hệ thống thật.");
}

// 03
{
  const s = beginSlide(3, "LAB01 / XSS", "Ba biến thể — một lỗi niềm tin", "Khác đường đi; giống kết quả: dữ liệu bị diễn giải như HTML/JavaScript.", "Lab01/app.py · templates · static/js");
  matrix(s, 3, "S3_XSS_MATRIX", ["BIẾN THỂ", "SOURCE", "TRUNG GIAN", "SINK / THỜI ĐIỂM"], [
    ["Reflected", "query q", "request → response", "Markup(q) · chạy khi mở URL"],
    ["Stored", "comment body", "SQLite", "Markup(body) · chạy với mọi người xem"],
    ["DOM", "location.hash", "browser only", "innerHTML · không cần server phản chiếu"],
  ], pos(56, 182, 1168, 286), [190, 236, 280, 462]);
  flow(s, 3, "S3_COMMON", ["UNTRUSTED\nDATA", "UNSAFE\nINTERPRETATION", "SCRIPT\nEXECUTION"], pos(170, 512, 940, 100), { size: 22, fill: C.panel2 });
  notes(s, 3, "Lab01", "Lab01/app.py; Lab01/static/js/dom_vulnerable.js; report Lab01", "Nhấn mạnh Stored nguy hiểm hơn vì payload tồn tại và phát lại cho nhiều nạn nhân. DOM XSS vẫn là XSS dù lỗi hoàn toàn ở client.");
}

// 04
{
  const s = beginSlide(4, "LAB01 / XSS", "Reflected và Stored: hai đường phát lại", "Reflected quay về ngay; Stored đi qua database rồi kích hoạt ở lần xem sau.", "Lab01/app.py · reflected/stored templates");
  flow(s, 4, "S4_REFLECTED", ["GET ?q=", "Markup(q)", "HTML response", "Browser chạy"], pos(56, 190, 724, 86), { size: 19 });
  flow(s, 4, "S4_STORED", ["POST body", "SQLite", "Markup(body)", "Mọi viewer"], pos(56, 312, 724, 86), { size: 19, arrowColor: C.red });
  placeholder(s, 4, "Lab01", "29_reflected_network_request.png", pos(818, 184, 406, 232), "Reflected XSS — request GET trong Network", "29_reflected_network_\nrequest.png");
  callout(s, 4, "S4_IMPACT", "THỰC HÀNH REFLECTED / STORED", "1 Chuỗi thường → 2 xem dữ liệu trong HTML → 3 payload alert an toàn → 4 xác định vị trí phản chiếu/nơi lưu → 5 reload hoặc dùng user khác để kiểm Stored chạy lại.", pos(56, 456, 1168, 150), C.orange);
  notes(s, 4, "Lab01", "Lab01/app.py routes /vulnerable/search và /vulnerable/post/1/comments", "Bắt đầu bằng baseline chuỗi thường, quan sát HTML, rồi mới gửi payload alert an toàn. Với Stored, reload hoặc dùng user khác để xác nhận dữ liệu đã lưu phát lại.");
}

// 05
{
  const s = beginSlide(5, "LAB01 / XSS", "DOM XSS: source và sink cùng ở browser", "Fragment không gửi lên server; JavaScript phía client tự biến nó thành DOM.", "Lab01/static/js/dom_vulnerable.js · dom_secure.js");
  flow(s, 5, "S5_DOM_FLOW", ["location.hash", "decodeURIComponent", "innerHTML", "DOM node / event"], pos(56, 184, 1168, 98), { size: 19 });
  codeBlock(s, 5, "S5_VULN_CODE", `// vulnerable\nconst value = decodeURIComponent(location.hash.slice(1));\nresult.innerHTML = value;`, pos(56, 326, 558, 188), C.red);
  codeBlock(s, 5, "S5_SAFE_CODE", `// secure\nconst value = decodeURIComponent(location.hash.slice(1));\nresult.textContent = value;`, pos(638, 326, 586, 188), C.green);
  callout(s, 5, "S5_ROOT", "ROOT CAUSE", "Dữ liệu chỉ nguy hiểm khi đi vào sink diễn giải mã. Kiểm sink DOM: innerHTML · document.write · eval · setTimeout(string) · location.hash.", pos(56, 548, 1168, 72), C.orange);
  notes(s, 5, "Lab01", "Lab01/static/js/dom_vulnerable.js; Lab01/static/js/dom_secure.js", "Đối chiếu đúng một dòng innerHTML và textContent. Fragment là source; DOM API là sink; server có thể không hề nhìn thấy payload.");
}

// 06
{
  const s = beginSlide(6, "LAB01 / XSS", "Bản vá gốc nằm tại output và DOM sink", "Encode theo ngữ cảnh · sanitize HTML có chủ đích · dùng API tạo text.", "Lab01/app.py · dom_secure.js · config.py");
  twoCards(s, 6, "S6_PATCH", "VULNERABLE\n\nMarkup(q)\nMarkup(comment.body)\ninnerHTML = value\n\nDữ liệu trở thành markup", "SECURE\n\nJinja auto-escape\nbleach.clean(..., strip=True)\ntextContent = value\n\nCONTEXTUAL ENCODING\nHTML · JavaScript · URL · Attribute", { top: 184, height: 250, size: 20 });
  placeholder(s, 6, "Lab01", "41_secure_dom_textcontent.png", pos(56, 466, 550, 170), "Elements chứng minh textContent an toàn");
  callout(s, 6, "S6_LAYERS", "DEFENSE IN DEPTH", "CSP giảm blast radius; HttpOnly/Secure/SameSite bảo vệ cookie; validation giảm input bất thường. Không lớp nào thay thế sửa sink.", pos(640, 470, 584, 158), C.orange);
  notes(s, 6, "Lab01", "Lab01/app.py secure routes; bleach.clean; CSP; static/js/dom_secure.js", "Phân biệt bản vá nguyên nhân gốc với lớp bổ sung. Contextual encoding phải đúng bốn ngữ cảnh HTML, JavaScript, URL và Attribute.");
}

// 07
{
  const s = beginSlide(7, "LAB01 / XSS", "Kiểm chứng và câu trả lời báo cáo", "Một bảng so sánh, năm kết luận, một checklist bằng chứng.", "BaiTapTopic04.docx · mục Lab01 · report Lab01");
  matrix(s, 7, "S7_MATRIX", ["LOẠI", "TỒN TẠI", "SERVER", "PATCH GỐC"], [
    ["Reflected", "không", "phản chiếu", "contextual encoding"],
    ["Stored", "SQLite", "lưu + phát lại", "sanitize/encode output"],
    ["DOM", "fragment", "không bắt buộc", "safe DOM API"],
  ], pos(56, 178, 540, 238), [120, 122, 145, 153], { size: 19 });
  qaGrid(s, 7, "S7_QA", [
    "Validation chưa đủ vì sink/ngữ cảnh quyết định cách diễn giải.",
    "Output encoding giữ dữ liệu không trở thành mã.",
    "Stored ảnh hưởng mọi người xem dữ liệu đã lưu.",
    "DOM XSS phát sinh và thực thi hoàn toàn ở browser.",
    "CSP hỗ trợ, không thay sửa code.",
    "Evidence: URL/request · storage · Elements · secure retest.",
  ], pos(624, 178, 600, 438));
  callout(s, 7, "S7_ANSWER", "PATCH + ẢNH CẦN CÓ", "Patch sink: escape output · sanitize HTML · textContent.\nẢnh cần có: normal input · payload · vị trí HTML/DOM · storage · secure retest.", pos(56, 450, 540, 166), C.orange);
  notes(s, 7, "Lab01", "BaiTapTopic04.docx; report 21127645_LeMinh_21127224_NguyenVuBach_Lab01_XSS.docx", "Dùng slide như checklist trả lời báo cáo. Bằng chứng phải cho thấy cả vulnerable và secure, không chỉ popup alert.");
}

// 08
{
  const s = beginSlide(8, "LAB02 / BUFFER OVERFLOW", "HTTP có thể chạm tới lỗi bộ nhớ native", "Flask chỉ là cầu nối; lỗi xảy ra trong process C khi input vượt sức chứa.", "Lab02/app.py · native_runner.py · native/*.c");
  flow(s, 8, "S8_ARCH", ["Browser", "POST /submit", "Flask", "subprocess\nshell=False", "C binary", "stack"], pos(56, 186, 1168, 94), { size: 19, gap: 8, arrowW: 22 });
  callout(s, 8, "S8_SCOPE", "PHẠM VI AN TOÀN", "Chỉ input local để quan sát response, ASan/GDB hoặc crash có kiểm soát. Không shellcode, ROP, chiếm quyền hay persistence.", pos(56, 322, 558, 168), C.orange);
  callout(s, 8, "S8_THESIS", "ĐIỂM GÃY", "Firewall thấy HTTP hợp lệ. Native code lại dùng API copy không biết kích thước đích; memory corruption xuất hiện sau boundary ứng dụng.", pos(638, 322, 586, 168), C.red);
  flow(s, 8, "S8_RESULT", ["input bytes", "unsafe copy", "adjacent memory", "crash / UB"], pos(170, 536, 940, 84), { size: 19, arrowColor: C.red });
  notes(s, 8, "Lab02", "Lab02/app.py; Lab02/native_runner.py; Lab02/native/vulnerable_processor.c", "Giải thích tại sao một request web bình thường vẫn kích hoạt bug native. Scope lab dừng ở crash/quan sát bộ nhớ, không chuyển sang khai thác thực chiến.");
}

// 09
{
  const s = beginSlide(9, "LAB02 / BUFFER OVERFLOW", "32 byte nghĩa là 31 byte dữ liệu + null", "strcpy không nhận capacity; byte thứ 33 bắt đầu chạm vùng lân cận.", "Lab02/native/vulnerable_processor.c · processor_common.h");
  codeBlock(s, 9, "S9_CODE", `char name[32];\nstrcpy(name, user_input);\n// Không có capacity trong lời gọi`, pos(56, 184, 470, 154), C.red);
  matrix(s, 9, "S9_STACK", ["VÙNG STACK", "INPUT ≤31", "INPUT 64"], [
    ["name[32]", "data + \\0", "đầy + vượt"],
    ["canary / padding", "không đổi", "có thể bị ghi"],
    ["frame / return", "không đổi", "corruption / UB"],
  ], pos(558, 184, 666, 238), [250, 190, 226]);
  flow(s, 9, "S9_BYTES", ["31 DATA", "1 NULL", "BYTE 33+", "ADJACENT MEMORY"], pos(56, 470, 1168, 92), { size: 19, arrowColor: C.red });
  callout(s, 9, "S9_DIFF", "KHÁC INJECTION", "Injection đổi ý nghĩa lệnh/query; Buffer Overflow ghi vượt vùng nhớ. Cả hai đều bắt đầu từ trust boundary nhưng phá vỡ primitive khác nhau.", pos(56, 592, 1168, 58), C.orange);
  notes(s, 9, "Lab02", "Lab02/native/vulnerable_processor.c; NAME_BUFFER_SIZE=32", "Không nói 32 ký tự dữ liệu hợp lệ: chuỗi C cần byte null. Hậu quả là undefined behavior, có thể crash hoặc phá hỏng control data.");
}

// 10
{
  const s = beginSlide(10, "LAB02 / BUFFER OVERFLOW", "Quan sát: từ request tới từ chối trước copy", "Ghi bằng chứng thật; không dựng crash log hoặc response giả.", "Lab02/README.md · gdb/README_GDB.md · evidence logs");
  flow(s, 10, "S10_STEPS", ["1 RUN", "2 INPUT", "3 POST", "4 TRACE", "5 ASan/GDB", "6 PATCH", "7 RETEST", "8 REPORT"], pos(56, 176, 1168, 70), { size: 19, gap: 4, arrowW: 14 });
  callout(s, 10, "S10_ENV", "MÔI TRƯỜNG", "Linux VM local · GCC · GDB · Python gửi request local.", pos(56, 256, 1168, 42), C.orange);
  placeholder(s, 10, "Lab02", "31_long_input_network_payload.png", pos(56, 326, 360, 270), "Payload 64 byte tới vulnerable", "31_long_input_\nnetwork_payload.png");
  placeholder(s, 10, "Lab02", "34_secure_length_network_response.png", pos(460, 326, 360, 270), "secure_length từ chối trước copy", "34_secure_length_\nnetwork_response.png");
  placeholder(s, 10, "Lab02", "Lab02_gdb_crash_log.png", pos(864, 326, 360, 270), "GDB/ASan: crash, stack, input length");
  notes(s, 10, "Lab02", "Lab02/README.md; Lab02/gdb/README_GDB.md; screenshot manifest", "Ảnh GDB/ASan phải cho thấy crash location, stack state và input length gây lỗi. Hai ảnh còn lại chứng minh payload thật và secure_length từ chối cùng độ dài.");
}

// 11
{
  const s = beginSlide(11, "LAB02 / BUFFER OVERFLOW", "Hai bản vá chặn lỗi trước thao tác copy", "Length check đặt invariant 31 byte; snprintf ràng buộc mọi ghi theo capacity.", "Lab02/native/secure_*_processor.c · config.py");
  codeBlock(s, 11, "S11_VULN", `// vulnerable\nchar name[32];\nstrcpy(name, user_input);`, pos(56, 184, 350, 154), C.red);
  codeBlock(s, 11, "S11_LENGTH", `// secure_length\nlen = strnlen(input, 33);\nif (len > 31) reject();\nmemcpy(name, input, len + 1);`, pos(430, 184, 382, 154), C.green);
  codeBlock(s, 11, "S11_SNPRINTF", `// secure_snprintf\nwritten = snprintf(name, 32, "%s", input);\nif (written >= 32) reject();`, pos(836, 184, 388, 154), C.green);
  matrix(s, 11, "S11_LAYERS", ["LỚP", "GIÁ TRỊ", "GIỚI HẠN"], [
    ["Request", "MAX_CONTENT_LENGTH=4096", "không biết capacity C"],
    ["Validation", "MAX_NAME_BYTES=256", "chưa đủ cho name[32]"],
    ["Native", "31-byte invariant", "bản vá nguyên nhân gốc"],
  ], pos(56, 382, 1168, 226), [230, 450, 488]);
  notes(s, 11, "Lab02", "Lab02/native/secure_length_processor.c; secure_snprintf_processor.c; Lab02/config.py", "Request limit và input limit web vẫn lớn hơn buffer native; vì vậy phải giữ invariant ngay tại boundary gọi code C.");
}

// 12
{
  const s = beginSlide(12, "LAB02 / BUFFER OVERFLOW", "Hardening giảm khả năng khai thác — không vá strcpy", "Source fix trước; compiler, loader và OS thu hẹp hậu quả.", "Lab02/Makefile · BaiTapTopic04.docx · mục Lab02");
  matrix(s, 12, "S12_HARDEN", ["LỚP", "CƠ CHẾ", "TÁC DỤNG"], [
    ["Source", "bounded copy + invariant", "ngăn overflow"],
    ["Compiler", "stack protector · FORTIFY", "phát hiện / abort"],
    ["Binary", "PIE · RELRO · NOW", "khó tái định vị/ghi GOT"],
    ["OS", "ASLR · NX/DEP", "khó dự đoán / chạy code"],
    ["Language", "memory-safe runtime", "loại lớp lỗi phổ biến"],
  ], pos(56, 178, 670, 390), [150, 250, 270]);
  qaGrid(s, 12, "S12_QA", [
    "CRASH XẢY RA Ở ĐÂU?",
    "STACK CÓ BỊ GHI ĐÈ KHÔNG?",
    "ĐỘ DÀI INPUT BẮT ĐẦU LỖI?",
    "Bản vá hiệu quả vì chặn trước copy.",
    "Canary/PIE/RELRO/NX là hardening, không root fix.",
    "Retest input ngắn, 31 byte, 32+, 64 byte.",
  ], pos(754, 178, 470, 438));
  callout(s, 12, "S12_ORDER", "THỨ TỰ", "Vá code → build hardening → kiểm thử boundary → ghi bằng chứng.", pos(56, 594, 670, 56), C.orange);
  notes(s, 12, "Lab02", "Lab02/Makefile; BaiTapTopic04.docx; report Lab02", "Trả lời trực tiếp năm câu hỏi báo cáo. Nhấn mạnh ASLR/NX/Canary có thể biến khai thác thành crash nhưng không làm strcpy an toàn.");
}

// 13
{
  const s = beginSlide(13, "LAB03 / PARAMETER TAMPERING", "Kiểu dữ liệu hợp lệ vẫn có thể trái policy", "Price, invoice id, user id và role đều do browser kiểm soát cho tới khi server xác minh.", "Lab03/app.py · services.py · authorization.py");
  flow(s, 13, "S13_BOUNDARY", ["FORM / URL /\nHIDDEN / COOKIE", "REQUEST", "SERVER\nVALIDATION", "AUTHORIZATION", "DB / RESPONSE"], pos(56, 186, 1168, 98), { size: 19 });
  matrix(s, 13, "S13_PARAMS", ["PARAMETER", "HỢP LỆ VỀ KIỂU", "CÂU HỎI POLICY"], [
    ["price=1", "integer", "có phải giá từ DB?"],
    ["id=1002", "integer", "user có sở hữu invoice?"],
    ["role=admin", "enum/string", "client có quyền đổi role?"],
  ], pos(56, 334, 1168, 242), [220, 320, 628]);
  callout(s, 13, "S13_KEY", "KEY IDEA", "Hidden field chỉ ẩn khỏi giao diện; nó không trở thành dữ liệu tin cậy.", pos(56, 604, 1168, 46), C.orange);
  notes(s, 13, "Lab03", "Lab03/app.py; Lab03/services.py; Lab03/authorization.py", "Tách validation kiểu/range khỏi authorization nghiệp vụ. Một integer đúng cú pháp vẫn có thể là object của người khác hoặc giá không hợp lệ.");
}

// 14
{
  const s = beginSlide(14, "LAB03 / PARAMETER TAMPERING", "Giá phải được quyết định ở server", "Client chỉ gửi product_id và quantity; server đọc price_vnd từ products.", "Lab03/services.py · seed.py product 5");
  flow(s, 14, "S14_VULN", ["price=1", "request.form", "total=1×qty", "ORDER SAI\nprice=1 được chấp nhận"], pos(56, 184, 650, 82), { size: 19, arrowColor: C.red });
  flow(s, 14, "S14_SAFE", ["product_id=5", "DB price=100000", "total=price×qty", "order đúng"], pos(56, 302, 650, 82), { size: 19, arrowColor: C.green });
  placeholder(s, 14, "Lab03", "45_checkout_tampered_payload.png", pos(748, 184, 476, 186), "Payload checkout sau sửa giá");
  placeholder(s, 14, "Lab03", "Lab03_checkout_vulnerable_accepted.png", pos(748, 408, 476, 186), "Vulnerable chấp nhận price=1", "Lab03_checkout_\nvulnerable_accepted.png");
  codeBlock(s, 14, "S14_CODE", `VULNERABLE: request.form["price"] → chấp nhận price=1 → tạo order sai.\nSECURE: SELECT price_vnd FROM products WHERE id = ?\nINVARIANT: total = server_price × quantity`, pos(56, 432, 650, 162), C.orange);
  notes(s, 14, "Lab03", "Lab03/services.py vulnerable_checkout/secure_checkout; seed product 5 price 100000", "Dùng cùng product_id=5, quantity=1 để đối chiếu. Client price chỉ là gợi ý hiển thị; quyết định tài chính phải dựa trên dữ liệu authoritative ở server.");
}

// 15
{
  const s = beginSlide(15, "LAB03 / PARAMETER TAMPERING", "IDOR là thiếu object-level authorization", "IDOR thuộc OWASP Broken Access Control: tìm thấy object không đồng nghĩa được phép đọc.", "Lab03/services.py · authorization.py · seed.py");
  flow(s, 15, "S15_VULN", ["user_a", "GET id=1002", "SELECT by id", "invoice user_b"], pos(56, 184, 650, 82), { size: 19, arrowColor: C.red });
  flow(s, 15, "S15_SAFE", ["user_a", "GET id=1002", "owner/admin?", "403"], pos(56, 302, 650, 82), { size: 19, arrowColor: C.green });
  placeholder(s, 15, "Lab03", "51_invoice_secure_403_response.png", pos(748, 184, 476, 252), "Response secure trả 403 cho invoice khác chủ");
  matrix(s, 15, "S15_POLICY", ["OBJECT", "REQUESTER", "POLICY", "RESULT"], [
    ["1001", "user_a", "owner", "allow"],
    ["1002", "user_a", "not owner/admin", "403"],
    ["1002", "admin", "admin", "allow + audit"],
  ], pos(56, 476, 1168, 150), [190, 210, 470, 298], { size: 19 });
  notes(s, 15, "Lab03", "Lab03/authorization.py authorize_invoice; seed invoices 1001/1002", "IDOR thuộc Broken Access Control. Route secure phải kiểm tra ownership theo session identity hoặc quyền admin trước khi trả dữ liệu.");
}

// 16
{
  const s = beginSlide(16, "LAB03 / PARAMETER TAMPERING", "Mass assignment biến profile thành privilege escalation", "Nếu server bind mọi field, role từ form có thể đi thẳng vào database.", "Lab03/services.py · authorization.py");
  codeBlock(s, 16, "S16_VULN", `# vulnerable\nemail = form["email"]\nrole  = form["role"]\nUPDATE users SET email=?, role=?`, pos(56, 184, 550, 190), C.red);
  codeBlock(s, 16, "S16_SAFE", `# secure allowlist\nallowed = {"email"}\nreject role, is_admin, balance, user_id\nUPDATE users SET email=? WHERE id=session.user_id`, pos(630, 184, 594, 190), C.green);
  flow(s, 16, "S16_FLOW", ["role=\nadmin", "generic binder", "users.role", "privilege ↑"], pos(56, 420, 560, 90), { size: 19, arrowColor: C.red });
  flow(s, 16, "S16_FLOW2", ["email only", "allowlist", "session id", "audit"], pos(660, 420, 564, 90), { size: 19, arrowColor: C.green });
  callout(s, 16, "S16_AUTH", "AUTHN ≠ AUTHZ", "Đăng nhập xác định bạn là ai; authorization quyết định bạn được đổi field nào trên object nào.", pos(56, 554, 1168, 70), C.orange);
  notes(s, 16, "Lab03", "Lab03/services.py vulnerable_profile/secure_profile; authorization.py", "Không chỉ blacklist role: dùng allowlist field cập nhật và identity từ session. Field nhạy cảm phải có command/route riêng với policy rõ ràng.");
}

// 17
{
  const s = beginSlide(17, "LAB03 / PARAMETER TAMPERING", "Ba tampering — ba kiểm tra authoritative", "Kiểu/range là cần thiết; policy và ownership mới quyết định an toàn.", "BaiTapTopic04.docx · mục Lab03 · report Lab03");
  matrix(s, 17, "S17_MATRIX", ["SCENARIO", "CLIENT SỬA", "SERVER PHẢI LÀM", "SECURE"], [
    ["Price", "price=1", "đọc giá từ DB", "server total"],
    ["IDOR", "id=1002", "owner/admin · OWASP Broken Access Control", "403"],
    ["Profile", "role=admin", "field allowlist", "email only"],
  ], pos(56, 178, 700, 238), [140, 140, 300, 120]);
  qaGrid(s, 17, "S17_QA", [
    "Không tin giá client vì người dùng kiểm soát request.",
    "IDOR thiếu authorization theo object.",
    "Role tampering là privilege escalation.",
    "Tampering khác SQLi: policy vs query syntax.",
    "Hidden field không phải security control.",
    "Audit: ai · object · field · before/after · result.",
  ], pos(784, 178, 440, 438));
  callout(s, 17, "S17_CONTROLS", "CHUỖI THỰC HÀNH", "Login user A → xem invoice 1001 → đổi id=1002 → vulnerable lộ dữ liệu → secure 403.", pos(56, 454, 700, 162), C.orange);
  notes(s, 17, "Lab03", "BaiTapTopic04.docx; report Lab03; source services/authorization", "Trả lời năm câu hỏi bắt buộc và nối mỗi scenario với đúng control authoritative, không dừng ở validation định dạng.");
}

// 18
{
  const s = beginSlide(18, "LAB04 / CSRF", "CSRF lợi dụng credential browser tự gửi", "Attacker không cần biết mật khẩu; chỉ cần khiến victim phát sinh state-changing request.", "Lab04/victim_app.py · attacker_app.py");
  flow(s, 18, "S18_TRIANGLE", ["ATTACKER\n:9004", "VICTIM\nBROWSER", "TARGET\n:5004"], pos(170, 190, 940, 112), { size: 22 });
  matrix(s, 18, "S18_COND", ["ĐIỀU KIỆN", "CÓ TRONG LAB", "Ý NGHĨA"], [
    ["Session sống", "cookie victim", "browser có credential"],
    ["State change", "đổi email", "tác động tài khoản"],
    ["Thiếu token", "vulnerable route", "không ràng buộc intent"],
    ["Cookie tự gửi", "same target origin", "attacker không cần mật khẩu"],
  ], pos(56, 356, 1168, 260), [260, 300, 608]);
  notes(s, 18, "Lab04", "Lab04/victim_app.py; attacker_app.py; report Lab04", "Phân biệt CSRF và XSS: CSRF khiến browser gửi request có credential; XSS chạy code trong origin nạn nhân. SOP không ngăn gửi form cross-origin.");
}

// 19
{
  const s = beginSlide(19, "LAB04 / CSRF", "SOP không ngăn request được gửi", "Browser có thể chặn attacker đọc response nhưng vẫn gửi form cùng cookie target.", "Lab04/attacker_templates · victim_app.py");
  flow(s, 19, "S19_FLOW", ["Victim login\n:5004", "Open attacker\n:9004", "USER BẤM\nSUBMIT", "COOKIE\nTỰ GỬI", "Email đổi"], pos(56, 184, 720, 98), { size: 19, gap: 5, arrowW: 18 });
  placeholder(s, 19, "Lab04", "Lab04_email_before_csrf.png", pos(814, 184, 410, 188), "Email victim trước CSRF");
  placeholder(s, 19, "Lab04", "08_email_after_csrf.png", pos(814, 408, 410, 188), "Email victim sau request CSRF");
  codeBlock(s, 19, "S19_FORM", `<form id="attack-form" method="POST" data-confirm-submit\n      action="http://127.0.0.1:5004/vulnerable/change-email">\n  <input name="email" value="demo_changed@lab.local">\n  <button type="submit">Gửi form</button>\n</form>`, pos(56, 326, 720, 224), C.red);
  callout(s, 19, "S19_SOP", "KHÁC ĐỀ BÀI", "Đề yêu cầu auto-submit; source hiện dùng submit thủ công có xác nhận. Không khẳng định auto-submit đã chạy.", pos(56, 574, 720, 58), C.orange);
  notes(s, 19, "Lab04", "Lab04/attacker_templates/attack_page.html; static/js/form-confirm.js; victim_app.vulnerable_change_email", "Source hiện dùng nút submit có xác nhận, không auto-submit. Báo cáo và slide ghi rõ khác biệt triển khai thay vì dựng kết quả.");
}

// 20
{
  const s = beginSlide(20, "LAB04 / CSRF", "Request hợp lệ về HTTP nhưng thiếu bằng chứng intent", "Cookie có mặt; token thiếu; Origin/Referer không thuộc allowlist — vulnerable route vẫn chấp nhận.", "Lab04/victim_app.py · csrf_service.py · origin_service.py");
  codeBlock(s, 20, "S20_REQUEST", `VALID REQUEST BAN ĐẦU\nVictim POST hợp lệ → có cookie → từ target origin →\nđổi email thành công.\n\nATTACK REQUEST\nPOST /vulnerable/change-email HTTP/1.1\nCookie: victim_session=...\nOrigin: http://127.0.0.1:9004\nemail=demo_changed%40lab.local\n# csrf_token: MISSING`, pos(56, 184, 650, 308), C.red);
  matrix(s, 20, "S20_CHECKS", ["TÍN HIỆU", "VULNERABLE", "SECURE"], [
    ["Session cookie", "tin là đủ", "chỉ xác thực user"],
    ["CSRF token", "không kiểm", "session-bound + compare"],
    ["Origin/Referer", "bỏ qua", "exact allowlist"],
    ["Method", "POST", "POST + policy"],
  ], pos(738, 184, 486, 308), [170, 150, 166]);
  callout(s, 20, "S20_DECISION", "DECISION", "Credential trả lời “ai”; CSRF defense trả lời “request này có phản ánh ý định của chính user hay không?”.", pos(56, 536, 1168, 82), C.orange);
  notes(s, 20, "Lab04", "Lab04/victim_app.py; csrf_service.py; origin_service.py", "Không hiển thị token thật trong slide/ảnh. Dùng request anatomy để chứng minh vì sao chỉ kiểm session là chưa đủ.");
}

// 21
{
  const s = beginSlide(21, "LAB04 / CSRF", "Secure route buộc request gắn với session và origin", "Token mạnh theo session + Origin/Referer exact + SameSite + re-auth cho hành động nhạy cảm.", "Lab04/csrf_service.py · origin_service.py · config.py");
  flow(s, 21, "S21_SECURE", ["GET form", "token_urlsafe(32)", "POST + token", "Origin exact", "compare_digest", "ALLOW / 403"], pos(56, 184, 730, 94), { size: 19, gap: 4, arrowW: 15, arrowColor: C.green });
  placeholder(s, 21, "Lab04", "13_secure_missing_token_403.png", pos(822, 184, 402, 244), "Response 403 khi thiếu CSRF token");
  matrix(s, 21, "S21_LAYERS", ["LỚP", "VAI TRÒ", "KHÔNG THAY THẾ"], [
    ["Token", "ràng buộc intent/session", "authn"],
    ["Origin/Referer", "xác minh nguồn", "token"],
    ["SameSite", "giảm cookie cross-site", "server check"],
    ["Re-auth", "step-up hành động nhạy cảm", "mọi request"],
  ], pos(56, 326, 730, 286), [160, 300, 270]);
  callout(s, 21, "S21_NOTE", "ROTATE + DENY", "Token sai/thiếu hoặc origin không hợp lệ → 403; không cập nhật email.", pos(822, 470, 402, 142), C.orange);
  notes(s, 21, "Lab04", "Lab04/csrf_service.py secrets.token_urlsafe(32), hmac.compare_digest; origin allowlist", "Giải thích defense-in-depth. CAPTCHA không phải lớp chính; GET không được dùng cho state change vì dễ kích hoạt và có thể bị prefetch/cache/log.");
}

// 22
{
  const s = beginSlide(22, "LAB04 / CSRF", "So sánh request và trả lời báo cáo", "Chỉ secure request có đồng thời session, token đúng và origin hợp lệ.", "BaiTapTopic04.docx · mục Lab04 · report Lab04");
  matrix(s, 22, "S22_MATRIX", ["REQUEST", "COOKIE", "TOKEN", "ORIGIN", "RESULT"], [
    ["Victim form", "có", "đúng", "allowed", "200"],
    ["Attacker → vulnerable", "có", "thiếu", "attacker", "email đổi"],
    ["Attacker → secure", "có", "thiếu", "attacker", "403"],
  ], pos(56, 178, 680, 238), [190, 100, 100, 140, 150]);
  qaGrid(s, 22, "S22_QA", [
    "Browser tự gửi cookie theo target origin.",
    "Attacker không cần biết mật khẩu.",
    "CSRF thường không cần đọc response.",
    "CSRF gửi request; XSS chạy script trong origin.",
    "GET không được làm state change.",
    "Evidence: before email · valid request · attacker form submit thủ công · after email · secure 403 · unchanged email.",
  ], pos(764, 178, 460, 438));
  callout(s, 22, "S22_PATCH", "PATCH", "POST-only · session token · exact Origin/Referer · SameSite · re-auth · audit.", pos(56, 456, 680, 160), C.orange);
  notes(s, 22, "Lab04", "BaiTapTopic04.docx; report Lab04; secure/vulnerable routes", "Slide tổng hợp năm câu hỏi. Bằng chứng sau vá phải cho thấy 403 và trạng thái email không đổi.");
}

// 23
{
  const s = beginSlide(23, "LAB05 / SQL INJECTION", "Lỗi xuất hiện trước SQL parser", "Nối chuỗi trộn code và data; parser nhận một câu lệnh có logic khác với ý định ban đầu.", "Lab05/vulnerable_queries.py · secure_queries.py");
  flow(s, 23, "S23_FLOW", ["INPUT", "STRING\nCONCAT", "SQL TEXT", "PARSER", "CHANGED\nRESULT"], pos(56, 188, 1168, 104), { size: 20, arrowColor: C.red });
  twoCards(s, 23, "S23_SPLIT", "PHẦN A: PHÁT HIỆN LỖI\n\n• Nhập dữ liệu bình thường vào login/search.\n• Thử dấu nháy đơn.\n• Quan sát SQL error hoặc hành vi bất thường.\n• Xác định input bị ảnh hưởng.", "ERROR-BASED DETECTION\n\nDấu nháy đơn làm query lỗi hoặc response bất thường.\n\nKhông hiển thị lỗi SQL chi tiết cho user; ghi log an toàn phía server.", { top: 340, height: 250, size: 20 });
  notes(s, 23, "Lab05", "Lab05/vulnerable_queries.py; Lab05/secure_queries.py", "SQLi không nằm ở dấu nháy đơn tự thân mà ở API xây query. Prepared statement tách cấu trúc SQL khỏi giá trị binding.");
}

// 24
{
  const s = beginSlide(24, "LAB05 / SQL INJECTION", "Một comment thay đổi logic xác thực", "Payload local cố định chỉ dùng để chứng minh authentication bypass trong database demo.", "Lab05/config.py · auth_service.py · vulnerable_queries.py");
  codeBlock(s, 24, "S24_QUERY", `INPUT: admin_lab' -- \n\nBEFORE\nWHERE username = '<input>' AND password = '<hash>'\n\nAFTER CONCATENATION\nWHERE username = 'admin_lab' -- ' AND password = '...'\n\nPhần kiểm tra password trở thành comment.`, pos(56, 184, 670, 316), C.red);
  placeholder(s, 24, "Lab05", "42_login_bypass_response.png", pos(758, 184, 466, 252), "Response vulnerable authentication bypass");
  callout(s, 24, "S24_SCOPE", "SAFE LAB SCOPE", "Chỉ SELECT/auth bypass trên SQLite local. Không DROP, DELETE, phá dữ liệu, trích xuất ngoài dataset lab hoặc thử website thật.", pos(56, 540, 670, 80), C.orange);
  callout(s, 24, "S24_CAUSE", "AUTHENTICATION BYPASS", "Mật khẩu hash không cứu được query đã bị đổi logic trước khi so sánh credential.", pos(758, 478, 466, 142), C.red);
  notes(s, 24, "Lab05", "Lab05/config.py AUTH_LOGIC_INPUT; vulnerable login route", "Dùng đúng payload repo. Mục tiêu là thấy transformation của WHERE, không phải mở rộng kỹ thuật khai thác.");
}

// 25
{
  const s = beginSlide(25, "LAB05 / SQL INJECTION", "Search injection mở rộng result set", "DATA EXTRACTION CƠ BẢN: expanded result set làm lộ nhiều hàng hơn dự kiến.", "Lab05/config.py · vulnerable_queries.vulnerable_search");
  flow(s, 25, "S25_NORMAL", ["USB", "LIKE '%USB%'", "matching rows"], pos(56, 184, 520, 86), { size: 20, arrowColor: C.green });
  flow(s, 25, "S25_ATTACK", ["%' OR 1=1 -- ", "concatenated SQL", "all rows"], pos(704, 184, 520, 86), { size: 19, arrowColor: C.red });
  codeBlock(s, 25, "S25_SQL", `# vulnerable_search\nquery = "SELECT ... WHERE name LIKE '%" + term + "%'"\n\n# payload local cố định\n%' OR 1=1 -- \n\n# expanded result set: data extraction cơ bản`, pos(56, 318, 650, 250), C.red);
  placeholder(s, 25, "Lab05", "Lab05_search_vulnerable_expanded_results.png", pos(744, 318, 480, 250), "Vulnerable search trả result set mở rộng", "Lab05_search_vulnerable_\nexpanded_results.png");
  matrix(s, 25, "S25_EVIDENCE", ["BASELINE", "INJECTION", "ĐƯỢC PHÉP"], [["USB", "expanded result set", "SELECT-only local"]], pos(56, 594, 1168, 56), [300, 430, 438], { size: 19 });
  notes(s, 25, "Lab05", "Lab05/config.py SEARCH_EXPANDED_INPUT; vulnerable_queries.py", "So sánh baseline USB và payload cố định. Không biến demo thành khai thác dữ liệu tùy ý; giữ phạm vi SELECT-only trên dataset lab.");
}

// 26
{
  const s = beginSlide(26, "LAB05 / SQL INJECTION", "Prepared statement giữ code và data tách rời", "Cùng payload được bind như username literal và bị từ chối.", "Lab05/secure_queries.py · auth_service.py · seed.py");
  codeBlock(s, 26, "S26_CODE", `sql = "SELECT id, username, password_hash, role\n       FROM users WHERE username = ?"\nrow = conn.execute(sql, (username,)).fetchone()\n\n# password: pbkdf2:sha256:600000\n# cùng payload vẫn chỉ là data`, pos(56, 184, 660, 250), C.green);
  placeholder(s, 26, "Lab05", "43_secure_login_same_payload.png", pos(754, 184, 470, 188), "Secure login từ chối cùng payload");
  placeholder(s, 26, "Lab05", "Lab05_search_secure_same_payload.png", pos(754, 408, 470, 188), "Secure search với cùng payload", "Lab05_search_secure_\nsame_payload.png");
  matrix(s, 26, "S26_LAYERS", ["LỚP", "VAI TRÒ"], [
    ["Parameter binding", "root fix: cấu trúc SQL cố định"],
    ["PBKDF2", "bảo vệ mật khẩu lưu trữ"],
    ["Generic error", "không lộ schema/query"],
    ["Least privilege", "giảm blast radius"],
  ], pos(56, 470, 660, 124), [220, 440], { size: 19 });
  notes(s, 26, "Lab05", "Lab05/secure_queries.py; auth_service.py; seed PBKDF2 600000", "Escaping thủ công dễ sai theo dialect/ngữ cảnh. ORM chỉ an toàn khi không quay lại raw string concatenation.");
}

// 27
{
  const s = beginSlide(27, "LAB05 / SQL INJECTION", "Defense in depth bắt đầu bằng query parameterized", "WAF, validation và logging hữu ích; không lớp nào sửa query nối chuỗi.", "BaiTapTopic04.docx · mục Lab05 · report Lab05");
  flow(s, 27, "S27_LAYERS", ["TYPE / RANGE", "PARAMETERIZED\nQUERY", "LEAST\nPRIVILEGE", "GENERIC\nERROR", "LOG / MONITOR", "WAF\nSUPPORT"], pos(56, 180, 1168, 96), { size: 19, gap: 5, arrowW: 17 });
  qaGrid(s, 27, "S27_QA", [
    "Lỗi ở tầng xây query, trước parser.",
    "Escaping thủ công phụ thuộc dialect và ngữ cảnh.",
    "Prepared statement cố định SQL, bind data riêng.",
    "ORM vẫn lỗi khi dùng raw/concat query.",
    "Lỗi chi tiết làm tăng khả năng dò schema.",
    "Retest login + search bằng cùng payload.",
  ], pos(56, 326, 760, 290));
  callout(s, 27, "S27_ANSWER", "KẾT LUẬN", "Root fix = parameter binding. Nếu lab có route user detail: không nối id/input vào SQL; dùng parameterized query và authorization.", pos(848, 326, 376, 290), C.orange);
  notes(s, 27, "Lab05", "BaiTapTopic04.docx; report Lab05; secure/vulnerable query source", "Trả lời năm câu hỏi và nhắc lại retest cùng payload là bằng chứng tốt nhất cho bản vá.");
}

// 28
{
  const s = beginSlide(28, "LAB06 / COOKIE POISONING", "Cookie vận chuyển state — không tạo niềm tin", "Mọi byte trong cookie quay lại từ client; server phải xác minh integrity và quyền.", "Lab06/app.py · cookie_service.py · seed.py");
  flow(s, 28, "S28_LOOP", ["SERVER SETS\nrole=user", "BROWSER\nSTORES", "USER EDITS\nrole=admin", "BROWSER SENDS", "SERVER TRUSTS"], pos(56, 188, 1168, 110), { size: 19, arrowColor: C.red });
  twoCards(s, 28, "S28_DIFF", "COOKIE POISONING\n\nChính client sửa nội dung cookie để thay đổi quyết định server.\n\nVí dụ: role=user → admin.", "SESSION HIJACKING\n\nKẻ tấn công lấy token/session hợp lệ của người khác.\n\nKhác về tài sản bị tấn công và control cần dùng.", { top: 350, height: 240, size: 20 });
  notes(s, 28, "Lab06", "Lab06/app.py; cookie_service.py; seed.py", "Cookie flags không làm role client trở thành authoritative. Phân biệt poisoning với hijacking để chọn defense đúng.");
}

// 29
{
  const s = beginSlide(29, "LAB06 / COOKIE POISONING", "Plain cookie: sửa một value, đổi một quyết định", "DevTools cho thấy Name/Value/Domain/Path/HttpOnly/Secure/SameSite và điểm server tin sai.", "Lab06/app.py plain routes · config.py");
  placeholder(s, 29, "Lab06", "51_plain_cookie_modified_application.png", pos(56, 184, 560, 292), "Sửa role cookie bằng DevTools");
  flow(s, 29, "S29_STEPS", ["LOGIN\nstudent", "lab06_role\nuser → admin", "RELOAD", "ADMIN"], pos(650, 184, 574, 94), { size: 19, gap: 5, arrowW: 18, arrowColor: C.red });
  matrix(s, 29, "S29_FLAGS", ["FLAG", "BẢO VỆ", "KHÔNG BẢO VỆ"], [
    ["HttpOnly", "JS đọc cookie", "server tin role"],
    ["Secure", "HTTP transport", "authorization"],
    ["SameSite", "cross-site send", "client edit"],
  ], pos(650, 322, 574, 206), [130, 205, 239], { size: 19 });
  callout(s, 29, "S29_PRIVACY", "ẢNH BẰNG CHỨNG", "Che token/session dài; chỉ giữ origin, cookie name, value, path/flags và kết quả quyền cần thiết.", pos(56, 552, 1168, 66), C.orange);
  notes(s, 29, "Lab06", "Lab06/app.py vulnerable plain cookie; HUONG_DAN_CHUP_ANH.md", "Dùng tài khoản student và chỉ sửa lab06_role. Không công bố giá trị session hoặc token dài trong ảnh.");
}

// 30
{
  const s = beginSlide(30, "LAB06 / COOKIE POISONING", "Encoding, signing và encryption giải quyết khác nhau", "Encryption bảo vệ confidentiality. Integrity chỉ có khi dùng authenticated encryption/AEAD hoặc encryption kèm MAC.", "Lab06/base64_cookie_service.py · signed/encrypted services");
  flow(s, 30, "S30_B64", ["DECODE", "XEM JSON", "SỬA ROLE", "ENCODE LẠI", "GỬI LẠI", "SERVER VULN\nCHẤP NHẬN"], pos(56, 184, 1168, 94), { size: 19, gap: 6, arrowW: 18, arrowColor: C.red });
  matrix(s, 30, "S30_COMPARE", ["CƠ CHẾ", "CONFIDENTIALITY", "INTEGRITY", "CLIENT THẤY/SỬA"], [
    ["Plain", "không", "không", "thấy + sửa"],
    ["Base64", "không", "không", "decode + sửa"],
    ["Signed", "không", "có", "thấy; sửa bị phát hiện"],
    ["Encrypted", "có", "chỉ khi AEAD/MAC", "không đọc;\nsửa cần key/MAC"],
  ], pos(56, 330, 690, 286), [150, 170, 180, 190]);
  placeholder(s, 30, "Lab06", "Lab06_base64_cookie_decode_edit_encode.png", pos(774, 330, 450, 286), "Decode → sửa role → encode lại", "Lab06_base64_cookie_\ndecode_edit_encode.png");
  notes(s, 30, "Lab06", "Lab06/base64_cookie_service.py; signed_cookie_service.py; encrypted_cookie_service.py", "Base64 không có secret và không có MAC. Signed cookie bảo vệ integrity nhưng vẫn lộ payload; encryption mới bảo vệ confidentiality khi triển khai đúng.");
}

// 31
{
  const s = beginSlide(31, "LAB06 / COOKIE POISONING", "Server session giữ quyền ở phía authoritative", "Signed cookie phát hiện tamper; server session giữ role authoritative và hỗ trợ rotate/revoke.", "Lab06/server_session_service.py · authorization_service.py");
  flow(s, 31, "S31_SESSION", ["opaque ID", "hash lookup", "active + expiry", "DB role", "authorize", "allow / deny"], pos(56, 184, 730, 94), { size: 19, gap: 4, arrowW: 15, arrowColor: C.green });
  placeholder(s, 31, "Lab06", "56_signed_cookie_rejected_response.png", pos(822, 184, 402, 244), "Response secure từ chối signed cookie sửa", "56_signed_cookie_\nrejected_response.png");
  matrix(s, 31, "S31_CONTROL", ["SỰ KIỆN", "SERVER ACTION", "HIỆU QUẢ"], [
    ["Login", "rotate ID", "chống fixation"],
    ["Request", "DB role + authz", "không tin client role"],
    ["Logout", "revoke session", "token cũ vô hiệu"],
    ["Tamper signed", "BadData → reject", "integrity fail closed"],
  ], pos(56, 326, 730, 286), [160, 280, 290]);
  callout(s, 31, "S31_FLAGS", "COOKIE FLAGS", "HttpOnly · Secure khi HTTPS · SameSite=Lax · Path=/ — lớp bổ sung cho token, không thay server-side authz.", pos(822, 470, 402, 142), C.orange);
  notes(s, 31, "Lab06", "Lab06/server_session_service.py; authorization_service.py; signed cookie BadData handling", "Rotate khi login, revoke khi logout, và đọc role từ DB ở mỗi quyết định. Trên localhost HTTP, Secure=false là cấu hình demo có chủ đích.");
}

// 32
{
  const s = beginSlide(32, "LAB06 / COOKIE POISONING", "Chọn state model theo thuộc tính cần bảo vệ", "Authorization nhạy cảm vẫn phải được quyết định ở server.", "BaiTapTopic04.docx · mục Lab06 · report Lab06");
  matrix(s, 32, "S32_MATRIX", ["MODEL", "C", "I", "REVOKE?", "DÙNG CHO ROLE?"], [
    ["Plain", "—", "—", "—", "không"],
    ["Base64", "—", "—", "—", "không"],
    ["Signed", "—", "✓", "khó", "vẫn cần server authz"],
    ["Encrypted", "✓", "AEAD/MAC mới có", "khó", "không làm nguồn quyền authoritative"],
    ["Server session", "✓", "✓", "✓", "khuyến nghị"],
  ], pos(56, 178, 690, 352), [150, 55, 175, 110, 200]);
  qaGrid(s, 32, "S32_QA", [
    "Cookie là client-controlled input.",
    "Poisoning sửa state; hijacking lấy token.",
    "Base64 là encoding, không encryption.",
    "Signed cookie phát hiện sửa đổi.",
    "Flags không thay authorization.",
    "Server session hỗ trợ rotate + revoke.",
  ], pos(774, 178, 450, 438));
  callout(s, 32, "S32_RULE", "RULE", "Không lưu role, is_admin, balance hoặc permission như dữ liệu authoritative ở client.", pos(56, 566, 690, 52), C.orange);
  notes(s, 32, "Lab06", "BaiTapTopic04.docx; report Lab06; cookie/session services", "Dùng matrix để trả lời câu hỏi về confidentiality, integrity và revocation. Kết luận không đổi: authorization phải dựa vào server state.");
}

// 33 — Closing
{
  const s = beginSlide(33, "TỔNG KẾT", "", "", "BaiTapTopic04.docx · phần bài học và tổng kết · Lab01–Lab06", { orange: true });
  label(s, "S33_KICKER", "SECURITY CYCLE / ROOT-CAUSE FIRST", 56, 40, 700, { color: C.black });
  text(s, "S33_TITLE", "THEO DẤU DỮ LIỆU.\nVÁ ĐÚNG ĐIỂM GÃY.", pos(52, 92, 1170, 130), { size: 54, bold: true, color: C.black, insets: { top: 0, right: 0, bottom: 0, left: 0 } });
  const steps = ["1 NHẬN DIỆN", "2 KHAI THÁC LOCAL", "3 QUAN SÁT", "4 PHÂN TÍCH", "5 ĐÁNH GIÁ", "6 VÁ", "7 RETEST"];
  steps.forEach((step, i) => {
    box(s, `S33_STEP_${i + 1}`, step, pos(56 + (i % 4) * 292, 278 + Math.floor(i / 4) * 96, 270, 72), { fill: "none", line: C.black, size: 20, bold: true, color: C.black, align: "center", valign: "middle" });
  });
  zone(33, "cycle", 56, 278, 1146, 168);
  text(s, "S33_RULES", "XSS → SAFE OUTPUT/SINK   /   BUFFER → BOUNDED COPY   /   TAMPERING → SERVER POLICY\nCSRF → INTENT PROOF   /   SQLi → PARAMETER BINDING   /   COOKIE → SERVER AUTHORIZATION", pos(56, 502, 1168, 82), { mono: true, size: 20, bold: true, color: C.black, align: "center", valign: "middle" });
  text(s, "S33_CLOSE", "CẤU TRÚC BÁO CÁO 11 MỤC\nTên lab · Mục tiêu · Môi trường · Các bước · Kết quả · Nguyên nhân\nẢnh hưởng · Phòng chống · Bản vá · Bài học · Phụ lục ảnh/log/request-response.", pos(56, 588, 1168, 64), { mono: true, size: 19, bold: true, color: C.black, align: "center", valign: "middle" });
  notes(s, 33, "Tổng kết", "BaiTapTopic04.docx · cấu trúc báo cáo 11 mục; toàn bộ source/report", "Kết lại bằng quy trình bảy bước và cấu trúc báo cáo thống nhất cho cả sáu lab.");
}

function validateGeometry() {
  const errors = [];
  for (const slide of qaSlides) {
    for (const z of slide.zones) {
      if (z.left < 0 || z.top < 0 || z.width <= 0 || z.height <= 0 || z.left + z.width > W || z.top + z.height > H) {
        errors.push(`Slide ${slide.index}: out of bounds ${z.name}`);
      }
      if (z.top < 160 && slide.index !== 1 && slide.index !== 33) {
        errors.push(`Slide ${slide.index}: content zone enters title area ${z.name}`);
      }
      if (z.top + z.height > 668) {
        errors.push(`Slide ${slide.index}: content zone enters footer ${z.name}`);
      }
    }
    for (let i = 0; i < slide.zones.length; i += 1) {
      for (let j = i + 1; j < slide.zones.length; j += 1) {
        const a = slide.zones[i];
        const b = slide.zones[j];
        const overlap = a.left < b.left + b.width && a.left + a.width > b.left && a.top < b.top + b.height && a.top + a.height > b.top;
        if (overlap) errors.push(`Slide ${slide.index}: zone overlap ${a.name} <> ${b.name}`);
      }
    }
  }
  if (errors.length) throw new Error(`Geometry QA failed:\n${errors.join("\n")}`);
}

async function main() {
  if (presentation.slides.items.length !== 33) throw new Error(`Expected 33 slides, got ${presentation.slides.items.length}`);
  if (placeholderManifest.length !== 18) throw new Error(`Expected 18 placeholders, got ${placeholderManifest.length}`);
  const expectedCounts = new Map([["Lab01", 2], ["Lab02", 3], ["Lab03", 3], ["Lab04", 3], ["Lab05", 4], ["Lab06", 3]]);
  for (const [lab, count] of expectedCounts) {
    const actual = placeholderManifest.filter((p) => p.lab === lab).length;
    if (actual !== count) throw new Error(`${lab}: expected ${count} placeholders, got ${actual}`);
  }
  validateGeometry();
  await fs.mkdir(path.dirname(OUT), { recursive: true });
  await fs.mkdir(QA, { recursive: true });
  for (const [i, slide] of presentation.slides.items.entries()) {
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(QA, `slide-${String(i + 1).padStart(2, "0")}.layout.json`), await layout.text(), "utf8");
  }
  if (RENDER) {
    await fs.mkdir(RENDER, { recursive: true });
    for (const [i, slide] of presentation.slides.items.entries()) {
      const png = await presentation.export({ slide, format: "png", scale: 1 });
      await fs.writeFile(path.join(RENDER, `slide-${String(i + 1).padStart(2, "0")}.png`), new Uint8Array(await png.arrayBuffer()));
    }
    const montage = await presentation.export({ format: "webp", montage: true, scale: 0.4 });
    await fs.writeFile(path.join(RENDER, "montage.webp"), new Uint8Array(await montage.arrayBuffer()));
  }
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(OUT);
  const imported = await PresentationFile.importPptx(await FileBlob.load(OUT));
  if (imported.slides.items.length !== 33) throw new Error(`Round-trip import found ${imported.slides.items.length} slides`);
  const inspected = await imported.inspect({ kind: "slide,notes", maxChars: 12000 });
  await fs.writeFile(path.join(QA, "inspect.ndjson"), inspected.ndjson, "utf8");
  await fs.rm(`${OUT}.inspect.ndjson`, { force: true });
  await fs.writeFile(path.join(QA, "placeholder-manifest.json"), JSON.stringify(placeholderManifest, null, 2), "utf8");
  await fs.writeFile(path.join(QA, "qa-summary.json"), JSON.stringify({
    output: OUT,
    slideSize: { widthPx: W, heightPx: H, widthIn: W / 96, heightIn: H / 96 },
    slides: presentation.slides.items.length,
    labSlides: 30,
    placeholders: placeholderManifest.length,
    notesAssigned: 33,
    geometry: "pass",
    roundTripImport: "pass",
    renderedImagesCreated: RENDER ? 33 : 0,
    renderedMontageCreated: Boolean(RENDER),
    pdfCreated: false,
  }, null, 2), "utf8");
  process.stdout.write(JSON.stringify({ output: OUT, slides: 33, placeholders: placeholderManifest }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
