(async function () {
  const res = await fetch("assets/nav.json");
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
              <a href="${ch.href}">
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

  const strip = document.getElementById("diagram-strip");
  const diagramFiles = [
    "diagram-p008.jpg",
    "diagram-p140.jpg",
    "diagram-p161.jpg",
    "diagram-p165.jpg",
    "diagram-p195.jpg",
    "diagram-p205.jpg",
  ];
  strip.innerHTML = diagramFiles
    .map(
      (f, i) => `
      <figure class="diagram-card">
        <a href="chapters/00-how-to-use.html">
          <img src="assets/diagrams/${f}" alt="Book diagram ${i + 1}" loading="lazy" />
          <figcaption>Diagram</figcaption>
        </a>
      </figure>`
    )
    .join("");

  const header = document.getElementById("site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 12);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
