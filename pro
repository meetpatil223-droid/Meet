Absolutely. Here is the **updated master prompt**. This version focuses on **correct personal information**, removes generic placeholder claims, keeps the **beige premium design**, and makes the roadmap/profile data accurate and easy to update later.

# MASTER PROMPT — PERSONAL PROFILE + CAREER ROADMAP WEBSITE

Build my **personal profile and career roadmap website from scratch**.

This is a website for my **personal use**, not a generic portfolio template.

The website should represent **me, my actual skills, education, projects, learning journey, interests, and future career goals**.

The design is already conceptually decided: **premium, minimal, elegant, modern, beige/cream themed**.

The most important requirement is:

> **Display accurate personal information. Do not invent achievements, experience, certifications, skills, project completion status, or progress percentages.**

---

# 1. TECHNOLOGY

Frontend only for this stage.

Use:

* HTML5
* CSS3
* Bootstrap 5
* Bootstrap Icons
* Vanilla JavaScript

Do NOT use:

* React
* Vue
* Angular
* Tailwind
* Next.js

Backend will be added later using:

* Python
* Flask
* SQLite

Therefore, structure the frontend so it can easily be connected to Flask APIs later.

---

# 2. MY ACTUAL PROFILE INFORMATION

Use the following information as the starting profile data.

## Name

**Meet Patil**

## Current Education

**Diploma — 3rd Year**

## Academic Context

**MSBTE Diploma**

## Career Interests

My main career interests are:

* Cloud Computing
* Big Data
* Software Development
* Web Development
* AI-powered applications

## Current Development Level

I am an intermediate-level developer who is continuously learning and building projects.

Do NOT display:

* "Senior Developer"
* "Expert"
* "Mastered"
* "Professional Engineer"

unless I explicitly add those claims later.

Use wording such as:

* Learning
* Building
* Exploring
* Developing
* Currently working on
* Growing my skills

---

# 3. MAIN PERSONAL MESSAGE

The website should communicate this idea:

**Building. Learning. Growing.**

I am a student/developer who is learning modern technologies by actually building projects.

The website should feel like a **digital representation of my development journey**, not simply a resume.

---

# 4. DESIGN SYSTEM

The entire website must use a **BEIGE / CREAM visual identity**.

Primary background:

```text
#F5EFE6
```

Secondary beige:

```text
#EDE3D5
```

Card background:

```text
#FFFDF8
```

Primary text:

```text
#29251F
```

Secondary text:

```text
#6F665C
```

Accent:

```text
#8B6F47
```

Light accent:

```text
#B7A083
```

Border:

```text
#DED2C2
```

Hover:

```text
#E8DDCC
```

The website should feel:

**Elegant + Warm + Personal + Premium + Minimal + Modern**

Avoid:

* Neon colors
* Blue/purple gradients
* Cyberpunk styling
* Excessive glassmorphism
* Excessive animations
* Generic AI-looking templates

---

# 5. TYPOGRAPHY

Use:

### Headings

Playfair Display

### Body

DM Sans

Use large editorial-style headings.

Example:

```text
Hi, I'm
Meet Patil.
```

with "Meet Patil" highlighted using the accent brown.

---

# 6. NAVBAR

Create a sticky responsive Bootstrap navbar.

Left:

```text
● MEET PATIL
```

Right:

```text
Home
About
Skills
Roadmap
Projects
Journey
Profile
Contact
```

Requirements:

* Sticky
* Beige translucent background
* Subtle backdrop blur
* Thin border
* Active navigation indicator
* Mobile hamburger menu
* Smooth scrolling
* Navbar shrinks slightly when scrolling

---

# 7. HOME / HERO SECTION

Create a premium hero section.

Display:

```text
WELCOME TO MY DIGITAL SPACE

Hi, I'm
Meet Patil.

Developer • Student • Technology Explorer
```

Description:

```text
I'm a developer and student who enjoys building digital
experiences, exploring new technologies and turning ideas
into practical projects.
```

Buttons:

```text
Explore My Journey →
View My Projects
```

Social icons:

* GitHub
* LinkedIn
* Instagram
* Email

Use placeholder links only where an actual link has not been provided.

Do NOT invent social usernames.

---

# 8. PROFILE IMAGE

Create a premium profile image card.

Use a clearly marked placeholder if no personal image is provided:

```text
YOUR PROFILE PHOTO
```

Do NOT use a random person's face and present it as Meet Patil.

The card should contain:

```text
CURRENT FOCUS

Building.
Learning.
Growing.
```

Use beige, cream and brown styling.

---

# 9. ABOUT ME

Heading:

```text
ABOUT ME

More than just
code.
```

Content should accurately describe me as a student/developer.

Mention:

* Diploma student
* 3rd year
* MSBTE
* Developer
* Interested in Cloud Computing
* Interested in Big Data
* Interested in Web Development
* Interested in AI applications
* Interested in building practical projects

Do not invent:

* Company employment
* Professional work experience
* Certifications
* Awards
* Freelance clients
* Internships

unless they are explicitly added later.

---

# 10. EDUCATION

Create a small education card.

Display:

```text
EDUCATION

MSBTE Diploma

3rd Year

Currently pursuing diploma studies
while developing practical technology projects.
```

Keep the content factual.

---

# 11. SKILLS

Create a skill dashboard.

Divide skills into categories.

## Web Development

* HTML
* CSS
* JavaScript
* Bootstrap
* Responsive Design

## Programming

* Java
* Python
* JavaScript

## Backend

* Node.js
* Flask
* REST APIs

## Database

* SQL
* SQLite
* Supabase

## AI / APIs

* Gemini / Google GenAI
* OpenRouter
* AI API integration

## Cloud & Data

* Cloud Computing
* Big Data

IMPORTANT:

Do not display fake percentages such as:

```text
Java — 95%
Python — 90%
```

unless I provide those percentages.

Instead use skill levels:

```text
Learning
Developing
Comfortable
Exploring
```

or allow the percentages to be configured from one JavaScript data object.

---

# 12. CAREER ROADMAP

This is one of the MOST IMPORTANT sections.

Create an interactive vertical career roadmap.

The roadmap should represent my **actual learning direction**, not pretend that I have already mastered everything.

Use:

### Milestone 1

```text
Web Development

STATUS:
Developed / Practiced

TECHNOLOGIES:
HTML
CSS
JavaScript
Bootstrap
Responsive Design
```

### Milestone 2

```text
Programming & Java

STATUS:
Currently Developing

TECHNOLOGIES:
Java
OOP
Data Structures
Problem Solving
```

### Milestone 3

```text
Backend Development

STATUS:
Currently Developing

TECHNOLOGIES:
Node.js
Python
Flask
REST APIs
Databases
```

### Milestone 4

```text
Cloud Computing

STATUS:
CAREER FOCUS

GOAL:
Build strong knowledge of cloud infrastructure,
deployment and scalable applications.

TECHNOLOGIES TO EXPLORE:
Cloud Platforms
Linux
Deployment
Containers
Networking
```

### Milestone 5

```text
Big Data

STATUS:
UPCOMING

GOAL:
Learn large-scale data processing, analytics
and distributed systems.

TECHNOLOGIES TO EXPLORE:
Big Data
Data Processing
ETL
Distributed Systems
```

### Milestone 6

```text
Advanced Cloud & Data Engineering

STATUS:
FUTURE

GOAL:
Combine cloud computing and big data knowledge
to build scalable real-world applications.
```

---

# 13. ROADMAP INTERACTION

Every roadmap milestone should be clickable.

On clicking, display a detail panel containing:

```text
TITLE

STATUS

DESCRIPTION

WHAT I'M LEARNING

TECHNOLOGIES

CURRENT PROGRESS

NEXT GOAL
```

Do not invent progress values.

Progress should be configurable from JavaScript.

Example:

```javascript
progress: null
```

If progress is null, display:

```text
Progress: Not specified
```

instead of inventing a percentage.

---

# 14. PROJECTS

Create a project showcase.

IMPORTANT:

Only display projects that are actually associated with my development work.

Initial project list can include:

### PeopleFirst AI

An AI-powered platform project involving features such as AI interaction, education/knowledge features and other civic/student-oriented functionality.



# 15. PROJECT STATUS

Use honest statuses:

```text
IDEA
IN DEVELOPMENT
COMPLETED
EXPERIMENT
PLANNED
```

The status must be easy to change from JavaScript.

---

# 16. PROJECT FILTER

Add Bootstrap/JavaScript filters:

```text
All
Web
AI
Backend
Cloud
Data
```

Filtering should happen without reloading the page.

---

# 17. CURRENTLY LEARNING

Create a section titled:

```text
CURRENTLY LEARNING

What I'm working on
right now.
```

Include:

### Cloud Computing

Status:

```text
Learning
```

### Backend Development

Status:

```text
Developing
```

### Java / Data Structures

Status:

```text
Learning
```

### Big Data

Status:

```text
Exploring
```

Do not use fake progress percentages unless configured.

---

# 18. LEARNING JOURNEY

Create a timeline showing:

```text
Learning
   ↓
Practicing
   ↓
Building Projects
   ↓
Understanding Real Problems
   ↓
Improving Technical Skills
   ↓
Cloud & Big Data
   ↓
Career
```

Make this visually different from the main roadmap.

---

# 19. ACHIEVEMENTS

Do NOT create fake achievements.

Instead, create an editable section with placeholders:

```text
Achievements will be added here.
```

Allow future entries for:

* Certifications
* Hackathons
* Awards
* Courses
* Academic achievements
* Project milestones

If no achievement exists, don't display fake content.

---

# 20. PERSONAL PROFILE DASHBOARD

Create a premium profile dashboard.

Display:

```text
MEET PATIL

Developer • Student • Technology Explorer
```

Information:

```text
Education
MSBTE Diploma — 3rd Year

Career Interest
Cloud Computing & Big Data

Current Focus
Building & Learning

Primary Interests
Web Development
Cloud
Big Data
AI
```

Statistics should NOT be invented.

Instead of:

```text
12+ Skills
08 Projects
12 Milestones
```

use values dynamically calculated from the actual JavaScript data.

For example:

```javascript
skills.length
projects.length
roadmap.length
```

This ensures the numbers are always correct.

---

# 21. PROFILE DATA ARCHITECTURE

VERY IMPORTANT:

Do not hardcode my information in dozens of different HTML locations.

Create a single central JavaScript object:

```javascript
const profileData = {

    name: "Meet Patil",

    role: "Developer • Student • Technology Explorer",

    education: {
        program: "MSBTE Diploma",
        year: "3rd Year"
    },

    interests: [
        "Cloud Computing",
        "Big Data",
        "Web Development",
        "AI"
    ],

    skills: [],

    projects: [],

    roadmap: [],

    learning: [],

    achievements: [],

    social: {
        github: "",
        linkedin: "",
        instagram: "",
        email: ""
    }

};
```

The UI should be generated from this data wherever practical.

This will make the future Flask backend integration much easier.

---

# 22. NO FALSE INFORMATION

This rule is extremely important.

Never invent:

* Experience
* Companies
* Clients
* Certifications
* Awards
* Salary
* Job titles
* Percentages
* Project completion
* GitHub repositories
* Live URLs
* Social usernames
* Professional claims

If information is missing, use:

```text
Not added yet
```

or

```text
Coming Soon
```

instead.

---

# 23. CONTACT SECTION

Create:

```text
GET IN TOUCH

Let's create
something.
```

Contact form:

```text
Name
Email
Subject
Message
Send Message
```

Frontend only for now.

On submission:

```text
Thanks! Your message has been received.
```

Do not actually send email yet.

The backend will be connected later.

---

# 24. FOOTER

Use a dark brown footer.

Display:

```text
MEET PATIL

Building. Learning. Growing.
```

Social icons should only become clickable when actual URLs are provided.

Footer:

```text
© 2026 Meet Patil
```

---

# 25. RESPONSIVE DESIGN

The website must work on:

* Desktop
* Laptop
* Tablet
* Mobile

Mobile requirements:

* Hamburger navbar
* Single-column hero
* Responsive profile image
* Single-column roadmap
* Responsive project cards
* Responsive skill cards
* Responsive profile dashboard
* Contact form fits mobile width

---

# 26. ANIMATIONS

Use subtle animations:

* Hero fade-in
* Scroll reveal
* Roadmap reveal
* Card hover
* Button hover
* Progress animation
* Navbar shrink
* Smooth scrolling

Animations should be professional and fast.

Do not make the website feel like a gaming site.

---

# 27. FILE STRUCTURE

Create:

```text
personal-profile/
│
├── index.html
├── style.css
└── script.js
```

Do not create the Flask backend yet.

---

# 28. CODE QUALITY

Use:

* Semantic HTML
* Clean CSS
* Bootstrap grid
* Reusable JavaScript functions
* Centralized profile data
* Clear comments
* Responsive design
* Accessible buttons and navigation
* Proper alt text
* No unnecessary libraries

---



# FINAL RESULT

The final website should feel like:

**Meet Patil's Personal Digital Profile**

not a generic portfolio.

The visual identity should be:

**Beige + Cream + Brown + Editorial Typography + Minimal UI**

The content identity should be:

**Student + Developer + Builder + Learner + Cloud/Big Data Career Journey**

Most importantly:

> **The website must show accurate information and honest progress. It should never make me look more experienced than I actually am.**

Generate the complete:

```text
index.html
style.css
script.js
```

and make sure all three files work together immediately in a browser.
