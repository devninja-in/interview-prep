(async function () {
  const res = await fetch("assets/nav.json");
  const data = await res.json();
  const chapters = data.chapters.filter((c) => c.num || c.lab || c.guide);

  const parts = {
    front: { title: "Interview prep guides", items: [] },
    cp: { title: "Competitive Programming", items: [] },
    sd: { title: "System Design", items: [] },
    ai: { title: "AI Engineering", items: [] },
  };

  for (const ch of chapters) {
    if (parts[ch.part]) parts[ch.part].items.push(ch);
  }

  const grid = document.getElementById("toc-grid");
  grid.innerHTML = Object.values(parts)
    .filter((part) => part.items.length)
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
                <span class="num">${ch.lab ? "Lab" : ch.guide ? "Guide" : ch.num}</span>
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
    { file: "load-balancer.svg", href: "chapters/21-scaling.html", label: "Load balancer" },
    { file: "url-shortener-detailed.svg", href: "chapters/28-url-shortener.html", label: "URL shortener" },
    { file: "rag-detailed.svg", href: "chapters/37-rag.html", label: "RAG pipeline" },
    { file: "kafka-partitions.svg", href: "chapters/26-queues.html", label: "Kafka partitions" },
    { file: "uber-matching.svg", href: "chapters/34-uber.html", label: "Uber matching" },
    { file: "feed-hybrid-fanout.svg", href: "chapters/30-instagram.html", label: "Feed fanout" },
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
