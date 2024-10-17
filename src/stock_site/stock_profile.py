import mysql.connector

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
        """
        Retrieves stock information for all products and their vending machines.

        Returns:
            stock_info (list): A list of dictionaries containing stock details.
        """
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
        """Closes the database connection."""
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    stock_profile = StockProfile(**db_config)
    stock_info = stock_profile.get_stock_info()
    for stock in stock_info:
        print(stock)

    stock_profile.close()
