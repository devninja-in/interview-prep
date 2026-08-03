(function () {
  const chapter = document.body.dataset.chapter || "";
  if (!chapter.startsWith("interview-")) return;

  const KEY = "interview-prep-progress-v1";
  const cards = [...document.querySelectorAll("details.qa[id^='q']")];
  if (!cards.length) return;

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "{}");
    } catch {
      return {};
    }
  }

  function save(data) {
    localStorage.setItem(KEY, JSON.stringify(data));
  }

  function doneSet() {
    const all = load();
    return new Set(all[chapter] || []);
  }

  function persist(set) {
    const all = load();
    all[chapter] = [...set];
    save(all);
  }

  const body = document.querySelector(".chapter-body");
  if (!body) return;

  const wrap = document.createElement("div");
  wrap.className = "progress-bar-wrap";
  wrap.innerHTML = `
    <div class="progress-bar" aria-hidden="true"><span></span></div>
    <div class="progress-label" id="lab-progress-label">0 / ${cards.length} practiced</div>
  `;
  body.insertBefore(wrap, body.firstChild);

  const bar = wrap.querySelector(".progress-bar > span");
  const label = wrap.querySelector("#lab-progress-label");

  function render() {
    const done = doneSet();
    cards.forEach((card) => {
      const id = card.id;
      card.classList.toggle("done", done.has(id));
      const btn = card.querySelector("[data-mark-done]");
      if (btn) btn.textContent = done.has(id) ? "Marked practiced ✓" : "Mark as practiced";
    });
    const n = done.size;
    const pct = Math.round((n / cards.length) * 100);
    bar.style.width = `${pct}%`;
    label.textContent = `${n} / ${cards.length} practiced`;
  }

  cards.forEach((card) => {
    const footer = document.createElement("div");
    footer.className = "mark-done";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.dataset.markDone = "1";
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const done = doneSet();
      if (done.has(card.id)) done.delete(card.id);
      else done.add(card.id);
      persist(done);
      render();
    });
    footer.appendChild(btn);
    card.querySelector(".qa-body")?.appendChild(footer);
  });

  render();
})();
