(() => {
  let activeShell = null;

  const setPresentation = (shell, enabled) => {
    activeShell = enabled ? shell : null;
    document.body.classList.toggle("presentation", enabled);
    document.querySelectorAll("[data-action='presentation']").forEach(button => {
      button.textContent = enabled ? "Thoát Presentation" : "Presentation Mode";
      button.setAttribute("aria-pressed", String(enabled));
    });
    if (enabled) {
      const current = shell?.querySelector(".trace-step.current");
      if (current) current.open = true;
    }
  };

  window.addEventListener("lab:presentation", event => {
    const shell = event.detail?.shell;
    setPresentation(shell, !document.body.classList.contains("presentation"));
  });

  document.addEventListener("keydown", event => {
    if (!document.body.classList.contains("presentation") || !activeShell) return;
    if (event.target.matches("input, textarea, select")) return;
    if (event.key === "Escape") {
      event.preventDefault();
      setPresentation(activeShell, false);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      activeShell.querySelector("[data-action='next']")?.click();
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      activeShell.querySelector("[data-action='prev']")?.click();
    }
    if (event.key === " ") {
      event.preventDefault();
      const action = activeShell.dataset.playing === "true" ? "pause" : "autoplay";
      activeShell.querySelector(`[data-action='${action}']`)?.click();
    }
  });
})();
