import gc
import os
import re
import smtplib
import socket
import threading
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables before importing database
load_dotenv()

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import supabase, get_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")
CORS(app)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def handle_error(message, status_code=500, details=None):
    """Standardized error handler function returning JSON."""
    if details:
        app.logger.error(f"Internal Error: {details}")
    return jsonify({
        "success": False,
        "error": message
    }), status_code


def send_email_notification(name, email, subject, message):
    """Dispatches email notification asynchronously in a background daemon thread."""
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    to_email = os.getenv("TO_EMAIL", email_user)

    if not email_user or not email_pass:
        app.logger.warning("Email credentials missing in environment variables.")
        return False

    # Gmail app passwords frequently contain spaces when generated (e.g. 'xxxx xxxx xxxx xxxx')
    clean_pass = email_pass.replace(" ", "") if (" " in email_pass and len(email_pass.replace(" ", "")) == 16) else email_pass

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📩 New Portfolio Message: {subject}"
    msg["From"] = f"{name} <{email_user}>"
    msg["To"] = to_email
    msg["Reply-To"] = email

    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ded2c2; border-radius: 8px;">
      <h2 style="color: #333;">New Contact Form Submission</h2>
      <p><strong>Name:</strong> {name}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Subject:</strong> {subject}</p>
      <hr style="border: 0.5px solid #eee;" />
      <p><strong>Message:</strong></p>
      <p style="white-space: pre-wrap; background: #f9f9f9; padding: 15px; border-radius: 5px;">{message}</p>
    </div>
    """
    msg.attach(MIMEText(html_content, "html"))

    def _dispatch():
        # Primary attempt: Port 587 (STARTTLS) with IPv4 resolution
        try:
            try:
                addr_info = socket.getaddrinfo("smtp.gmail.com", 587, socket.AF_INET, socket.SOCK_STREAM)
                target_ip = addr_info[0][4][0]
            except Exception:
                target_ip = "smtp.gmail.com"

            with smtplib.SMTP(target_ip, 587, timeout=5) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(email_user, clean_pass)
                server.send_message(msg)
            return True
        except Exception as e1:
            # Secondary fallback: Port 465 (SSL) with IPv4 resolution
            try:
                addr_info_ssl = socket.getaddrinfo("smtp.gmail.com", 465, socket.AF_INET, socket.SOCK_STREAM)
                target_ip_ssl = addr_info_ssl[0][4][0]
            except Exception:
                target_ip_ssl = "smtp.gmail.com"

            try:
                with smtplib.SMTP_SSL(target_ip_ssl, 465, timeout=5) as server:
                    server.login(email_user, clean_pass)
                    server.send_message(msg)
                return True
            except Exception as e2:
                app.logger.warning(f"Background email dispatch error: {e2}")
                return False

    # Launch daemon background thread immediately without blocking the HTTP response
    t = threading.Thread(target=_dispatch, daemon=True)
    t.start()
    return True


# -------------------------------------------------------------------
# FRONTEND & UTILITY ROUTES
# -------------------------------------------------------------------

@app.route("/", methods=["GET"])
def serve_index():
    """Serves index.html directly from the root folder."""
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """Silences browser 404 errors when requesting favicon."""
    return "", 204


# -------------------------------------------------------------------
# PUBLIC APIS (Static Data & Health Check)
# -------------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "Backend is running"
    }), 200


@app.route("/api/profile", methods=["GET"])
def get_profile():
    return jsonify({
        "success": True,
        "profile": {
            "full_name": "Meet Patil",
            "role": "Frontend Developer • AI Application Developer • Backend Learner",
            "location": "Maharashtra, India",
            "about": [
                "I am a Frontend Developer and AI Application Developer actively expanding my capabilities into full-stack and backend engineering.",
                "My focus is on creating responsive, intuitive user interfaces and connecting them with AI capabilities and Node.js backend services to build practical digital products."
            ]
        }
    }), 200


@app.route("/api/skills", methods=["GET"])
def get_skills():
    return jsonify({
        "success": True,
        "skills": [
            {
                "category": "Frontend Development",
                "icon": "bi-layout-text-window-reverse",
                "items": [
                    {"name": "HTML5 / CSS3", "level": "Comfortable"},
                    {"name": "JavaScript (ES6+)", "level": "Comfortable"},
                    {"name": "Bootstrap 5", "level": "Comfortable"},
                    {"name": "Tailwind CSS", "level": "Developing"},
                    {"name": "Responsive UI/UX", "level": "Comfortable"}
                ]
            },
            {
                "category": "AI & APIs",
                "icon": "bi-cpu",
                "items": [
                    {"name": "AI API Integration", "level": "Comfortable"},
                    {"name": "AI Chat Services", "level": "Comfortable"},
                    {"name": "AI Prompt Engineering", "level": "Comfortable"},
                    {"name": "RESTful APIs", "level": "Comfortable"}
                ]
            },
            {
                "category": "Backend Learning Path",
                "icon": "bi-server",
                "items": [
                    {"name": "Node.js & Express", "level": "Building"},
                    {"name": "User Authentication", "level": "Building"},
                    {"name": "Databases (SQL/NoSQL)", "level": "Learning"},
                    {"name": "System Architecture", "level": "Learning"}
                ]
            }
        ]
    }), 200


@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify({
        "success": True,
        "projects": [
            {
                "name": "PeopleFirst",
                "category": "Full-Stack AI",
                "icon": "bi-person-badge",
                "status": "Completed",
                "description": "Full-stack AI platform integrating chat, career roadmaps, and Node.js APIs.",
                "features": [
                    "AI Chat & AI Quiz Generator",
                    "Education Features & Student News",
                    "AI Career Roadmap Generator",
                    "User Authentication & Secure API Integrations",
                    "Modern Responsive UI/UX"
                ],
                "technologies": ["Frontend (JS/CSS)", "Node.js Backend", "Express", "AI APIs", "Authentication"],
                "github_url": "",
                "live_url": ""
            },
            {
                "name": "CivicSphere",
                "category": "Full-Stack AI",
                "icon": "bi-building-gear",
                "status": "Currently Working On",
                "description": "AI platform for emergency response coordination and civic grievance management.",
                "features": [
                    "AI-Powered Civic Assistance",
                    "Disaster & Emergency Response Coordination",
                    "Farmer Support & Agricultural Tools",
                    "Smart Grievance Management System",
                    "Citizen-Focused Information Portal"
                ],
                "technologies": ["Frontend Architecture", "Node.js Backend", "Databases", "AI Integration", "API Architecture"],
                "github_url": "",
                "live_url": ""
            }
        ]
    }), 200


@app.route("/api/roadmap", methods=["GET"])
def get_roadmap():
    return jsonify({
        "success": True,
        "roadmap": [
            {
                "title": "1. Core Web Foundation",
                "status": "Completed",
                "statusClass": "status-completed",
                "description": "Mastered frontend styling and structural principles through clean HTML5, CSS3, and responsive design systems.",
                "learning": "Semantic markup, CSS Flexbox/Grid, mobile-first design.",
                "technologies": ["HTML5", "CSS3", "Responsive Web Design"],
                "progress": 100,
                "nextGoal": "Advanced JavaScript functionality"
            },
            {
                "title": "2. Modern JavaScript & Frameworks",
                "status": "Completed",
                "statusClass": "status-completed",
                "description": "Built dynamic web interfaces utilizing ES6 JavaScript syntax alongside modern UI toolkits like Bootstrap 5 and Tailwind CSS.",
                "learning": "DOM manipulation, async programming, UI components.",
                "technologies": ["JavaScript (ES6+)", "Bootstrap 5", "Tailwind CSS"],
                "progress": 100,
                "nextGoal": "API integrations and dynamic data flows"
            },
            {
                "title": "3. Full-Stack AI Platforms (PeopleFirst)",
                "status": "Completed",
                "statusClass": "status-completed",
                "description": "Successfully built and deployed PeopleFirst — an AI-powered platform integrating chat, career roadmaps, authentication, and Node.js API services.",
                "learning": "Full-stack integration, authentication, AI APIs, responsive UX.",
                "technologies": ["Node.js", "Express", "AI APIs", "Authentication", "JavaScript"],
                "progress": 100,
                "nextGoal": "Architecting large-scale civic systems"
            },
            {
                "title": "4. Civic Engineering & Disaster Response (CivicSphere)",
                "status": "Currently Developing",
                "statusClass": "status-currently-working-on",
                "description": "Building CivicSphere — an AI platform designed for emergency response coordination, smart grievance management, and citizen support.",
                "learning": "Scalable backend architecture, real-time coordination feeds, database integration.",
                "technologies": ["AI Coordination", "Node.js Architecture", "Smart Grievances", "Databases"],
                "progress": 60,
                "nextGoal": "Complete end-to-end backend and deploy live testing"
            }
        ]
    }), 200


@app.route("/api/learning", methods=["GET"])
def get_learning():
    return jsonify({
        "success": True,
        "learning": [
            {"name": "Node.js & Express Architecture", "icon": "bi-server", "status": "Active Focus"},
            {"name": "Database Design & Management", "icon": "bi-database", "status": "Learning"},
            {"name": "Advanced AI API Orchestration", "icon": "bi-cpu", "status": "Building"},
            {"name": "System Authentication & Security", "icon": "bi-shield-lock", "status": "Building"}
        ]
    }), 200


@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    return jsonify({"success": True, "achievements": []}), 200


# -------------------------------------------------------------------
# DATABASE API (Supabase + Local SQLite Dual Support & Background Email)
# -------------------------------------------------------------------

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    try:
        data = request.get_json(silent=True) or {}

        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        subject = str(data.get("subject", "")).strip()
        message = str(data.get("message", "")).strip()

        if not name or not email or not subject or not message:
            return handle_error("All fields (name, email, subject, message) are required.", status_code=400)

        if not EMAIL_REGEX.match(email):
            return handle_error("Invalid email address format.", status_code=400)

        payload = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "is_read": False
        }

        saved_id = None

        # 1. Primary storage: Supabase table 'messages'
        if supabase:
            try:
                response = supabase.table("messages").insert(payload).execute()
                if response.data and len(response.data) > 0:
                    saved_id = response.data[0].get("id")
            except Exception as sb_err:
                app.logger.warning(f"Supabase write error, falling back to SQLite: {sb_err}")

        # 2. Secondary fallback storage: Local SQLite database
        if saved_id is None:
            try:
                with get_db() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO messages (name, email, subject, message, is_read) VALUES (?, ?, ?, ?, ?)",
                        (name, email, subject, message, 0)
                    )
                    conn.commit()
                    saved_id = cur.lastrowid
            except Exception as db_err:
                app.logger.error(f"Local database write error: {db_err}")

        if saved_id is not None:
            # Dispatch background email notification (non-blocking)
            send_email_notification(name, email, subject, message)

            return jsonify({
                "success": True,
                "message": "Message received successfully",
                "id": saved_id
            }), 201

        return handle_error("Could not save message.", status_code=500)

    except Exception as e:
        return handle_error("An error occurred while submitting your message.", details=traceback.format_exc())
    finally:
        gc.collect()


if __name__ == "__main__":
    print("======================================")
    print("[*] Personal Profile App")
    print("[*] Website: http://127.0.0.1:5000/")
    print("======================================")

    app.run(host="127.0.0.1", port=5000, debug=True)
