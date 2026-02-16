import schedule
import time
import requests
from datetime import datetime

def cleanup_old_history():
    """Cleanup chat history older than 7 days"""
    try:
        response = requests.delete('http://localhost:8000/api/kb/0/history/cleanup')
        if response.status_code == 200:
            result = response.json()
            print(f"[{datetime.now()}] {result['message']}")
        else:
            print(f"[{datetime.now()}] Cleanup failed: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Cleanup error: {str(e)}")

# Schedule cleanup daily at 2 AM
schedule.every().day.at("02:00").do(cleanup_old_history)

print("Cleanup scheduler started. Running daily at 2:00 AM...")
print("Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)
