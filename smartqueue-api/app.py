from flask import Flask, request, jsonify, send_file
import redis
import json

app = Flask(__name__)

# Connect to our new internal Kubernetes Redis service
r = redis.Redis(host='redis-service', port=6379, decode_responses=True)

# Initialize default values if Redis is completely empty
if not r.exists("facility_status"):
    r.set("facility_status", "Active")
    r.set("last_issued_token", "0")
    r.set("currently_serving", "0")

@app.route('/', methods=['GET'])
def serve_patient_portal():
    return send_file('index.html')

@app.route('/admin', methods=['GET'])
def serve_admin_portal():
    return send_file('admin.html')

@app.route('/book', methods=['POST'])
def book_ticket():
    status = r.get("facility_status")
    if status == "Closed":
        return jsonify({"error": "Facility is currently closed."}), 403

    data = request.json
    
    # Atomically increment the token number in Redis
    new_token = r.incr("last_issued_token")
    
    patient_info = {
        "token": new_token,
        "name": data.get("patient_name"),
        "department": data.get("department")
    }
    
    # Push the new patient onto the right side of the Redis Queue (list)
    r.rpush("queue", json.dumps(patient_info))
    
    return jsonify({"message": "Booking successful", "patient": patient_info}), 200

@app.route('/status', methods=['GET'])
def get_status():
    queue_length = r.llen("queue")
    
    # Peek at the first patient in the queue without removing them
    next_patient_str = r.lindex("queue", 0)
    next_patient = json.loads(next_patient_str) if next_patient_str else None
    
    return jsonify({
        "currently_serving": int(r.get("currently_serving") or 0),
        "facility_status": r.get("facility_status"),
        "queue_length": queue_length,
        "next_patient": next_patient
    }), 200

@app.route('/admin/action', methods=['POST'])
def admin_action():
    action = request.json.get("action")
    
    if action == "Admit":
        # Pop the patient off the left side of the Redis Queue
        patient_str = r.lpop("queue")
        if patient_str:
            patient_data = json.loads(patient_str)
            r.set("currently_serving", patient_data["token"])
        r.set("facility_status", "Active")
        
    elif action == "Break":
        r.set("facility_status", "On Break")
    elif action == "Close":
        r.set("facility_status", "Closed")
        
    return jsonify({"message": "Status updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)