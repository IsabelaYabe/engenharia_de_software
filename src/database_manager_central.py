"""
Module for creating the `DatabaseManagerCentral` class.

This module provides a centralized manager to handle all table-specific database managers
using a singleton pattern. The class includes methods to manage CRUD operations, foreign key validations, 
event notifications, and other database-related functionality.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: In Progress (pending additional tests and logging updates)

Dependencies:
    - database_manager.DatabaseManager
    - event_manager.EventManager
    - sub_strategy.PurchaseProductSubUpdateStrategy
    - singleton_decorator.singleton
    - custom_logger.setup_logger
    - dataclasses.dataclass
"""
from database_manager import DatabaseManager, Config, ConfigPub, ConfigSub
from event_manager.event_manager import EventManager
from sub_strategy.sub_update_strategy import PurchaseProductSubUpdateStrategy
from singleton_decorator import singleton
from custom_logger import setup_logger
from dataclasses import dataclass
from password_hasher import PasswordHasher, hash_password_decorator
import mysql.connector

logger = setup_logger()

@dataclass
class InstancesTables:
    """
    Dataclass to organize and store instances of table-specific DatabaseManager objects.
    """
    products_profile: DatabaseManager 
    users_profile: DatabaseManager
    vending_machines_profile: DatabaseManager 
    owners_profile: DatabaseManager
    product_complaint: DatabaseManager
    product_comment: DatabaseManager
    purchase_transaction: DatabaseManager
    vending_machine_complaint: DatabaseManager
    vending_machine_comment: DatabaseManager
    favorite_products: DatabaseManager
    favorite_vending_machines: DatabaseManager
    
@singleton
class DatabaseManagerCentral:
    """
    Singleton class to manage multiple table-specific DatabaseManager instances.

    The `DatabaseManagerCentral` class initializes and organizes instances of 
    `DatabaseManager` for each database table. It provides methods to perform 
    CRUD operations, manage relationships between tables, handle events, and 
    ensure data integrity.

    Attributes:
        __host (str): The MySQL server host.
        __user (str): The MySQL username.
        __password (str): The MySQL password.
        __database (str): The name of the MySQL database.
        event_manager (EventManager): Centralized event manager for handling notifications.
        __instance_tables (InstancesTables): Dataclass instance containing table-specific managers.
    """
    def __init__(self, host, user, password, database):
        """
        Initializes the `DatabaseManagerCentral` instance and sets up the event manager and table managers.

        Args:
            host (str): The MySQL server host.
            user (str): The MySQL username.
            password (str): The MySQL password.
            database (str): The name of the MySQL database.
        """
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__password_hasher = PasswordHasher()

        self.create_tables()

        self.event_manager = EventManager()
        self.event_manager.update_strategies["PurchaseProductEvent"] = PurchaseProductSubUpdateStrategy()

        self.__products_config = Config(self.host, self.user, self.password, self.database, "products_profile", ["id", "name", "description", "price", "quantity", "vending_machine_id", "timestamp"], "id")
        self.__products_config_pub = None
        self.__products_config_sub = ConfigSub(event_manager=self.event_manager, events_type_sub=["PurchaseProductEvent"])
        self.__products_profile = DatabaseManager(self.__products_config, self.__products_config_pub, self.__products_config_sub, immutable_columns=None, foreign_keys={"vending_machine_id": "vending_machines_profile"})
        
        self.__users_config = Config(self.host, self.user, self.password, self.database, "users_profile", ["id", "username", "email", "password", "first_name", "last_name", "birthdate", "phone number", "address", "budget"], "id")
        self.__users_config_pub = None
        self.__users_config_sub = None
        self.__users_profile = DatabaseManager(self.__users_config, self.__users_config_pub, self.__users_config_sub, immutable_columns=["birthdate", "first_name", "last_name"])
        
        self.__vending_machines_config = Config(self.host, self.user, self.password, self.database, "vending_machines_profile", ["id", "name", "location", "status", "timestamp", "owner_id"], "id")
        self.__vending_machines_config_pub = None
        self.__vending_machines_config_sub = None
        self.__vending_machines_profile = DatabaseManager(self.__vending_machines_config, self.__vending_machines_config_pub, self.__vending_machines_config_sub, immutable_columns=None, foreign_keys={"owner_id": "owners_profile"})

        self.__owners_config = Config(self.host, self.user, self.password, self.database, "owners_profile", ["id", "username", "email", "password", "first name", "last name", "birthdate", "phone_number", "address", "budget"], "id")
        self.__owners_config_pub = None
        self.__owners_config_sub = None
        self.__owners_profile = DatabaseManager(self.__owners_config, self.__owners_config_pub, self.__owners_config_sub, immutable_columns=["birthdate", "first_name", "last_name"])
    
        self.__product_complaint_config = Config(self.host, self.user, self.password, self.database, "product_complaint", ["id", "text", "product_id", "user_id", "timestamp"], column_id="id")
        self.__product_complaint_config_pub = None
        self.__product_complaint_config_sub = None
        self.__product_complaint = DatabaseManager(self.__product_complaint_config, self.__product_complaint_config_pub, self.__product_complaint_config_sub, immutable_columns=None, foreign_keys={"product_id": "products_profile", "user_id": "users_profile"})

        self.__product_comment_config = Config(self.host, self.user, self.password, self.database, "product_comment", ["id", "text", "product_id", "user_id", "timestamp"], column_id="id")
        self.__product_comment_config_pub = None
        self.__product_comment_config_sub = None
        self.__product_comment = DatabaseManager(self.__product_comment_config, self.__product_comment_config_pub, self.__product_comment_config_sub, immutable_columns=None, foreign_keys={"product_id": "products_profile", "user_id": "users_profile"})

        self.__purchase_transaction_config = Config(self.host, self.user, self.password, self.database, "purchase_transaction", ["id", "user_id", "product_id", "vending_machine_id", "timestamp", "quantity", "amount_paid_per_unit"], column_id="id")
        self.__purchase_transaction_config_pub = ConfigPub(event_manager=self.event_manager, events_type_pub=["PurchaseProductEvent"])
        self.__purchase_transaction_config_sub = None
        self.__purchase_transaction = DatabaseManager(self.__purchase_transaction_config, self.__purchase_transaction_config_pub, self.__purchase_transaction_config_sub, immutable_columns=None, foreign_keys={"user_id": "users_profile", "product_id": "products_profile", "vending_machine_id": "vending_machines_profile"})
        
        self.__vending_machine_complaint_config = Config(self.host, self.user, self.password, self.database, "vending_machine_complaint", ["id", "text", "vending_machine_id", "user id", "timestamp"], column_id="id")
        self.__vending_machine_complaint_config_pub = None
        self.__vending_machine_complaint_config_sub = None
        self.__vending_machine_complaint = DatabaseManager( self.__vending_machine_complaint_config, self.__vending_machine_complaint_config_pub, self.__vending_machine_complaint_config_sub, immutable_columns=None, foreign_keys={"vending_machine_id": "vending_machines_profile", "user_id": "users_profile"})

        self.__vending_machine_comment_config = Config(self.host, self.user, self.password, self.database, "vending_machine_comment", ["id", "text", "vending_machine_id", "user_id", "timestamp"], column_id="id")
        self.__vending_machine_comment_config_pub = None
        self.__vending_machine_comment_config_sub = None
        self.__vending_machine_comment = DatabaseManager( self.__vending_machine_comment_config, self.__vending_machine_comment_config_pub, self.__vending_machine_comment_config_sub, immutable_columns=None, foreign_keys={"vending_machine_id": "vending_machines_profile", "user_id": "users_profile"})

        self.__favorite_vending_machines_config = Config(self.host, self.user, self.password, self.database, "favorite_vending_machines", ["id", "vending_machine_id", "user_id"], column_id="id")
        self.__favorite_vending_machines_config_pub = None
        self.__favorite_vending_machines_config_sub = None
        self.__favorite_vending_machines = DatabaseManager( self.__favorite_vending_machines_config, self.__favorite_vending_machines_config_pub, self.__favorite_vending_machines_config_sub, immutable_columns=None, foreign_keys={"vending_machine_id": "vending_machines_profile", "user_id": "users_profile"})

        self.__favorite_products_config = Config(self.host, self.user, self.password, self.database, "favorite_products", ["id", "product_id", "user_id"], column_id="id")
        self.__favorite_products_config_pub = None
        self.__favorite_products_config_sub = None
        self.__favorite_products = DatabaseManager( self.__favorite_products_config, self.__favorite_products_config_pub, self.__favorite_products_config_sub, immutable_columns=None, foreign_keys={"product_id": "products_profile", "user_id": "users_profile"})

        self.__instance_tables = InstancesTables(
            products_profile = self.__products_profile,
            users_profile = self.__users_profile,
            vending_machines_profile = self.__vending_machines_profile,
            owners_profile = self.__owners_profile,
            product_complaint = self.__product_complaint,
            product_comment = self.__product_comment,
            purchase_transaction = self.__purchase_transaction,
            vending_machine_complaint = self.__vending_machine_complaint,
            vending_machine_comment = self.__vending_machine_comment,
            favorite_products = self.__favorite_products,
            favorite_vending_machines = self.__favorite_vending_machines
        )

    def create_tables(self):
        # Load SQL script to create tables and relationships
        try:
            with open("src\MYSQL\create_tables_relationships.sql", "r") as file:
                logger.debug("Reading SQL script to create tables and relationships.")
                create_tables_sql = file.read()
        except FileNotFoundError:
            logger.error("SQL script file not found.")
            raise
        except Exception as e:
            logger.error(f"Error reading SQL script file: {e}")
            raise

        try:
            conn = mysql.connector.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__database)
            logger.debug("Successful connection")
        except mysql.connector.Error as e:
            logger.error("Unsuccessful connection: %s (errno=%d)", e.msg, e.errno)
            raise
        logger.info("Connected into database")

        # Execute the SQL script to create tables and relationships
        with conn.cursor() as cursor:
            cursor.execute(create_tables_sql)
        
        #conmfirming the creation of the tables
        for table_name, table_instance in self.__instance_tables.__dict__.items():
            logger.debug(f"Checking if table '{table_name}' exists.")
            table_exists = table_instance.table_exists()
            if not table_exists:
                logger.error(f"Table '{table_name}' not found.")
                raise ValueError(f"Table '{table_name}' not found.")
            logger.debug(f"Table '{table_name}' found.")

        logger.debug("Database tables and relationships created successfully.")
    
    def drop_tables(self):
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
            conn = mysql.connector.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__database)
            logger.debug("Successful connection")
        except mysql.connector.Error as e:
            logger.error("Unsuccessful connection: %s (errno=%d)", e.msg, e.errno)
            raise
        logger.info("Connected into database")

        # Execute the SQL script to drop tables
        with conn.cursor() as cursor:
            cursor.execute(drop_tables_sql)

        logger.debug("Database tables dropped successfully.")

    def show(self):
        for table_name, table_instance in self.instance_tables.__dict__.items():
            print(f"Table: {table_name}")
            head, records = table_instance.show_table()
            print("Columns:")
            for col in head:
                print(col, end=" ")
            print()
            print("Records:")
            if records:
                for record in records:
                    print(record)
            else:
                print("No records found.")

    def insert_record(self, table_name, data, foreign_keys=None):
        """
        Centralized logic for inserting a record into a specified table.

        Parameters:
            table_name (str): The name of the table to insert the record into.
            data (dict): A dictionary of column names and their values for the new record.
            foreign_keys (dict, optional): A dictionary of foreign key validations where 
                                           key is the foreign table name and value is the column to validate.

        Returns:
            str: The ID of the inserted record.

        Raises:
            ValueError: If any validation fails or insertion encounters an issue.
        """
        try:
            logger.debug(f"Validating record data for table '{table_name}'")
            if foreign_keys:
                for fk_table, fk_column in foreign_keys.items():
                    logger.debug(f"Validating foreign key '{fk_column}' in table '{fk_table}'")
                    fk_value = data.get(fk_column)
                    logger.debug(f"Foreign key value: {fk_value}")
                    if fk_value is None:
                        logger.error(f"Foreign key '{fk_column}' must be provided.")
                        raise ValueError(f"Foreign key '{fk_column}' must be provided.")

                    logger.debug(f"Validating foreign key '{fk_column}' with value '{fk_value}' in table '{fk_table}'")
                    table_instance = getattr(self.instance_tables, fk_table, None)
                    logger.debug(f"Table instance: {table_instance}")
                    if not table_instance:
                        raise ValueError(f"Foreign key table '{fk_table}' not found in instance tables.")
                    record_exists = table_instance.search_record(**{fk_column: fk_value})

                    logger.debug(f"Record exists: {record_exists}")
                    if not record_exists:
                        raise ValueError(f"Foreign key value '{fk_value}' does not exist in table '{fk_table}'.")
                    logger.debug(f"Foreign key '{fk_column}' with value '{fk_value}' validated in table '{fk_table}'")

            table_instance = getattr(self.instance_tables, table_name, None)
            if not table_instance:
                raise ValueError(f"Table '{table_name}' not found in instance tables.")
            logger.debug(f"Inserting record into '{table_name}' with data {data}")

            try:
                record_id = table_instance.insert_row(**data)
                logger.info(f"Record added to '{table_name}' with ID '{record_id}' and data {data}")
                return record_id
            except Exception as e:
                logger.error(f"Error inserting record into '{table_name}': {e}")
                raise
        except Exception as e:
            logger.error(f"Error inserting record into '{table_name}': {e}")
            raise

    def add_product(self, name, description, price, quantity, vending_machine_id):
        """
        Adds a new product to the `products_profile` table.

        Args:
            name (str): Name of the product.
            description (str): Description of the product.
            price (float): Price of the product.
            quantity (int): Available quantity of the product.
            vending_machine_id (str): ID of the vending machine where the product is located.

        Returns:
            str: ID of the inserted product.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "name": name,
            "description": description,
            "price": price,
            "quantity": quantity,
            "vending_machine_id": vending_machine_id,
        }
        return self.insert_record(
            table_name="products_profile",
            data=data,
            foreign_keys={"vending_machines_profile": "vending_machine_id"}
        )

    @hash_password_decorator(password_position=2)
    def add_user(self, username, email, password, first_name, last_name, birthdate, phone_number, address, budget):
        """
        Adds a new user to the `users_profile` table.

        Args:
            username (str): User's username.
            email (str): User's email address.
            password (str): Encrypted password.
            first_name (str): User's first name.
            last_name (str): User's last name.
            birthdate (str): User's birth date.
            phone_number (str): User's phone number.
            address (str): User's address.
            budget (float): User's budget.

        Returns:
            str: ID of the inserted user.
        """
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "phone_number": phone_number,
            "address": address,
            "budget": budget,
        }
        return self.insert_record("users_profile", data)
    
    def add_product_comment(self, product_id, user_id, text):
        """
        Adds a comment for a product in the `product_comment` table.

        Args:
            product_id (str): ID of the product being commented on.
            user_id (str): ID of the user making the comment.
            text (str): Content of the comment.

        Returns:
            str: ID of the inserted comment.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "product_id": product_id,
            "user_id": user_id,
            "text": text,
        }
        return self.insert_record(
            "product_comment",
            data,
            foreign_keys={"products_profile": "product_id", "users_profile": "user_id"}
        )

    def add_favorite_product(self, user_id, product_id):
        """
        Adds a product to a user's favorites in the `favorite_products` table.

        Args:
            user_id (str): ID of the user adding the product to favorites.
            product_id (str): ID of the product to be added to favorites.

        Returns:
            str: ID of the inserted favorite entry.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "user_id": user_id,
            "product_id": product_id,
        }
        return self.insert_record(
            "favorite_products",
            data,
            foreign_keys={"products_profile": "product_id", "users_profile": "user_id"}
        )

    def add_favorite_vending_machine(self, user_id, vending_machine_id):
        """
        Adds a vending machine to a user's favorites in the `favorite_vending_machines` table.

        Args:
            user_id (str): ID of the user adding the vending machine to favorites.
            vending_machine_id (str): ID of the vending machine to be added to favorites.

        Returns:
            str: ID of the inserted favorite entry.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "user_id": user_id,
            "vending_machine_id": vending_machine_id,
        }
        return self.insert_record(
            "favorite_vending_machines",
            data,
            foreign_keys={"vending_machines_profile": "vending_machine_id", "users_profile": "user_id"}
        )

    def add_vending_machine_comment(self, vending_machine_id, user_id, text):
        """
        Adds a comment for a vending machine in the `vending_machine_comment` table.

        Args:
            vending_machine_id (str): ID of the vending machine being commented on.
            user_id (str): ID of the user making the comment.
            text (str): Content of the comment.

        Returns:
            str: ID of the inserted comment.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "vending_machine_id": vending_machine_id,
            "user_id": user_id,
            "text": text,
        }
        return self.insert_record(
            "vending_machine_comment",
            data,
            foreign_keys={"vending_machines_profile": "vending_machine_id", "users_profile": "user_id"}
        )

    def add_vending_machine_complaint(self, vending_machine_id, user_id, text):
        """
        Adds a complaint for a vending machine in the `vending_machine_complaint` table.

        Args:
            vending_machine_id (str): ID of the vending machine being complained about.
            user_id (str): ID of the user making the complaint.
            text (str): Content of the complaint.

        Returns:
            str: ID of the inserted complaint.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "vending_machine_id": vending_machine_id,
            "user_id": user_id,
            "text": text,
        }
        return self.insert_record(
            "vending_machine_complaint",
            data,
            foreign_keys={"vending_machines_profile": "vending_machine_id", "users_profile": "user_id"}
        )

    def add_product_complaint(self, product_id, user_id, text):
        """
        Adds a complaint for a product in the `product_complaint` table.

        Args:
            product_id (str): ID of the product being complained about.
            user_id (str): ID of the user making the complaint.
            text (str): Content of the complaint.

        Returns:
            str: ID of the inserted complaint.

        Raises:
            ValueError: If foreign key validation fails.
        """
        data = {
            "product_id": product_id,
            "user_id": user_id,
            "text": text,
        }
        return self.insert_record(
            "product_complaint",
            data,
            foreign_keys={"products_profile": "product_id", "users_profile": "user_id"}
        )

    @hash_password_decorator(password_position=2)
    def add_owner(self, username, email, password, first_name, last_name, birthdate, phone_number, address, budget):
        """
        Updates the budget of an owner in the database.

        Args:
            owner_id (str): ID of the owner to update.
            new_budget (float): The new budget value.

        Raises:
            Exception: If an error occurs during the update operation.
        """
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "phone_number": phone_number,
            "address": address,
            "budget": budget,
        }
        return self.insert_record("owners_profile", data)

    def add_vending_machine(self, name, location, owner_id):
        """
        Adds a new vending machine to the `vending_machines_profile` table.

        Args:
            name (str): Name of the vending machine.
            location (str): Location of the vending machine.
            status (str): Current status of the vending machine (e.g., active/inactive).
            owner_id (str): ID of the owner associated with the vending machine.

        Returns:
            str: ID of the inserted vending machine.

        Raises:
            ValueError: If foreign key validation fails.
        """        
        data = {
            "name": name,
            "location": location,
            "owner_id": owner_id,
        }
        
        return self.insert_record(
            "vending_machines_profile",
            data,
            foreign_keys={"owners_profile": "owner_id"}
        )
    
    def add_purchase_transaction(self, user_id, product_id, vending_machine_id, quantity, amount_paid_per_unit):
        """
        Adds a purchase transaction and handles event notifications.

        Args:
            user_id (str): ID of the user making the purchase.
            product_id (str): ID of the purchased product.
            vending_machine_id (str): ID of the vending machine.
            quantity (int): Quantity of the product purchased.
            amount_paid_per_unit (float): Price paid per unit.

        Returns:
            str: ID of the transaction.

        Raises:
            ValueError: If validations fail.
            RuntimeError: If event notification fails.
        """
        try:
            product = self.products_profile.search_record(id=product_id)
            if not product:
                raise ValueError(f"Product with ID '{product_id}' does not exist.")
            
            logger.debug(f"Product found: {product}")
            available_quantity = product[0]["quantity"]
            
            if available_quantity < quantity:
                raise ValueError(f"Insufficient quantity for product ID '{product_id}'. Available: {available_quantity}, Requested: {quantity}.")
            logger.debug(f"Product quantity available: {available_quantity}")
            
            data = {
                "user_id": user_id,
                "product_id": product_id,
                "vending_machine_id": vending_machine_id,
                "quantity": quantity,
                "amount_paid_per_unit": amount_paid_per_unit,
            }
            transaction_id = self.insert_record(
                "purchase_transaction",
                data,
                foreign_keys={
                    "users_profile": "user_id",
                    "products_profile": "product_id",
                    "vending_machines_profile": "vending_machine_id"
                }
            )
            logger.info(f"Purchase transaction recorded with ID '{transaction_id}' for user '{user_id}'")

            event_data = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "product_id": product_id,
            "vending_machine_id": vending_machine_id,
            "quantity": quantity,
            "amount_paid_per_unit": amount_paid_per_unit,
            }
            if self.__purchase_transaction_config_pub and self.__purchase_transaction_config_pub.event_manager:
                try:
                    self.__purchase_transaction_config_pub.event_manager.notify("PurchaseProductEvent", event_data)
                    logger.info(f"Event 'PurchaseProductEvent' published with data: {event_data}")
                except Exception as notify_error:
                    logger.error(f"Failed to notify event 'PurchaseProductEvent': {notify_error}")
                    raise RuntimeError(f"Failed to publish event: {notify_error}")
            else:
                logger.warning("No EventManager configured for event publishing.")
            return transaction_id
        
        except Exception as e:
            logger.error(f"Error registering purchase transaction: {e}")
            raise

    def update_vending_machine_status(self, vending_machine_id, status):
        """
        Updates the status of a vending machine.

        Args:
            vending_machine_id (str): ID of the vending machine to update.
            status (str): The new status for the vending machine.

        Raises:
            Exception: If an error occurs during the update operation.
        """
        try:
            self.__vending_machines_profile.update_row(
                record_id=vending_machine_id,
                status=status
            )
            logger.info(f"Vending machine status '{vending_machine_id}' updated to '{status}'")
        except Exception as e:
            logger.error(f"Error updating vending machine status '{vending_machine_id}': {e}")
            raise

    def update_owner_budget(self, owner_id, new_budget):
        """
        Updates the budget of a specific owner in the `owners_profile` table.

        Args:
            owner_id (str): ID of the owner whose budget needs to be updated.
            new_budget (float): The new budget value to be set.

        Returns:
            None

        Logs:
            - Logs a success message if the budget update is successful.
            - Logs an error message if an exception occurs.

        Raises:
            Exception: If an error occurs during the update operation.
        """
        try:
            self.__owners_profile.update_row(
                record_id=owner_id,
                budget=new_budget
            )
            logger.info(f"Owner's budget '{owner_id}' updated to '{new_budget}'")
        except Exception as e:
            logger.error(f"Error updating owner's budget '{owner_id}': {e}")
            raise

    def add_product_quantity(self, product_id=None, name=None, vending_machine_id=None, quantity_to_add=0):
        """
        Adds a specified quantity to an existing product in the database.

        Args:
            product_id (str, optional): ID of the product to update. Defaults to None.
            name (str, optional): Name of the product to update (used with `vending_machine_id`). Defaults to None.
            vending_machine_id (str, optional): ID of the vending machine containing the product. Defaults to None.
            quantity_to_add (int): The quantity to add to the product. Must be greater than 0.

        Returns:
            int: The new quantity of the product after the addition.

        Raises:
            ValueError: If `quantity_to_add` is not greater than 0, or if the product is not found.
            Exception: If an error occurs during the update operation.
        """
        try:
            if quantity_to_add <= 0:
                raise ValueError("The quantity to be added must be greater than zero.")

            if product_id:
                product = self.__products_profile.get_by_id(product_id)
            elif name and vending_machine_id:
                products = self.__products_profile.search_record(name=name, vending_machine_id=vending_machine_id)
                if not products:
                    raise ValueError("Product not found with the criteria provided.")
                product = products[0]  
            else:
                raise ValueError("Either a 'product_id' or 'name' and 'vending_machine_id' must be provided.")

            if not product:
                raise ValueError(f"Product not found.")

            current_quantity = product[4]  
            new_quantity = current_quantity + quantity_to_add

            self.__products_profile.update_row(record_id=product[0], quantity=new_quantity)
            logger.info(f"Product quantity '{product[1]}' (ID: {product[0]}) increased from {current_quantity} to {new_quantity}.")
            return new_quantity
        except Exception as e:
            logger.error(f"Error adding quantity to product: {e}")
            raise

    def search_table(self, table_name, **filters):
        """
        Searches for records in a specified table using the provided filters.

        Args:
            table_name (str): Name of the table to search.
            **filters: Arbitrary keyword arguments representing column-value pairs to filter the search.

        Returns:
            list: A list of records matching the filters.

        Raises:
            ValueError: If the specified table does not exist.
            Exception: If an error occurs while fetching records.
        """
        try:
            table_instance = getattr(self.instance_tables, table_name, None)
            if not table_instance:
                raise ValueError(f"Table '{table_name}' not found.")

            records = table_instance.search_record(**filters)
            logger.info(f"Search performed on table '{table_name}' with filters {filters}: {records}")
            return records
        except Exception as e:
            logger.error(f"Error fetching from table '{table_name}': {e}")
            raise

    def get_sales_report(self, start_date, end_date):
        """
        Generates a sales report for a specified time range.

        Args:
            start_date (str): The start date for the report in 'YYYY-MM-DD' format.
            end_date (str): The end date for the report in 'YYYY-MM-DD' format.

        Returns:
            list: A list of dictionaries containing product IDs and total quantities sold.

        Raises:
            Exception: If an error occurs while executing the query or fetching the data.
        """
        try:
            query = """
                SELECT product_id, SUM(quantity) as total_sold
                FROM purchase_transaction
                WHERE timestamp BETWEEN %s AND %s
                GROUP BY product_id
                ORDER BY total_sold DESC;
            """
            sales_data = self.purchase_transaction.execute_sql(query, params=(start_date, end_date), fetch_all=True)
            logger.info(f"Sales report generated between {start_date} and {end_date}: {sales_data}")
            return sales_data
        except Exception as e:
            logger.error(f"Error generating sales report: {e}")
            raise

    def login_user(self, table_name: str, username: str, password: str):
        """
        Logs in a user by validating the username and password for a specific table.

        Args:
            table_name (str): The name of the table where the user data is stored.
            username (str): The username provided by the user.
            password (str): The plain text password provided by the user.

        Returns:
            dict: The user information if the login is successful.
            None: If the login fails (invalid username or password).

        Logs:
            - Logs an info message indicating the login attempt.
            - Logs an error message if the login fails.
            - Logs an error message if a system error occurs.

        Raises:
            ValueError: If the table does not exist.
            Exception: If any system-related error occurs (like SQL query issues).
        """
        try:
            table_instance = getattr(self.instance_tables, table_name, None)
            if not table_instance:
                logger.error(f"Table '{table_name}' not found in instance tables.")
                raise ValueError(f"Table '{table_name}' not found in instance tables.")

            encrypted_password = self.password_hasher.hash_password(password)

            logger.info(f"Attempting login for user: {username} in table: {table_name}")

            user_record = table_instance.search_record(username=username, password=encrypted_password)

            if user_record:
                user_data = self._map_tuple_to_dict(user_record[0], table_instance.columns)
                logger.info(f"Login successful for user: {username} in table: {table_name}")
                return user_data
            else:
                logger.error(f"Invalid username or password for user: {username} in table: {table_name}")
                return None

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            raise  

        except Exception as e:
            logger.error(f"System error during login for username '{username}' in table '{table_name}': {str(e)}")
            raise Exception("An error occurred while attempting to log in.") from e

    def _map_tuple_to_dict(self, record_tuple, columns):
        """
        Maps a tuple (from SQL result) to a dictionary using the list of column names.

        Args:
            record_tuple (tuple): The tuple representing a single record.
            columns (list): The list of column names corresponding to the tuple.

        Returns:
            dict: A dictionary where keys are column names and values are the respective values from the tuple.
        """
        return {column: value for column, value in zip(columns, record_tuple)}


    @property
    def host(self):
        return self.__host
    
    @property
    def user(self):
        return self.__user
    
    @property
    def password(self):
        return self.__password
    
    @property
    def database(self):
        return self.__database
    
    @property
    def instance_tables(self):
        return self.__instance_tables

    @property
    def vending_machine_comment(self):
        return self.__vending_machine_comment
    
    @property 
    def vending_machine_complaint(self):
        return self.__vending_machine_complaint

    @property 
    def purchase_transaction(self):
        return self.__purchase_transaction
    
    @property 
    def product_comment(self):
        return self.__product_comment
    
    @property 
    def product_complaint(self):
        return self.__product_complaint


    @property
    def owners_profile(self):
        return self.__owners_profile

    @property
    def vending_machines_profile(self):
        return self.__vending_machines_profile

    @property
    def users_profile(self):
        return self.__users_profile
    
    @property
    def products_profile(self):
        return self.__products_profile

    @property
    def favorite_vending_machines(self):
        return self.__favorite_vending_machines

    @property
    def favorite_products(self):
        return self.__favorite_products
    
    @property
    def password_hasher(self):
        return self.__password_hasher

    @host.setter
    def host(self, value):
        self.__host = value
    
    @user.setter
    def user(self, value):
        self.__user = value
    
    @password.setter
    def password(self, value):
        self.__password = value

    @database.setter
    def database(self, value):
        self.__database = value

    @instance_tables.setter
    def dict_instance_tables(self, new_instance_tables):
        self.__instance_tables = new_instance_tables


    @products_profile.setter
    def products_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__products_profile.delete_table()
            self.__products_config_pub = new_config_pub
            self.__products_config_sub = new_config_sub
            self.__products_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.products_profile = self.__products_profile
            logger.info(f"Update products_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @vending_machine_comment.setter
    def vending_machine_comment(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__vending_machine_comment.delete_table()
            self.__vending_machine_comment_config_pub = new_config_pub
            self.__vending_machine_comment_config_sub = new_config_sub
            self.__vending_machine_comment = DatabaseManager( new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.vending_machine_comment = self.__vending_machine_comment 
            logger.info(f"Update vending_machine_comment, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @vending_machine_complaint.setter
    def vending_machine_complaint(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__vending_machine_complaint.delete_table() 
            self.__vending_machine_complaint_config_pub = new_config_pub
            self.__vending_machine_complaint_config_sub = new_config_sub
            self.__vending_machine_complaint = DatabaseManager( new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.vending_machine_complaint = self.__vending_machine_complaint
            logger.info(f"Update vending_machine_complaint, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @purchase_transaction.setter
    def purchase_transaction(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__purchase_transaction.delete_table()
            self.__purchase_transaction_config_pub = new_config_pub
            self.__purchase_transaction_config_sub = new_config_sub
            self.__purchase_transaction = DatabaseManager(new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns)
            self.__instance_tables.purchase_transaction = self.__purchase_transaction
            logger.info(f"Update purchase_transaction, new name: {new_config.table_name}")
        except Exception as e:
                logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @product_comment.setter
    def product_comment(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__product_comment.delete_table()
            self.__product_comment_config_pub = new_config_pub
            self.__product_comment_config_sub = new_config_sub
            self.__product_comment = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.product_comment = self.__product_comment
            logger.info(f"Update product_comment, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @product_complaint.setter
    def product_complaint(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__product_complaint.delete_table()
            self.__product_complaint_config_pub = new_config_pub
            self.__product_complaint_config_sub = new_config_sub
            self.__product_complaint = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.product_complaint = self.__product_complaint
            logger.info(f"Update product_complaint, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @owners_profile.setter
    def owners_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__owners_profile.delete_table()
            self.__owners_config_pub = new_config_pub
            self.__owners_config_sub = new_config_sub
            self.__owners_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.owners_profile = self.__owners_profile
            logger.info(f"Update owners_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @vending_machines_profile.setter
    def vending_machines_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__vending_machines_profile.delete_table()
            self.__vending_machines_config_pub = new_config_pub
            self.__vending_machines_config_sub = new_config_sub
            self.__vending_machines_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.vending_machine = self.__vending_machines_profile
            logger.info(f"Update vending_machines_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @users_profile.setter
    def users_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__users_profile.delete_table()
            self.__users_config_pub = new_config_pub
            self.__users_config_sub = new_config_sub
            self.__users_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.users_profile = self.__users_profile
            logger.info(f"Update users_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failled to setter {new_config.table_name}: {e}")

    @favorite_vending_machines.setter
    def favorite_vending_machines(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None): 
        try:
            self.__favorite_vending_machines.delete_table()
            self.__favorite_vending_machines_config_pub = new_config_pub
            self.__favorite_vending_machines_config_sub = new_config_sub
            self.__favorite_vending_machines = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.favorite_vending_machines = self.__favorite_vending_machines
            logger.info(f"Update favorite_vending_machines, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failled to setter {new_config.table_name}: {e}")


    @favorite_products.setter
    def favorite_products(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None): 
        try:
            self.__favorite_products.delete_table()
            self.__favorite_products_config_pub = new_config_pub
            self.__favorite_products_config_sub = new_config_sub
            self.__favorite_products = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__instance_tables.favorite_products = self.__favorite_products
            logger.info(f"Update favorite_products, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failled to setter {new_config.table_name}: {e}")