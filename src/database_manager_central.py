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
from decorators_method import singleton
from custom_logger import setup_logger
logger = setup_logger()

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

        self.__products_config = Config(self.host, self.user, self.password, self.database, "products_profile", ["id", "name", "description", "price", "quantity"], "id")
        self.__products_config_pub = ConfigPub()
        self.__products_config_sub = ConfigSub()
        self.__products_profile = DatabaseManager(self.__products_config, self.__products_config_pub, self.__products_config_sub, immutable_columns=None, foreign_keys=None)

        self.__comments_config = Config(self.host, self.user, self.password, self.database, "comments_profile", ["id", "text", "timestamp"], "id")
        self.__comments_config_pub = ConfigPub()
        self.__comments_config_sub = ConfigSub()
        self.__comments_profile = DatabaseManager(self.__comments_config, self.__comments_config_pub, self.__comments_config_sub, immutable_columns=None, foreign_keys=None)
        
        self.__users_config = Config(self.host, self.user, self.password, self.database, "users_profile", ["id", "username", "email", "password", "first_name", "last_name", "birthdate", "phone number", "address"], "id")
        self.__users_config_pub = ConfigPub()
        self.__users_config_sub = ConfigSub()
        self.__users_profile = DatabaseManager(self.__users_config, self.__users_config_pub, self.__users_config_sub, immutable_columns=["birthdate", "first_name", "last_name"])
        
        self.__complaints_config = Config(self.host, self.user, self.password, self.database, "complaints_profile", ["id", "text", "timestamp"], "id")
        self.__complaints_config_pub = ConfigPub()
        self.__complaints_config_sub = ConfigSub()
        self.__complaints_profile = DatabaseManager(self.__complaints_config, self.__complaints_config_pub, self.__complaints_config_sub, immutable_columns=None, foreign_keys=None)
        
        self.__vending_machines_config = Config(self.host, self.user, self.password, self.database, "vending_machines_profile", ["id", "name", "location", "status"], "id")
        self.__vending_machine_config_pub = ConfigPub()
        self.__vending_machine_config_sub = ConfigSub()
        self.__vending_machines_profile = DatabaseManager(self.__vending_machines_config, self.__vending_machine_config_pub, self.__vending_machine_config_sub, immutable_columns=None, foreign_keys=None)

        self.__owners_config = Config(self.host, self.user, self.password, self.database, "owners_profile", ["id", "ownername", "email", "password", "first name", "last name", "birthdate", "phone_number", "address"], "id")
        self.__owners_config_pub = ConfigPub()
        self.__owners_config_sub = ConfigSub()
        self.__owners_profile = DatabaseManager(self.__owners_config, self.__owners_config_pub, self.__owners_config_sub, immutable_columns=["birthdate", "first_name", "last_name"])
    
        self.__add_products_config = Config(self.host, self.user, self.password, self.database, "add_products", ["id", "owner_id", "product_id", "vending_machine_id", "quantity", "timestamp"], "id")
        self.__add_products_config_pub = ConfigPub()
        self.__add_products_config_sub = ConfigSub()
        self.__add_products = DatabaseManager(self.__add_products_config, self.__add_products_config_pub, self.__add_products_config_sub, immutable_columns=None, foreign_keys = ["owner_id", "product_id", "vending_machine_id"])

        self.__create_vending_machine_config = Config(self.host, self.user, self.password, self.database, "create_vending_machine", ["id", "owner_id", "vending_machine_id", "timestamp"], column_id="id")
        self.__create_vending_machine_config_pub = ConfigPub()
        self.__create_vending_machine_config_sub = ConfigSub()
        self.__create_vending_machine = DatabaseManager(self.__create_vending_machine_config, self.__create_vending_machine_config_pub, self.__create_vending_machine_config_sub, immutable_columns=None, foreign_keys=["owner_id", "vending_machine_id"])
    
        self.__product_complaint_config = Config(self.host, self.user, self.password, self.database, "product_complaint", ["id", "complaint_id", "product_id", "user_id", "timestamp"], column_id="id")
        self.__product_complaint_config_pub = ConfigPub()
        self.__product_complaint_config_sub = ConfigSub()
        self.__product_complaint = DatabaseManager(self.__product_complaint_config, self.__product_complaint_config_pub, self.__product_complaint_config_sub, immutable_columns=None, foreign_keys=["complaint_id", "product_id", "user_id"])

        self.__product_comment_config = Config(self.host, self.user, self.password, self.database, "product_comment", ["id", "comment_id", "product_id", "user_id", "timestamp"], column_id="id")
        self.__product_comment_config_pub = ConfigPub()
        self.__product_comment_config_sub = ConfigSub()
        self.__product_comment = DatabaseManager(self.__product_comment_config, self.__product_comment_config_pub, self.__product_comment_config_sub, immutable_columns=None, foreign_keys=["comment_id", "product_id", "user_id"])

        self.__purchase_transaction_config = Config(self.host, self.user, self.password, self.database, "purchase_transaction", ["id", "user_id", "product_id", "vending_machine_id", "timestamp", "quantity", "amount_paid_per_unit"], column_id="id")
        self.__purchase_transaction_config_pub = ConfigPub()
        self.__purchase_transaction_config_sub = ConfigSub()
        self.__purchase_transaction = DatabaseManager(self.__purchase_transaction_config, self.__purchase_transaction_config_pub, self.__purchase_transaction_config_sub, immutable_columns=None, foreign_keys=["user_id", "product_id", "vending_machine_id"])
        
        self.__vending_machine_complaint_config = Config(self.host, self.user, self.password, self.database, "vending_machine_complaint", ["id", "complaint_id", "vending_machine_id", "user id", "timestamp"], column_id="id")
        self.__vending_machine_complaint_config_pub = ConfigPub()
        self.__vending_machine_complaint_config_sub = ConfigSub()
        self.__vending_machine_complaint = DatabaseManager( self.__vending_machine_complaint_config, self.__vending_machine_complaint_config_pub, self.__vending_machine_complaint_config_sub, immutable_columns=None, foreign_keys=["complaint_id", "vending_machine_id", "user id"])

        #Ouve: tabela de quem ouve
        #Pub: atualiza
        self.__vending_machine_comment_config = Config(self.host, self.user, self.password, self.database, "vending_machine_comment", ["id", "comment_id", "vending_machine id", "user_id", "timestamp"], column_id="id")
        self.__vending_machine_comment_config_pub = ConfigPub()
        self.__vending_machine_comment_config_sub = ConfigSub()
        self.__vending_machine_comment = DatabaseManager( self.__vending_machine_comment_config, self.__vending_machine_comment_config_pub, self.__vending_machine_comment_config_sub, immutable_columns=None, foreign_keys=["comment_id", "vending_machine id", "user_id"])

        self.__dict_instance_tables = {
            "products_profile": self.__products_profile,
            "comments_profile": self.__comments_profile,
            "users_profile": self.__users_profile,
            "complaints_profile": self.__complaints_profile,
            "vending_machines_profile": self.__vending_machines_profile,
            "owners_profile": self.__owners_profile
        }
        
        self.__dict_relationship_tables = {            
            "add_products": self.__add_products,
            "create_vending_machine": self.__create_vending_machine,
            "product_complaint": self.__product_complaint,
            "product_comment": self.__product_comment,
            "purchase_transaction": self.__purchase_transaction,
            "vending_machine_complaint": self.__vending_machine_complaint,
            "vending_machine_comment": self.__vending_machine_comment
            }

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
    def dict_instance_tables(self):
        return self.__dict_instance_tables
    
    @property
    def dict_relationship_tables(self):
        return self.__dict_relationship_tables

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

    @dict_instance_tables.setter
    def dict_instance_tables(self, new_dict_instance_tables):
        self.__dict_instance_tables = new_dict_instance_tables

    @dict_relationship_tables.setter
    def dict_relationship_tables(self, new_dict_relationship_tables):
        self.__dict_relationship_tables = new_dict_relationship_tables

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
    def create_vending_machine(self):
        return self.__create_vending_machine

    @property
    def add_products(self):
        return self.__add_products

    @property
    def owners_profile(self):
        return self.__owners_profile

    @property
    def vending_machines_profile(self):
        return self.__vending_machines_profile

    @property
    def complaints_profile(self):
        return self.__complaints_profile

    @property
    def users_profile(self):
        return self.__users_profile

    @property
    def comments_profile(self):
        return self.__comments_profile

    @property
    def products_profile(self):
        return self.__products_profile

    @vending_machine_comment.setter
    def vending_machine_comment(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__vending_machine_comment.delete_table()
            del self.__dict_relationship_tables["vending_machine_comment"]
            self.__vending_machine_comment = DatabaseManager( new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_relationship_tables[new_config.table_name] = self.__vending_machine_comment 
            logger.info(f"Update vending_machine_comment, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @vending_machine_complaint.setter
    def vending_machine_complaint(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__vending_machine_complaint.delete_table()
            del self.__dict_relationship_tables["vending_machine_complaint"]
            self.__vending_machine_complaint = DatabaseManager( new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_relationship_tables[new_config.table_name] = self.__vending_machine_complaint
            logger.info(f"Update vending_machine_complaint, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @purchase_transaction.setter
    def purchase_transaction(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__purchase_transaction.delete_table()
            del self.__dict_relationship_tables["purchase_transaction"]
            self.__purchase_transaction = DatabaseManager(new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns)
            self.__dict_relationship_tables[new_config.table_name] = self.__purchase_transaction
            logger.info(f"Update purchase_transaction, new name: {new_config.table_name}")
        except Exception as e:
                logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @product_comment.setter
    def product_comment(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__product_comment.delete_table()
            del self.__dict_relationship_tables["product_comment"]
            self.__product_comment = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_relationship_tables[new_config.table_name] = self.__product_comment
            logger.info(f"Update product_comment, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")


    @product_complaint.setter
    def product_complaint(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__product_complaint.delete_table()
            del self.__dict_relationship_tables["product_complaint"]
            self.__product_complaint = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_relationship_tables[new_config.table_name] = self.__product_complaint
            logger.info(f"Update product_complaint, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @create_vending_machine.setter
    def create_vending_machine(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__create_vending_machine.delete_table()
            del self.__dict_relationship_tables["create_vending_machine"]
            self.__create_vending_machine = DatabaseManager(new_config, new_config_pub, new_config_sub,new_immutable_columns, new_foreign_keys)
            self.__dict_relationship_tables[new_config.table_name] = self.__create_vending_machine
            logger.info(f"Update create_vending_machine, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @add_products.setter
    def add_products(self, new_config, new_config_pub, new_config_sub, new_foreign_keys, new_immutable_columns=None):
        try:
            self.__add_product.delete_table()
            del self.__dict_relationship_tables["add_products"]
            self.__add_product = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_relationship_tables[new_config.table_name] = self.__add_product
            logger.info(f"Update add_products, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @owners_profile.setter
    def owners_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__owners_profile.delete_table()
            del self.__dict_instance_tables["owners_profile"]
            self.__owners_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_instance_tables[new_config.table_name] = self.__owners_profile
            logger.info(f"Update owners_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @vending_machines_profile.setter
    def vending_machines_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__vending_machines_profile.delete_table()
            del self.__dict_instance_tables["vending_machine"]
            self.__vending_machines_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_instance_tables[new_config.table_name] = self.__vending_machines_profile
            logger.info(f"Update vending_machines_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @complaints_profile.setter
    def complaints_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__complaints_profile.delete_table()
            del self.__dict_instance_tables["complaints_profile"]
            self.__complaints_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_instance_tables[new_config.table_name] = self.__complaints_profile
            logger.info(f"Update complaints_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failled to setter {new_config.table_name}: {e}")

    @users_profile.setter
    def users_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__users_profile.delete_table()
            del self.__dict_instance_tables["users_profile"]
            self.__users_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_instance_tables[new_config.table_name] = self.__users_profile
            logger.info(f"Update users_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failled to setter {new_config.table_name}: {e}")

    @comments_profile.setter
    def comments_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
        try:
            self.__comments_profile.delete_table()
            del self.__dict_instance_tables["comments_profile"]
            self.__comments_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_instance_tables[new_config.table_name] = self.__comments_profile
            logger.info(f"Update comments_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")

    @products_profile.setter
    def products_profile(self, new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys):
        try:
            self.__products_profile.delete_table()
            del self.__dict_instance_tables["products_profile"]
            self.__products_profile = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns, new_foreign_keys)
            self.__dict_instance_tables[new_config.table_name] = self.__products_profile
            logger.info(f"Update products_profile, new name: {new_config.table_name}")
        except Exception as e:
            logger.error(f"Failed to setter {new_config.table_name}: {e}")