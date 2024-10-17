
from flask import Flask, request, jsonify, render_template
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from complaint_profile import Complaint  # Now imports the Complaint class
from utils import contains_banned_words
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}
complaint_manager = Complaint(**db_config)  # Instantiate the Complaint class

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('complaints_viewer_manager.html')

# Route to add a complaint
@app.route('/add_complaint', methods=['POST'])
def add_complaint():
    data = request.json
    vending_machine_id = data['vending_machine_id']
    text = data['text']

    try:
        complaint_id = complaint_manager.create_complaint(vending_machine_id, text)
        return jsonify({"success": True, "complaint_id": complaint_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    try:
        complaints = complaint_manager.get_all_complaints()  # Ensure the method from the class is implemented correctly
        return jsonify(complaints)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error message

# New route to check banned words (maintaining the same logic)
@app.route('/check_banned_words', methods=['POST'])
def check_banned_words():
    data = request.json
    text = data['text']
    
    contains_banned = contains_banned_words(text)
    return jsonify({"contains_banned_words": contains_banned})

if __name__ == '__main__':
    app.run(debug=True)
