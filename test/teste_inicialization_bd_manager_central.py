import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from database_manager_central import DatabaseManagerCentral, Config, ConfigPub, ConfigSub
from event_manager.event_manager import EventManager
from custom_logger import setup_logger

logger = setup_logger()


class TestDatabaseManagerCentral(unittest.TestCase):
    """
    Test suite for DatabaseManagerCentral initialization.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        # Define parâmetros básicos para teste
        self.host = "localhost"
        self.user = "root"
        self.password = "password"
        self.database = "test_db"

        # Mock do EventManager
        self.mock_event_manager = MagicMock(spec=EventManager)
        
        # Criação de instâncias reais de Config, ConfigPub e ConfigSub
        self.products_config = Config(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            table_name="products_profile",
            columns=["id", "name", "description", "price", "quantity", "vending_machine_id", "timestamp"]
        )

        self.purchase_transaction_config_pub = ConfigPub(
            event_manager=self.mock_event_manager,
            events_type_pub=["PurchaseProductEvent"]
        )

        self.products_config_sub = ConfigSub(
            event_manager=self.mock_event_manager,
            events_type_sub=["PurchaseProductEvent"]
        )

    @patch("database_manager_central.DatabaseManager")
    def test_initialization(self, MockDatabaseManager):
        """
        Test the initialization of DatabaseManagerCentral.
        """
        # Mocka DatabaseManager para evitar conexões reais
        MockDatabaseManager.return_value = MagicMock()

        # Inicializa a classe DatabaseManagerCentral com parâmetros reais
        manager = DatabaseManagerCentral(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # Verifica se as instâncias de Config foram configuradas corretamente
        self.assertEqual(manager.host, self.host)
        self.assertEqual(manager.user, self.user)
        self.assertEqual(manager.password, self.password)
        self.assertEqual(manager.database, self.database)

        # Verifica se DatabaseManager foi chamado com os argumentos esperados
        MockDatabaseManager.assert_any_call(
            self.products_config,
            None,  # products_config_pub não foi configurado no teste
            self.products_config_sub,
            immutable_columns=["timestamp"],
            foreign_keys={"vending_machine_id": "vending_machines_profile"}
        )

        #MockDatabaseManager.assert_any_call(
        #    Config(
        #        host=self.host,
        #        user=self.user,
        #        password=self.password,
        #        database=self.database,
        #        table_name="purchase_transaction",
        #        columns=["id", "user_id", "product_id", "vending_machine_id", "timestamp", "quantity", "amount_paid_per_unit"]
        #    ),
        #    self.purchase_transaction_config_pub,
        #    None,
        #    immutable_columns=None,
        #    foreign_keys={"user_id": "users_profile", "product_id": "products_profile", "vending_machine_id": "vending_machines_profile"}
        #)

        # Verifica se o EventManager foi configurado corretamente
        self.mock_event_manager.update_strategies.__setitem__.assert_called_with(
            "PurchaseProductEvent", MockDatabaseManager.return_value
        )
if __name__ == "__main__":
    unittest.main()