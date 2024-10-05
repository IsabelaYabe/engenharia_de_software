import unittest
from src.vending_machine import VendingMachine

class TestVendingMachine(unittest.TestCase):
    def setUp(self):
        self.vending_machine = VendingMachine("1", "Vending Machine 1", "1", "Location 1")

    def test_get_name(self):
        self.assertEqual(self.vending_machine.get_name(), "Vending Machine 1")

    def test_get_location(self):
        self.assertEqual(self.vending_machine.get_location(), "Location 1")

    def test_get_products_empty(self):
        self.assertEqual(self.vending_machine.get_products(), [])

    def test_get_products_one_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.assertEqual(self.vending_machine.get_products(), [{'name': 'Coke', 'price': 1.50, 'quantity': 10}])
    
    def test_get_products_multiple_products(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.add_product(name="Pepsi", price=1.75, quantity=5)
        self.assertEqual(self.vending_machine.get_products(), [{'name': 'Coke', 'price': 1.50, 'quantity': 10}, {'name': 'Pepsi', 'price': 1.75, 'quantity': 5}])

    def test_get_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 1.50, 'quantity': 10})

    def test_remove_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.remove_product(name="Coke")
        self.assertEqual(self.vending_machine.get_products(), [])

    def test_update_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.update_product(name="Coke", price=2.00, quantity=15)
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 2.00, 'quantity': 15})
    
    def test_update_product_not_found(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.update_product(name="Pepsi", price=2.00, quantity=15)
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 1.50, 'quantity': 10})
        self.assertEqual(self.vending_machine.get_product(name="Pepsi"), None)
    
    def test_remove_product_not_found(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.remove_product(name="Pepsi")
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 1.50, 'quantity': 10})
    
    def test_get_product_not_found(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.assertEqual(self.vending_machine.get_product(name="Pepsi"), None)

    def tearDown(self) -> None:
        del self.vending_machine
        return super().tearDown()

if __name__ == '__main__':
    unittest.main(verbosity=2)