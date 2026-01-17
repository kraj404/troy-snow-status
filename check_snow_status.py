import argparse
import time
import json
import urllib.request
import sys
import os

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

def send_notification(title, message):
    """Sends a desktop notification on macOS using osascript."""
    try:
        # Escape double quotes in title and message
        title = title.replace('"', '\\"')
        message = message.replace('"', '\\"')
        
        cmd = f'osascript -e "display notification \\"{message}\\" with title \\"{title}\\""'
        os.system(cmd)
    except Exception as e:
        print(f"Failed to send notification: {e}")

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
                    print("Section Completed! Sending notification...")
                    send_notification("Snow Cleaning Complete", f"Section {section_id} is now COMPLETED.")
                    break
                
                time.sleep(args.poll)
        except KeyboardInterrupt:
            print("\nPolling stopped.")
    else:
        status = get_snow_status(section_id)
        print(f"Status: {status}")

if __name__ == "__main__":
    main()
