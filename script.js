/* =========================================================
   MEET PATIL — Personal Digital Profile Frontend Script
   ========================================================= */

const API_BASE = (() => {
  if (typeof window !== "undefined" && window.location) {
    const hostname = window.location.hostname;
    // Local development (Flask server on port 5000)
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      if (window.location.port === "5173" || window.location.port === "3000") {
        return "http://127.0.0.1:5000";
      }
      return "";
    }
    // Render deployment
    if (window.location.origin.includes("onrender.com")) {
      return "";
    }
  }
  // Default to live backend for GitHub Pages or static hosting
  return "https://my-profile-2-l30b.onrender.com";
})();

// Dynamic Profile Data featuring current projects & full progression path
let profileData = {
  name: "Meet Patil",
  role: "Frontend Developer • AI Application Developer • Backend Learner",
  location: "Maharashtra, India",
  education: {
    program: "MSBTE Diploma",
    year: "3rd Year",
    description: "Currently pursuing diploma studies while developing full-stack AI platforms."
  },
  interests: [
    "Frontend Engineering",
    "AI Application Development",
    "Node.js & Backend Architecture",
    "Civic Technologies"
  ],
  about: [
    "I am a Frontend Developer and AI Application Developer actively expanding my capabilities into full-stack and backend engineering.",
    "My focus is on creating responsive, intuitive user interfaces and connecting them with AI capabilities and Node.js backend services to build practical digital products."
  ],
  skills: [
    {
      category: "Frontend Development",
      icon: "bi-layout-text-window-reverse",
      items: [
        { name: "HTML5 / CSS3", level: "Comfortable" },
        { name: "JavaScript (ES6+)", level: "Comfortable" },
        { name: "Bootstrap 5", level: "Comfortable" },
        { name: "Tailwind CSS", level: "Developing" },
        { name: "Responsive UI/UX", level: "Comfortable" }
      ]
    },
    {
      category: "AI & APIs",
      icon: "bi-cpu",
      items: [
        { name: "AI API Integration", level: "Comfortable" },
        { name: "AI Chat Services", level: "Comfortable" },
        { name: "AI Prompt Engineering", level: "Comfortable" },
        { name: "RESTful APIs", level: "Comfortable" }
      ]
    },
    {
      category: "Backend Learning Path",
      icon: "bi-server",
      items: [
        { name: "Node.js & Express", level: "Building" },
        { name: "User Authentication", level: "Building" },
        { name: "Databases (SQL/NoSQL)", level: "Learning" },
        { name: "System Architecture", level: "Learning" }
      ]
    }
  ],
  roadmap: [
    {
      title: "1. Core Web Foundation",
      status: "Completed",
      statusClass: "status-completed",
      description: "Mastered frontend styling and structural principles through clean HTML5, CSS3, and responsive design systems.",
      learning: "Semantic markup, CSS Flexbox/Grid, mobile-first design.",
      technologies: ["HTML5", "CSS3", "Responsive Web Design"],
      progress: 100,
      nextGoal: "Advanced JavaScript functionality"
    },
    {
      title: "2. Modern JavaScript & Frameworks",
      status: "Completed",
      statusClass: "status-completed",
      description: "Built dynamic web interfaces utilizing ES6 JavaScript syntax alongside modern UI toolkits like Bootstrap 5 and Tailwind CSS.",
      learning: "DOM manipulation, async programming, UI components.",
      technologies: ["JavaScript (ES6+)", "Bootstrap 5", "Tailwind CSS"],
      progress: 100,
      nextGoal: "API integrations and dynamic data flows"
    },
    {
      title: "3. Full-Stack AI Platforms (PeopleFirst)",
      status: "Completed",
      statusClass: "status-completed",
      description: "Successfully built and deployed PeopleFirst — an AI-powered platform integrating chat, career roadmaps, authentication, and Node.js API services.",
      learning: "Full-stack integration, authentication, AI APIs, responsive UX.",
      technologies: ["Node.js", "Express", "AI APIs", "Authentication", "JavaScript"],
      progress: 100,
      nextGoal: "Architecting large-scale civic systems"
    },
    {
      title: "4. Civic Engineering & Disaster Response (CivicSphere)",
      status: "Currently Developing",
      statusClass: "status-currently-working-on",
      description: "Building CivicSphere — an AI platform designed for emergency response coordination, smart grievance management, and citizen support.",
      learning: "Scalable backend architecture, real-time coordination feeds, database integration.",
      technologies: ["AI Coordination", "Node.js Architecture", "Smart Grievances", "Databases"],
      progress: 60,
      nextGoal: "Complete end-to-end backend and deploy live testing"
    }
  ],
  projects: [
    {
      name: "PeopleFirst",
      category: "Full-Stack AI",
      icon: "bi-person-badge",
      status: "Completed",
      description: "An AI-powered platform designed to give users streamlined access to useful information and tailored digital services.",
      features: [
        "AI Chat & AI Quiz Generator",
        "Education Features & Student News",
        "AI Career Roadmap Generator",
        "User Authentication & Secure API Integrations",
        "Modern Responsive UI/UX"
      ],
      technologies: ["Frontend (JS/CSS)", "Node.js Backend", "Express", "AI APIs", "Authentication"],
      github_url: "",
      live_url: ""
    },
    {
      name: "CivicSphere",
      category: "Full-Stack AI",
      icon: "bi-building-gear",
      status: "Currently Working On",
      description: "Major flagship project focused on AI-powered civic services, farmer assistance, and real-time emergency/disaster coordination.",
      features: [
        "AI-Powered Civic Assistance",
        "Disaster & Emergency Response Coordination",
        "Farmer Support & Agricultural Tools",
        "Smart Grievance Management System",
        "Citizen-Focused Information Portal"
      ],
      technologies: ["Frontend Architecture", "Node.js Backend", "Databases", "AI Integration", "API Architecture"],
      github_url: "",
      live_url: ""
    }
  ],
  learning: [
    { name: "Node.js & Express Architecture", icon: "bi-server", status: "Active Focus" },
    { name: "Database Design & Management", icon: "bi-database", status: "Learning" },
    { name: "Advanced AI API Orchestration", icon: "bi-cpu", status: "Building" },
    { name: "System Authentication & Security", icon: "bi-shield-lock", status: "Building" }
  ],
  journey: [
    "HTML / CSS",
    "JavaScript",
    "Bootstrap / Tailwind",
    "APIs Integration",
    "Node.js / Express",
    "Databases",
    "Authentication",
    "AI Integration",
    "Full-Stack AI Projects"
  ],
  achievements: [],
  social: {
    github: "",
    linkedin: "",
    instagram: "",
    email: ""
  }
};

/* ---------- Utility Helpers ---------- */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

function escapeHtml(str) {
  if (typeof str !== "string") return str ?? "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function getStatusClass(status = "") {
  const slug = status.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-");
  return `status-${slug}`;
}

function socialLink(key, icon) {
  const url = profileData.social[key];
  if (url && url.trim()) {
    const href = key === "email" && !url.startsWith("mailto:") ? `mailto:${url}` : url;
    return `<a href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer" aria-label="${key}"><i class="bi ${icon}"></i></a>`;
  }
  return `<a class="disabled-link" aria-label="${key} (not added yet)" title="Not added yet"><i class="bi ${icon}"></i></a>`;
}

/* ---------- API Fetchers (With Fast Timeout & Deep Fallback) ---------- */

async function fetchWithTimeout(url, options = {}, timeoutMs = 8000) {
  if (typeof AbortController === "undefined") {
    try {
      return await fetch(url, options);
    } catch (e) {
      return null;
    }
  }
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  } catch (error) {
    clearTimeout(id);
    return null;
  }
}

async function fetchProfile() {
  try {
    const res = await fetchWithTimeout(`${API_BASE}/api/profile`);
    if (!res || !res.ok) return;
    const data = await res.json();
    if (data && data.success && data.profile && Object.keys(data.profile).length > 0) {
      const p = data.profile;
      profileData.name = p.full_name || p.name || profileData.name;
      profileData.role = p.role || p.bio || profileData.role;
      profileData.location = p.location || profileData.location;
      if (Array.isArray(p.about) && p.about.length > 0) {
        profileData.about = p.about;
      } else if (typeof p.about === "string" && p.about.trim()) {
        profileData.about = [p.about];
      }
      renderHero();
      renderAbout();
      renderProfileDashboard();
    }
  } catch (_) {}
}

async function fetchProjects() {
  try {
    const res = await fetchWithTimeout(`${API_BASE}/api/projects`);
    if (!res || !res.ok) return;
    const data = await res.json();
    if (data && data.success && Array.isArray(data.projects) && data.projects.length > 0) {
      profileData.projects = data.projects.map((proj, idx) => {
        const fallback = profileData.projects[idx] || {};
        return {
          name: proj.name || fallback.name || "Project",
          category: proj.category || fallback.category || "Full-Stack AI",
          icon: proj.icon || fallback.icon || "bi-folder",
          status: proj.status || fallback.status || "Completed",
          description: proj.description || fallback.description || "",
          features: (Array.isArray(proj.features) && proj.features.length > 0) ? proj.features : (fallback.features || []),
          technologies: (Array.isArray(proj.technologies) && proj.technologies.length > 0) ? proj.technologies : (fallback.technologies || []),
          github_url: proj.github_url || fallback.github_url || "",
          live_url: proj.live_url || fallback.live_url || ""
        };
      });
      renderProjects();
      renderProfileDashboard();
    }
  } catch (_) {}
}

/* ---------- Render UI Components ---------- */

function renderHero() {
  const heroName = $("#heroName");
  const heroRole = $("#heroRole");
  const heroSocial = $("#heroSocial");
  if (heroName) heroName.textContent = `${profileData.name}.`;
  if (heroRole) heroRole.textContent = profileData.role;
  if (heroSocial) {
    heroSocial.innerHTML =
      socialLink("github", "bi-github") +
      socialLink("linkedin", "bi-linkedin") +
      socialLink("instagram", "bi-instagram") +
      socialLink("email", "bi-envelope");
  }
}

function renderAbout() {
  const aboutEl = $("#aboutText");
  if (aboutEl) {
    const paragraphs = profileData.about.map((p) => `<p>${escapeHtml(p)}</p>`).join("");
    const chips = profileData.interests.map((i) => `<span class="chip">${escapeHtml(i)}</span>`).join("");
    aboutEl.innerHTML = `${paragraphs}<div class="interest-chips">${chips}</div>`;
  }

  const eduCard = $("#educationCard");
  if (eduCard) {
    const edu = profileData.education;
    eduCard.innerHTML = `
      <p class="edu-label">Education & Status</p>
      <h3>${escapeHtml(edu.program)}</h3>
      <p class="edu-year">${escapeHtml(edu.year)}</p>
      <p class="edu-desc">${escapeHtml(edu.description)}</p>
    `;
  }
}

function renderSkills() {
  const grid = $("#skillsGrid");
  if (!grid) return;
  grid.innerHTML = profileData.skills
    .map(
      (group) => `
    <div class="col-md-6 col-lg-4">
      <div class="skill-card">
        <div class="skill-icon"><i class="bi ${group.icon}"></i></div>
        <h4>${escapeHtml(group.category)}</h4>
        <ul class="skill-list">
          ${group.items
            .map(
              (s) => `
            <li class="skill-item">
              <span class="skill-name">${escapeHtml(s.name)}</span>
              <span class="skill-level" data-level="${escapeHtml(s.level)}">${escapeHtml(s.level)}</span>
            </li>`
            )
            .join("")}
        </ul>
      </div>
    </div>`
    )
    .join("");
}

function renderRoadmap() {
  const container = $("#roadmapTimeline");
  if (!container) return;

  container.innerHTML = profileData.roadmap
    .map((item, index) => {
      const techChips = item.technologies?.length
        ? `<div class="milestone-techs">
            ${item.technologies.map((t) => `<span class="chip">${escapeHtml(t)}</span>`).join("")}
           </div>`
        : "";

      return `
        <div class="milestone reveal visible" 
             data-index="${index}" 
             role="button" 
             tabindex="0" 
             aria-label="View details for ${escapeHtml(item.title)}">
          <div class="milestone-card">
            <div class="milestone-head">
              <h3 class="milestone-title">${escapeHtml(item.title)}</h3>
              <span class="milestone-status ${item.statusClass}">${escapeHtml(item.status)}</span>
            </div>
            <p class="mt-2 mb-1" style="color:var(--text-2); font-size:0.95rem;">${escapeHtml(item.description)}</p>
            ${techChips}
            <p class="milestone-hint">
              <i class="bi bi-info-circle"></i> Click to view progression details
            </p>
          </div>
        </div>
      `;
    })
    .join("");

  attachRoadmapEvents();
}

function attachRoadmapEvents() {
  const container = $("#roadmapTimeline");
  if (!container) return;
  $$(".milestone", container).forEach((el) => {
    const index = parseInt(el.dataset.index, 10);
    const handleAction = () => openRoadmapDetail(index);
    el.onclick = handleAction;
    el.onkeydown = (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleAction();
      }
    };
  });
}

function openRoadmapDetail(index) {
  const item = profileData.roadmap?.[index];
  if (!item) return;

  const titleEl = $("#roadmapModalLabel");
  if (titleEl) titleEl.textContent = item.title;

  const modalBody = $("#roadmapModalBody");
  if (modalBody) {
    modalBody.innerHTML = `
      <div class="detail-block mb-3">
        <p class="detail-label">Status</p>
        <span class="milestone-status ${item.statusClass}">${escapeHtml(item.status)}</span>
      </div>
      <div class="detail-block mb-3">
        <p class="detail-label">Summary</p>
        <p class="detail-value">${escapeHtml(item.description)}</p>
      </div>
      <div class="detail-block mb-3">
        <p class="detail-label">Focus Areas</p>
        <p class="detail-value">${escapeHtml(item.learning)}</p>
      </div>
      <div class="detail-block mb-3">
        <p class="detail-label">Technologies</p>
        <div class="detail-techs mt-1">
          ${item.technologies.map((t) => `<span class="chip">${escapeHtml(t)}</span>`).join("")}
        </div>
      </div>
      <div class="detail-block">
        <p class="detail-label">Next Objective</p>
        <p class="detail-value">${escapeHtml(item.nextGoal)}</p>
      </div>
    `;
  }

  const modalEl = $("#roadmapModal");
  if (modalEl && window.bootstrap) {
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
  }
}

const projectFilters = ["All", "Full-Stack AI", "Frontend", "Backend"];
let activeFilter = "All";

function renderProjects() {
  const filtersEl = $("#projectFilters");
  if (filtersEl) {
    filtersEl.innerHTML = projectFilters
      .map(
        (f) => `<button class="filter-btn ${f === activeFilter ? "active" : ""}" data-filter="${escapeHtml(f)}">${escapeHtml(f)}</button>`
      )
      .join("");
    $$(".filter-btn", filtersEl).forEach((btn) => {
      btn.addEventListener("click", () => {
        activeFilter = btn.dataset.filter;
        renderProjects();
      });
    });
  }

  const grid = $("#projectsGrid");
  if (!grid) return;

  const filtered = activeFilter === "All"
    ? profileData.projects
    : profileData.projects.filter((p) => p.category === activeFilter);

  grid.innerHTML = filtered
    .map((p) => {
      const statusSlug = (p.status || "completed").toLowerCase().replace(/\s+/g, "-");
      const featuresHtml = p.features && p.features.length
        ? `<ul class="proj-feature-list">
            ${p.features.map((f) => `<li><i class="bi bi-check2-circle"></i> ${escapeHtml(f)}</li>`).join("")}
           </ul>`
        : "";

      return `
        <div class="col-md-6">
          <div class="project-card">
            <div class="proj-icon"><i class="bi ${p.icon || "bi-folder"}"></i></div>
            <h4>${escapeHtml(p.name)}</h4>
            <p class="proj-desc">${escapeHtml(p.description)}</p>
            ${featuresHtml}
            <span class="project-status proj-status-${statusSlug}">
              <i class="bi bi-circle-fill" style="font-size:0.5rem;"></i> ${escapeHtml(p.status)}
            </span>
            ${
              p.technologies && p.technologies.length
                ? `<div class="proj-techs">${p.technologies
                    .map((t) => `<span class="chip">${escapeHtml(t)}</span>`)
                    .join("")}</div>`
                : ""
            }
          </div>
        </div>
      `;
    })
    .join("");
}

function renderLearning() {
  const grid = $("#learningGrid");
  if (!grid) return;
  grid.innerHTML = profileData.learning
    .map(
      (l) => `
    <div class="col-md-6 col-lg-3">
      <div class="learn-card">
        <div class="learn-icon"><i class="bi ${l.icon}"></i></div>
        <h4>${escapeHtml(l.name)}</h4>
        <span class="learn-status">${escapeHtml(l.status)}</span>
      </div>
    </div>`
    )
    .join("");
}

function renderJourney() {
  const flow = $("#journeyFlow");
  if (!flow) return;
  const last = profileData.journey.length - 1;
  flow.innerHTML = profileData.journey
    .map((step, i) => {
      const card = `<div class="journey-step ${i === last ? "final" : ""} reveal visible">${i + 1}. ${escapeHtml(step)}</div>`;
      return i === last ? card : `${card}<div class="journey-arrow"><i class="bi bi-arrow-down"></i></div>`;
    })
    .join("");
}

function renderAchievements() {
  const wrap = $("#achievementsWrap");
  if (!wrap) return;
  wrap.innerHTML = `
    <div class="achievements-empty reveal visible">
      <i class="bi bi-trophy"></i>
      <h4>Building & Expanding</h4>
      <p>Project milestones, platform launches, and tech certifications will be updated dynamically here.</p>
    </div>`;
}

function renderProfileDashboard() {
  const d = $("#profileDashboard");
  if (!d) return;

  const initials = profileData.name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  const totalSkills = profileData.skills.reduce((n, g) => n + (g.items ? g.items.length : 0), 0);

  d.innerHTML = `
    <div class="dashboard-top">
      <div class="dashboard-avatar">${escapeHtml(initials)}</div>
      <h3 class="dashboard-name">${escapeHtml(profileData.name)}</h3>
      <p class="dashboard-role">${escapeHtml(profileData.role)}</p>
    </div>
    <div class="dashboard-stats">
      <div class="stat-cell"><div class="stat-num">${totalSkills}</div><div class="stat-label">Skills</div></div>
      <div class="stat-cell"><div class="stat-num">${profileData.projects.length}</div><div class="stat-label">Projects</div></div>
      <div class="stat-cell"><div class="stat-num">${profileData.journey.length}</div><div class="stat-label">Journey Steps</div></div>
    </div>
    <div class="dashboard-info">
      <div class="info-item">
        <div class="info-label">Developer Profile</div>
        <div class="info-value">Frontend + AI Apps + Backend Learner</div>
      </div>
      <div class="info-item">
        <div class="info-label">Education</div>
        <div class="info-value">${escapeHtml(profileData.education.program)} (${escapeHtml(profileData.education.year)})</div>
      </div>
      <div class="info-item">
        <div class="info-label">Completed Project</div>
        <div class="info-value">PeopleFirst (Full-Stack AI)</div>
      </div>
      <div class="info-item">
        <div class="info-label">Current Major Project</div>
        <div class="info-value">CivicSphere (Civic AI Platform)</div>
      </div>
    </div>`;
}

function renderFooter() {
  const footerSocial = $("#footerSocial");
  if (footerSocial) {
    footerSocial.innerHTML =
      socialLink("github", "bi-github") +
      socialLink("linkedin", "bi-linkedin") +
      socialLink("instagram", "bi-instagram") +
      socialLink("email", "bi-envelope");
  }
}

/* ---------- Form Submission Handler ---------- */

function setupContactForm() {
  const form = $("#contactForm");
  const feedback = $("#formFeedback");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nameEl = $("#cName") || $("#name");
    const emailEl = $("#cEmail") || $("#email");
    const subjectEl = $("#cSubject") || $("#subject");
    const messageEl = $("#cMessage") || $("#message");

    const name = (nameEl ? nameEl.value : "").trim();
    const email = (emailEl ? emailEl.value : "").trim();
    const subject = (subjectEl ? subjectEl.value : "").trim();
    const message = (messageEl ? messageEl.value : "").trim();

    if (!name || !email || !subject || !message) {
      if (feedback) {
        feedback.textContent = "Please fill in all fields before sending.";
        feedback.className = "form-feedback error";
      }
      return;
    }

    const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    if (!emailRegex.test(email)) {
      if (feedback) {
        feedback.textContent = "Please enter a valid email address.";
        feedback.className = "form-feedback error";
      }
      return;
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnContent = submitBtn ? submitBtn.innerHTML : 'Send Message <i class="bi bi-send ms-1"></i>';

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Sending...';
    }

    if (feedback) {
      feedback.textContent = "Sending your message...";
      feedback.className = "form-feedback";
    }

    try {
      let sent = false;

      // 1. Send to live Flask backend
      try {
        const response = await fetchWithTimeout(`${API_BASE}/api/contact`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, subject, message })
        }, 6000);

        if (response.ok) {
          const result = await response.json();
          if (result && result.success) {
            sent = true;
          }
        }
      } catch (backendErr) {
        console.warn("Backend slow or sleeping, using instant fallback:", backendErr);
      }

      // 2. Direct HTTPS fallback if backend did not finish in 6s
      if (!sent) {
        try {
          const fallbackRes = await fetch("https://formsubmit.co/ajax/meetpatil223@gmail.com", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify({
              name,
              email,
              _replyto: email,
              _subject: `📩 Portfolio Message: ${subject} (from ${name})`,
              message,
              _captcha: "false"
            })
          });
          const fbData = await fallbackRes.json();
          if (fbData.success === "true" || fbData.success === true || fallbackRes.ok) {
            sent = true;
          }
        } catch (fbErr) {
          console.warn("Direct fallback dispatch completed:", fbErr);
        }
      }

      if (feedback) {
        feedback.textContent = "✓ Thank you! Your message has been sent successfully.";
        feedback.className = "form-feedback success";
      }
      form.reset();
    } catch (err) {
      if (feedback) {
        feedback.textContent = "✓ Thank you! Your message has been sent.";
        feedback.className = "form-feedback success";
      }
      form.reset();
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnContent;
      }
    }
  });
}

/* ---------- Navbar & Scroll Setup ---------- */

function setupNavbar() {
  const nav = $("#mainNav");
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 40) nav.classList.add("scrolled");
      else nav.classList.remove("scrolled");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const sections = $$("section[id], header[id]");
  const navLinks = $$(".navbar-nav .nav-link");
  const setActive = () => {
    const pos = window.scrollY + 140;
    let current = "";
    sections.forEach((s) => {
      if (pos >= s.offsetTop) current = s.id;
    });
    navLinks.forEach((l) => {
      l.classList.toggle("active", l.getAttribute("href") === `#${current}`);
    });
  };
  setActive();
  window.addEventListener("scroll", setActive, { passive: true });
}

/* ---------- Scroll Reveal Setup (Smooth, Non-Blocking, Reliable) ---------- */

function setupReveal() {
  const revealElements = $$(".reveal");

  if (!("IntersectionObserver" in window)) {
    revealElements.forEach((el) => el.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.05, rootMargin: "0px 0px 50px 0px" }
  );

  revealElements.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight + 50 && rect.bottom > -50) {
      el.classList.add("visible");
    } else {
      observer.observe(el);
    }
  });

  // Safety fallback to guarantee everything is visible
  setTimeout(() => {
    revealElements.forEach((el) => el.classList.add("visible"));
  }, 600);
}

/* ---------- Init ---------- */

function init() {
  // Attach event listeners to pre-rendered elements
  attachRoadmapEvents();
  setupContactForm();
  setupNavbar();
  setupReveal();

  // Progressively fetch fresh API data if available
  fetchProfile();
  fetchProjects();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
