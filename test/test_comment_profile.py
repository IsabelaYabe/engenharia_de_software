import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/comment_site'))
from comment_profile import CommentProfile
from utils import contains_banned_words

class TestCommentProfile(unittest.TestCase):

    def setUp(self):
        # Configuração inicial do teste: Mock da conexão com o banco de dados
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "Alacazumba123*",
            "database": "my_database"
        }
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        
        # Patching mysql.connector.connect para retornar o mock da conexão
        patcher = patch('mysql.connector.connect', return_value=self.mock_conn)
        self.addCleanup(patcher.stop)
        self.mock_connect = patcher.start()

        self.mock_conn.cursor.return_value = self.mock_cursor
        self.comment_profile = CommentProfile(**self.db_config)

    def test_create_comment_success(self):
        # Testa a criação de comentário com sucesso

        # Mock do retorno de _get_current_timestamp e lastrowid
        self.comment_profile._get_current_timestamp = MagicMock(return_value="2024-10-23 10:00:00")
        self.mock_cursor.lastrowid = 123
        
        # Executa a função que cria o comentário
        comment_id = self.comment_profile.create_comment(1, 1, "Great product!")

        # Verifica se o comentário foi criado corretamente
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO comments (product_id, user_id, text, timestamp) VALUES (%s, %s, %s, %s)",
            (1, 1, "Great product!", "2024-10-23 10:00:00")
        )
        self.mock_conn.commit.assert_called_once()
        self.assertEqual(comment_id, 123)

    def test_create_comment_empty_text(self):
        # Testa a criação de um comentário vazio (deve gerar um erro)

        with self.assertRaises(ValueError) as context:
            self.comment_profile.create_comment(1, 1, "")
        self.assertEqual(str(context.exception), "Comment cannot be empty.")

    @patch('utils.contains_banned_words', return_value=True)
    def test_create_comment_with_banned_words(self, mock_contains_banned_words):
        # Testa a criação de um comentário com palavras proibidas (deve gerar um erro)
        
        with self.assertRaises(ValueError) as context:
            self.comment_profile.create_comment(1, 1, "Bad comment")
        self.assertEqual(str(context.exception), "Comment contains banned words.")
        mock_contains_banned_words.assert_called_once_with("Bad comment")

    def test_get_comments_by_product(self):
        # Testa a obtenção de comentários por ID do produto
        self.mock_cursor.fetchall.return_value = [
            (1, "2024-10-23 10:00:00", 1, 1, "Great product!"),
            (2, "2024-10-23 11:00:00", 1, 2, "Nice product!")
        ]
        
        comments = self.comment_profile.get_comments_by_product(1)

        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM comments WHERE product_id = %s", (1,))
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0]['comment_id'], 1)
        self.assertEqual(comments[0]['text'], "Great product!")
        self.assertEqual(comments[1]['comment_id'], 2)
        self.assertEqual(comments[1]['text'], "Nice product!")

if __name__ == '__main__':
    unittest.main()
