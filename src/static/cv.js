document.addEventListener("DOMContentLoaded", async () => {
  // Set current year in footer
  document.getElementById("cv-year").textContent = new Date().getFullYear();

  try {
    const response = await fetch("/cv");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const cv = await response.json();

    renderPersonal(cv.personal);
    renderExperience(cv.experience);
    renderEducation(cv.education);
    renderSkills(cv.skills);
    renderCertifications(cv.certifications);
    renderLanguages(cv.languages);
  } catch (err) {
    console.error("Failed to load CV data:", err);
    document.querySelector(".cv-layout").innerHTML =
      '<p class="load-error">Could not load CV data. Please try again later.</p>';
  }
});

// ── Helper: create an element with text content and optional class ─────────────
function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

// ── Personal info ──────────────────────────────────────────────────────────────
function renderPersonal(p) {
  document.title = `CV – ${p.name}`;
  document.getElementById("cv-name").textContent = p.name;
  document.getElementById("cv-title").textContent = p.title;
  document.getElementById("cv-location").textContent = `📍 ${p.location}`;
  document.getElementById("cv-summary").textContent = p.summary;

  const links = [
    { icon: "✉", label: p.email, href: `mailto:${p.email}` },
    { icon: "📞", label: p.phone, href: `tel:${p.phone}` },
    { icon: "🔗", label: p.linkedin, href: `https://${p.linkedin}` },
    { icon: "🐙", label: p.github, href: `https://${p.github}` },
  ];

  const ul = document.getElementById("cv-contact");
  links.forEach(({ icon, label, href }) => {
    const li = document.createElement("li");
    const iconSpan = el("span", icon, "contact-icon");
    const a = document.createElement("a");
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = label;
    li.appendChild(iconSpan);
    li.appendChild(a);
    ul.appendChild(li);
  });
}

// ── Work experience ────────────────────────────────────────────────────────────
function renderExperience(jobs) {
  const container = document.getElementById("cv-experience");
  jobs.forEach((job) => {
    const article = document.createElement("article");
    article.className = "timeline-item";

    const header = document.createElement("div");
    header.className = "timeline-header";
    header.appendChild(el("h3", job.role, "timeline-role"));
    header.appendChild(el("span", job.period, "timeline-period"));
    article.appendChild(header);

    const org = document.createElement("p");
    org.className = "timeline-org";
    org.appendChild(document.createTextNode(`${job.company} — `));
    org.appendChild(el("em", job.location));
    article.appendChild(org);

    const ul = document.createElement("ul");
    ul.className = "timeline-highlights";
    job.highlights.forEach((h) => ul.appendChild(el("li", h)));
    article.appendChild(ul);

    container.appendChild(article);
  });
}

// ── Education ─────────────────────────────────────────────────────────────────
function renderEducation(entries) {
  const container = document.getElementById("cv-education");
  entries.forEach((edu) => {
    const article = document.createElement("article");
    article.className = "timeline-item";

    const header = document.createElement("div");
    header.className = "timeline-header";
    header.appendChild(el("h3", edu.degree, "timeline-role"));
    header.appendChild(el("span", edu.period, "timeline-period"));
    article.appendChild(header);

    article.appendChild(el("p", edu.institution, "timeline-org"));
    const details = document.createElement("p");
    details.className = "timeline-details";
    details.appendChild(el("em", edu.details));
    article.appendChild(details);

    container.appendChild(article);
  });
}

// ── Skills ────────────────────────────────────────────────────────────────────
function renderSkills(skillGroups) {
  const container = document.getElementById("cv-skills");
  Object.entries(skillGroups).forEach(([category, items]) => {
    const div = document.createElement("div");
    div.className = "skill-group";
    div.appendChild(el("h4", category, "skill-category"));

    const ul = document.createElement("ul");
    ul.className = "skill-list";
    items.forEach((s) => ul.appendChild(el("li", s, "skill-tag")));
    div.appendChild(ul);

    container.appendChild(div);
  });
}

// ── Certifications ────────────────────────────────────────────────────────────
function renderCertifications(certs) {
  const ul = document.getElementById("cv-certifications");
  certs.forEach((cert) => {
    const li = document.createElement("li");
    li.className = "cert-item";
    li.appendChild(el("strong", cert.name));
    li.appendChild(document.createElement("br"));
    li.appendChild(el("span", `${cert.issuer}, ${cert.year}`));
    ul.appendChild(li);
  });
}

// ── Languages ─────────────────────────────────────────────────────────────────
function renderLanguages(langs) {
  const ul = document.getElementById("cv-languages");
  langs.forEach(({ language, level }) => {
    const li = document.createElement("li");
    li.className = "lang-item";
    li.appendChild(el("span", language, "lang-name"));
    li.appendChild(el("span", level, "lang-level"));
    ul.appendChild(li);
  });
}

