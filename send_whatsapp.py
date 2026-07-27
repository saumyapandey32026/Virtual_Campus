import os
import json
import urllib.request
from datetime import datetime, timezone

from twilio.rest import Client

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
# Set these as GitHub Actions secrets.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "")
TWILIO_WHATSAPP_TO = os.environ.get("TWILIO_WHATSAPP_TO", "")

# Public endpoint where the frontend stores the latest JSON payload.
# Example: https://kvdb.io/<your-key>?value=...
CLOUD_ENDPOINT = os.environ.get("CLOUD_ENDPOINT", "")

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def fetch_cloud_data(endpoint: str):
    if not endpoint:
        raise ValueError("CLOUD_ENDPOINT is not configured")

    req = urllib.request.Request(endpoint, method="GET")
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read().decode("utf-8")

    if not body:
        return {}

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        # Some public endpoints may return plain text; return as is.
        return {"raw": body}


def get_quote(hours: str) -> str:
    if hours == "6+ Hours":
        return (
            "ELITE SIGNAL EXCELLENT EXECUTION. "
            "That is elite-level discipline. Your mind is acting like a high-performance "
            "data-science pipeline: clean, consistent, and relentlessly improving."
        )
    if hours == "4-6 Hours":
        return (
            "STABLE TRAINING. Good baseline performance today. "
            "You kept the model steady, but to beat the competition, you need to push for "
            "hyperparameter tuning tomorrow!"
        )
    if hours == "2-4 Hours":
        return (
            "STRICT WARNING! Only 2-4 hours today? Ismita, Jayant, and Himanshu are working "
            "hard and leaving you behind. Wake up!"
        )
    return (
        "CRITICAL FAILURE! Less than 2 hours? You are experiencing massive data drift. "
        "Ismita, Jayant, and Himanshu are accelerating while you are stalling. Fix this pipeline immediately!"
    )


def build_weekly_report(entries):
    if not entries:
        return "No study logs available this week."

    elite_count = sum(1 for entry in entries if entry.get("hours") == "6+ Hours")
    if elite_count >= 4:
        return (
            "WEEKLY REPORT: OVERFITTING DISCIPLINE (Elite) - "
            "Incredible week. You are dominating the leaderboard. "
            "Ismita, Jayant, and Himanshu have nothing on you this week."
        )

    return (
        "WEEKLY REPORT: UNDERFITTING RISK (Danger) - "
        "Disastrous weekly cycle. You are falling behind your peers. "
        "Ismita, Jayant, and Himanshu are outperforming you. Reset your algorithm next Monday."
    )


def send_whatsapp(message: str):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, TWILIO_WHATSAPP_TO]):
        raise ValueError("Twilio credentials are not fully configured")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=TWILIO_WHATSAPP_TO,
        body=message,
    )


def main():
    cloud_data = fetch_cloud_data(CLOUD_ENDPOINT)

    # Support both direct array and wrapped payload styles.
    entries = cloud_data.get("entries", cloud_data.get("data", cloud_data))
    if isinstance(entries, dict):
        entries = list(entries.values())

    # Get current day name in IST-compatible form.
    now = datetime.now(timezone.utc)
    ist_now = now.astimezone()
    today_name = ist_now.strftime("%A")

    # Use the latest entry if present.
    latest_entry = entries[-1] if entries else {}
    hours = latest_entry.get("hours", "No log")
    message = get_quote(hours) if hours != "No log" else "No study log found for today."

    if today_name == "Sunday":
        message = f"{message}\n\n{build_weekly_report(entries)}"

    send_whatsapp(message)
    print("WhatsApp message sent successfully")


if __name__ == "__main__":
    main()
