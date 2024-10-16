

class VendingMachine():
    """
    VendingMachine class
    
    Attributes:
    - __ID: str
    - __name: str
    - __owner_ID: str
    - __location: str
    - __products: list

    Methods:
    - get_id: get the ID of the vending machine
    - get_name: get the name of the vending machine
    - __set_name: change the name of the vending machine
    - get_location: get the location of the vending machine
    - __set_location: change the location of the vending machine
    - get_owner_id: get the owner of the vending machine
    - get_products: get all products in the vending machine
    - get_product: get a specific product in the vending machine
    - add_product: add a product to the vending machine
    - remove_product: remove a product from the vending machine
    - update_product: update a product in the vending machine
    - __check_string: check if a string is valid
    """
    def __init__(self, ID, name, owner_ID, location, **kwargs):
        """
        Constructor for VendingMachine class
        
        Parameters:
        - ID (str): ID of the vending machine
        - name (str): Name of the vending machine
        - owner_ID (str): ID of the owner of the vending machine
        - location (str): Location of the vending machine
        - kwargs (dict): Contains additional parameters for the vending machine

        Returns:
        - None
        """
        self.__ID = ID
        self.__set_name(name)
        self.__set_owner_id(owner_ID)
        self.__set_location(location)
        self.__products = []
    
    def get_id(self):
        return self.__ID
    
    def get_name(self):
        return self.__name 
    
    def __set_name(self, name):
        self.__name = name

    def get_location(self):
        return self.__location
    
    def __set_location(self, location):
        self.__location = location

    def get_owner_id(self):
        return self.__owner_ID

    def get_products(self):
        return self.__products
     
    def get_product(self, *kwargs):
        """
        Get a specific product in the vending machine

        Parameters:
        - kwargs (dict): Contains parameters that identify the product to be retrieved

        Returns:
        - dict: Product in the vending machine
        """
        pass

    def add_product(self, **kwargs):
        """
    '   Add a product to the vending machine

        Parameters:
        - kwargs (dict): Contains parameters for the product to be added

        Returns:
        - None
        """
        pass

    def remove_product(self, *kwargs):
        """
        Remove a product from the vending machine

        Parameters:
        - kwargs (dict): Contains parameters that identify the product to be removed

        Returns:
        - None
        """
        pass

    def update_product(self, **kwargs):
        """
        Update a product in the vending machine

        Parameters:
        - kwargs (dict): Contains parameters that identify the product to be updated and provide the new values

        Returns:
        - None
        """
        pass

    def check_string(self, string):
        """
        Check if a string is valid

        Parameters:
        - string (str): String to be checked

        Returns:
        - bool: True if the string is valid, False otherwise
        """
        pass

    def __del__(self):
        """
        Destructor for VendingMachine class

        Parameters:
        - None

        Returns:
        - None
        """
        pass