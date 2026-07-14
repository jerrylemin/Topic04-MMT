const setPresentation = (enabled, button) => {
  document.body.classList.toggle("is-presenting", enabled);
  document.querySelectorAll("[data-presentation-toggle]").forEach((toggle) => {
    toggle.setAttribute("aria-pressed", String(enabled));
    toggle.textContent = enabled ? "Thoát trình chiếu" : "Presentation Mode";
  });
  if (enabled) button?.closest("[data-trace-shell]")?.querySelector(".timeline-summary")?.focus();
};

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-presentation-toggle]");
  if (button) setPresentation(!document.body.classList.contains("is-presenting"), button);
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && document.body.classList.contains("is-presenting")) setPresentation(false);
  if (!document.body.classList.contains("is-presenting")) return;
  const shell = document.querySelector("[data-trace-shell]");
  if (event.key === "ArrowRight") shell?.querySelector('[data-trace-action="next"]')?.click();
  if (event.key === "ArrowLeft") shell?.querySelector('[data-trace-action="prev"]')?.click();
});
