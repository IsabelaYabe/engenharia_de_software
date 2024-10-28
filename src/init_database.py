"""
    Module to initialize the database.

    It the tables and inserts mock data.

    Author: Rodrigo Kalil

    Date: 15/10/2024
"""
import mysql.connector
from database_manager import DatabaseManager

def init_database(db_config):
    """
    Initializes the database by creating the necessary tables and inserting mock data.
    """

    manager = DatabaseManager(**db_config)

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Users", ["name", "email", "password"], ["Alice", "Alice@gmail.com", "123456"])
    manager.insert_row("Users", ["name", "email", "password"], ["Bob", "Bob@gmail.com", "123456"])
    manager.insert_row("Users", ["name", "email", "password"], ["Charlie", "Charlie@gmail.com", "123456"])


    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Owner
        (
        OwnerID INT AUTO_INCREMENT,
        PRIMARY KEY (OwnerID)
        );
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Owner", ["OwnerID"], [1])
    manager.insert_row("Owner", ["OwnerID"], [2])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS User
        (
        UserID INT AUTO_INCREMENT,
        PRIMARY KEY (UserID)
        );
    """

    manager.create_table(create_table_sql)

    manager.insert_row("User", ["UserID"], [1])
    manager.insert_row("User", ["UserID"], [2])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS VMs
        (
        VMID INT AUTO_INCREMENT,
        Name VARCHAR(30) NOT NULL,
        Location VARCHAR(50) NOT NULL,
        OwnerID INT NOT NULL,
        Status VARCHAR(10) DEFAULT 'active',
        PRIMARY KEY (VMID),
        FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID)
);
    """

    manager.create_table(create_table_sql)

    manager.insert_row("VMs", ["Name", "Location", "OwnerID"], ["Máquina de café", "14 Andar", 1])
    manager.insert_row("VMs", ["Name", "Location", "OwnerID"], ["Wizmart", "Saguão", 1])
    manager.insert_row("VMs", ["Name", "Location", "OwnerID"], ["Cesta de brownies", "4 Andar", 2])


    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Products
        (
        ProductID INT AUTO_INCREMENT,
        Name VARCHAR(30) NOT NULL,
        Description VARCHAR(100) NOT NULL,
        Price FLOAT NOT NULL,
        Quantity INT,
        VMID INT NOT NULL,
        PRIMARY KEY (ProductID),
        FOREIGN KEY (VMID) REFERENCES VMs(VMID)
        );
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Products", ["Name", "Description", "Price", "VMID"], ["Café curto", "Café numa quantidade pequena", 0.0, 1])
    manager.insert_row("Products", ["Name", "Description", "Price", "VMID"], ["Café longo", "Café numa quantidade maior", 0.0, 1])
    manager.insert_row("Products", ["Name", "Description", "Price", "VMID"], ["Capuccino", "Bebida de café, leite e canela", 2.5, 1])
    manager.insert_row("Products", ["Name", "Description", "Price", "Quantity", "VMID"], ["Água", "H2O", 4.0, 5, 2])
    manager.insert_row("Products", ["Name", "Description", "Price", "Quantity", "VMID"], ["Brownie", "Delicioso bolo de chocolate caseiro", 5.0, 12, 3])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Complaints
        (
        ComplaintID INT AUTO_INCREMENT,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Text VARCHAR(250) NOT NULL,
        VMID INT,
        PRIMARY KEY (ComplaintID),
        FOREIGN KEY (VMID) REFERENCES VMs(VMID)
        );
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Complaints", ["Text", "VMID"], ["Tá sem açúcasr.", 1])
    manager.insert_row("Complaints", ["Text", "VMID"], ["Esse café tá aguado", 1])
    manager.insert_row("Complaints", ["Text", "VMID"], ["Água cara", 2])
    manager.insert_row("Complaints", ["Text", "VMID"], ["Não aceitou meu vale refeição", 2])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Comments
        (
        CommentID INT AUTO_INCREMENT,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Text VARCHAR(250) NOT NULL,
        ProductID INT NOT NULL,
        UserID INT NOT NULL,
        PRIMARY KEY (CommentID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
        FOREIGN KEY (UserID) REFERENCES User(UserID)
        );
    """

    manager.create_table(create_table_sql)

    manager.insert_row("Comments", ["Text", "ProductID", "UserID"], ["Não tem como começar o dia sem.", 1, 1])
    manager.insert_row("Comments", ["Text", "ProductID", "UserID"], ["Estavam deliciosos", 5, 1])
    manager.insert_row("Comments", ["Text", "ProductID", "UserID"], ["Até que é bom.", 3, 2])
    manager.insert_row("Comments", ["Text", "ProductID", "UserID"], ["Beba água", 4, 2])



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

    manager = DatabaseManager(**db_config)
    manager.delete_table("Complaints")
    manager.delete_table("Comments")
    manager.delete_table("Products")
    manager.delete_table("VMs")
    manager.delete_table("Owner")
    manager.delete_table("User")

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
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    drop_database(db_config)
    init_database(db_config)
    show_users(db_config)
    show_vms(db_config)
    show_products(db_config)
    show_complaints(db_config)
    show_comments(db_config)
