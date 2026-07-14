const localOnly = () => ["127.0.0.1", "localhost", "::1"].includes(location.hostname);

document.querySelectorAll("[data-trace-shell]").forEach((shell) => {
  const jsonNode = shell.querySelector("[data-trace-json]");
  let trace = {};
  try { trace = JSON.parse(jsonNode?.textContent || "{}"); } catch { trace = {}; }
  let current = 0;
  let autoplay;

  const steps = () => [...shell.querySelectorAll("[data-step-index]")];
  const activatePanel = (name) => {
    shell.querySelectorAll("[data-trace-tab]").forEach((tab) => tab.classList.toggle("is-active", tab.dataset.traceTab === name));
    shell.querySelectorAll("[data-trace-panel]").forEach((panel) => panel.classList.toggle("is-active", panel.dataset.tracePanel === name));
  };
  const showStep = (index) => {
    const items = steps();
    if (!items.length) return;
    current = Math.max(0, Math.min(index, items.length - 1));
    items.forEach((item, itemIndex) => item.classList.toggle("is-current", itemIndex === current));
    const percent = ((current + 1) / items.length) * 100;
    const progress = shell.querySelector(".trace-progress");
    progress?.setAttribute("aria-valuenow", String(Math.round(percent)));
    progress?.querySelector("span")?.style.setProperty("transform", `scaleX(${percent / 100})`);
    shell.querySelectorAll("[data-current-step]").forEach((node) => node.textContent = String(current + 1));
  };
  const downloadTrace = () => {
    const blobUrl = URL.createObjectURL(new Blob([JSON.stringify(trace, null, 2)], {type: "application/json"}));
    const anchor = Object.assign(document.createElement("a"), {href: blobUrl, download: `${trace.trace_id || "trace"}.json`});
    anchor.click();
    URL.revokeObjectURL(blobUrl);
  };

  shell.querySelectorAll("[data-total-steps]").forEach((node) => node.textContent = String(steps().length));
  shell.addEventListener("click", async (event) => {
    const summary = event.target.closest(".timeline-summary");
    if (summary) {
      const expanded = summary.getAttribute("aria-expanded") === "true";
      summary.setAttribute("aria-expanded", String(!expanded));
      current = Number(summary.closest("[data-step-index]").dataset.stepIndex);
      showStep(current);
    }
    const tab = event.target.closest("[data-trace-tab]");
    if (tab) activatePanel(tab.dataset.traceTab);
    const inspectorButton = event.target.closest("[data-inspector-open]");
    if (inspectorButton) activatePanel(inspectorButton.dataset.inspectorOpen);
    const action = event.target.closest("[data-trace-action]")?.dataset.traceAction;
    if (!action) return;
    if (action === "next") showStep(current + 1);
    if (action === "prev") showStep(current - 1);
    if (action === "pause") clearInterval(autoplay);
    if (action === "autoplay") {
      clearInterval(autoplay);
      autoplay = setInterval(() => current < steps().length - 1 ? showStep(current + 1) : clearInterval(autoplay), 1600);
    }
    if (action === "copy") await navigator.clipboard?.writeText(JSON.stringify(trace, null, 2));
    if (action === "export") downloadTrace();
    if (action === "replay") location.reload();
    if (action === "clear" && localOnly()) {
      clearInterval(autoplay);
      try { await fetch("/api/trace/clear", {method: "POST", credentials: "same-origin"}); } catch { /* UI still clears the current view. */ }
      shell.querySelector(".timeline")?.replaceChildren();
      shell.querySelector(".trace-progress span")?.style.setProperty("transform", "scaleX(0)");
      shell.querySelector(".trace-progress")?.setAttribute("aria-valuenow", "0");
    }
  });
  showStep(0);
});
