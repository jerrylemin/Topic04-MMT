(() => {
  document.querySelectorAll("[data-parameter-inspector]").forEach((panel) => {
    const value = panel.querySelector("[data-parameter-value]");
    if (value && value.textContent.trim() !== "—") value.classList.add("parameter-highlight");
  });
})();
