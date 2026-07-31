(async function () {
  const TOTAL = 212;
  const pageImage = document.getElementById("page-image");
  const pageIndicator = document.getElementById("page-indicator");
  const readerTitle = document.getElementById("reader-title");
  const chapterLabel = document.getElementById("chapter-label");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const tocEl = document.getElementById("toc");
  const search = document.getElementById("search");
  const menuToggle = document.getElementById("menu-toggle");
  const backdrop = document.getElementById("sidebar-backdrop");
  const pageStage = document.getElementById("page-stage");

  const res = await fetch("assets/book-data.json");
  const data = await res.json();
  const chapters = data.chapters;

  let page = 1;

  function chapterForPage(n) {
    return (
      chapters.find((c) => n >= c.start && n <= c.end) || {
        id: "cover",
        title: "Interview Prep",
        num: null,
      }
    );
  }

  function pageSrc(n) {
    return `assets/pages/page-${String(n).padStart(3, "0")}.jpg`;
  }

  function setHash(n, ch) {
    const hash = location.hash.slice(1);
    if (hash && /^p\d{3}$/.test(hash) === false && chapters.some((c) => c.id === hash)) {
      // keep chapter hash until page leaves chapter
      const current = chapters.find((c) => c.id === hash);
      if (current && n >= current.start && n <= current.end) return;
    }
    history.replaceState(null, "", `#p${String(n).padStart(3, "0")}`);
  }

  function go(n, { pushChapter } = {}) {
    page = Math.max(1, Math.min(TOTAL, n));
    const ch = chapterForPage(page);
    const frame = pageImage.closest(".page-frame");
    frame.style.animation = "none";
    // restart animation
    void frame.offsetWidth;
    frame.style.animation = "";

    pageImage.src = pageSrc(page);
    pageImage.alt = `${ch.title} — page ${page}`;
    pageIndicator.textContent = `${page} / ${TOTAL}`;
    readerTitle.textContent = ch.num ? `${ch.num} · ${ch.title}` : ch.title;
    chapterLabel.textContent = ch.num ? `Chapter ${ch.num}` : ch.title;
    prevBtn.disabled = page <= 1;
    nextBtn.disabled = page >= TOTAL;

    document.querySelectorAll(".toc-item").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.id === ch.id);
    });

    if (pushChapter) {
      history.replaceState(null, "", `#${ch.id}`);
    } else {
      setHash(page, ch);
    }

    localStorage.setItem("interview-prep-page", String(page));
    pageStage.scrollTop = 0;
  }

  function renderToc(filter = "") {
    const q = filter.trim().toLowerCase();
    const groups = [
      { key: "front", title: "Front matter" },
      { key: "cp", title: "Competitive Programming" },
      { key: "sd", title: "System Design" },
      { key: "ai", title: "AI Engineering" },
    ];

    tocEl.innerHTML = groups
      .map((g) => {
        const items = chapters.filter((c) => {
          if (c.part !== g.key) return false;
          if (!q) return true;
          return (
            c.title.toLowerCase().includes(q) ||
            (c.num && c.num.includes(q)) ||
            c.id.includes(q)
          );
        });
        if (!items.length) return "";
        return `
          <div class="toc-group">
            <div class="toc-group-title">${g.title}</div>
            ${items
              .map(
                (c) => `
              <button class="toc-item" type="button" data-id="${c.id}" data-start="${c.start}">
                ${c.num ? `<span class="num">${c.num}</span>` : ""}
                ${c.title}
              </button>`
              )
              .join("")}
          </div>`;
      })
      .join("");

    tocEl.querySelectorAll(".toc-item").forEach((btn) => {
      btn.addEventListener("click", () => {
        go(Number(btn.dataset.start), { pushChapter: true });
        closeSidebar();
      });
    });
  }

  function parseHash() {
    const raw = decodeURIComponent(location.hash.slice(1) || "");
    if (!raw) {
      const saved = Number(localStorage.getItem("interview-prep-page") || "1");
      return Number.isFinite(saved) ? saved : 1;
    }
    if (/^p\d{1,3}$/i.test(raw)) {
      return Number(raw.slice(1));
    }
    const ch = chapters.find((c) => c.id === raw);
    if (ch) return ch.start;
    return 1;
  }

  function openSidebar() {
    document.body.classList.add("sidebar-open");
    backdrop.hidden = false;
  }

  function closeSidebar() {
    document.body.classList.remove("sidebar-open");
    backdrop.hidden = true;
  }

  renderToc();
  go(parseHash());

  prevBtn.addEventListener("click", () => go(page - 1));
  nextBtn.addEventListener("click", () => go(page + 1));
  search.addEventListener("input", () => renderToc(search.value));
  menuToggle.addEventListener("click", openSidebar);
  backdrop.addEventListener("click", closeSidebar);

  window.addEventListener("hashchange", () => go(parseHash()));

  window.addEventListener("keydown", (e) => {
    if (e.target.matches("input, textarea")) return;
    if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === "j") {
      e.preventDefault();
      go(page + 1);
    } else if (e.key === "ArrowLeft" || e.key === "PageUp" || e.key === "k") {
      e.preventDefault();
      go(page - 1);
    } else if (e.key === "Escape") {
      closeSidebar();
    }
  });

  // Prefetch neighbors
  pageImage.addEventListener("load", () => {
    [page - 1, page + 1].forEach((n) => {
      if (n >= 1 && n <= TOTAL) {
        const img = new Image();
        img.src = pageSrc(n);
      }
    });
  });
})();
