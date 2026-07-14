document.addEventListener("click", (event) => {
  const toggle = event.target.closest("[data-nav-toggle]");
  if (!toggle) return;
  const nav = document.querySelector("[data-nav]");
  nav?.classList.toggle("open");
  toggle.setAttribute("aria-expanded", String(nav?.classList.contains("open")));
});
