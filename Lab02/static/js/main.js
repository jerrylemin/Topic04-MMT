(() => {
  const byteLength = value => new TextEncoder().encode(value).length;

  document.querySelectorAll("[data-lab-form]").forEach(form => {
    const input = form.querySelector("[data-name-input]");
    if (!input) return;

    const charOutput = form.querySelector("[data-char-count]");
    const byteOutput = form.querySelector("[data-byte-count]");
    const byteError = form.querySelector("[data-byte-error]");
    const submit = form.querySelector("[data-submit]");
    const status = form.querySelector("[data-submit-status]");
    const maxBytes = Number(input.dataset.maxBytes || 256);

    const update = () => {
      const chars = Array.from(input.value).length;
      const bytes = byteLength(input.value);
      const invalid = bytes > maxBytes;
      if (charOutput) charOutput.textContent = String(chars);
      if (byteOutput) byteOutput.textContent = String(bytes);
      if (byteError) byteError.hidden = !invalid;
      input.setAttribute("aria-invalid", String(invalid));
      input.setCustomValidity(invalid ? `Input không được vượt ${maxBytes} byte UTF-8.` : "");
    };

    form.addEventListener("click", event => {
      const sample = event.target.closest("[data-sample-text], [data-sample-length], [data-sample-clear]");
      if (!sample || !form.contains(sample)) return;
      if (sample.hasAttribute("data-sample-clear")) input.value = "";
      else if (sample.dataset.sampleLength) input.value = "A".repeat(Number(sample.dataset.sampleLength));
      else input.value = sample.dataset.sampleText || "";
      update();
      input.focus();
    });

    input.addEventListener("input", update);
    form.addEventListener("submit", event => {
      update();
      if (!form.checkValidity()) {
        event.preventDefault();
        form.reportValidity();
        return;
      }
      if (submit) submit.disabled = true;
      if (status) status.textContent = "Đang chạy tiến trình C và tạo trace...";
    });
    update();
  });

  document.querySelectorAll(".nav-menu nav a").forEach(link => {
    link.addEventListener("click", () => {
      const menu = link.closest("details");
      if (menu && window.matchMedia("(max-width: 980px)").matches) menu.open = false;
    });
  });
})();
