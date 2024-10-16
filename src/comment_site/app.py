from flask import Flask, request, jsonify, render_template
from comment_profile import CommentProfile  
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
comment_profile = CommentProfile(**db_config)

# Rota para servir o arquivo index.html
@app.route('/')
def index():
    return render_template('index.html')

# Rota para adicionar um comentário
@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    product_id = data['product_id']
    user_id = data['user_id']
    text = data['text']

    try:
        comment_id = comment_profile.create_comment(product_id, user_id, text)
        return jsonify({"success": True, "comment_id": comment_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})

# Rota para buscar comentários por produto
@app.route('/get_comments/<int:product_id>', methods=['GET'])
def get_comments(product_id):
    comments = comment_profile.get_comments_by_product(product_id)
    return jsonify(comments)

# Nova rota para verificar palavras banidas
@app.route('/check_banned_words', methods=['POST'])
def check_banned_words():
    data = request.json
    text = data['text']
    
    contains_banned = contains_banned_words(text)
    return jsonify({"contains_banned_words": contains_banned})

if __name__ == '__main__':
    app.run(debug=True)
