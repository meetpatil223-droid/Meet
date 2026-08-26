// Live API Endpoint Configuration
const API_BASE = "https://my-profile-2-l30b.onrender.com/api";

document.addEventListener("DOMContentLoaded", () => {
  fetchProfile();
  fetchSkills();
  fetchProjects();
  fetchRoadmap();
  fetchLearning();
  fetchAchievements();
  setupContactForm();
});

// -------------------------------------------------------------------
// 1. Profile Data Fetcher & DOM Renderer
// -------------------------------------------------------------------
async function fetchProfile() {
  try {
    const response = await fetch(`${API_BASE}/profile`);
    if (!response.ok) throw new Error("Failed to fetch profile");
    const data = await response.json();
    if (data.success && data.profile) {
      renderProfile(data.profile);
    }
  } catch (err) {
    console.warn("Using fallback for Profile API", err);
    renderProfile({
      full_name: "Meet Patil",
      bio: "Frontend Developer • AI Application Developer • Backend Learner"
    });
  }
}

function renderProfile(profile) {
  const heroName = document.getElementById("heroName");
  const heroRole = document.getElementById("heroRole");
  const aboutText = document.getElementById("aboutText");
  const educationCard = document.getElementById("educationCard");

  if (heroName) heroName.textContent = `${profile.full_name || "Meet Patil"}.`;
  if (heroRole) heroRole.textContent = profile.bio;

  if (aboutText) {
    aboutText.innerHTML = `
      <p class="lead text-secondary">
        I build digital web platforms, combining smooth frontend user experiences with modern backend architectures and artificial intelligence integrations.
      </p>
    `;
  }

  if (educationCard) {
    educationCard.innerHTML = `
      <div class="card p-4 shadow-sm border-0">
        <h5 class="fw-bold mb-2"><i class="bi bi-mortarboard me-2"></i>Education & Focus</h5>
        <p class="mb-1 text-dark fw-semibold">Computer Science & Full-Stack Development</p>
        <p class="text-muted small m-0">Specializing in Python Flask, Node.js, and Modern Web Systems.</p>
      </div>
    `;
  }
}

// -------------------------------------------------------------------
// 2. Skills Fetcher (Matches app.py /api/skills)
// -------------------------------------------------------------------
async function fetchSkills() {
  try {
    const response = await fetch(`${API_BASE}/skills`);
    if (!response.ok) throw new Error("Failed to fetch skills");
    const data = await response.json();
    if (data.success && data.skills) {
      renderSkills(data.skills);
    }
  } catch (err) {
    console.warn("Using fallback for Skills API", err);
    renderSkills([
      { name: "JavaScript (ES6+)", category: "Frontend" },
      { name: "Bootstrap 5", category: "Frontend" },
      { name: "Python & Flask", category: "Backend" },
      { name: "Node.js & Express", category: "Backend" },
      { name: "AI API Integration", category: "AI" }
    ]);
  }
}

function renderSkills(skills) {
  const container = document.getElementById("skillsGrid");
  if (!container) return;
  container.innerHTML = skills
    .map(
      (skill) => `
    <div class="col-md-4 col-sm-6">
      <div class="p-3 border rounded bg-light text-center h-100 shadow-sm">
        <h6 class="fw-bold mb-1">${skill.name}</h6>
        <span class="badge bg-secondary">${skill.category}</span>
      </div>
    </div>
  `
    )
    .join("");
}

// -------------------------------------------------------------------
// 3. Projects Fetcher (Matches app.py /api/projects)
// -------------------------------------------------------------------
async function fetchProjects() {
  try {
    const response = await fetch(`${API_BASE}/projects`);
    if (!response.ok) throw new Error("Failed to fetch projects");
    const data = await response.json();
    if (data.success && data.projects) {
      renderProjects(data.projects);
    }
  } catch (err) {
    console.warn("Using fallback for Projects API", err);
    renderProjects([
      {
        name: "PeopleFirst",
        category: "Full-Stack AI",
        description: "Full-stack AI platform integrating chat, career roadmaps, and Node.js APIs."
      },
      {
        name: "CivicSphere",
        category: "Full-Stack AI",
        description: "AI platform for emergency response coordination and civic grievance management."
      }
    ]);
  }
}

function renderProjects(projects) {
  const container = document.getElementById("projectsGrid");
  if (!container) return;
  container.innerHTML = projects
    .map(
      (p) => `
    <div class="col-md-6">
      <div class="card h-100 p-4 shadow-sm border-0">
        <div class="card-body">
          <span class="badge bg-primary mb-2">${p.category || "Full-Stack"}</span>
          <h4 class="card-title fw-bold">${p.name || p.title}</h4>
          <p class="card-text text-muted mt-2">${p.description}</p>
        </div>
      </div>
    </div>
  `
    )
    .join("");
}

// -------------------------------------------------------------------
// 4. Roadmap Fetcher & Fallback Handling
// -------------------------------------------------------------------
async function fetchRoadmap() {
  try {
    const response = await fetch(`${API_BASE}/roadmap`);
    const data = await response.json();
    if (data.success && data.roadmap && data.roadmap.length > 0) {
      renderRoadmap(data.roadmap);
    } else {
      throw new Error("Empty roadmap payload");
    }
  } catch (err) {
    renderRoadmap([
      { title: "Frontend Foundation", desc: "Mastered HTML5, Responsive CSS3, and Modern JavaScript." },
      { title: "Backend Systems", desc: "Building Python Flask APIs, managing Supabase databases, and deploying." },
      { title: "AI Integration", desc: "Integrating LLM end-points, workflow automation, and full-stack services." }
    ]);
  }
}

function renderRoadmap(items) {
  const container = document.getElementById("roadmapTimeline");
  if (!container) return;
  container.innerHTML = items
    .map(
      (item, idx) => `
    <div class="roadmap-item p-3 mb-3 border-start border-3 border-primary bg-light rounded shadow-sm">
      <h6 class="fw-bold m-0">Milestone ${idx + 1}: ${item.title}</h6>
      <p class="text-muted small m-0 mt-1">${item.desc}</p>
    </div>
  `
    )
    .join("");
}

// -------------------------------------------------------------------
// 5. Learning & Journey Fetcher & Fallback
// -------------------------------------------------------------------
async function fetchLearning() {
  try {
    const response = await fetch(`${API_BASE}/learning`);
    const data = await response.json();
    if (data.success && data.learning && data.learning.length > 0) {
      renderLearning(data.learning);
    } else {
      throw new Error("Empty learning payload");
    }
  } catch (err) {
    renderLearning([
      { title: "Advanced Node.js & Microservices", status: "In Progress" },
      { title: "Supabase RLS & Database Optimization", status: "Completed" }
    ]);
  }
}

function renderLearning(items) {
  const learningGrid = document.getElementById("learningGrid");
  const journeyFlow = document.getElementById("journeyFlow");

  if (learningGrid) {
    learningGrid.innerHTML = items
      .map(
        (i) => `
      <div class="col-md-6">
        <div class="p-3 border rounded shadow-sm bg-white">
          <h6 class="fw-bold mb-1">${i.title}</h6>
          <span class="badge bg-info text-dark">${i.status}</span>
        </div>
      </div>
    `
      )
      .join("");
  }

  if (journeyFlow) {
    journeyFlow.innerHTML = `
      <div class="p-3 border rounded bg-light text-muted">
        Currently expanding full-stack engineering skills, cloud deployment processes, and AI backend pipelines.
      </div>
    `;
  }
}

// -------------------------------------------------------------------
// 6. Achievements & Profile Dashboard Fetcher
// -------------------------------------------------------------------
async function fetchAchievements() {
  const achievementsWrap = document.getElementById("achievementsWrap");
  const profileDashboard = document.getElementById("profileDashboard");

  if (achievementsWrap) {
    achievementsWrap.innerHTML = `
      <div class="alert alert-light border text-center shadow-sm" role="alert">
        🚀 Successfully deployed live backend on Render connected with Supabase database!
      </div>
    `;
  }

  if (profileDashboard) {
    profileDashboard.innerHTML = `
      <div class="row g-3 text-center">
        <div class="col-md-4"><div class="p-3 bg-white rounded shadow-sm border"><strong>Status</strong><br><span class="text-success">Live & Operational</span></div></div>
        <div class="col-md-4"><div class="p-3 bg-white rounded shadow-sm border"><strong>Backend API</strong><br>Python Flask</div></div>
        <div class="col-md-4"><div class="p-3 bg-white rounded shadow-sm border"><strong>Database</strong><br>Supabase PostgreSQL</div></div>
      </div>
    `;
  }
}

// -------------------------------------------------------------------
// 7. Contact Form Handler (Submits exact payload expected by app.py)
// -------------------------------------------------------------------
function setupContactForm() {
  const form = document.getElementById("contactForm");
  const feedback = document.getElementById("formFeedback");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    // Intercept default submission to prevent 404 navigation
    e.preventDefault();

    const name = document.getElementById("cName")?.value.trim() || "";
    const email = document.getElementById("cEmail")?.value.trim() || "";
    const subject = document.getElementById("cSubject")?.value.trim() || "";
    const message = document.getElementById("cMessage")?.value.trim() || "";

    // Field Validation matching app.py requirements
    if (!name || !email || !subject || !message) {
      if (feedback) {
        feedback.textContent = "All fields (name, email, subject, message) are required.";
        feedback.className = "form-feedback text-danger mt-2 fw-semibold";
      }
      return;
    }

    if (feedback) {
      feedback.textContent = "Sending message...";
      feedback.className = "form-feedback text-info mt-2 fw-semibold";
    }

    try {
      const response = await fetch(`${API_BASE}/contact`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, subject, message })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        if (feedback) {
          feedback.textContent = "Thank you! Message submitted successfully.";
          feedback.className = "form-feedback text-success mt-2 fw-semibold";
        }
        form.reset();
      } else {
        if (feedback) {
          feedback.textContent = result.error || "Failed to submit message.";
          feedback.className = "form-feedback text-danger mt-2 fw-semibold";
        }
      }
    } catch (err) {
      if (feedback) {
        feedback.textContent = "An error occurred while connecting to backend.";
        feedback.className = "form-feedback text-danger mt-2 fw-semibold";
      }
    }
  });
}
