import unittest
from unittest.mock import MagicMock, patch

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from decorators import foreign_key_validation

class TestClass:
    def __init__(self):
        self.foreign_keys = ["complaints", "product", "users"]

    @foreign_key_validation(["complaints", "product", "users"])
    def insert_row(self, complaint_id, product_id, user_id):
        return "Record insertd successfully"
    
class TestForeignValidationDecorator(unittest.TestCase):
    @patch("main_file.relationship_manager_central")
    def test_foreign_key_validation_success(self, mock_relationship_manager_central):
        # Mock para simular a existência das chaves estrangeiras
        mock_relationship_manager_central.dict_relationships = {
            "complaints": MagicMock(),
            "products": MagicMock(),
            "users": MagicMock()
        }
        
        # Simula que todos os IDs existem nas tabelas correspondentes
        mock_relationship_manager_central.dict_relationships["complaints"].get_by_id.return_value = True
        mock_relationship_manager_central.dict_relationships["products"].get_by_id.return_value = True
        mock_relationship_manager_central.dict_relationships["users"].get_by_id.return_value = True

        # Instancia a classe e chama o método decorado
        example = TestClass()
        result = example.insert_row(complaint_id="1", product_id="2", user_id="3")

        self.assertEqual(result, "Record inserted successfully")
'''
    @patch('main_file.relationship_manager_central')  # substitua 'your_module' pelo nome do módulo correto
    def test_foreign_key_validation_missing_foreign_key(self, mock_relationship_manager_central):
        # Mock para simular o relacionamento
        mock_relationship_manager_central.dict_relationships = {
            "complaints": MagicMock(),
            "products": MagicMock(),
            "users": MagicMock()
        }

        # Simula a falta de um ID de chave estrangeira
        mock_relationship_manager_central.dict_relationships["complaints"].get_by_id.return_value = None  # Não existe
        mock_relationship_manager_central.dict_relationships["products"].get_by_id.return_value = True
        mock_relationship_manager_central.dict_relationships["users"].get_by_id.return_value = True

        # Instancia a classe e chama o método decorado
        example = TestClass()
        result = example.insert_row(complaint_id="1", product_id="2", user_id="3")

        # Verifica se o decorador retornou o erro esperado
        self.assertEqual(result, "complaint_id `1` does not exist.")

    @patch('main_file.relationship_manager_central')  # substitua 'your_module' pelo nome do módulo correto
    def test_foreign_key_validation_multiple_missing_keys(self, mock_relationship_manager_central):
        # Mock para simular o relacionamento
        mock_relationship_manager_central.dict_relationships = {
            "complaints": MagicMock(),
            "products": MagicMock(),
            "users": MagicMock()
        }

        # Simula a falta de vários IDs de chaves estrangeiras
        mock_relationship_manager_central.dict_relationships["complaints"].get_by_id.return_value = None
        mock_relationship_manager_central.dict_relationships["products"].get_by_id.return_value = None
        mock_relationship_manager_central.dict_relationships["users"].get_by_id.return_value = True

        # Instancia a classe e chama o método decorado
        example = TestClass()
        result = example.insert_row(complaint_id="1", product_id="2", user_id="3")

        # Verifica se o decorador retorna o primeiro erro encontrado
        self.assertEqual(result, "complaint_id `1` does not exist.")
'''
if __name__ == "__main__":
    unittest.main()