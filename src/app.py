from flask import Flask, jsonify, render_template
from profiles.stock_profile import StockProfile
from profiles.vms_profile import VMProfile

app = Flask(__name__)

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
    stock_profile = StockProfile(**db_config)
    stock_info = stock_profile.get_stock_info()
    stock_profile.close()
    return jsonify(stock_info)

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
    vm_profile = VMProfile(**db_config)
    vm_info = vm_profile.get_vm_info()
    vm_profile.close()
    return jsonify(vm_info)

if __name__ == "__main__":
    app.run(debug=True)
