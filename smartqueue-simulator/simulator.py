import time
import json
import random
from datetime import datetime, timezone
from google.cloud import storage
import uuid

# Your newly created bucket name
BUCKET_NAME = "smartqueue-raw-logs-495820"
DEPARTMENTS = ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "General"]

def generate_and_upload():
    # Initialize the GCS client
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    
    while True:
        # Task T2.1: Data Design Schema
        event_data = {
            "patient_id": str(uuid.uuid4())[:8],
            "dept": random.choice(DEPARTMENTS),
            "check_in": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "wait_min": random.randint(5, 120),
            "doctor_id": f"DR-{random.randint(10,99)}",
            "region": "Pakistan"
        }
        
        # Create a unique filename
        file_name = f"visit_{event_data['patient_id']}_{int(time.time())}.json"
        blob = bucket.blob(file_name)
        
        # Upload the JSON string to GCS
        blob.upload_from_string(json.dumps(event_data), content_type="application/json")
        print(f"Uploaded {file_name} to {BUCKET_NAME}")
        
        # Wait 30 seconds before generating the next event
        time.sleep(0.1)

if __name__ == "__main__":
    print(f"Starting SmartQueue Simulator...")
    print(f"Uploading synthetic data to gs://{BUCKET_NAME} every 30s...")
    generate_and_upload()