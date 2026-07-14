document.querySelectorAll("[data-confirm-submit]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!confirm("Gửi form minh họa tới Victim Application local?")) event.preventDefault();
  });
});
