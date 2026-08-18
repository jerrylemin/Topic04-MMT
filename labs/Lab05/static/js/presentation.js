(() => {
  const setPresentation = (enabled, source) => {
    document.body.classList.toggle("is-presenting", enabled);
    document.querySelectorAll("[data-presentation-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", String(enabled));
      button.textContent = enabled ? "Thoát trình chiếu" : "Presentation Mode";
    });
    if (enabled) source?.closest("[data-trace-shell]")?.querySelector(".timeline-summary")?.focus();
    else source?.focus();
  };
  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-presentation-toggle]");
    if (button) setPresentation(!document.body.classList.contains("is-presenting"), button);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.body.classList.contains("is-presenting")) setPresentation(false, document.querySelector("[data-presentation-toggle]"));
    if (!document.body.classList.contains("is-presenting")) return;
    const shell = document.querySelector("[data-trace-shell]");
    if (event.key === "ArrowRight") { event.preventDefault(); shell?.querySelector('[data-trace-action="next"]')?.click(); }
    if (event.key === "ArrowLeft") { event.preventDefault(); shell?.querySelector('[data-trace-action="prev"]')?.click(); }
  });
})();
