document.querySelectorAll("[data-trace-shell]").forEach((shell) => {
  const items = [...shell.querySelectorAll("[data-step-index]")];
  let current = 0;
  let autoplay;
  const show = (index) => {
    if (!items.length) return;
    current = Math.max(0, Math.min(index, items.length - 1));
    items.forEach((item, i) => item.classList.toggle("current", i === current));
    const percent = (current + 1) / items.length;
    shell.querySelector(".progress span")?.style.setProperty("transform", `scaleX(${percent})`);
    shell.querySelector(".progress")?.setAttribute("aria-valuenow", String(Math.round(percent * 100)));
    shell.querySelectorAll("[data-current-step]").forEach((node) => node.textContent = String(current + 1));
  };
  shell.querySelectorAll("[data-total-steps]").forEach((node) => node.textContent = String(items.length));
  shell.addEventListener("click", (event) => {
    const summary = event.target.closest(".timeline-summary");
    if (summary) { summary.setAttribute("aria-expanded", String(summary.getAttribute("aria-expanded") !== "true")); show(Number(summary.closest("[data-step-index]").dataset.stepIndex)); }
    const tab = event.target.closest("[data-trace-tab]");
    const inspector = event.target.closest("[data-inspector-open]");
    const panelName = tab?.dataset.traceTab || inspector?.dataset.inspectorOpen;
    if (panelName) {
      shell.querySelectorAll("[data-trace-tab]").forEach((node) => node.classList.toggle("active", node.dataset.traceTab === panelName));
      shell.querySelectorAll("[data-trace-panel]").forEach((node) => node.classList.toggle("active", node.dataset.tracePanel === panelName));
    }
    const action = event.target.closest("[data-trace-action]")?.dataset.traceAction;
    if (action === "next") show(current + 1);
    if (action === "prev") show(current - 1);
    if (action === "pause") clearInterval(autoplay);
    if (action === "autoplay") { clearInterval(autoplay); autoplay = setInterval(() => current < items.length - 1 ? show(current + 1) : clearInterval(autoplay), 1600); }
  });
  show(0);
});
