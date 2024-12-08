from flask import Flask, request, jsonify, render_template, redirect, url_for
from database_manager_central import DatabaseManagerCentral
from flask_cors import CORS
from custom_logger import setup_logger

app = Flask(__name__)
CORS(app)

logger = setup_logger()
active_user = {
    "username": None,
    "user_type": None
}

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
    active_user['username'] = None
    active_user['user_type'] = None
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user_type = request.form['user-type']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    birthdate = request.form['birthdate']
    phone_number = request.form['phone-number']
    address = request.form['address']

    info = [username, email, password, first_name, last_name, birthdate, phone_number, address, 0]

    if password != confirm_password:
        return "Passwords do not match", 400

    manager = DatabaseManagerCentral(**db_config)
    if user_type == 'user':
        table = manager
        table.add_user(*info)

    elif user_type == 'owner':
        table = manager
        table.add_owner(*info)

        active_user['user_type'] = user_type
    active_user['username'] = username
    return redirect(url_for('menu'))
    
@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user-type']
    username = request.form['username']
    password = request.form['password']

    manager = DatabaseManagerCentral(**db_config)
    
    
    try:
        exists = manager.login_user(f"{user_type}s_profile", username, password)
        if not exists:
            return "Invalid username or password", 400
        active_user['user_type'] = user_type
        active_user['username'] = username
        return redirect(url_for('menu'))
    except ValueError as e:
        return str(e), 400


@app.route('/logout')
def logout():
    active_user = None
    return redirect(url_for('index'))

@app.route('/user_profile')
def user_profile():
    """
    Render the user profile page.
    """
    return render_template('user_profile.html')

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    """
    Endpoint for retrieving user information.
    """
    logger.debug(f"Active user: {active_user}")
    user_type = active_user['user_type']
    username = active_user['username']
    logger.debug(f"Getting info for {user_type} {username}")
    manager = DatabaseManagerCentral(**db_config)
    if user_type == 'user':
        table = manager.users_profile
    elif user_type == 'owner':
        table = manager.owners_profile
    info = table.search_record(username=username)
    logger.debug(f"User info: {info}")
    info = info[0]
    response = {
        "username": info[1],
        "email": info[2],
        "first_name": info[4],
        "last_name": info[5],
        "birthdate": info[6],
        "phone_number": info[7],
        "address": info[8],
        "budget": info[9],
        "user_type": user_type
    }
    return jsonify(response)


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
    data = request.json
    id = data['id']
    manager = DatabaseManagerCentral(**db_config)
    user = manager.users_profile.search_record(username=active_user['username'])
    if active_user['user_type'] == 'owner':
        return jsonify({"success": False, "error": "Owners cannot comment"})
    if not user:
        return jsonify({"success": False, "error": "User not found"})
    user_id = user[0][0]
    text = data['text']
    type = data['type']

    try:
        manager = DatabaseManagerCentral(**db_config)
        if type == 'product':
            comment_profile = manager.product_comment
            comment_profile.insert_row(text=text, product_id=id, user_id=user_id)
        elif type == 'vending_machine':
            comment_profile = manager.vending_machine_comment
            comment_profile.insert_row(text=text, vending_machine_id=id, user_id=user_id)
        comment_id = comment_profile.get_last_id()
        return jsonify({"success": True, "comment_id": comment_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})
    
# Route to get comments for a products
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
    

if __name__ == "__main__":
    app.run(debug=True)
