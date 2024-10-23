from flask import Flask, jsonify, render_template
from stock_profile import StockProfile  # Importando a classe StockProfile

app = Flask(__name__)

# Configurações de banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}

@app.route('/')
def index():
    """Renderiza a página principal de informações de estoque."""
    return render_template('stock.html')

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    """
    Endpoint da API para recuperar informações de estoque.

    Retorna:
        jsonify: Resposta JSON contendo informações de estoque de todos os produtos.
    """
    stock_profile = StockProfile(**db_config)  # Usando a classe importada
    stock_info = stock_profile.get_stock_info()
    stock_profile.close()
    return jsonify(stock_info)

if __name__ == "__main__":
    app.run(debug=True)
