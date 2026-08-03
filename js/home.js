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
  const featured = [
    { file: "hash-map.svg", href: "chapters/03-arrays.html", label: "Hash map" },
    { file: "load-balancer.svg", href: "chapters/21-scaling.html", label: "Load balancer" },
    { file: "url-shortener.svg", href: "chapters/28-url-shortener.html", label: "URL shortener" },
    { file: "rag.svg", href: "chapters/37-rag.html", label: "RAG" },
    { file: "agent-loop.svg", href: "chapters/39-agents.html", label: "Agent loop" },
    { file: "mcp.svg", href: "chapters/40-mcp.html", label: "MCP" },
  ];
  strip.innerHTML = featured
    .map(
      (d) => `
      <figure class="diagram-card">
        <a href="${d.href}">
          <img src="assets/diagrams/${d.file}" alt="${d.label}" loading="lazy" />
          <figcaption>${d.label}</figcaption>
        </a>
      </figure>`
    )
    .join("");

  const header = document.getElementById("site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 12);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
