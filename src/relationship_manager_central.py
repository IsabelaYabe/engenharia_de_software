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
from dataclasses import dataclass
from relationships.create_vending_machine import CreateVM
from relationships.product_complaint import ProductComplaint
from relationships.product_review import ProductReview
from relationships.purchase_transaction import PurchaseTransaction
from relationships.vending_machine_complaint import VMComplaint
from relationships.vending_machine_review import VMReview 
from decorators import singleton

@singleton
@dataclass
class RelationshipManagerCentral:
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

        self.create_vm = CreateVM(self.host, self.user, self.password, self.database)
        self.product_complaint = ProductComplaint(self.host, self.user, self.password, self.database)
        self.product_review = ProductReview(self.host, self.user, self.password, self.database)
        self.purchase_transaction = PurchaseTransaction(self.host, self.user, self.password, self.database)
        self.vending_machine_complaint = VMComplaint(self.host, self.user, self.password, self.database)
        self.vending_machine_review = VMReview(self.host, self.user, self.password, self.database)
        
        self.dict_relationships = {
            "create vm": self.create_vm,
            "product complaint": self.product_complaint,
            "product review": self.product_review,
            "purchase transaction": self.purchase_transaction,
            "vending machine complaint": self.vending_machine_complaint,
            "vending machine review": self.vending_machine_review
            }