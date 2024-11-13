from unittest.mock import patch, MagicMock
import mysql.connector

# Mocar o método mysql.connector.connect
with patch("mysql.connector.connect") as mock_connect:
    # Cria um objeto de conexão fictício
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn  # Faz o connect retornar o mock_conn

    # Exibe os métodos e atributos do objeto de conexão falso (mock)
    print(dir(mock_conn))

    # Agora, se você quiser verificar, por exemplo, os métodos de cursor:
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor  # Configura o retorno do cursor
    
    print(dir(mock_cursor))  # Exibe métodos e atributos do cursor simulado
