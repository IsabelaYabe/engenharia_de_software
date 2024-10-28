from flask import Flask, request, jsonify, render_template
from comment_profile import CommentProfile  

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
comment_profile = CommentProfile(**db_config)

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to add a comment
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

# Route to get comments for a product
@app.route('/get_comments/<int:product_id>', methods=['GET'])
def get_comments(product_id):
    comments = comment_profile.get_comments_by_product(product_id)
    return jsonify(comments)


if __name__ == '__main__':
    app.run(debug=True)
