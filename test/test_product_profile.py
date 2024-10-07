import unittest
import uuid
from src.ProductProfile import ProductProfile
from src.utils import load_banned_words, contains_banned_words

class TestProductProfile(unittest.TestCase):

    def setUp(self):
        """This method sets up a default product to be used in each test."""
        # Gera um UUID único para o product_id
        self.product_id = str(uuid.uuid4())  
        
        self.product = ProductProfile(product_id=self.product_id, name="The Good Cookie", description="A good cookie, that cookie covered in chocolate chips and filled with a filling that makes you feel goood.", price=5.50)
        self.banned_words = load_banned_words() 

    def test_initialization(self):
        """Test if the product profile is initialized correctly."""
        self.assertEqual(self.product.name, "The Good Cookie") 
        self.assertEqual(self.product.description, "A good cookie, that cookie covered in chocolate chips and filled with a filling that makes you feel goood.")
        self.assertEqual(self.product.price, 5.50)
        self.assertIsNotNone(self.product.product_id)  
        self.assertEqual(self.product.product_id, self.product_id)

    def test_name_validity(self):
        """Test if the product name is valid."""
        self.assertTrue(contains_banned_words("The Twat Cookie"))  
        self.assertFalse(contains_banned_words("The Good Cookie"))
        self.assertLessEqual(len(self.product.name), 35)

    def test_description_validity(self):
        """Test if the product description is valid."""
        self.assertTrue(contains_banned_words("A twat cookie, that cookie covered in chocolate chips and filled with a filling that makes you feel goood."))  
        self.assertFalse(contains_banned_words("Just a good cookie, nothing special, like you as an human.")) 
        self.assertLessEqual(len(self.product.description), 300)

    def test_update_name(self):
        """Test if the product name updates correctly."""
        self.product.update_name("The Great Cookie")
        self.assertEqual(self.product.name, "The Great Cookie")

    def test_update_description(self):
        """Test if the product description updates correctly."""
        self.product.update_description("Just a good cookie, nothing special, like you as an human.")
        self.assertEqual(self.product.description, "Just a good cookie, nothing special, like you as an human.")

    def test_update_price(self):
        """Test if the product price updates correctly."""
        self.product.update_price(6.50)
        self.assertEqual(self.product.price, 6.50)

    def test_apply_discount(self):
        """Test if the discount is applied correctly."""
        self.product.apply_discount(10) 
        self.assertEqual(self.product.price, 4.95)
        with self.assertRaises(ValueError):
            self.product.apply_discount(110)  
        with self.assertRaises(ValueError):
            self.product.apply_discount(-10)
        with self.assertRaises(ValueError):
            self.product.apply_discount(0)
        with self.assertRaises(ValueError):
            self.product.apply_discount("10")
        with self.assertRaises(ValueError):
            self.product.apply_discount(10.5)

    def test_delete_product(self):
        """Test if the product is deleted correctly."""
        self.product.delete_product()
        self.assertIsNone(self.product.name)
        self.assertIsNone(self.product.description)
        self.assertIsNone(self.product.price)


if __name__ == '__main__':
    unittest.main()