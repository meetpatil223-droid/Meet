import gc
import json
import os
import re
import smtplib
import threading
import traceback
import urllib.error
import urllib.request
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
    """
    Sends email notification via Resend HTTPS REST API (cloud-safe, no SMTP blocking)
    with fallback to direct Gmail SMTP if configured.
    """
    resend_api_key = (os.getenv("RESEND_API_KEY") or "").strip().strip('"').strip("'")
    resend_to_email = (os.getenv("RESEND_TO_EMAIL") or os.getenv("TO_EMAIL") or "meetpatil223@gmail.com").strip()
    to_email = (os.getenv("TO_EMAIL") or "meetpatil223@gmail.com").strip()

    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 24px; border: 1px solid #ded2c2; border-radius: 12px; background-color: #fffdf8; color: #29251f; max-width: 600px;">
      <h2 style="color: #8b6f47; margin-top: 0; border-bottom: 2px solid #ded2c2; padding-bottom: 12px;">📩 New Portfolio Message</h2>
      <p style="margin: 8px 0;"><strong>From:</strong> {name}</p>
      <p style="margin: 8px 0;"><strong>Email:</strong> <a href="mailto:{email}" style="color: #8b6f47;">{email}</a></p>
      <p style="margin: 8px 0;"><strong>Subject:</strong> {subject}</p>
      <hr style="border: 0.5px solid #ded2c2; margin: 16px 0;" />
      <p style="margin: 8px 0;"><strong>Message:</strong></p>
      <div style="white-space: pre-wrap; background: #f5efe6; padding: 16px; border-radius: 8px; border: 1px solid #ded2c2; font-size: 15px; line-height: 1.6;">{message}</div>
      <p style="margin-top: 20px; font-size: 12px; color: #6f665c;">Sent automatically from your Meet Patil Portfolio.</p>
    </div>
    """

    def _dispatch():
        # 1. Primary Method: Resend HTTPS REST API (Works 100% on Render, Vercel & Cloud)
        if resend_api_key:
            try:
                print(f"[NOTIFICATION] Attempting Resend API dispatch to {resend_to_email}...", flush=True)
                payload = json.dumps({
                    "from": "Portfolio Contact <onboarding@resend.dev>",
                    "to": [resend_to_email],
                    "reply_to": email,
                    "subject": f"📩 Portfolio Message: {subject} (from {name})",
                    "html": html_content
                }).encode("utf-8")

                req = urllib.request.Request(
                    "https://api.resend.com/emails",
                    data=payload,
                    headers={
                        "Authorization": f"Bearer {resend_api_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "MeetPatil-Portfolio/1.0"
                    }
                )
                with urllib.request.urlopen(req, timeout=10) as res:
                    res_body = res.read().decode("utf-8")
                    print(f"[NOTIFICATION SUCCESS] Email sent via Resend API: {res_body}", flush=True)
                    app.logger.info(f"Email sent via Resend API: {res_body}")
                    return True
            except urllib.error.HTTPError as he:
                error_body = he.read().decode("utf-8", errors="ignore")
                print(f"[NOTIFICATION ERROR] Resend API HTTP {he.code}: {error_body}", flush=True)
                app.logger.warning(f"Resend API HTTP Error {he.code}: {error_body}")
            except Exception as resend_err:
                print(f"[NOTIFICATION ERROR] Resend API dispatch failed: {resend_err}", flush=True)
                app.logger.warning(f"Resend API dispatch failed: {resend_err}")
        else:
            print("[NOTIFICATION INFO] RESEND_API_KEY not set. Check your Render Environment Variables.", flush=True)

        # 2. Secondary Method: FormSubmit HTTPS Gateway (Cloud-safe, direct inbox delivery to meetpatil223@gmail.com)
        try:
            print(f"[NOTIFICATION] Attempting FormSubmit HTTPS gateway to {to_email}...", flush=True)
            fs_payload = json.dumps({
                "name": name,
                "email": email,
                "_replyto": email,
                "_subject": f"📩 Portfolio Message: {subject} (from {name})",
                "message": message,
                "_template": "table"
            }).encode("utf-8")

            fs_req = urllib.request.Request(
                f"https://formsubmit.co/ajax/{to_email}",
                data=fs_payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Origin": "https://my-profile-2-l30b.onrender.com",
                    "Referer": "https://my-profile-2-l30b.onrender.com/"
                }
            )
            with urllib.request.urlopen(fs_req, timeout=10) as fs_res:
                fs_body = fs_res.read().decode("utf-8")
                print(f"[NOTIFICATION SUCCESS] Email dispatched via FormSubmit: {fs_body}", flush=True)
                app.logger.info(f"Email dispatched via FormSubmit: {fs_body}")
                return True
        except Exception as fs_err:
            print(f"[NOTIFICATION ERROR] FormSubmit dispatch failed: {fs_err}", flush=True)
            app.logger.warning(f"FormSubmit dispatch failed: {fs_err}")

        # 3. Tertiary Fallback: Direct Gmail SMTP (Local development)
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        if email_user and email_pass:
            try:
                print(f"[NOTIFICATION] Attempting Gmail SMTP dispatch...", flush=True)
                clean_pass = email_pass.replace(" ", "") if (" " in email_pass and len(email_pass.replace(" ", "")) == 16) else email_pass
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"📩 New Portfolio Message: {subject}"
                msg["From"] = f"{name} <{email_user}>"
                msg["To"] = to_email
                msg["Reply-To"] = email
                msg.attach(MIMEText(html_content, "html"))

                with smtplib.SMTP("smtp.gmail.com", 587, timeout=8) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(email_user, clean_pass)
                    server.send_message(msg)
                print("[NOTIFICATION SUCCESS] Email sent via Gmail SMTP", flush=True)
                app.logger.info("Email sent via Gmail SMTP")
                return True
            except Exception as smtp_err:
                print(f"[NOTIFICATION ERROR] Gmail SMTP fallback failed: {smtp_err}", flush=True)
                app.logger.warning(f"Gmail SMTP fallback failed: {smtp_err}")

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
# DATABASE API (Supabase + Local SQLite Dual Support & Resend Email)
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
            # Dispatch background email notification via Resend HTTPS API (non-blocking)
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
