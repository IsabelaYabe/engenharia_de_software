"""
    Module for creating the DatabaseManagerCentral class.

    Author: Isabela Yabe
    Last Modified: 03/11/2024
    Status: Preciso atualiza colocando o no init, por logs e fazer testes

    Dependencies:
        - product_profile
        - decorators
        - tables
"""
from database_manager import DatabaseManager, Config, ConfigPub, ConfigSub
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
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

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

        self.__products_config = Config(self.host, self.user, self.password, self.database, "products_profile", ["id", "name", "description", "price", "quantity"], "id")
        self.__products_config_pub = ConfigPub()
        self.__products_config_sub = ConfigSub()
        self.__products_profile = DatabaseManager(self.__products_config, self.__products_config_pub, self.__products_config_sub, immutable_columns=None, foreign_keys=None)
        @property
        def products_profile(self):
            return self.__products_profile
        @products_profile.setter
        def products_profile(self, new_products_config, new_products_config_pub, new_products_config_sub, new_immutable_columns, new_foreign_keys):
            self.__products_profile.delete_table
            self.__products_profile = DatabaseManager(new_products_config, new_products_config_pub, new_products_config_sub, new_immutable_columns, new_foreign_keys)

        self.__comments_config = Config(self.host, self.user, self.password, self.database, "comments_profile", ["id", "text", "timestamp"], "id")
        self.__comments_config_pub = ConfigPub()
        self.__comments_config_sub = ConfigSub()
        self.__comments_profile = DatabaseManager(self.__comments_config, self.__comments_config_pub, self.__comments_config_sub, immutable_columns=None, foreign_keys=None)
        @property
        def comments_profile(self):
            return self.__comments_profile
        @comments_profile.setter
        def comments_profile(self, new_comments_config, new_comments_config_pub, new_comments_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__comments_profile.delete_table()
            self.__comments_profile = DatabaseManager(new_comments_config, new_comments_config_pub, new_comments_config_sub, new_immutable_columns, new_foreign_keys)

        
        self.users_config = Config(self.host, self.user, self.password, self.database, "users_profile", ["id", "username", "email", "password", "first_name", "last_name", "birthdate", "phone number", "address"], "id")
        self.users_config_pub = ConfigPub()
        self.users_config_sub = ConfigSub()
        self.__users_profile = DatabaseManager(self.__users_config, self.__users_config_pub, self.__users_config_sub, immutable_columns=["birthdate", "first_name", "last_name"])
        @property
        def users_profile(self):
            return self.__users_profile
        @users_profile.setter
        def users_profile(self, new_users_config, new_users_config_pub, new_users_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__users_profile.delete_table()
            self.__users_profile = DatabaseManager(new_users_config, new_users_config_pub, new_users_config_sub, new_immutable_columns, new_foreign_keys)

        
        self.complaints_config = Config(self.host, self.user, self.password, self.database, "complaints_profile", ["id", "text", "timestamp"], "id")
        self.complaints_config_pub = ConfigPub()
        self.complaints_config_sub = ConfigSub()
        self.__complaints_profile = DatabaseManager(self.__complaints_config, self.__complaints_config_pub, self.__complaints_config_sub, immutable_columns=None, foreign_keys=None)
        @property
        def complaints_profile(self):
            return self.__complaints_profile
        @complaints_profile.setter
        def complaints_profile(self, new_complaints_config, new_complaints_config_pub, new_complaints_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__complaints_profile.delete_table()
            self.__complaints_profile = DatabaseManager(new_complaints_config, new_complaints_config_pub, new_complaints_config_sub, new_immutable_columns, new_foreign_keys)

        
        self.vending_machines_config = Config(self.host, self.user, self.password, self.database, "vending_machines_profile", ["id", "name", "location", "status"], "id")
        self.vending_machine_config_pub = ConfigPub()
        self.vending_machine_config_sub = ConfigSub()
        self.__vending_machines_profile = DatabaseManager(self.__vending_machines_config, self.__vending_machine_config_pub, self.__vending_machine_config_sub, immutable_columns=None, foreign_keys=None)
        @property
        def vending_machines_profile(self):
            return self.__vending_machines_profile
        @vending_machines_profile.setter
        def vending_machines_profile(self, new_vending_machines_config, new_vending_machine_config_pub, new_vending_machine_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__vending_machines_profile.delete_table()
            self.__vending_machines_profile = DatabaseManager(new_vending_machines_config, new_vending_machine_config_pub, new_vending_machine_config_sub, new_immutable_columns, new_foreign_keys)


        self.owners_config = Config(self.host, self.user, self.password, self.database, "owners_profile", ["id", "ownername", "email", "password", "first name", "last name", "birthdate", "phone_number", "address"], "id")
        self.owners_config_pub = ConfigPub()
        self.owners_config_sub = ConfigSub()
        self.__owners_profile = DatabaseManager(self.__owners_config, self.__owners_config_pub, self.__owners_config_sub, immutable_columns=["birthdate", "first_name", "last_name"])
        @property
        def owners_profile(self):
            return self.__owners_profile
        @owners_profile.setter
        def owners_profile(self, new_owners_config, new_owners_config_pub, new_owners_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__owners_profile.delete_table()
            self.__owners_profile = DatabaseManager(new_owners_config, new_owners_config_pub, new_owners_config_sub, new_immutable_columns, new_foreign_keys)
        
        self.__add_products_config = Config(self.host, self.user, self.password, self.database, "add_products", ["id", "owner_id", "product_id", "vending_machine_id", "quantity", "timestamp"], "id")
        self.__add_products_config_pub = ConfigPub()
        self.__add_products_config_sub = ConfigSub()
        self.__add_products = DatabaseManager(self.__add_products_config, self.__add_products_config_pub, self.__add_products_config_sub, immutable_columns=None, foreign_keys = ["owner_id", "product_id", "vending_machine_id"])
        @property
        def add_products(self):
            return self.__add_products
        @add_products.setter
        def add_products(self, new_add_products_config, new_add_products_config_pub, new_products_config_sub, new_immutable_columns, new_foreign_keys):
            self.__add_product.delete_table()
            self.__add_product = DatabaseManager(new_add_products_config, new_add_products_config_pub, new_products_config_sub, new_immutable_columns, new_foreign_keys)

        self.create_vending_machine_config = Config(self.host, self.user, self.password, self.database, "create_vending_machine", ["id", "owner_id", "vending_machine_id", "timestamp"], column_id="id")
        self.create_vending_machine_config_pub = ConfigPub()
        self.create_vending_machine_config_sub = ConfigSub()
        self.__create_vending_machine = DatabaseManager(
            self.__create_vending_machine_config,
            self.__create_vending_machine_config_pub,
            self.__create_vending_machine_config_sub,
            immutable_columns=None,
            foreign_keys=["owner_id", "vending_machine_id"]
        )
        @property
        def create_vending_machine(self):
            return self.__create_vending_machine
        @create_vending_machine.setter
        def create_vending_machine(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__create_vending_machine.delete_table()
            self.__create_vending_machine = DatabaseManager(new_config, new_config_pub, new_config_sub,new_immutable_columns, new_foreign_keys)
        
        self.product_complaint_config = Config(self.host, self.user, self.password, self.database, "product_complaint", ["id", "complaint_id", "product_id", "user_id", "timestamp"], column_id="id")
        self.products_complaing_config_pub = ConfigPub()
        self.products_complaing_config_sub = ConfigSub()
        self.__product_complaint = DatabaseManager(self.__product_complaint_config, self.__product_complaint_config_pub,self.__product_complaint_config_sub, immutable_columns=None,foreign_keys=["complaint_id", "product_id", "user_id"]
        )
        @property
        def product_complaint(self):
            return self.__product_complaint
    
        @product_complaint.setter
        def product_complaint(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__product_complaint.delete_table()
            self.__product_complaint = DatabaseManager(new_config, new_config_pub, new_config_sub, new_immutable_columns,new_foreign_keys)

        self.product_comment_config = Config(self.host, self.user, self.password, self.database, "product_comment", ["id", "comment_id", "product_id", "user_id", "timestamp"], column_id="id")
        self.products_review_config_pub = ConfigPub()
        self.products_review_config_sub = ConfigSub()
        self.__product_comment = DatabaseManager(self.__product_comment_config,self.__product_comment_config_pub,self.__product_comment_config_sub,immutable_columns=None,foreign_keys=["comment_id", "product_id", "user_id"])

        @property
        def product_comment(self):
            return self.__product_comment

        @product_comment.setter
        def product_comment(self, new_config, new_config_pub, new_config_sub, new_immutable_columns=None, new_foreign_keys=None):
            self.__product_comment.delete_table()
            self.__product_comment = DatabaseManager(new_config,new_config_pub,new_config_sub,new_immutable_columns,new_foreign_keys)

        self.purchase_transaction_config = Config(self.host, self.user, self.password, self.database, "purchase_transaction", ["id", "user_id", "product_id", "vending_machine_id", "timestamp", "quantity", "amount_paid_per_unit"], column_id="id")
        self.purchase_transaction_config_pub = ConfigPub()
        self.purchase_transaction_config_sub = ConfigSub()
        self.purchase_transaction = DatabaseManager(self.purchase_transaction_config)

        self.vending_machine_complaint_config = Config(self.host, self.user, self.password, self.database, "vending_machine_complaint", ["id", "complaint_id", "vending_machine_id", "user id", "timestamp"], column_id="id")
        self.vending_machine_complaint_config_pub = ConfigPub()
        self.vending_machine_complaint_config_sub = ConfigSub()
        self.vending_machine_complaint = DatabaseManager(self.vending_machine_complaint_config)

        self.vending_machine__comment_config = Config(self.host, self.user, self.password, self.database, "vending_machine__comment", ["id", "comment_id", "vending_machine id", "user_id", "timestamp"], column_id="id")
        self.vending_machine__comment_config_pub = ConfigPub()
        self.vending_machine__comment_config_sub = ConfigSub()
        self.vending_machine__comment = DatabaseManager(self.vending_machine__comment_config)

           