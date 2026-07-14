(() => {
  const navToggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("#primary-nav");
  navToggle?.addEventListener("click", () => {
    const open = nav?.classList.toggle("is-open") || false;
    navToggle.setAttribute("aria-expanded", String(open));
  });

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-fill]");
    if (!trigger) return;
    let values = {};
    try { values = JSON.parse(trigger.dataset.fill || "{}"); } catch { return; }
    const form = trigger.closest(".workbench")?.querySelector("[data-lab-form]");
    Object.entries(values).forEach(([name, value]) => {
      const field = form?.elements.namedItem(name);
      if (field) field.value = String(value);
    });
    const firstField = form?.querySelector("input");
    firstField?.focus();
  });

  document.querySelectorAll("[data-table-filter]").forEach((input) => {
    input.addEventListener("input", () => {
      const table = document.getElementById(input.dataset.tableFilter);
      const term = input.value.trim().toLocaleLowerCase("vi");
      table?.querySelectorAll("tbody tr").forEach((row) => {
        row.hidden = Boolean(term) && !row.textContent.toLocaleLowerCase("vi").includes(term);
      });
    });
  });
})();
