import unittest
import requests
from bs4 import BeautifulSoup

class TestVendingMachinePageContent(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://example.com"
        self.param = "machine_id=1"
        self.url = f"{self.base_url}?{self.param}"

    def test_access_page(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.assertEqual(soup.title.string, "VM 1")
    
    def test_page_heading(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.assertEqual(soup.h1.string, "Vending Machine 1")

    def test_page_content(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        self.assertEqual(soup.p.string, "This is vending machine 1")

    def test_product_list(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("li")
        self.assertEqual(len(products), 3)
        self.assertEqual(products[0].string, "Cola")
        self.assertEqual(products[1].string, "Chips")
    
    def tearDown(self) -> None:
        del self.vm
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()