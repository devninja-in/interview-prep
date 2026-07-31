(async function () {
  const res = await fetch("assets/book-data.json");
  const data = await res.json();
  const chapters = data.chapters.filter((c) => c.num);

  const parts = {
    cp: { title: "Competitive Programming", items: [] },
    sd: { title: "System Design", items: [] },
    ai: { title: "AI Engineering", items: [] },
  };

  for (const ch of chapters) {
    if (parts[ch.part]) parts[ch.part].items.push(ch);
  }

  const grid = document.getElementById("toc-grid");
  grid.innerHTML = Object.values(parts)
    .map(
      (part) => `
      <div class="toc-col">
        <h3>${part.title}</h3>
        <ol>
          ${part.items
            .map(
              (ch) => `
            <li>
              <a href="read.html#${ch.id}">
                <span class="num">${ch.num}</span>
                <span>${ch.title}</span>
              </a>
            </li>`
            )
            .join("")}
        </ol>
      </div>`
    )
    .join("");

  const diagramPages = data.pages.filter((p) => p.is_diagram).slice(0, 12);
  const strip = document.getElementById("diagram-strip");
  strip.innerHTML = diagramPages
    .map(
      (p) => `
      <figure class="diagram-card">
        <a href="read.html#p${String(p.page).padStart(3, "0")}">
          <img src="${p.file}" alt="Diagram from page ${p.page}" loading="lazy" />
          <figcaption>Page ${p.page}</figcaption>
        </a>
      </figure>`
    )
    .join("");

  const header = document.getElementById("site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 12);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
