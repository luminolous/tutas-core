from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Data storage files
REGISTRATIONS_FILE = 'data/registrations.json'
MATCHED_PAIRS_FILE = 'data/matched_pairs.json'
STUDY_GROUPS_FILE = 'data/study_groups.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def load_json_file(filename):
    """Load data from JSON file, return empty list if file doesn't exist"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json_file(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def initialize_sample_data():
    """Initialize sample data if files don't exist"""
    
    # Sample matched pairs
    if not os.path.exists(MATCHED_PAIRS_FILE):
        sample_pairs = [
            {
                "id": "pair_1",
                "tutorName": "Dr. Sarah Johnson",
                "studentName": "Alice Chen",
                "subject": "Mathematics",
                "subtopic": "Calculus and derivatives",
                "schedule": "Monday, Wednesday 2:00 PM",
                "learningMode": "Online",
                "tutorWhatsapp": "+6281234567890",
                "studentWhatsapp": "+6281234567891"
            },
            {
                "id": "pair_2",
                "tutorName": "Prof. Michael Davis",
                "studentName": "Bob Wilson",
                "subject": "Physics",
                "subtopic": "Quantum mechanics basics",
                "schedule": "Tuesday, Thursday 10:00 AM",
                "learningMode": "Online, Offline near ITS",
                "tutorWhatsapp": "+6281234567892",
                "studentWhatsapp": "+6281234567893"
            },
            {
                "id": "pair_3",
                "tutorName": "Dr. Emily Rodriguez",
                "studentName": "Charlie Brown",
                "subject": "Programming",
                "subtopic": "Python for Data Science",
                "schedule": "Friday 3:00 PM",
                "learningMode": "Online, Chat",
                "tutorWhatsapp": "+6281234567894",
                "studentWhatsapp": "+6281234567895"
            }
        ]
        save_json_file(MATCHED_PAIRS_FILE, sample_pairs)
    
    # Sample study groups
    if not os.path.exists(STUDY_GROUPS_FILE):
        sample_groups = [
            {
                "id": "group_1",
                "courseName": "Mathematics",
                "subtopic": "Advanced Calculus and Mathematical Analysis",
                "tutor": {
                    "name": "Dr. Sarah Johnson",
                    "whatsapp": "+6281234567890"
                },
                "students": [
                    {"name": "Alice Chen", "whatsapp": "+6281234567891"},
                    {"name": "David Kim", "whatsapp": "+6281234567896"},
                    {"name": "Eva Martinez", "whatsapp": "+6281234567897"}
                ],
                "schedule": "Monday, Wednesday, Friday at 2:00 PM",
                "learningMode": "Online",
                "maxStudents": 5
            },
            {
                "id": "group_2",
                "courseName": "Physics",
                "subtopic": "Quantum Mechanics and Modern Physics",
                "tutor": {
                    "name": "Prof. Michael Davis",
                    "whatsapp": "+6281234567892"
                },
                "students": [
                    {"name": "Bob Wilson", "whatsapp": "+6281234567893"},
                    {"name": "Frank Miller", "whatsapp": "+6281234567898"},
                    {"name": "Grace Lee", "whatsapp": "+6281234567899"},
                    {"name": "Henry Zhang", "whatsapp": "+6281234567800"}
                ],
                "schedule": "Tuesday, Thursday at 10:00 AM",
                "learningMode": "Online, Offline near ITS",
                "maxStudents": 5
            },
            {
                "id": "group_3",
                "courseName": "Programming",
                "subtopic": "Full-Stack Web Development with React and Node.js",
                "tutor": {
                    "name": "Dr. Emily Rodriguez",
                    "whatsapp": "+6281234567894"
                },
                "students": [
                    {"name": "Charlie Brown", "whatsapp": "+6281234567895"},
                    {"name": "Ivy Chen", "whatsapp": "+6281234567801"}
                ],
                "schedule": "Saturday at 9:00 AM",
                "learningMode": "Online, Chat",
                "maxStudents": 5
            }
        ]
        save_json_file(STUDY_GROUPS_FILE, sample_groups)

@app.route('/submit', methods=['POST'])
def submit_registration():
    """Handle registration form submission"""
    try:
        data = request.get_json()
        
        # Add unique ID and timestamp
        registration = {
            'id': str(uuid.uuid4()),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'fullName': data.get('fullName'),
            'whatsappNumber': data.get('whatsappNumber'),
            'status': data.get('status'),
            'courseName': data.get('courseName'),
            'topicSubtopic': data.get('topicSubtopic'),
            'preferredDate': data.get('preferredDate'),
            'preferredTime': data.get('preferredTime'),
            'flexibleSchedule': data.get('flexibleSchedule'),
            'learningStyle': data.get('learningStyle'),
            'learningMode': data.get('learningMode'),
            'matchingType': data.get('matchingType'),
            'statusProses': ''  # Empty by default
        }
        
        # Load existing registrations
        registrations = load_json_file(REGISTRATIONS_FILE)
        
        # Add new registration
        registrations.append(registration)
        
        # Save updated registrations
        save_json_file(REGISTRATIONS_FILE, registrations)
        
        return jsonify({
            'success': True,
            'message': 'Registration submitted successfully',
            'id': registration['id']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing registration: {str(e)}'
        }), 500

@app.route('/available', methods=['GET'])
def get_available_pairs():
    """Get matched 1-on-1 pairs"""
    try:
        matched_pairs = load_json_file(MATCHED_PAIRS_FILE)
        
        return jsonify({
            'success': True,
            'matched_pairs': matched_pairs,
            'count': len(matched_pairs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching matched pairs: {str(e)}',
            'matched_pairs': []
        }), 500

@app.route('/tutas-circle', methods=['GET'])
def get_study_groups():
    """Get Tutas Circle study groups"""
    try:
        study_groups = load_json_file(STUDY_GROUPS_FILE)
        
        return jsonify({
            'success': True,
            'study_groups': study_groups,
            'count': len(study_groups)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching study groups: {str(e)}',
            'study_groups': []
        }), 500

@app.route('/registrations', methods=['GET'])
def get_registrations():
    """Get all registrations (for admin purposes)"""
    try:
        registrations = load_json_file(REGISTRATIONS_FILE)
        
        return jsonify({
            'success': True,
            'registrations': registrations,
            'count': len(registrations)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching registrations: {str(e)}',
            'registrations': []
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Tutas Flask backend is running',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    # Initialize sample data on startup
    initialize_sample_data()
    
    print("🚀 Starting Tutas Flask Backend...")
    print("📝 Registration endpoint: http://localhost:5000/submit")
    print("👥 Available pairs endpoint: http://localhost:5000/available")
    print("🔄 Tutas Circle endpoint: http://localhost:5000/tutas-circle")
    print("💚 Health check: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
