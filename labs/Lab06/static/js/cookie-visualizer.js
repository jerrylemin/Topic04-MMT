(() => {
  document.querySelectorAll("[data-cookie-visualizer]").forEach((visualizer) => {
    const before = visualizer.querySelector("[data-cookie-before]");
    const after = visualizer.querySelector("[data-cookie-after]");
    if (!before || !after) return;
    visualizer.classList.toggle("has-change", before.textContent.trim() !== after.textContent.trim());
  });
})();
