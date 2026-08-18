const LOCAL_HOSTS = new Set(["127.0.0.1", "localhost", "::1"]);
const FIXED_ROUTES = Object.freeze({
  "checkout:vulnerable": ["POST", "/vulnerable/checkout"],
  "checkout:secure": ["POST", "/secure/checkout"],
  "invoice:vulnerable": ["GET", "/vulnerable/invoice"],
  "invoice:secure": ["GET", "/secure/invoice"],
  "profile:vulnerable": ["POST", "/vulnerable/profile/update"],
  "profile:secure": ["POST", "/secure/profile/update"]
});

document.querySelectorAll("[data-request-console]").forEach((consoleElement) => {
  const form = consoleElement.querySelector(".console-form");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const status = consoleElement.querySelector("[data-console-status]");
    const trace = consoleElement.querySelector("[data-console-trace]");
    const open = consoleElement.querySelector("[data-console-open]");
    const route = FIXED_ROUTES[`${consoleElement.dataset.scenario}:${consoleElement.dataset.mode}`];
    if (!LOCAL_HOSTS.has(location.hostname) || !route) {
      status.textContent = "blocked: local route only";
      return;
    }

    const [method, path] = route;
    const parameters = new URLSearchParams(new FormData(form));
    const target = method === "GET" ? `${path}?${parameters}` : path;
    status.textContent = "sending";
    open.hidden = true;
    try {
      const response = await fetch(target, {
        method,
        body: method === "POST" ? parameters : undefined,
        headers: method === "POST" ? {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"} : undefined,
        credentials: "same-origin",
        redirect: "follow"
      });
      status.textContent = `HTTP ${response.status}`;
      trace.textContent = response.headers.get("X-Trace-ID") || response.headers.get("Trace-ID") || "xem response";
      const responseUrl = new URL(response.url);
      if (responseUrl.origin === location.origin) {
        open.href = responseUrl.href;
        open.textContent = "Mở response";
        open.hidden = false;
      }
    } catch (error) {
      status.textContent = `error: ${error.message}`;
    }
  });
});
