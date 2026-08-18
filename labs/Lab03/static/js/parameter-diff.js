const updateDiff = (input) => {
  const row = input.closest(".parameter-row");
  if (!row) return;
  const modified = input.value !== input.dataset.original;
  row.classList.toggle("is-modified", modified);
  const output = row.querySelector("[data-param-diff]");
  if (output) output.textContent = modified ? `${input.dataset.original} → ${input.value}` : "unchanged";
};

document.querySelectorAll("[data-original]").forEach((input) => {
  input.addEventListener("input", () => updateDiff(input));
  updateDiff(input);
});
