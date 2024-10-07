import uuid
from utils import contains_banned_words
    

class ProductProfile:
    """
    ProductProfile class.
    
    This class represents a product profile, storing its ID, name, description, and price.

    Attributes:
    - product_id (str): The product ID.
    - name (str): The name of the product.
    - description (str): The description of the product.
    - price (float): The price of the product.

    Methods:
    - __init__(self, product_id=None, name="", description="", price=0.0): Constructor for the ProductProfile class.
    - __set_name(self, name): Define a name of the product, ensuring it is valid.
    - __set_price(self, price): Define a price for the product, ensuring it is valid.
    - __set_description(self, description): Define a description for the product, ensuring it is valid.
    - update_price(self, price): Update the price for the product, ensuring it is valid.
    - update_name(self, name): Update the name for the product, ensuring it is valid.
    - update_description(self, description): Update the description for the product, ensuring it is valid.
    - delete_product(self): Delete the product, setting its attributes to None.

    """
    def __init__(self, name, description, price):
        """
        Constructor for the ProductProfile class.
        
        Parameters:
            product_id (str): The product ID.
            name (str): The name of the product.
            description (str): The description of the product.
            price (float): The price of the product.

        Returns:
            None
        """
        self.product_id.__set_product_id()
        self.__set_name(name)
        self.__set_description(description)
        self.__set_price(price)
    
    def __set_product_id(self):
        """
        Define a product ID, ensuring it is valid.

        Parameters:
            None

        Returns:
            None
        """
    
    def __set_name(self, name):
        """
        Define a name of the product, ensuring it is valid.

        Parameters:
            name (str): The name of the product.
        
        Returns:
            None
        """

    def __set_price(self, price):
        """
        Define a price for the product, ensuring it is valid.

        Parameters:
            price (float): The price of the product.

        Returns:
            None
        """


    def __set_description(self, description):
        """
        Define a description for the product, ensuring it is valid.

        Parameters:
            description (str): The description of the product.

        Returns:
            None
        """


    def update_price(self, price):
        """
        Update the price for the product, ensuring it is valid.

        Parameters:
            price (float): The price of the product.

        Returns:
            None
        """


    def update_name(self, name):
        """
        Update the name for the product, ensuring it is valid.	

        Parameters:
            name (str): The name of the product.

        Returns:
            None
        """


    def update_description(self, description):
        """
        Update the description for the product, ensuring it is valid.

        Parameters:
            description (str): The description of the product.

        Returns:
            None
        """

    def delete_product(self):
        """
        Delete the product, setting its attributes to None.

        Parameters:
            None

        Returns:
            None
        """