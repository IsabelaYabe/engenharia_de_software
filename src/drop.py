"""
    Module to initialize the database.

    It the tables and inserts mock data.

    Author: Rodrigo Kalil

    Date: 15/10/2024
"""
import mysql.connector
from database_manager_central import DatabaseManagerCentral
from custom_logger import setup_logger

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


    manager.show()


def drop_database(db_config):
    """
    Drops the database.
    """
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
    drop_database(db_config)
    #init_database(db_config)
    #print("iurbfquwcrhfcmpwoerjfh 94ufb pwrg fquirh qieb qwbrf iergnipqe fprh f hqrf iro roph oqwr ojwji"*3)
    #populate_database(db_config)