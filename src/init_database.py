from database_manager_central import DatabaseManagerCentral

def init_database():
    """
    Initializes the database by creating the necessary tables and populating them with initial data.
    """
    host = "localhost"
    user = "root"
    password = "134351"
    database = "my_database"

    db_manager = DatabaseManagerCentral(host, user, password, database)

    db_manager._create_all_tables()

    id = db_manager.product_manager.create_product(
        name="Coke",
        description="Refreshing soda",
        price=2.50,
        quantity=10
    )

    print(f"Product {id} added to the database.")

if __name__ == "__main__":
    init_database()
