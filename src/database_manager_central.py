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
from decorators import singleton

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

        self.products_configig = ConfigClass(self.host, self.user, self.password, self.database, "products", ["id", "name", "description", "price", "quantity"], "id")
        self.products_profile = DatabaseManager(products_config)

        self.comments_config = ConfigClass(self.host, self.user, self.password, self.database, "comments", ["id", "text", "timestamp"], "id")
        self.comments_profile = DatabaseManager(comments_config)
        
        self.users_config = ConfigClass(self.host, self.user, self.password, self.database, "users", ["id", "username", "email", "password", "first name", "last name", "birthdate", "phone number", "address"], "id")
        self.users_profile = DatabaseManager(users_config, immutable_columns=["birthdate", "first name", "last name"])
        
        self.complaints_config = ConfigClass(self.host, self.user, self.password, self.database, "complaints", ["id", "text", "timestamp"], "id")
        self.complaints_profile = DatabaseManager(complaints_config)
        
        self.vending_machines_config = ConfigClass(self.host, self.user, self.password, self.database, "vending_machines", ["id", "name", "location", "status"], "id")
        self.vending_machines_profile = DatabaseManager(vending_machines_config)
        
        self.owners_config = ConfigClass(self.host, self.user, self.password, self.database, "owners", ["id", "ownername", "email", "password", "first name", "last name", "birthdate", "phone number", "address"], "id")
        self.owners_profile = DatabaseManager(owners_config, immutable_columns=["birthdate", "first name", "last name"])
        
        self.add_product_config = ConfigClass(self.host, self.user, self.password, self.database, "add_product", ["id", "owner id", "product id", "vending machine id", "timestamp", "quantity", "price"], "id")
        self.add_product = DatabaseManager(add_product_config, foreign_keys=["vending machines", "products", "owners"])

        self.add_product_config = ConfigClass(self.host, self.user, self.password, self.database, "create_vm", ["id", "owner id", "vending machine id", "timestamp"], "id")
        self.create_vm = CreateVM(self.host, self.user, self.password, self.database, column_id="id")
        self.product_complaint = ProductComplaint(self.host, self.user, self.password, self.database, column_id="id")
        self.product_review = ProductReview(self.host, self.user, self.password, self.database, column_id="id")
        self.purchase_transaction = PurchaseTransaction(self.host, self.user, self.password, self.database, column_id="id")
        self.vending_machine_complaint = VMComplaint(self.host, self.user, self.password, self.database, column_id="id")
        self.vending_machine_review = VMReview(self.host, self.user, self.password, self.database, column_id="id")
        
        self.dict_tables = {
            "product table": self.product_profile,
            "comment table": self.comment_profile,
            "user table": self.user_profile,
            "complaint profile": self.complaint_profile,
            "vm table": self.vending_machine_profile,
            "owner table": self.owner_profile,
            "create vm": self.create_vm,
            "product complaint": self.product_complaint,
            "product review": self.product_review,
            "purchase transaction": self.purchase_transaction,
            "vending machine complaint": self.vending_machine_complaint,
            "vending machine review": self.vending_machine_review
            }     