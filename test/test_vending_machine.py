import unittest
from src.vending_machine import VendingMachine

class TestVendingMachine(unittest.TestCase):
    # Uma vez que o método setUp é chamado antes de cada teste, a instância do objeto vending_machine é criada antes de cada teste
    def setUp(self):
        self.vending_machine = VendingMachine("1", "Vending Machine 1", "1", "Location 1")

    # Testes para o método get_id
    def test_get_id(self):
        self.assertEqual(self.vending_machine.get_id(), "1")

    # Testes para o método get_name
    def test_get_name(self):
        self.assertEqual(self.vending_machine.get_name(), "Vending Machine 1")

    # Testes para o método set_name
    def test_set_name(self):
        self.vending_machine.set_name("Vending Machine 2")
        self.assertEqual(self.vending_machine.get_name(), "Vending Machine 2")

        # Teste para palavras ofensivas
        self.vending_machine.set_name("Vending Machine Jerk")
        self.assertEqual(self.vending_machine.get_name(), "Vending Machine")

        # Teste para nomes longos
        self.vending_machine.set_name("Vending Machine 2" * 100)
        self.assertEqual(self.vending_machine.get_name(), "Vending Machine")

    # Testes para o método get_owner_id
    def test_get_owner_id(self):
        self.assertEqual(self.vending_machine.get_owner_id(), "1")

    # Testes para o método get_location
    def test_get_location(self):
        self.assertEqual(self.vending_machine.get_location(), "Location 1")

    # Testes para o método set_location
    def test_set_location(self):
        self.vending_machine.set_location("Location 2")
        self.assertEqual(self.vending_machine.get_location(), "Location 2")

        # Teste para palavras ofensivas
        self.vending_machine.set_location("Location Jerk")
        self.assertEqual(self.vending_machine.get_location(), "Location")

        # Teste para nomes longos
        self.vending_machine.set_location("Location 2" * 100)
        self.assertEqual(self.vending_machine.get_location(), "Location")

    # Testes para o método add_product
    def test_get_products_empty(self):
        self.assertEqual(self.vending_machine.get_products(), [])

    # Testes para o método add_product e get_products
    def test_get_products_one_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.assertEqual(self.vending_machine.get_products(), [{'name': 'Coke', 'price': 1.50, 'quantity': 10}])
    
    def test_get_products_multiple_products(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.add_product(name="Pepsi", price=1.75, quantity=5)
        self.assertEqual(self.vending_machine.get_products(), [{'name': 'Coke', 'price': 1.50, 'quantity': 10}, {'name': 'Pepsi', 'price': 1.75, 'quantity': 5}])

    # Testes para o método get_product
    def test_get_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 1.50, 'quantity': 10})
    
    def test_get_product_not_found(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.assertEqual(self.vending_machine.get_product(name="Pepsi"), None)

    # Testes para o método remove_product
    def test_remove_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.remove_product(name="Coke")
        self.assertEqual(self.vending_machine.get_products(), [])
    
    def test_remove_product_not_found(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.remove_product(name="Pepsi")
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 1.50, 'quantity': 10})

    # Testes para o método update_product
    def test_update_product(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.update_product(name="Coke", price=2.00, quantity=15)
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 2.00, 'quantity': 15})
    
    def test_update_product_not_found(self):
        self.vending_machine.add_product(name="Coke", price=1.50, quantity=10)
        self.vending_machine.update_product(name="Pepsi", price=2.00, quantity=15)
        self.assertEqual(self.vending_machine.get_product(name="Coke"), {'name': 'Coke', 'price': 1.50, 'quantity': 10})
        self.assertEqual(self.vending_machine.get_product(name="Pepsi"), None)

    # Uma vez que o método tearDown é chamado após cada teste, a instância do objeto vending_machine é deletada após cada teste
    def tearDown(self) -> None:
        del self.vending_machine
        return super().tearDown()

if __name__ == '__main__':
    unittest.main(verbosity=2)