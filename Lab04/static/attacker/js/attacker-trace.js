document.querySelectorAll("[data-attacker-timeline] li").forEach((step, index) => {
  step.dataset.step = String(index + 1);
});
