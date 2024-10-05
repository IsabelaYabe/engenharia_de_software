

class VendingMachine():
    """
    VendingMachine class
    
    Attributes:
    - ID: str
    - name: str
    - owner_ID: str
    - location: str
    - products: list

    Methods:
    - get_name: get the name of the vending machine
    - get_location: get the location of the vending machine
    - get_products: get all products in the vending machine
    - get_product: get a specific product in the vending machine
    - add_product: add a product to the vending machine
    - remove_product: remove a product from the vending machine
    - update_product: update a product in the vending machine
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
        self.ID = ID
        self.name = name
        self.owner_ID = owner_ID
        self.location = location
        self.products = []
    def get_name(self):
        """
        Get the name of the vending machine

        Parameters:
        - None

        Returns:
        - str: Name of the vending machine
        """
        return self.name 
    def get_location(self):
        """
        Get the location of the vending machine

        Parameters:
        - None

        Returns:
        - str: Location of the vending machine
        """
        return self.location
    def get_products(self):
        """
        Get all products in the vending machine

        Parameters:
        - None

        Returns:
        - list: List of products in the vending machine
        """
        return self.products  
    def get_product(self, *args):
        """
        Get a specific product in the vending machine

        Parameters:
        - args (list): Contains parameters that identify the product to be retrieved

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
    def remove_product(self, *args):
        """
        Remove a product from the vending machine

        Parameters:
        - args (list): Contains parameters that identify the product to be removed

        Returns:
        - None
        """
        pass
    def update_product(self, *args, **kwargs):
        """
        Update a product in the vending machine

        Parameters:
        - args (list): Contains parameters that identify the product to be updated
        - kwargs (dict): Contains parameters for the product to be updated

        Returns:
        - None
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