

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
        
    def add_product(self, **kwargs):
        """
    '   Add a product to the vending machine

        Parameters:
        - kwargs (dict): Contains parameters for the product to be added

        Returns:
        - None
        """
        pass
    def remove_product(self, **kwargs):
        """
        Remove a product from the vending machine

        Parameters:
        - kwargs (dict): Contains parameters that identify the product to be removed

        Returns:
        - None
        """
        pass