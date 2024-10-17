from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}

class StockProfile:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def get_stock_info(self):
        """Recupera informações de estoque para todos os produtos e suas máquinas de venda."""
        query = """
        SELECT 
            p.id AS product_id, 
            p.name AS product_name, 
            p.price AS product_price,
            p.quantity AS product_quantity,
            p.vending_machine_id AS vending_machine_id,
            vm.name AS vending_machine_name
        FROM 
            Products AS p
        JOIN 
            VendingMachines AS vm ON p.vending_machine_id = vm.id
        """
        self.cursor.execute(query)
        stock_info = self.cursor.fetchall()
        
        return [
            {
                'product_id': row[0],
                'product_name': row[1],
                'product_price': row[2],
                'product_quantity': row[3],
                'vending_machine_id': row[4],
                'vending_machine_name': row[5]
            }
            for row in stock_info
        ]

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.cursor.close()
        self.connection.close()

@app.route('/')
def index():
    return render_template('stock.html')

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    stock_profile = StockProfile(**db_config)
    stock_info = stock_profile.get_stock_info()
    stock_profile.close()
    return jsonify(stock_info)

if __name__ == "__main__":
    app.run(debug=True)
