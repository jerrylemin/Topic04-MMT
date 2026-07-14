(() => {
  const copyText = async text => {
    if (navigator.clipboard) return navigator.clipboard.writeText(text);
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.append(area);
    area.select();
    document.execCommand("copy");
    area.remove();
  };

  document.querySelectorAll("[data-trace-shell]").forEach(shell => {
    const jsonNode = shell.querySelector(".trace-json");
    let trace = {};
    try { trace = JSON.parse(jsonNode?.textContent || "{}"); } catch { trace = {}; }
    shell.labTrace = trace;

    const steps = [...shell.querySelectorAll("[data-step-index]")];
    const progress = shell.querySelector("[data-progress-bar]");
    const progressTrack = shell.querySelector("[role='progressbar']");
    const counter = shell.querySelector("[data-step-counter]");
    const announcer = shell.querySelector("[data-presentation-announcer]");
    let current = 0;
    let timer = 0;

    const setPlaying = playing => {
      shell.dataset.playing = String(playing);
      if (!playing) window.clearInterval(timer);
    };

    const show = index => {
      if (!steps.length) return;
      current = Math.max(0, Math.min(index, steps.length - 1));
      const presenting = document.body.classList.contains("presentation");
      steps.forEach((step, stepIndex) => {
        const selected = stepIndex === current;
        step.classList.toggle("current", selected);
        if (presenting) step.open = selected;
      });
      const position = current + 1;
      if (progress) progress.style.width = `${position / steps.length * 100}%`;
      if (progressTrack) progressTrack.setAttribute("aria-valuenow", String(position));
      if (counter) counter.textContent = `${position} / ${steps.length}`;
      if (announcer) {
        const title = steps[current].querySelector(".step-heading b")?.textContent || `Bước ${position}`;
        announcer.textContent = `${title}, bước ${position} trên ${steps.length}`;
      }
    };

    const activate = (name, focus = false) => {
      const tabs = [...shell.querySelectorAll("[role='tab']")];
      tabs.forEach(tab => {
        const selected = tab.dataset.tab === name;
        tab.setAttribute("aria-selected", String(selected));
        tab.tabIndex = selected ? 0 : -1;
        if (selected && focus) tab.focus();
      });
      shell.querySelectorAll("[data-panel]").forEach(panel => {
        const selected = panel.dataset.panel === name;
        panel.hidden = !selected;
        panel.classList.toggle("active", selected);
      });
    };

    shell.addEventListener("keydown", event => {
      const tab = event.target.closest("[role='tab']");
      if (!tab) return;
      const tabs = [...shell.querySelectorAll("[role='tab']")];
      const index = tabs.indexOf(tab);
      let next = null;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next === null) return;
      event.preventDefault();
      activate(tabs[next].dataset.tab, true);
    });

    shell.addEventListener("click", async event => {
      const tab = event.target.closest("[data-tab]");
      if (tab) activate(tab.dataset.tab);

      const panelButton = event.target.closest("[data-open-panel]");
      if (panelButton) {
        if (document.body.classList.contains("presentation")) {
          window.dispatchEvent(new CustomEvent("lab:presentation", { detail: { shell } }));
        }
        activate(panelButton.dataset.openPanel, true);
      }

      const action = event.target.closest("[data-action]")?.dataset.action;
      if (!action) return;
      if (action === "next") show(current + 1);
      if (action === "prev") show(current - 1);
      if (action === "replay") { setPlaying(false); show(0); }
      if (action === "presentation") window.dispatchEvent(new CustomEvent("lab:presentation", { detail: { shell } }));
      if (action === "pause") setPlaying(false);
      if (action === "autoplay") {
        setPlaying(false);
        shell.dataset.playing = "true";
        timer = window.setInterval(() => {
          if (current >= steps.length - 1) { setPlaying(false); return; }
          show(current + 1);
        }, 1800);
      }
      if (action === "copy") {
        try {
          await copyText(JSON.stringify(trace, null, 2));
          if (announcer) announcer.textContent = "Đã sao chép trace.";
        } catch {
          if (announcer) announcer.textContent = "Không thể sao chép trace.";
        }
      }
      if (action === "export") {
        const blobUrl = URL.createObjectURL(new Blob([JSON.stringify(trace, null, 2)], { type: "application/json" }));
        const link = document.createElement("a");
        link.href = blobUrl;
        link.download = `${trace.trace_id || "lab02-trace"}.json`;
        link.click();
        window.setTimeout(() => URL.revokeObjectURL(blobUrl), 0);
      }
      if (action === "clear") {
        try {
          const response = await fetch("/api/trace/clear", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ trace_id: trace.trace_id || "" })
          });
          if (!response.ok) throw new Error("clear failed");
          setPlaying(false);
          shell.replaceChildren(Object.assign(document.createElement("p"), { textContent: "Trace đã được xóa." }));
        } catch {
          if (announcer) announcer.textContent = "Không thể xóa trace. Kiểm tra endpoint local.";
        }
      }
    });

    show(0);
  });
})();
