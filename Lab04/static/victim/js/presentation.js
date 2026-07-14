const setPresentation = (enabled) => {
  document.body.classList.toggle("presenting", enabled);
  document.querySelectorAll("[data-presentation-toggle]").forEach((button) => {
    button.setAttribute("aria-pressed", String(enabled));
    button.textContent = enabled ? "Thoát trình chiếu" : "Presentation Mode";
  });
};
document.addEventListener("click", (event) => {
  if (event.target.closest("[data-presentation-toggle]")) setPresentation(!document.body.classList.contains("presenting"));
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setPresentation(false);
  if (!document.body.classList.contains("presenting")) return;
  const action = event.key === "ArrowRight" ? "next" : event.key === "ArrowLeft" ? "prev" : "";
  document.querySelector(`[data-trace-action="${action}"]`)?.click();
});
