"""
    Module for creating the DatabaseManagerCentral class.

    Author: Isabela Yabe
    Last Modified: 03/11/2024
    Status: cagado

    Dependencies:
        - product_profile
        - decorators
        - tables
"""
from database_manager_refactoring import DatabaseManager, ConfigClass
from decorators_method import singleton

@singleton
class DatabaseManagerCentral:
    """
    DatabaseManagerCentral class.
    
    This class provides a central manager for all the individual table managers.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the central manager with table-specific managers.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.products_config = ConfigClass(self.host, self.user, self.password, self.database, "products_profile", ["id", "name", "description", "price", "quantity"], "id")
        self.products_profile = DatabaseManager(self.products_config)

        self.comments_config = ConfigClass(self.host, self.user, self.password, self.database, "comments_profile", ["id", "text", "timestamp"], "id")
        self.comments_profile = DatabaseManager(self.comments_config)
        
        self.users_config = ConfigClass(self.host, self.user, self.password, self.database, "users_profile", ["id", "username", "email", "password", "first_name", "last_name", "birthdate", "phone number", "address"], "id")
        self.users_profile = DatabaseManager(self.users_config, immutable_columns=["birthdate", "first_name", "last_name"])
        
        self.complaints_config = ConfigClass(self.host, self.user, self.password, self.database, "complaints_profile", ["id", "text", "timestamp"], "id")
        self.complaints_profile = DatabaseManager(self.complaints_config)
        
        self.vending_machines_config = ConfigClass(self.host, self.user, self.password, self.database, "vending_machines_profile", ["id", "name", "location", "status"], "id")
        self.vending_machines_profile = DatabaseManager(self.vending_machines_config)
        
        self.owners_config = ConfigClass(self.host, self.user, self.password, self.database, "owners_profile", ["id", "ownername", "email", "password", "first name", "last name", "birthdate", "phone_number", "address"], "id")
        self.owners_profile = DatabaseManager(self.owners_config, immutable_columns=["birthdate", "first_name", "last_name"])
        
        self.add_product_config = ConfigClass(self.host, self.user, self.password, self.database, "add_product", ["id", "owner_id", "product_id", "vending_machine_id", "timestamp", "quantity", "price"], "id")
        self.add_product = DatabaseManager(self.add_product_config, columns_foreign_keys_table={"owner_id": self.vending_machines, "product_id": self.products_profile, "owner_id": self.owners_profile})

        self.create_vending_machine_config = ConfigClass(self.host, self.user, self.password, self.database, "create_vending_machine", ["id", "owner_id", "vending_machine_id", "timestamp"], column_id="id")
        self.create_vending_machine = DatabaseManager(self.create_vending_machine_config, columns_foreign_keys_table={"owner_id": self.owners_profile, "vending_machine_id": self.vending_machines_profile})
        
        self.product_complaint_config = ConfigClass(self.host, self.user, self.password, self.database, "product_complaint", ["id", "complaint_id", "product_id", "user_id", "timestamp"], column_id="id")
        self.product_complaing = DatabaseManager(self.product_complaint_config, columns_foreign_keys_table = {"complaint_id": self.complaints_profile, "product_id": self.products_profile, "user_id": self.users_profile})

        self.product_review_config = ConfigClass(self.host, self.user, self.password, self.database, "product_review", ["id", "comment_id", "product_id", "user_id", "timestamp"], column_id="id")
        self.product_review = DatabaseManager(self.product_review_config, columns_foreign_keys_table={"comment_id": self.comments_profile, "product_id": self.products_profile, "user_id": self.users_profile})

        self.purchase_transaction_config = ConfigClass(self.host, self.user, self.password, self.database, "purchase_transaction", ["id", "user_id", "product_id", "vending_machine_id", "timestamp", "quantity", "amount_paid_per_unit"], column_id="id")
        self.purchase_transaction = DatabaseManager(self.purchase_transaction_config, columns_foreign_keys_table={"user_id": self.users_profile, "product_id": self.products_profile, "vending_machine_id": self.vending_machines_profile})

        self.vending_machine_complaint_config = ConfigClass(self.host, self.user, self.password, self.database, "vending_machine_complaint", ["id", "complaint_id", "vending_machine_id", "user id", "timestamp"], column_id="id")
        self.vending_machine_complaint = DatabaseManager(self.vending_machine_complaint_config, columns_foreign_keys_table={"complaint_id": self.complaints_profile, "vending_machine_id": self.vending_machines_profile, "user_id": self.users_profile})

        self.vending_machine_review_config = ConfigClass(self.host, self.user, self.password, self.database, "vending_machine_review", ["id", "comment_id", "vending_machine id", "user_id", "timestamp"], column_id="id")
        self.vending_machine_review = DatabaseManager(self.vending_machine_review_config, columns_foreign_keys_table={"comment_id": self.comments_profile, "vending_machine_id": self.vending_machines_profile, "user_id": self.users_profile})
        
        self.dict_tables = {
            "products_profile": self.product_profile,
            "comments_profile": self.comment_profile,
            "users_profile": self.user_profile,
            "complaints_profile": self.complaint_profile,
            "vending_machines_profile": self.vending_machine_profile,
            "owners_profile": self.owner_profile,
            "create_vending_machine": self.create_vending_machine,
            "product_complaint": self.product_complaint,
            "product_review": self.product_review,
            "purchase_transaction": self.purchase_transaction,
            "vending_machine_complaint": self.vending_machine_complaint,
            "vending_machine_review": self.vending_machine_review
            }     