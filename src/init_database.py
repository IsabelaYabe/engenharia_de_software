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

    



    print("Database initialized with mock data.")


def show_users(db_config):
    """
    Retrieves all users from the database.
    """

    manager = DatabaseManager(**db_config)
    cols = manager.get_cols("Users")
    users = manager.get_all("Users")
    print("Users:")
    for col in cols:
        print(col[0], end=" ")
    print()
    for user in users:
        print(user)
    
def show_vms(db_config):
    """
    Retrieves all vending machines from the database.
    """

    manager = DatabaseManager(**db_config)
    cols = manager.get_cols("VMs")
    vms = manager.get_all("VMs")
    print("Vending Machines:")
    for col in cols:
        print(col[0], end=" ")
    print()
    for vm in vms:
        print(vm)

def show_products(db_config):
    """
    Retrieves all products from the database.
    """

    manager = DatabaseManager(**db_config)
    cols = manager.get_cols("Products")
    products = manager.get_all("Products")
    print("Products:")
    for col in cols:
        print(col[0], end=" ")
    print()
    for product in products:
        print(product)

def show_complaints(db_config):
    """
    Retrieves all complaints from the database.
    """

    manager = DatabaseManager(**db_config)
    cols = manager.get_cols("Complaints")
    complaints = manager.get_all("Complaints")
    print("Complaints:")
    for col in cols:
        print(col[0], end=" ")
    print()
    for complaint in complaints:
        print(complaint)

def show_comments(db_config):
    """
    Retrieves all comments from the database.
    """

    manager = DatabaseManager(**db_config)
    cols = manager.get_cols("Comments")
    comments = manager.get_all("Comments")
    print("Comments:")
    for col in cols:
        print(col[0], end=" ")
    print()
    for comment in comments:
        print(comment)
    

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
    init_database(db_config)
    drop_database(db_config)