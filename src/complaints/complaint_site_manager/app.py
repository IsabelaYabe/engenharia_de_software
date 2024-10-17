from flask import Flask, request, jsonify, render_template
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from complaint_profile import Complaint  # Agora importa a classe Complaint
from utils import contains_banned_words
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}
complaint_manager = Complaint(**db_config)  # Instancia a classe Complaint

# Rota para servir o arquivo index.html
@app.route('/')
def index():
    return render_template('complaints_viewer_manager.html')

# Rota para adicionar uma reclamação
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

# Rota para buscar reclamações por vending machine
@app.route('/get_complaints/<int:vending_machine_id>', methods=['GET'])
def get_complaints(vending_machine_id):
    complaints = complaint_manager.get_complaints_by_vending_machine(vending_machine_id)
    return jsonify(complaints)

@app.route('/get_all_complaints', methods=['GET'])
def get_all_complaints():
    complaints = complaint_manager.get_all_complaints()  # Método que retorna todas as reclamações
    return jsonify(complaints)

# Nova rota para verificar palavras banidas (mantendo a mesma lógica)
@app.route('/check_banned_words', methods=['POST'])
def check_banned_words():
    data = request.json
    text = data['text']
    
    contains_banned = contains_banned_words(text)
    return jsonify({"contains_banned_words": contains_banned})

if __name__ == '__main__':
    app.run(debug=True)
