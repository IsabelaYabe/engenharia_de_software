""" 
Module for the Flask application.

This module provides an API endpoint for retrieving stock information about products and their associated vending machines.

Author: Lavinia Dias

Date: 23/10/2024
"""


from flask import Flask, jsonify, render_template
from stock_profile import StockProfile  

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
    Render the home page.

    Returns:
        render_template: Template for the home page.
    """
    return render_template('stock.html')

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    """
    Endpoint for retrieving stock information about products and their associated vending machines.

    Returns:
        jsonify: JSON response containing stock information.
    """
    stock_profile = StockProfile(**db_config)  # Usando a classe importada
    stock_info = stock_profile.get_stock_info()
    stock_profile.close()
    return jsonify(stock_info)

if __name__ == "__main__":
    app.run(debug=True)
