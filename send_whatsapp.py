import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from twilio.rest import Client

def fetch_cloud_data(url):
    if not url:
        print("⚡ CLOUD_ENDPOINT configured nahi hai, local fallback use kar rahe hain.")
        return None
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"⚠️ Cloud par abhi file nahi bani hai (HTTP Error {e.code}). Local testing query run hogi.")
        return None
    except Exception as e:
        print(f"⚠️ Cloud connection error: {e}")
        return None

def main():
    # Credentials fetch kar rahe hain
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    cloud_endpoint = os.environ.get('CLOUD_ENDPOINT')
    to_whatsapp = os.environ.get('MY_WHATSAPP_NUMBER')
    from_whatsapp = 'whatsapp:+14155238886' # Twilio default sandbox number

    # GitHub workflow menu se aane wala input check karein
    test_input = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Cloud data fetch karein
    cloud_data = fetch_cloud_data(cloud_endpoint)
    
    # Hours logic decide karein
    logged_hours = "6+ Hours" # Default fallback
    if test_input and test_input.strip():
        if "6+" in test_input: logged_hours = "6+ Hours"
        elif "4-6" in test_input: logged_hours = "4-6 Hours"
        elif "2-4" in test_input: logged_hours = "2-4 Hours"
        elif "<2" in test_input: logged_hours = "<2 Hours"
    elif cloud_data and isinstance(cloud_data, dict):
        # Agar cloud data available hai
        logged_hours = cloud_data.get('hours', '6+ Hours')

    # Quotes Mapping Logic
    quote = ""
    if logged_hours == "6+ Hours":
        quote = "⚡ ELITE SIGNAL! EXCELLENT EXECUTION. That is elite-level discipline. Your mind is acting like a high-performance data-science pipeline: clean, consistent, and relentlessly improving."
    elif logged_hours == "4-6 Hours":
        quote = "📉 STABLE TRAINING. Good baseline performance today. You kept the model steady, but to beat the competition, you need to push for hyperparameter tuning tomorrow!"
    elif logged_hours == "2-4 Hours":
        quote = "🚨 STRICT WARNING! Only 2-4 hours today? Ismita, Jayant, and Himanshu are working hard and leaving you behind. Wake up!"
    else:
        quote = "💥 CRITICAL FAILURE! Less than 2 hours? You are experiencing massive data drift. Ismita, Jayant, and Himanshu are accelerating while you are stalling. Fix this pipeline immediately!"

    # Agar Sunday raat hai toh weekly logic jodna
    if datetime.now().strftime('%A') == 'Sunday':
        quote += "\n\n📊 WEEKLY REPORT CARD: OVERFITTING DISCIPLINE (Elite)! Incredible week. You are dominating the leaderboard. Ismita, Jayant, and Himanshu have nothing on you this week."

    # Twilio client initiate karke message bhej dena
    if account_sid and auth_token and to_whatsapp:
        client = Client(account_sid, auth_token)
        # Formating recipient number
        clean_to = to_whatsapp.strip()
        if not clean_to.startswith('whatsapp:'):
            clean_to = f'whatsapp:{clean_to}'
            
        message = client.messages.create(
            body=quote,
            from_=from_whatsapp,
            to=clean_to
        )
        print(f"✅ Success! Message sent successfully. SID: {message.sid}")
    else:
        print("❌ Error: Twilio Credentials ya WhatsApp Number missing hai settings mein.")

if __name__ == "__main__":
    main()
