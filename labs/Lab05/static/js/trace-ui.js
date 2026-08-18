(() => {
  document.querySelectorAll("[data-trace-shell]").forEach((shell) => {
    const jsonNode = shell.querySelector("[data-trace-json]");
    let trace = {};
    try { trace = JSON.parse(jsonNode?.textContent || "{}"); } catch { trace = {}; }
    let current = 0;
    let timer = null;
    const steps = () => [...shell.querySelectorAll("[data-step-index]")];
    const status = shell.querySelector("[data-copy-status]");

    const activatePanel = (name) => {
      shell.querySelectorAll("[data-trace-tab]").forEach((tab) => {
        const active = tab.dataset.traceTab === name;
        tab.classList.toggle("is-active", active);
        tab.setAttribute("aria-selected", String(active));
      });
      shell.querySelectorAll("[data-trace-panel]").forEach((panel) => panel.classList.toggle("is-active", panel.dataset.tracePanel === name));
      shell.querySelector(`[data-trace-panel="${CSS.escape(name)}"] h3`)?.focus?.();
    };
    const showStep = (index) => {
      const items = steps();
      if (!items.length) return;
      current = Math.max(0, Math.min(index, items.length - 1));
      items.forEach((item, itemIndex) => {
        const active = itemIndex === current;
        item.classList.toggle("is-current", active);
        item.querySelector(".timeline-summary")?.setAttribute("aria-expanded", String(active));
      });
      const percent = Math.round(((current + 1) / items.length) * 100);
      const progress = shell.querySelector(".trace-progress");
      if (progress) {
        progress.value = percent;
        progress.textContent = `${percent}%`;
      }
      shell.querySelectorAll("[data-current-step]").forEach((node) => { node.textContent = String(current + 1); });
    };
    const stopAutoPlay = () => {
      clearInterval(timer);
      timer = null;
      shell.querySelectorAll('[data-trace-action="autoplay"]').forEach((button) => {
        button.setAttribute("aria-pressed", "false");
        button.textContent = "Auto Play";
      });
    };
    const toggleAutoPlay = (button) => {
      if (timer) { stopAutoPlay(); return; }
      button.setAttribute("aria-pressed", "true");
      button.textContent = "Tạm dừng";
      timer = window.setInterval(() => {
        if (current >= steps().length - 1) { stopAutoPlay(); return; }
        showStep(current + 1);
      }, 1800);
    };
    const exportTrace = () => {
      const url = URL.createObjectURL(new Blob([JSON.stringify(trace, null, 2)], { type: "application/json" }));
      const link = Object.assign(document.createElement("a"), { href: url, download: `${trace.trace_id || "trace"}.json` });
      link.click();
      URL.revokeObjectURL(url);
    };

    shell.querySelectorAll("[data-total-steps]").forEach((node) => { node.textContent = String(steps().length); });
    shell.addEventListener("click", async (event) => {
      const summary = event.target.closest(".timeline-summary");
      if (summary) showStep(Number(summary.closest("[data-step-index]").dataset.stepIndex));
      const tab = event.target.closest("[data-trace-tab]");
      if (tab) activatePanel(tab.dataset.traceTab);
      const inspector = event.target.closest("[data-inspector-open]");
      if (inspector) activatePanel(inspector.dataset.inspectorOpen);
      const control = event.target.closest("[data-trace-action]");
      if (!control) return;
      const action = control.dataset.traceAction;
      if (action === "prev") showStep(current - 1);
      if (action === "next") showStep(current + 1);
      if (action === "restart") { stopAutoPlay(); showStep(0); }
      if (action === "autoplay") toggleAutoPlay(control);
      if (action === "export") exportTrace();
      if (action === "copy") {
        try {
          await navigator.clipboard.writeText(JSON.stringify(trace, null, 2));
          if (status) status.textContent = "Đã sao chép trace JSON.";
        } catch { if (status) status.textContent = "Trình duyệt không cho phép sao chép tự động."; }
      }
    });
    showStep(0);
  });
})();
