"""
    Module to initialize the database.

    It the tables and inserts mock data.

    Author: Rodrigo Kalil

    Date: 15/10/2024
"""
import mysql.connector
from database_manager_central import DatabaseManagerCentral

def init_database(db_config):
    """
    Initializes the database by creating the necessary tables and inserting mock data.
    """

    manager = DatabaseManagerCentral(**db_config)
    manager.show()

    print("Database initialized with mock data.")
    
def populate_database(db_config):

    manager = DatabaseManagerCentral(**db_config)
    manager.create_tables()

    # Inserting mock data
    users = [
    ["Al1ce", "alicinha@gmail.com", "alqqq", "Alice", "Silva", "2024-12-07", "pizzaria_buonasserra", "Rua de Baixo", 50.0],
    ["Bob", "bob@example.com", "bob123", "Bob", "Smith", "2024-12-07", "pizzaria_buonasserra", "Rua de Cima", 60.0],
    ["Charlie", "charlie@example.com", "charlie123", "Charlie", "Brown", "2024-12-07", "pizzaria_buonasserra", "Rua do Meio", 70.0],
    ["David", "david@example.com", "david123", "David", "Johnson", "2024-12-07", "pizzaria_buonasserra", "Rua Nova", 80.0],
    ["Eve", "eve@example.com", "eve123", "Eve", "Davis", "2024-12-07", "pizzaria_buonasserra", "Rua Velha", 90.0],
    ["Frank", "frank@example.com", "frank123", "Frank", "Miller", "2024-12-06", "pizzaria_buonasserra", "Rua Alta", 100.0]
    ]

    for user in users:
        manager.add_user(*user)

    owners = [
        ["Garry", "g2@gmail.com", "sdf", "Gar", "Ry", "2024-12-05", "4002-8922", "Rua de Baixo", 52.0],
        ["Harry", "harry@example.com", "harry123", "Harry", "Potter", "2024-12-06", "4002-8923", "Rua de Cima", 62.0]
    ]

    for owner in owners:
        manager.add_owner(*owner)
    
    vms = [
        ["VM1", "Rua de Baixo", "13"],
        ["VM2", "Rua de Cima", "13"],
        ["VM3", "Rua do Meio", "14"]
    ]

    for vm in vms:
        manager.add_vending_machine(*vm)

    manager.show()


def drop_database(db_config):
    """
    Drops the database.
    """

    manager = DatabaseManagerCentral(**db_config)
    manager.drop_tables()

    print("Database dropped.")




if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    drop_database(db_config)
    init_database(db_config)
    populate_database(db_config)