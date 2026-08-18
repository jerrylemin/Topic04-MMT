document.documentElement.classList.add("js");

document.addEventListener("click", (event) => {
  const toggle = event.target.closest("[data-nav-toggle]");
  if (toggle) {
    const nav = document.getElementById(toggle.getAttribute("aria-controls"));
    const open = nav?.classList.toggle("is-open") ?? false;
    toggle.setAttribute("aria-expanded", String(open));
  }

  const compareTab = event.target.closest("[data-compare-tab]");
  if (compareTab) {
    const key = compareTab.dataset.compareTab;
    document.querySelectorAll("[data-compare-tab]").forEach((tab) => tab.classList.toggle("is-active", tab === compareTab));
    document.querySelectorAll("[data-compare-panel]").forEach((panel) => panel.classList.toggle("is-active", panel.dataset.comparePanel === key));
  }
});
