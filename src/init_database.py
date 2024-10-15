"""
    Module to initialize the database.

    It the tables and inserts mock data.

    Author: Rodrigo Kalil

    Date: 15/10/2024
"""
import mysql.connector
from database_manager import DatabaseManager

def init_database():
    """
    Initializes the database by creating the necessary tables and inserting mock data.
    """
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "nova_senha",
        "database": "my_database"
    }

    manager = DatabaseManager(**db_config)

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS VendingMachines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        owner_id INT NOT NULL,
        location VARCHAR(255) NOT NULL
    )
    """

    manager.create_table(create_table_sql)

    manager.insert_row("VendingMachines", ["name", "owner_id", "location"], ["Vending Machine 1", 1, "Building A"])
    manager.insert_row("VendingMachines", ["name", "owner_id", "location"], ["Vending Machine 2", 2, "Building B"])
    manager.insert_row("VendingMachines", ["name", "owner_id", "location"], ["Vending Machine 3", 2, "Building A"])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price FLOAT NOT NULL,
        quantity INT NOT NULL,
        vending_machine_id INT NOT NULL,
        FOREIGN KEY (vending_machine_id) REFERENCES VendingMachines(id)
    )
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Products", ["name", "price", "quantity", "vending_machine_id"], ["Coke", 2.5, 10, 1])
    manager.insert_row("Products", ["name", "price", "quantity", "vending_machine_id"], ["Pepsi", 2.5, 10, 1])
    manager.insert_row("Products", ["name", "price", "quantity", "vending_machine_id"], ["Chips", 1.5, 20, 2])
    manager.insert_row("Products", ["name", "price", "quantity", "vending_machine_id"], ["Chocolate", 2.0, 15, 2])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Complaints (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        vending_machine_id INT NOT NULL,
        text TEXT NOT NULL,
        FOREIGN KEY (vending_machine_id) REFERENCES VendingMachines(id)
    )
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Complaints", ["vending_machine_id", "text"], [1, "Out of stock"])
    manager.insert_row("Complaints", ["vending_machine_id", "text"], [2, "Machine not working"])
    manager.insert_row("Complaints", ["vending_machine_id", "text"], [3, "Wrong item dispensed"])

    print("Database initialized with mock data.")


def show_vms():
    """
    Retrieves all vending machines from the database.
    """
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "nova_senha",
        "database": "my_database"
    }

    manager = DatabaseManager(**db_config)
    cols = manager.get_cols("VendingMachines")
    vms = manager.get_all("VendingMachines")
    print("Vending Machines:")
    for col in cols:
        print(col[0], end=" ")
    print()
    for vm in vms:
        print(vm)
    

def drop_database():
    """
    Drops the database.
    """
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "nova_senha",
        "database": "my_database"
    }

    manager = DatabaseManager(**db_config)
    manager.delete_table("Complaints")
    manager.delete_table("Products")
    manager.delete_table("VendingMachines")

    conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS my_database;")
    cursor.close()
    conn.close()

    print("Database dropped.")




if __name__ == "__main__":
    init_database()
    show_vms()
    #drop_database()