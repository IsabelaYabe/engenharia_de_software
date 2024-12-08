from flask import Flask, request, jsonify, render_template
from database_manager_central import DatabaseManagerCentral
from flask_cors import CORS
from custom_logger import setup_logger

app = Flask(__name__)
CORS(app)

logger = setup_logger()

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}

@app.route('/')
def index():
    """
    Render the home page with buttons to other pages.
    """
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user_type = request.form['user_type']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        return "Passwords do not match", 400

    manager = DatabaseManagerCentral(**db_config)
    if user_type == 'user':
        table = manager.users_profile
    elif user_type == 'owner':
        table = manager.owners_profile
    pass
    try:
        table.insert_row(username=username, password=password)

    return redirect(url_for('home'))


@app.route('/menu')
def menu():
    """
    Render the menu page.
    """
    return render_template('menu.html')

@app.route('/stock')
def stock():
    """
    Render the stock page.
    """
    return render_template('stock.html')

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    """
    Endpoint for retrieving stock information about products and their associated vending machines.
    """
    pass

@app.route('/vms')
def vms():
    """
    Render the vending machines page.
    """
    return render_template('vms.html')

@app.route('/get_vm_info', methods=['GET'])
def get_vm_info():
    """
    Endpoint for retrieving vending machine information.
    """
    manager = DatabaseManagerCentral(**db_config)
    table = manager.vending_machines_profile
    info = table.get_info()
    logger.debug(f"Vending machines info: {info}")
    return jsonify({"header": info["head"], "data": info["rows"]})

@app.route('/vm_profile/<int:vm_id>')
def vm_profile(vm_id):
    """
    Render the vending machine profile page.
    """
    return render_template('vm_profile.html', vm_id=vm_id)

@app.route('/get_vm_products/<int:vm_id>', methods=['GET'])
def get_vm_products(vm_id):
    """
    Endpoint for retrieving vending machine products.
    """
    manager = DatabaseManagerCentral(**db_config)
    table = manager.products_profile
    info = table.search_record(vending_machine_id = vm_id)
    logger.debug(f"Products of vm {vm_id}: {info}")
    return jsonify({"data": info})

@app.route('/comment')
def comment():
    """
    Render the comment page.
    """
    return render_template('comment.html')

# Route to add a comment
@app.route('/add_comment', methods=['POST'])
def add_comment():
    pass

    data = request.json
    id = data['product_id']
    user_id = data['user_id']
    text = data['text']
    tipe = data['type']

    try:
        manager = DatabaseManagerCentral(**db_config)
        if tipe == 'product':
            comment_profile = manager.product_comment
        elif tipe == 'vending_machine':
            comment_profile = manager.vending_machine_comment
        comment_id = comment_profile.insert_row(id=id, user_id=user_id, text=text)
        return jsonify({"success": True, "comment_id": comment_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})
    
# Route to get comments for a product
@app.route('/get_comments/<int:product_id>', methods=['GET'])
def get_comments(product_id):
    pass

# Route to the complaints page for commun users
@app.route('/complaint')
def complaints():
    return render_template('complaints.html')

# Route to add a complaint
@app.route('/add_complaint', methods=['POST'])
def add_complaint():
    pass
    """data = request.json
    vending_machine_id = data.get('vending_machine_id')  # Usa get para evitar KeyError
    user_id = data.get('user_id')  # Usa get para evitar KeyError
    text = data.get('text')  # Usa get para evitar KeyError

    try:
        complaint_manager = Complaint(**db_config)
        complaint_id = complaint_manager.create_complaint(user_id, vending_machine_id, text)  # Alterado a ordem dos parâmetros
        return jsonify({"success": True, "complaint_id": complaint_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})"""



# Route to the complaints page for admin users
@app.route('/admin_complaints')
def admin_complaints():
    return render_template('complaints_viewer_manager.html')


# Route to get complaints 
@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    pass

#Register a new user and login
    

if __name__ == "__main__":
    app.run(debug=True)
