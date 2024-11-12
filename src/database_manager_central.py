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

        self.product_profile = ProductProfile(self.host, self.user, self.password, self.database)
        self.comment_profile = CommentProfile(self.host, self.user, self.password, self.database)
        self.user_profile = UserProfile(self.host, self.user, self.password, self.database)
        self.complaint_profile = ComplaintProfile(self.host, self.user, self.password, self.database)
        self.vending_machine_profile = VMProfile(self.host, self.user, self.password, self.database)
        self.owner_profile = OwnerProfile(self.host, self.user, self.password, self.database)
        
        self.dict_tables = {
            "product table": self.product_profile,
            "comment table": self.comment_profile,
            "user table": self.user_profile,
            "complaint profile": self.complaint_profile,
            "vm table": self.vending_machine_profile,
            "owner table": self.owner_profile
            }     