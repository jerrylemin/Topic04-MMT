(() => {
  const flows = {
    vulnerable: [
      ["User Input", "untrusted value"], ["Python String", "request value"], ["String Concatenation", "SQL text", "risk"],
      ["Final SQL Text", "structure may change", "risk"], ["SQLite Parser", "parses changed text"], ["Unexpected Result", "error or extra rows", "risk"]
    ],
    secure: [
      ["User Input", "untrusted value"], ["Python Value", "validated length"], ["SQL Template", "placeholder ?"],
      ["Parameter Binding", "driver separates value"], ["SQLite Parser", "structure preserved"], ["Expected Result", "bounded rows"]
    ]
  };
  document.querySelectorAll("[data-query-visualizer]").forEach((root) => {
    const mode = root.dataset.mode === "vulnerable" ? "vulnerable" : "secure";
    flows[mode].forEach(([title, detail, state]) => {
      const node = document.createElement("div");
      node.className = `flow-node${state ? ` is-${state}` : ""}`;
      const heading = document.createElement("b");
      const copy = document.createElement("span");
      heading.textContent = title;
      copy.textContent = detail;
      node.append(heading, copy);
      root.append(node);
    });
  });
})();
