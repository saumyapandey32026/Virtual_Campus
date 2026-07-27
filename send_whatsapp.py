import os
import sys
from datetime import datetime
from twilio.rest import Client

def main():
    # Credentials fetch kar rahe hain
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    to_whatsapp = os.environ.get('MY_WHATSAPP_NUMBER')
    from_whatsapp = 'whatsapp:+14155238886' # Twilio default sandbox number

    # GitHub workflow input se ghante read karna (default '6+')
    test_input = sys.argv[1] if len(sys.argv) > 1 else '6+'
    test_input = test_input.strip()

    # Dynamic Hours Logic Mapping
    logged_hours = "6+ Hours"
    if "4-6" in test_input:
        logged_hours = "4-6 Hours"
    elif "2-4" in test_input:
        logged_hours = "2-4 Hours"
    elif "<2" in test_input:
        logged_hours = "<2 Hours"

    # Exact Custom Quotes Logic
    quote = ""
    if logged_hours == "6+ Hours":
        quote = "⚡ ELITE SIGNAL! EXCELLENT EXECUTION. That is elite-level discipline. Your mind is acting like a high-performance data-science pipeline: clean, consistent, and relentlessly improving."
    elif logged_hours == "4-6 Hours":
        quote = "📉 STABLE TRAINING. Good baseline performance today. You kept the model steady, but to beat the competition, you need to push for hyperparameter tuning tomorrow!"
    elif logged_hours == "2-4 Hours":
        quote = "🚨 STRICT WARNING! Only 2-4 hours today? Ismita, Jayant, and Himanshu are working hard and leaving you behind. Wake up!"
    else:
        quote = "💥 CRITICAL FAILURE! Less than 2 hours? You are experiencing massive data drift. Ismita, Jayant, and Himanshu are accelerating while you are stalling. Fix this pipeline immediately!"

    # Sunday Automatic Weekly Report Card Logic
    if datetime.now().strftime('%A') == 'Sunday':
        quote += "\n\n📊 WEEKLY REPORT CARD SUMMARY: Evaluated over past cycles. Keep optimizing your performance parameters to outperform Ismita, Jayant, and Himanshu!"

    # Message Sending Execution
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
        print(f"✅ Success! Accurate Message sent. SID: {message.sid}")
    else:
        print("❌ Error: Twilio Credentials ya WhatsApp Number missing hai settings mein.")

if __name__ == "__main__":
    main()

