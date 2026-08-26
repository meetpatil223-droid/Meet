/* =========================================================
   MEET PATIL — Personal Digital Profile Frontend Script
   ========================================================= */
// Base API Endpoint Configuration
const API_BASE = "https://my-profile-2-l30b.onrender.com/api";

document.addEventListener("DOMContentLoaded", () => {
  fetchProfile();
  fetchSkills();
  fetchProjects();
  setupContactForm();
});

// -------------------------------------------------------------------
// Profile Data Fetcher
// -------------------------------------------------------------------
async function fetchProfile() {
  try {
    const response = await fetch(`${API_BASE}/profile`);
    if (!response.ok) throw new Error("Failed to fetch profile");
    const data = await response.json();
    if (data.success && data.profile) {
      const heroName = document.getElementById("heroName");
      const heroRole = document.getElementById("heroRole");
      if (heroName) heroName.textContent = `${data.profile.full_name}.`;
      if (heroRole) heroRole.textContent = data.profile.bio;
    }
  } catch (err) {
    console.warn("Using local fallback for Profile API", err);
  }
}

// -------------------------------------------------------------------
// Skills Fetcher & Dynamic Rendering
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
    console.warn("Using local fallback for Skills API", err);
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
// Projects Fetcher & Dynamic Rendering
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
    console.warn("Using local fallback for Projects API", err);
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
          <span class="badge bg-accent text-dark mb-2">${p.category || "Full-Stack"}</span>
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
// Contact Form Handler (Prevents 404 Navigation & Sends JSON Payload)
// -------------------------------------------------------------------
function setupContactForm() {
  const form = document.getElementById("contactForm");
  const feedback = document.getElementById("formFeedback");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    // Stop native browser page refresh / navigation to /#contact
    e.preventDefault();

    // Map fields matching index.html IDs
    const name = document.getElementById("cName")?.value.trim() || "";
    const email = document.getElementById("cEmail")?.value.trim() || "";
    const subject = document.getElementById("cSubject")?.value.trim() || "";
    const message = document.getElementById("cMessage")?.value.trim() || "";

    if (!name || !email || !subject || !message) {
      if (feedback) {
        feedback.textContent = "Please fill in all required fields.";
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
          feedback.textContent = "Thank you, Meet will get back to you soon! Message sent successfully.";
          feedback.className = "form-feedback text-success mt-2 fw-semibold";
        }
        form.reset();
      } else {
        if (feedback) {
          feedback.textContent = result.error || "Failed to send message.";
          feedback.className = "form-feedback text-danger mt-2 fw-semibold";
        }
      }
    } catch (err) {
      if (feedback) {
        feedback.textContent = "Unable to connect to the backend server.";
        feedback.className = "form-feedback text-danger mt-2 fw-semibold";
      }
    }
  });
}