import os
import sys
from datetime import datetime
from twilio.rest import Client

def main():
    # Environment credentials read karna
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    to_whatsapp = os.environ.get('MY_WHATSAPP_NUMBER')
    from_whatsapp = 'whatsapp:+14155238886'

    # Sys args reading fallback filter logic
    input_argument = ""
    if len(sys.argv) > 1 and sys.argv[1]:
        input_argument = str(sys.argv[1]).strip()
    
    print(f"DEBUG PIPELINE: System received parameter raw text -> '{input_argument}'")

    # Accurate baseline hours detection
    logged_hours = "6+ Hours" # Default fallback string
    if "4-6" in input_argument:
        logged_hours = "4-6 Hours"
    elif "2-4" in input_argument:
        logged_hours = "2-4 Hours"
    elif "<2" in input_argument:
        logged_hours = "<2 Hours"

    print(f"DEBUG PIPELINE: Mapped execution route set to -> '{logged_hours}'")

    # Core Custom Structural Phrases
    quote = ""
    if logged_hours == "6+ Hours":
        quote = "⚡ ELITE SIGNAL! EXCELLENT EXECUTION. That is elite-level discipline. Your mind is acting like a high-performance data-science pipeline: clean, consistent, and relentlessly improving."
    elif logged_hours == "4-6 Hours":
        quote = "📉 STABLE TRAINING. Good baseline performance today. You kept the model steady, but to beat the competition, you need to push for hyperparameter tuning tomorrow!"
    elif logged_hours == "2-4 Hours":
        quote = "🚨 STRICT WARNING! Only 2-4 hours today? Ismita, Jayant, and Himanshu are working hard and leaving you behind. Wake up!"
    else:
        quote = "💥 CRITICAL FAILURE! Less than 2 hours? You are experiencing massive data drift. Ismita, Jayant, and Himanshu are accelerating while you are stalling. Fix this pipeline immediately!"

    # Automatic evaluation conditional node
    if datetime.now().strftime('%A') == 'Sunday':
        quote += "\n\n📊 WEEKLY REPORT CARD SUMMARY: Evaluated over past cycles. Keep optimizing your performance parameters to outperform Ismita, Jayant, and Himanshu!"

    # Final execution matrix
    if account_sid and auth_token and to_whatsapp:
        client = Client(account_sid, auth_token)
        clean_to = to_whatsapp.strip()
        if not clean_to.startswith('whatsapp:'):
            clean_to = f'whatsapp:{clean_to}'
            
        message = client.messages.create(
            body=quote,
            from_=from_whatsapp,
            to=clean_to
        )
        print(f"✅ Core Success! WhatsApp Dispatch Confirmed. SID: {message.sid}")
    else:
        print("❌ System Configuration Error: Missing authentication environment keys.")

if __name__ == "__main__":
    main()
