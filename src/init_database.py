"""
    Module to initialize the database.

    It the tables and inserts mock data.

    Author: Rodrigo Kalil

    Date: 15/10/2024
"""
import mysql.connector
from database_manager_central import DatabaseManagerCentral
from custom_logger import setup_logger
from datetime import datetime

logger = setup_logger()

def init_database(db_config):
    """
    Initializes the database by creating the necessary tables and inserting mock data.
    """

    manager = DatabaseManagerCentral(**db_config)
    manager.show()

    print("Database initialized with mock data.")
    
def populate_database(db_config):

    manager = DatabaseManagerCentral(**db_config)

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
        logger.debug(f"Inserting user: {user}")
        manager.add_user(*user)
        logger.debug("User inserted.")

    logger.debug("Users inserted.")

    owners = [
        ["Garry", "g2@gmail.com", "sdf", "Gar", "Ry", "2024-12-05", "4002-8922", "Rua de Baixo", 52.0],
        ["Harry", "harry@example.com", "harry123", "Harry", "Potter", "2024-12-06", "4002-8923", "Rua de Cima", 62.0]
    ]

    for owner in owners:
        logger.debug(f"Inserting owner: {owner}")
        manager.add_owner(*owner)
    
    logger.debug("Owners inserted.")
    
    vms = [
        ["VM1", "Rua de Baixo", "1"],
        ["VM2", "Rua de Cima", "1"],
        ["VM3", "Rua do Meio", "2"]
    ]

    for vm in vms:
        logger.debug(f"Inserting vending machine: {vm}")
        manager.add_vending_machine(*vm)
        logger.debug("Vending machine inserted.")
    
    logger.debug("Vending machines inserted")

    products = [
        ["Coca-Cola", "Refrescante demais", 5.0, 10, 1],
        ["Pepsi", "Muito refrescante", 4.5, 15, 1],
        ["Fanta", "Sabor laranja", 4.0, 20, 2],
        ["Sprite", "Refrescante e limonada", 4.0, 25, 3],
        ["Guaraná", "Sabor original", 4.5, 30, 1],
        ["Água", "Mineral", 2.0, 50, 2],
        ["Suco de Laranja", "Natural", 3.5, 10, 3],
        ["Suco de Uva", "Natural", 3.5, 15, 1],
        ["Chá Gelado", "Sabor limão", 3.0, 20, 2],
        ["Energético", "Para dar energia", 6.0, 5, 3],
        ["Cerveja", "Gelada", 5.0, 10, 1]
    ]

    for product in products:
        logger.debug(f"Inserting product: {product}")
        manager.add_product(*product)
        logger.debug("Product inserted.")

    logger.debug("Products inserted.")

    product_complaint = [
        ["Produto vencido", 1, 2],
        ["Produto vencido", 2, 3],
        ["Produto vencido", 3, 1]
    ]

    for complaint in product_complaint:
        logger.debug(f"Inserting product complaint: {complaint}")
        manager.add_product_complaint(*complaint)
        logger.debug("Product complaint inserted.")

    logger.debug("Product complaints inserted.")

    product_comment = [
        ["Muito bom", 1, 2],
        ["Muito bom", 2, 3],
        ["Muito bom", 3, 1]
    ]

    for comment in product_comment:
        logger.debug(f"Inserting product comment: {comment}")
        manager.add_product_comment(*comment)
        logger.debug("Product comment inserted.")

    logger.debug("Product comments inserted.")

    vm_complaint = [
        ["Máquina quebrada", 1, 2],
        ["Máquina quebrada", 2, 3],
        ["Máquina quebrada", 3, 1]
    ]

    for complaint in vm_complaint:
        logger.debug(f"Inserting vending machine complaint: {complaint}")
        manager.add_vending_machine_complaint(*complaint)
        logger.debug("Vending machine complaint inserted.")

    logger.debug("Vending machine complaints inserted.")

    vm_comment = [
        ["Muito bom", 1, 2],
        ["Muito bom", 2, 3],
        ["Muito bom", 3, 1]
    ]

    for comment in vm_comment:
        logger.debug(f"Inserting vending machine comment: {comment}")
        manager.add_vending_machine_comment(*comment)
        logger.debug("Vending machine comment inserted.")

    logger.debug("Vending machine comments inserted.")

    pro_favorite = [
        [1, 1],
        [2, 2],
        [3, 3]
    ]

    for favorite in pro_favorite:
        logger.debug(f"Inserting product favorite: {favorite}")
        manager.add_favorite_product(*favorite)
        logger.debug("Product favorite inserted.")

    logger.debug("Product favorites inserted.")

    vm_favorite = [
        [1, 1],
        [2, 2],
        [3, 3]
    ]

    for favorite in vm_favorite:
        logger.debug(f"Inserting vending machine favorite: {favorite}")
        manager.add_favorite_vending_machine(*favorite)
        logger.debug("Vending machine favorite inserted.")

    logger.debug("Vending machine favorites inserted.")

    transactions = [
        [1, 1, 1, 3, 5.0],
        [2, 2, 1, 1, 4.5],
        [3, 3, 2, 5, 4.0]
    ]

    for transaction in transactions:
        logger.debug(f"Inserting transaction: {transaction}")
        manager.add_purchase_transaction(*transaction)
        logger.debug("Transaction inserted.")

    logger.debug("Transactions inserted.")



    manager.show()


def drop_database(db_config):
    """
    Drops the database.
    """

    # Load SQL script to drop tables
    try:
        with open("src\MYSQL\drop_tables_relationships.sql", "r") as file:
            logger.debug("Reading SQL script to drop tables.")
            drop_tables_sql = file.read()
    except FileNotFoundError:
        logger.error("SQL script file not found.")
        raise
    except Exception as e:
        logger.error(f"Error reading SQL script file: {e}")
        raise

    try:
        conn = mysql.connector.connect(**db_config)
        logger.debug("Successful connection")
    except mysql.connector.Error as e:
        logger.error("Unsuccessful connection: %s (errno=%d)", e.msg, e.errno)
        raise
    logger.info("Connected into database")

    # Execute the SQL script to drop tables
    with conn.cursor() as cursor:
        cursor.execute(drop_tables_sql)

    logger.debug("Database tables dropped successfully.")

    print("Database dropped.")




if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    #drop_database(db_config)
    init_database(db_config)
    print("iurbfquwcrhfcmpwoerjfh 94ufb pwrg fquirh qieb qwbrf iergnipqe fprh f hqrf iro roph oqwr ojwji"*3)
    populate_database(db_config)

    manager = DatabaseManagerCentral(**db_config)
    manager.update_vending_machine_status("1", "inactive")
    manager.update_owner_budget("1", 100.0)
    manager.add_product_quantity("1", "1", 200)
    print(manager.search_table("products_profile", quantity=15))
    print(manager.get_sales_report(datetime(2024, 12, 7, 00, 00, 00), datetime(2024, 12, 8, 00, 00, 00)))
    manager.withdraw_money_from_vm("1", "1", 10.0)
    print("\n\n\n\n")
    
    
    manager.show()

    items = manager.vending_machines_profile.show_table()
    print(items)
    