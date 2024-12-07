"""
    Module for creating the DatabaseManagerCentral class.

    Author: Isabela Yabe
    Last Modified: 19/11/2024
    Status: Preciso atualiza colocando o no init, por logs e fazer testes

    Dependencies:
        - product_profile
        - decorators
        - tables
        - custom_logger
"""
from database_manager import DatabaseManager, Config, ConfigPub, ConfigSub
from event_manager.event_manager import EventManager
from sub_strategy.sub_update_strategy import PurchaseProductSubUpdateStrategy
from singleton_decorator import singleton
from custom_logger import setup_logger
from dataclasses import dataclass

logger = setup_logger()

@dataclass
class InstancesTables:
    products_profile: DatabaseManager 
    users_profile: DatabaseManager
    product_comment: DatabaseManager 
    favorite_products: DatabaseManager
    favorite_vending_machines: DatabaseManager 
    vending_machine_comment: DatabaseManager
    vending_machine_complaint: DatabaseManager
    product_complaint: DatabaseManager 
    owners_profile: DatabaseManager
    vending_machines_profile: DatabaseManager 
    purchase_transaction: DatabaseManager
    
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
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

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

        self.__owners_config = Config(self.host, self.user, self.password, self.database, "owners_profile", ["id", "ownername", "email", "password", "first name", "last name", "birthdate", "phone_number", "address", "budget"], "id")
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
            if foreign_keys:
                for fk_table, fk_column in foreign_keys.items():
                    fk_value = data.get(fk_column)
                    if fk_value is None:
                        logger.error(f"Foreign key '{fk_column}' must be provided.")
                        raise ValueError(f"Foreign key '{fk_column}' must be provided.")

                    logger.debug(f"Validating foreign key '{fk_column}' with value '{fk_value}' in table '{fk_table}'")
                    table_instance = getattr(self.instance_tables, fk_table, None)

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

    def add_user(self, username, email, password, first_name, last_name, birthdate, phone_number, address, budget):
        """
        Add a new user to the database.
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
        Add a comment to a product.
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
        Add a product to the user's favorites.
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
        Add a vending machine to the user's favorites.
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
        Add a comment to a vending machine.
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
        Add a complaint to a vending machine.
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
        Add a complaint to a product.
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

    def add_owner(self, ownername, email, password, first_name, last_name, birthdate, phone_number, address, budget):
        """
        Add a new owner to the database.
        """
        data = {
            "ownername": ownername,
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

    def add_vending_machine(self, name, location, status, owner_id):
        """
        Add a vending machine.
        """
        data = {
            "name": name,
            "location": location,
            "status": status,
            "owner_id": owner_id,
        }
        
        return self.insert_record(
            "vending_machines_profile",
            data,
            foreign_keys={"owners_profile": "owner_id"}
        )
    
    def add_purchase_transaction(self, user_id, product_id, vending_machine_id, quantity, amount_paid_per_unit):
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