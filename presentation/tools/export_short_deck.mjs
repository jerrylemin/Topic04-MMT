import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const TOOL_DIR = path.dirname(fileURLToPath(import.meta.url));
const { chromium } = require(path.join(TOOL_DIR, "playwright", "node_modules", "playwright"));
const PptxGenJS = require("pptxgenjs");

const PRESENTATION_DIR = path.resolve(TOOL_DIR, "..");
const HTML_PATH = path.resolve(process.argv[2] ?? path.join(PRESENTATION_DIR, "Topic04_6Labs_short.html"));
const PPTX_PATH = path.resolve(
  process.argv[3] ?? path.join(PRESENTATION_DIR, "21127645_LeMinh_21127224_NguyenVuBach_Topic04_6Labs_short.pptx"),
);
const QA_DIR = path.resolve(
  process.argv[4] ?? path.join(os.tmpdir(), "codex-presentations", "topic04-short", "qa"),
);
const SLIDE_DIR = path.join(QA_DIR, "slides");

const VIEWPORTS = [
  { width: 1920, height: 1080, name: "1920x1080" },
  { width: 1280, height: 720, name: "1280x720" },
  { width: 768, height: 1024, name: "768x1024" },
  { width: 375, height: 667, name: "375x667" },
  { width: 667, height: 375, name: "667x375" },
];

async function inspectSlide(page, slideIndex) {
  return page.evaluate((index) => {
    window.deckController.showSlide(index);
    const stage = document.getElementById("deckStage");
    const slide = document.querySelectorAll(".slide")[index];
    const stageRect = stage.getBoundingClientRect();
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.visibility !== "hidden" && style.opacity !== "0" && rect.width > 0 && rect.height > 0;
    };
    const relativeRect = (element) => {
      const rect = element.getBoundingClientRect();
      return {
        left: (rect.left - stageRect.left) / (stageRect.width / 1920),
        top: (rect.top - stageRect.top) / (stageRect.height / 1080),
        right: (rect.right - stageRect.left) / (stageRect.width / 1920),
        bottom: (rect.bottom - stageRect.top) / (stageRect.height / 1080),
        width: rect.width / (stageRect.width / 1920),
        height: rect.height / (stageRect.height / 1080),
      };
    };

    const boundSelectors = [
      "[data-overlap-check]", "h1", "h2", ".chrome", ".foot", ".catalogue",
      ".cover-meta", ".cover-title", ".cover-subtitle", ".cover-authors",
      ".chapter-title", ".three-questions", ".chapter-sub", ".closing-title",
      ".closing-principles",
    ];
    const boundElements = Array.from(slide.querySelectorAll(boundSelectors.join(","))).filter(visible);
    const bounds = boundElements
      .map((element) => ({ element, rect: relativeRect(element) }))
      .filter(({ rect }) => rect.left < -0.5 || rect.top < -0.5 || rect.right > 1920.5 || rect.bottom > 1080.5)
      .map(({ element, rect }) => ({
        selector: element.className || element.tagName,
        text: element.textContent.trim().slice(0, 90),
        rect,
      }));

    const fontIssues = Array.from(slide.querySelectorAll("*"))
      .filter((element) => visible(element) && element.children.length === 0 && element.textContent.trim())
      .map((element) => ({ element, size: parseFloat(getComputedStyle(element).fontSize) }))
      .filter(({ size }) => size < 21.33)
      .map(({ element, size }) => ({
        selector: element.className || element.tagName,
        text: element.textContent.trim().slice(0, 90),
        fontSizePx: size,
      }));

    const overflow = [];
    const clippedContainers = Array.from(slide.querySelectorAll(".content,[data-overlap-check]"))
      .filter(visible)
      .filter((element) => {
        const style = getComputedStyle(element);
        return [style.overflow, style.overflowX, style.overflowY].some((value) => ["hidden", "clip", "auto", "scroll"].includes(value));
      });
    clippedContainers.forEach((element) => {
      if (element.scrollWidth > element.clientWidth + 1 || element.scrollHeight > element.clientHeight + 1) {
        overflow.push({
          selector: element.className || element.tagName,
          text: element.textContent.trim().slice(0, 90),
          client: [element.clientWidth, element.clientHeight],
          scroll: [element.scrollWidth, element.scrollHeight],
        });
      }
    });

    Array.from(slide.querySelectorAll("*") )
      .filter((element) => visible(element) && element.children.length === 0 && element.textContent.trim())
      .forEach((element) => {
        const container = element.closest("[data-overlap-check]");
        if (!container || container === element) return;
        const rect = element.getBoundingClientRect();
        const parent = container.getBoundingClientRect();
        if (rect.left < parent.left - 1 || rect.top < parent.top - 1 || rect.right > parent.right + 1 || rect.bottom > parent.bottom + 1) {
          overflow.push({
            selector: element.className || element.tagName,
            text: element.textContent.trim().slice(0, 90),
            container: container.className || container.tagName,
            elementRect: [rect.left, rect.top, rect.right, rect.bottom],
            containerRect: [parent.left, parent.top, parent.right, parent.bottom],
          });
        }
      });

    const overlapElements = Array.from(slide.querySelectorAll("[data-overlap-check]")).filter(visible);
    const overlaps = [];
    for (let i = 0; i < overlapElements.length; i += 1) {
      for (let j = i + 1; j < overlapElements.length; j += 1) {
        const a = overlapElements[i];
        const b = overlapElements[j];
        if (a.contains(b) || b.contains(a)) continue;
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        const x = Math.max(0, Math.min(ar.right, br.right) - Math.max(ar.left, br.left));
        const y = Math.max(0, Math.min(ar.bottom, br.bottom) - Math.max(ar.top, br.top));
        if (x * y > 1) {
          overlaps.push({
            first: `${a.className || a.tagName}: ${a.textContent.trim().slice(0, 60)}`,
            second: `${b.className || b.tagName}: ${b.textContent.trim().slice(0, 60)}`,
            intersectionArea: Math.round(x * y),
          });
        }
      }
    }

    return {
      slide: index + 1,
      ariaLabel: slide.getAttribute("aria-label"),
      activeCount: document.querySelectorAll(".slide.active").length,
      visibleCount: document.querySelectorAll(".slide.visible").length,
      slideClient: [slide.clientWidth, slide.clientHeight],
      slideScroll: [slide.scrollWidth, slide.scrollHeight],
      bounds,
      fontIssues,
      overflow,
      overlaps,
    };
  }, slideIndex);
}

async function validateViewport(browser, viewport) {
  const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height } });
  await page.goto(pathToFileURL(HTML_PATH).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => document.body.classList.add("export-settle"));
  const meta = await page.evaluate(() => ({
    slideCount: document.querySelectorAll(".slide").length,
    stageWidth: document.getElementById("deckStage").offsetWidth,
    stageHeight: document.getElementById("deckStage").offsetHeight,
    hasController: Boolean(window.deckController),
  }));
  const slides = [];
  for (let index = 0; index < meta.slideCount; index += 1) {
    slides.push(await inspectSlide(page, index));
  }
  await page.close();
  return { viewport, meta, slides };
}

async function captureSlides(browser, slideCount) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(HTML_PATH).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => document.body.classList.add("capture-mode"));
  const paths = [];
  for (let index = 0; index < slideCount; index += 1) {
    await page.evaluate((slideIndex) => {
      document.body.classList.remove("export-settle");
      window.deckController.showSlide(slideIndex);
    }, index);
    await page.waitForTimeout(760);
    await page.evaluate(() => document.body.classList.add("export-settle"));
    const output = path.join(SLIDE_DIR, `slide-${String(index + 1).padStart(2, "0")}.png`);
    await page.locator("#deckStage").screenshot({ path: output, type: "png" });
    paths.push(output);
  }
  await page.close();
  return paths;
}

async function buildPptx(slideImages) {
  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "Lê Minh (21127645); Nguyễn Vũ Bách (21127224)";
  pptx.company = "Topic04";
  pptx.subject = "Sáu lab bảo mật ứng dụng web";
  pptx.title = "Sáu lỗ hổng, một ranh giới niềm tin";
  pptx.lang = "vi-VN";
  pptx.theme = {
    headFontFace: "Barlow",
    bodyFontFace: "Barlow",
    lang: "vi-VN",
  };
  pptx.defineSlideMaster({
    title: "FULL_BLEED",
    background: { color: "111111" },
    objects: [],
    slideNumber: { x: 0, y: 0, color: "111111", fontSize: 1 },
  });
  for (const imagePath of slideImages) {
    const slide = pptx.addSlide("FULL_BLEED");
    slide.addImage({ path: imagePath, x: 0, y: 0, w: 13.333333, h: 7.5 });
  }
  await pptx.writeFile({ fileName: PPTX_PATH, compression: true });
}

async function main() {
  await fs.mkdir(SLIDE_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const reports = [];
    for (const viewport of VIEWPORTS) reports.push(await validateViewport(browser, viewport));
    const firstMeta = reports[0].meta;
    if (firstMeta.slideCount < 16 || firstMeta.slideCount > 18) {
      throw new Error(`Slide count ${firstMeta.slideCount} is outside 16–18.`);
    }
    if (firstMeta.stageWidth !== 1920 || firstMeta.stageHeight !== 1080) {
      throw new Error(`Stage is ${firstMeta.stageWidth}×${firstMeta.stageHeight}, expected 1920×1080.`);
    }
    const issues = reports.flatMap((report) => report.slides.flatMap((slide) => {
      const count = slide.bounds.length + slide.fontIssues.length + slide.overflow.length + slide.overlaps.length;
      const stateBad = slide.activeCount !== 1 || slide.visibleCount !== 1 || slide.slideClient[0] !== 1920 || slide.slideClient[1] !== 1080;
      return count || stateBad ? [{ viewport: report.viewport.name, ...slide }] : [];
    }));
    await fs.writeFile(path.join(QA_DIR, "html-qa.json"), JSON.stringify({ reports, issues }, null, 2), "utf8");
    if (issues.length) throw new Error(`HTML QA found ${issues.length} slide/viewport issue records. See ${path.join(QA_DIR, "html-qa.json")}`);

    const slideImages = await captureSlides(browser, firstMeta.slideCount);
    await buildPptx(slideImages);
    const stats = await fs.stat(PPTX_PATH);
    const summary = {
      html: HTML_PATH,
      pptx: PPTX_PATH,
      qaDir: QA_DIR,
      slideCount: firstMeta.slideCount,
      stage: "1920x1080",
      pptxBytes: stats.size,
      validatedViewports: VIEWPORTS.map((v) => v.name),
      issueCount: 0,
    };
    await fs.writeFile(path.join(QA_DIR, "summary.json"), JSON.stringify(summary, null, 2), "utf8");
    process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
