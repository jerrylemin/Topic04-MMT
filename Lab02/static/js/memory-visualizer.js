(() => {
  const number = (value, fallback = 0) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) && parsed >= 0 ? parsed : fallback;
  };

  document.querySelectorAll("[data-memory-visualizer]").forEach(visualizer => {
    const raw = visualizer.dataset.input || "";
    const encoded = new TextEncoder().encode(raw);
    const declaredBytes = number(visualizer.dataset.inputBytes, encoded.length);
    const inputBytes = declaredBytes || encoded.length;
    const bufferSize = number(visualizer.dataset.bufferSize, 32) || 32;
    const safeCapacity = Math.max(0, bufferSize - 1);
    const overflowData = Math.max(0, inputBytes - bufferSize);
    const overflowWrites = Math.max(0, inputBytes + 1 - bufferSize);
    const totalWrites = inputBytes + 1;
    const visibleLimit = bufferSize + 65;
    const visibleCells = Math.max(bufferSize, Math.min(totalWrites, visibleLimit));
    const hasExactBytes = encoded.length === inputBytes;

    const setStat = (name, value) => {
      const node = visualizer.querySelector(`[data-memory-stat='${name}']`);
      if (node) node.textContent = String(value);
    };
    setStat("input", inputBytes);
    setStat("safe", safeCapacity);
    setStat("overflow-data", overflowData);
    setStat("overflow-write", overflowWrites);

    const grid = visualizer.querySelector("[data-byte-grid]");
    if (!grid) return;
    const fragment = document.createDocumentFragment();

    for (let index = 0; index < visibleCells; index += 1) {
      const cell = document.createElement("span");
      const offset = document.createElement("small");
      const value = document.createElement("b");
      const outside = index >= bufferSize;
      const dataByte = index < inputBytes;
      const nullByte = index === inputBytes;

      cell.className = "memory-byte";
      if (outside) cell.classList.add("byte-overflow");
      if (dataByte) cell.classList.add("byte-data");
      if (nullByte) cell.classList.add("byte-null");
      if (index === bufferSize - 1) cell.classList.add("buffer-end");

      offset.textContent = String(index).padStart(2, "0");
      if (dataByte) value.textContent = hasExactBytes ? encoded[index].toString(16).toUpperCase().padStart(2, "0") : "DATA";
      else if (nullByte) value.textContent = "NUL";
      else value.textContent = "--";
      cell.setAttribute("aria-label", `Byte ${index}: ${value.textContent}${outside ? ", ngoài buffer" : ", trong buffer"}`);
      cell.append(offset, value);
      fragment.append(cell);
    }
    grid.replaceChildren(fragment);

    const hiddenWrites = Math.max(0, totalWrites - visibleCells);
    const summary = visualizer.querySelector("[data-memory-summary]");
    if (summary) {
      const boundary = overflowWrites
        ? `${overflowData} byte dữ liệu và null terminator tạo ${overflowWrites} write ngoài buffer.`
        : `${inputBytes} byte dữ liệu và null terminator nằm trong buffer.`;
      summary.textContent = hiddenWrites ? `${boundary} Còn ${hiddenWrites} write không vẽ để giữ sơ đồ dễ đọc.` : boundary;
    }
  });
})();
