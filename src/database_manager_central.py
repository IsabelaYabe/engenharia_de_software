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

from profiles.product_profile import ProductProfile
from profiles.comment_profile import CommentProfile
from profiles.user_profile import UserProfile
from profiles.complaint_profile import ComplaintProfile
from profiles.vending_machine_profile import VMProfile
from profiles.owner_profile import OwnerProfile
from relationships.create_vending_machine import CreateVM
from relationships.product_complaint import ProductComplaint
from relationships.product_review import ProductReview
from relationships.purchase_transaction import PurchaseTransaction
from relationships.vending_machine_complaint import VMComplaint
from relationships.vending_machine_review import VMReview 

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
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

        self.__product_profile = ProductProfile(self.host, self.user, self.password, self.database)
        self.__comment_profile = CommentProfile(self.host, self.user, self.password, self.database)
        self.__user_profile = UserProfile(self.host, self.user, self.password, self.database)
        self.__complaint_profile = ComplaintProfile(self.host, self.user, self.password, self.database)
        self.__vending_machine_profile = VMProfile(self.host, self.user, self.password, self.database)
        self.__owner_profile = OwnerProfile(self.host, self.user, self.password, self.database)

        self.__create_vm = CreateVM(self.host, self.user, self.password, self.database)
        self.__product_complaint = ProductComplaint(self.host, self.user, self.password, self.database)
        self.__product_review = ProductReview(self.host, self.user, self.password, self.database)
        self.__purchase_transaction = PurchaseTransaction(self.host, self.user, self.password, self.database)
        self.__vending_machine_complaint = VMComplaint(self.host, self.user, self.password, self.database)
        self.__vending_machine_review = VMReview(self.host, self.user, self.password, self.database)
        
        self.__dict_tables = {
            "product table": self.__product_profile,
            "comment table": self.__comment_profile,
            "user table": self.__user_profile,
            "complaint profile": self.__complaint_profile,
            "vm table": self.__vending_machine_profile,
            "owner table": self.__owner_profile
            }
        
        self.__dict_relationships = {
            "create vm": self.__create_vm,
            "product complaint": self.__product_complaint,
            "product review": self.__product_review,
            "purchase transaction": self.__purchase_transaction,
            "vending machine complaint": self.__vending_machine_complaint,
            "vending machine review": self.__vending_machine_review
            }
        
        self.tables_on = False
        self.relationship_on = False

        self._create_all_tables()
        self._create_all_relationships()

    def _create_all_tables(self):
        """
        Creates all the necessary tables in the database.
        """
        for table in self.__dict_tables.values():
            try:
                table._create_table()
            except:
                raise
        self.tables_on = True

    def _create_all_relationships(self):
        for relationship in self.__dict_relationships.values():
            try:    
                relationship._create_table()
            except:
                raise
        self.relationship_on = True
    
    def _drop_all_tables(self):
        """
        Drops all tables from the database.
        """
        if self.tables_on:
            for table in self.__dict_tables.values():
                try:
                    table._delete_table()
                except:
                    raise
            self.tables_on = False
        else:
            print("There is no table to delete")

    def _drop_all_relationship(self):
        if self.relationship_on:
            for relationship in self.__dict_relationships.values():
                try:
                    relationship._delete_table()
                except:
                    raise
            else:
                print("There is no relationship to delete")
           
    def _reset_database(self):
        """
        Resets the database by dropping all tables and then recreating them.
        """
        self._drop_all_tables()
        self._drop_all_relationship()
        self._create_all_tables()
        self._create_all_relationships()

    def _add_instance(self, table_manager_num, **kwargs):
        """
        Adds an instance to a table managed by the given table_manager_num.

        Parameters:
            table_manager_num (int): The num's table.
            **kwargs: Keyword arguments representing the data of the instance.

        Return:
            bool: True if the instance was added, False otherwise.
        """
        
        self.__dict_tables[table_manager_num].create_instance(kwargs)
    
    def _update_instance_itens(self, table_manager_num, record_id, column_id, **kwargs):
        self.__dict_tables[table_manager_num]._update_row(record_id, column_id, kwargs) 

    def get_by_id(self, table_manager_num, record_id):
        self.__dict_tables[table_manager_num].get_by_id(record_id)
    
    

        
        