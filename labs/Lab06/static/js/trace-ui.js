(() => {
  document.querySelectorAll("[data-trace-shell]").forEach((shell) => {
    const jsonNode = shell.querySelector("[data-trace-json]");
    const statusNode = shell.querySelector("[data-copy-status]");
    let trace = {};
    let current = 0;
    let timer = null;
    try { trace = JSON.parse(jsonNode ? jsonNode.textContent : "{}"); } catch (_error) { trace = {}; }
    const items = () => Array.from(shell.querySelectorAll("[data-step-index]"));
    const activatePanel = (name) => {
      shell.querySelectorAll("[data-trace-tab]").forEach((tab) => {
        const active = tab.dataset.traceTab === name;
        tab.classList.toggle("is-active", active);
        tab.setAttribute("aria-selected", String(active));
      });
      shell.querySelectorAll("[data-trace-panel]").forEach((panel) => panel.classList.toggle("is-active", panel.dataset.tracePanel === name));
    };
    const showStep = (index) => {
      const steps = items();
      if (!steps.length) return;
      current = Math.max(0, Math.min(index, steps.length - 1));
      steps.forEach((item, itemIndex) => {
        const active = itemIndex === current;
        item.classList.toggle("is-current", active);
        const summary = item.querySelector(".timeline-summary");
        if (summary) summary.setAttribute("aria-expanded", String(active));
      });
      const percent = Math.round(((current + 1) / steps.length) * 100);
      const progress = shell.querySelector(".trace-progress");
      if (progress) progress.setAttribute("aria-valuenow", String(percent));
      const fill = progress ? progress.querySelector("span") : null;
      if (fill) fill.style.transform = "scaleX(" + (percent / 100) + ")";
      shell.querySelectorAll("[data-current-step]").forEach((node) => { node.textContent = String(current + 1); });
    };
    const stop = () => {
      window.clearInterval(timer);
      timer = null;
      shell.querySelectorAll('[data-trace-action="autoplay"]').forEach((button) => {
        button.setAttribute("aria-pressed", "false");
        button.textContent = "Tự chạy";
      });
    };
    const toggleAutoplay = (button) => {
      if (timer) { stop(); return; }
      button.setAttribute("aria-pressed", "true");
      button.textContent = "Tạm dừng";
      timer = window.setInterval(() => {
        if (current >= items().length - 1) { stop(); return; }
        showStep(current + 1);
      }, 1800);
    };
    const exportTrace = () => {
      const blobUrl = URL.createObjectURL(new Blob([JSON.stringify(trace, null, 2)], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = String(trace.trace_id || "lab06-trace") + ".json";
      link.click();
      URL.revokeObjectURL(blobUrl);
    };
    shell.querySelectorAll("[data-total-steps]").forEach((node) => { node.textContent = String(items().length); });
    shell.addEventListener("click", async (event) => {
      const summary = event.target.closest(".timeline-summary");
      if (summary) showStep(Number(summary.closest("[data-step-index]").dataset.stepIndex));
      const tab = event.target.closest("[data-trace-tab]");
      if (tab) activatePanel(tab.dataset.traceTab);
      const shortcut = event.target.closest("[data-inspector-open]");
      if (shortcut) activatePanel(shortcut.dataset.inspectorOpen);
      const control = event.target.closest("[data-trace-action]");
      if (!control) return;
      const action = control.dataset.traceAction;
      if (action === "prev") showStep(current - 1);
      if (action === "next") showStep(current + 1);
      if (action === "restart") { stop(); showStep(0); }
      if (action === "autoplay") toggleAutoplay(control);
      if (action === "export") exportTrace();
      if (action === "copy") {
        try {
          await navigator.clipboard.writeText(JSON.stringify(trace, null, 2));
          if (statusNode) statusNode.textContent = "Đã sao chép trace JSON đã được server che dữ liệu nhạy cảm.";
        } catch (_error) {
          if (statusNode) statusNode.textContent = "Trình duyệt không cho phép sao chép tự động.";
        }
      }
    });
    showStep(0);
  });
})();
