import gc
import os
import re
import smtplib
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
    """Sends an email notification via Gmail SMTP."""
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    to_email = os.getenv("TO_EMAIL", email_user)

    if not email_user or not email_pass:
        app.logger.warning("Email credentials (EMAIL_USER / EMAIL_PASS) missing in .env")
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

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
    return True


# -------------------------------------------------------------------
# FRONTEND & UTILITY ROUTES
# -------------------------------------------------------------------

@app.route("/", methods=["GET"])
def serve_index():
    """Serves index.html directly from the current folder."""
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """Silences browser 404 errors when requesting favicon."""
    return "", 204


# -------------------------------------------------------------------
# PUBLIC APIS (Static Data)
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
            "bio": "Welcome to my personal portfolio website!"
        }
    }), 200


@app.route("/api/skills", methods=["GET"])
def get_skills():
    return jsonify({
        "success": True,
        "skills": [
            {"name": "Python", "category": "Backend"},
            {"name": "Flask", "category": "Backend"},
            {"name": "JavaScript", "category": "Frontend"},
            {"name": "HTML/CSS", "category": "Frontend"}
        ]
    }), 200


@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify({
        "success": True,
        "projects": [
            {
                "title": "PeopleFirst",
                "description": "Full-Stack AI Platform."
            },
            {
                "title": "CivicSphere",
                "description": "AI-powered civic engineering and disaster response platform."
            }
        ]
    }), 200


@app.route("/api/roadmap", methods=["GET"])
def get_roadmap():
    return jsonify({
        "success": True,
        "roadmap": []
    }), 200


@app.route("/api/learning", methods=["GET"])
def get_learning():
    return jsonify({
        "success": True,
        "learning": []
    }), 200


@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    return jsonify({
        "success": True,
        "achievements": []
    }), 200


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

        # Inserts into the single 'messages' table in Supabase
        response = supabase.table("messages").insert(payload).execute()

        if response.data:
            created_message = response.data[0]

            # Send email alert to your inbox
            try:
                send_email_notification(name, email, subject, message)
            except Exception as mail_err:
                app.logger.error(f"Failed to send email notification: {mail_err}")

            return jsonify({
                "success": True,
                "message": "Message received successfully",
                "id": created_message.get("id")
            }), 201

        return handle_error("Could not save message.", status_code=500)

    except Exception as e:
        return handle_error("An error occurred while submitting your message.", details=traceback.format_exc())
    finally:
        # Free memory immediately after request processing
        gc.collect()


if __name__ == "__main__":
    print("======================================")
    print("🚀 Personal Profile App")
    print("🌐 Website: http://127.0.0.1:5000/")
    print("======================================")

    app.run(host="127.0.0.1", port=5000, debug=True)