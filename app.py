import concurrent.futures
import gc
import os
import re
import smtplib
import socket
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables before importing database
load_dotenv()

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import supabase

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
    """Sends an email notification using thread execution and port fallbacks to prevent cloud firewall timeouts."""
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    to_email = os.getenv("TO_EMAIL", email_user)

    if not email_user or not email_pass:
        app.logger.warning("Email credentials missing in environment variables.")
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📩 New Portfolio Message: {subject}"
    msg['From'] = f"{name} <{email_user}>"
    msg['To'] = to_email
    msg['Reply-To'] = email

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
    msg.attach(MIMEText(html_content, 'html'))

    def _dispatch():
        # Force socket resolution to IPv4 (AF_INET) to prevent IPv6 network routing failures on Render
        addr_info = socket.getaddrinfo('smtp.gmail.com', 587, socket.AF_INET, socket.SOCK_STREAM)
        target_ip = addr_info[0][4][0]

        # Primary attempt: Port 587 (STARTTLS)
        try:
            with smtplib.SMTP(target_ip, 587, timeout=7) as server:
                server.server_hostname = 'smtp.gmail.com'
                server.starttls()
                server.login(email_user, email_pass)
                server.send_message(msg)
            return True
        except Exception:
            # Secondary fallback: Port 465 (SSL)
            addr_info_ssl = socket.getaddrinfo('smtp.gmail.com', 465, socket.AF_INET, socket.SOCK_STREAM)
            target_ip_ssl = addr_info_ssl[0][4][0]
            with smtplib.SMTP_SSL(target_ip_ssl, 465, timeout=7) as server:
                server.server_hostname = 'smtp.gmail.com'
                server.login(email_user, email_pass)
                server.send_message(msg)
            return True

    try:
        # Enforce non-blocking background dispatch with a maximum runtime ceiling
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_dispatch)
            return future.result(timeout=8)
    except Exception as mail_err:
        app.logger.error(f"Failed to send email notification: {mail_err}")
        return False


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
            "bio": "Frontend Developer • AI Application Developer • Backend Learner"
        }
    }), 200


@app.route("/api/skills", methods=["GET"])
def get_skills():
    return jsonify({
        "success": True,
        "skills": [
            {"name": "JavaScript (ES6+)", "category": "Frontend"},
            {"name": "Bootstrap 5", "category": "Frontend"},
            {"name": "Python & Flask", "category": "Backend"},
            {"name": "Node.js & Express", "category": "Backend"},
            {"name": "AI API Integration", "category": "AI"}
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
                "description": "Full-stack AI platform integrating chat, career roadmaps, and Node.js APIs."
            },
            {
                "name": "CivicSphere",
                "category": "Full-Stack AI",
                "description": "AI platform for emergency response coordination and civic grievance management."
            }
        ]
    }), 200


@app.route("/api/roadmap", methods=["GET"])
def get_roadmap():
    return jsonify({"success": True, "roadmap": []}), 200


@app.route("/api/learning", methods=["GET"])
def get_learning():
    return jsonify({"success": True, "learning": []}), 200


@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    return jsonify({"success": True, "achievements": []}), 200


# -------------------------------------------------------------------
# DATABASE API (Supabase Integration + Email Dispatch)
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

        # Insert record into Supabase 'messages' table
        response = supabase.table("messages").insert(payload).execute()

        if response.data:
            created_message = response.data[0]

            # Dispatch outbound email via multi-port IPv4 threading
            send_email_notification(name, email, subject, message)

            return jsonify({
                "success": True,
                "message": "Message received successfully",
                "id": created_message.get("id")
            }), 201

        return handle_error("Could not save message.", status_code=500)

    except Exception as e:
        return handle_error("An error occurred while submitting your message.", details=traceback.format_exc())
    finally:
        # Free memory immediately to prevent free-tier out-of-memory restarts
        gc.collect()


if __name__ == "__main__":
    print("======================================")
    print("🚀 Personal Profile App")
    print("🌐 Website: http://127.0.0.1:5000/")
    print("======================================")

    app.run(host="127.0.0.1", port=5000, debug=True)



