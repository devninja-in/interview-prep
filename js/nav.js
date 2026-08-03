(async function () {
  const res = await fetch("../assets/nav.json");
  const data = await res.json();
  const chapters = data.chapters;
  const current = document.body.dataset.chapter;
  const sidebar = document.getElementById("sidebar");
  const pager = document.getElementById("chapter-pager");
  const menuToggle = document.getElementById("menu-toggle");
  const backdrop = document.getElementById("sidebar-backdrop");

  const groups = [
    { key: "front", title: "Front matter" },
    { key: "cp", title: "Competitive Programming" },
    { key: "sd", title: "System Design" },
    { key: "ai", title: "AI Engineering" },
  ];

  sidebar.innerHTML = `
    <a class="brand" href="../">Interview Prep <span>DevNinja</span></a>
    ${groups
      .map((g) => {
        const items = chapters.filter((c) => c.part === g.key);
        if (!items.length) return "";
        return `
          <div class="toc-group">
            <div class="toc-group-title">${g.title}</div>
            ${items
              .map(
                (c) => `
              <a class="toc-item${c.id === current ? " active" : ""}" href="./${c.id}.html">
                ${
                  c.lab
                    ? `<span class="num">Lab</span>`
                    : c.guide
                      ? `<span class="num guide">Guide</span>`
                      : c.num
                        ? `<span class="num">${c.num}</span>`
                        : ""
                }
                ${c.title}
              </a>`
              )
              .join("")}
          </div>`;
      })
      .join("")}
  `;

  const idx = chapters.findIndex((c) => c.id === current);
  const prev = idx > 0 ? chapters[idx - 1] : null;
  const next = idx >= 0 && idx < chapters.length - 1 ? chapters[idx + 1] : null;

  pager.innerHTML = `
    ${
      prev
        ? `<a class="prev" href="./${prev.id}.html"><span class="dir">Previous</span><span>${
            prev.num ? prev.num + " · " : ""
          }${prev.title}</span></a>`
        : "<span></span>"
    }
    ${
      next
        ? `<a class="next" href="./${next.id}.html"><span class="dir">Next</span><span>${
            next.num ? next.num + " · " : ""
          }${next.title}</span></a>`
        : ""
    }
  `;

  function openSidebar() {
    document.body.classList.add("sidebar-open");
    backdrop.hidden = false;
  }
  function closeSidebar() {
    document.body.classList.remove("sidebar-open");
    backdrop.hidden = true;
  }

  menuToggle?.addEventListener("click", openSidebar);
  backdrop?.addEventListener("click", closeSidebar);
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeSidebar();
    if (e.target.matches?.("input, textarea")) return;
    if (e.key === "ArrowRight" && next) location.href = `./${next.id}.html`;
    if (e.key === "ArrowLeft" && prev) location.href = `./${prev.id}.html`;
  });

  localStorage.setItem("interview-prep-chapter", current || "");
})();
