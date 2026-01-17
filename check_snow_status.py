import argparse
import time
import json
import urllib.request
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file if it exists
def load_env():
    env_vars = {}
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

ENV = load_env()

def get_snow_status(section_id):
    base_url = "https://gis1.troymi.gov/server/rest/services/Snow_Plow/MapServer/2/query"
    params = {
        "where": f"SECTIONNUMBER='{section_id}'",
        "outFields": "STATUS,SECTIONNUMBER",
        "f": "json"
    }
    
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                return "ERROR: API returned status code " + str(response.status)
            
            data = json.loads(response.read().decode())
            
            if "features" in data and len(data["features"]) > 0:
                return data["features"][0]["attributes"]["STATUS"]
            else:
                return "NOT FOUND"
                
    except Exception as e:
        return f"ERROR: {str(e)}"

def send_desktop_notification(title, message):
    """Sends a desktop notification on macOS using osascript."""
    try:
        # Escape double quotes in title and message
        title = title.replace('"', '\\"')
        message = message.replace('"', '\\"')
        
        cmd = f'osascript -e "display notification \\"{message}\\" with title \\"{title}\\""'
        os.system(cmd)
    except Exception as e:
        print(f"Failed to send desktop notification: {e}")

def send_email_notification(section_id):
    """Sends an email notification using SMTP."""
    if ENV.get('EMAIL_ENABLED', 'false').lower() != 'true':
        return
    
    try:
        email_from = ENV.get('EMAIL_FROM')
        email_to = ENV.get('EMAIL_TO')
        email_password = ENV.get('EMAIL_PASSWORD')
        smtp_server = ENV.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(ENV.get('SMTP_PORT', '587'))
        
        if not all([email_from, email_to, email_password]):
            print("Email credentials not configured. Skipping email notification.")
            return
        
        subject = f"Troy Snow Cleaning Complete - Section {section_id}"
        body = f"Good news! Snow cleaning for Section {section_id} has been completed."
        
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
        
        print(f"Email notification sent to {email_to}")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def send_twitter_notification(section_id):
    """Posts a tweet about the snow cleaning completion."""
    if ENV.get('TWITTER_ENABLED', 'false').lower() != 'true':
        return
    
    try:
        # Try to import tweepy
        try:
            import tweepy
        except ImportError:
            print("tweepy not installed. Run: pip install tweepy")
            print("Skipping Twitter notification.")
            return
        
        api_key = ENV.get('TWITTER_API_KEY')
        api_secret = ENV.get('TWITTER_API_SECRET')
        access_token = ENV.get('TWITTER_ACCESS_TOKEN')
        access_secret = ENV.get('TWITTER_ACCESS_SECRET')
        
        if not all([api_key, api_secret, access_token, access_secret]):
            print("Twitter credentials not configured. Skipping Twitter notification.")
            return
        
        # Authenticate with Twitter API v2
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        tweet_text = f"🚨 Snow cleaning complete for Section {section_id} in Troy, MI! ❄️ #TroyMI #SnowRemoval"
        
        response = client.create_tweet(text=tweet_text)
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Failed to send Twitter notification: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check Troy Snow Cleaning Status")
    parser.add_argument("--section", type=str, required=True, help="Section number to check")
    parser.add_argument("--poll", type=int, help="Polling interval in seconds (e.g., 60). If not set, checks once.")
    
    args = parser.parse_args()
    section_id = args.section
    
    print(f"Checking status for Section {section_id}...")
    
    if args.poll:
        print(f"Polling every {args.poll} seconds. Press Ctrl+C to stop.")
        try:
            while True:
                status = get_snow_status(section_id)
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] Status: {status}")
                
                if status.upper() == "COMPLETED":
                    print("Section Completed! Sending notifications...")
                    send_desktop_notification("Snow Cleaning Complete", f"Section {section_id} is now COMPLETED.")
                    send_email_notification(section_id)
                    send_twitter_notification(section_id)
                    break
                
                time.sleep(args.poll)
        except KeyboardInterrupt:
            print("\nPolling stopped.")
    else:
        status = get_snow_status(section_id)
        print(f"Status: {status}")

if __name__ == "__main__":
    main()
