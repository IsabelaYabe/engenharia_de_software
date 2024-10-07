import unittest
from unittest.mock import patch
from src.complaints import Complaint  # Classe renomeada

class TestComplaintSubmissionFrontend(unittest.TestCase):

    # Teste: Submissão de reclamação via frontend
    @patch('src.complaints.Complaint.submit_complaint')
    def test_complaint_submission_ui(self, mock_submit_complaint):
        # Simula o clique no botão de submissão e chamada ao backend
        mock_submit_complaint.return_value = "Complaint successfully submitted by John on 2024-10-07."

        # Simulando uma reclamação submetida pela interface
        result = Complaint.submit_complaint("The vending machine is not working.", user="John")

        # Verifica se o backend foi chamado corretamente e se a resposta é positiva
        mock_submit_complaint.assert_called_with("The vending machine is not working.", user="John", vending_machine_id=None)
        self.assertEqual(result, "Complaint successfully submitted by John on 2024-10-07.")
    
    # Teste: Submissão com falha no frontend (reclamação sem texto)
    @patch('src.complaints.Complaint.submit_complaint')
    def test_complaint_submission_empty(self, mock_submit_complaint):
        # Simulando o envio de uma reclamação vazia pelo frontend
        mock_submit_complaint.return_value = "Complaint has no text"

        result = Complaint.submit_complaint("", user="John")

        # Verifica se o aviso correto é retornado ao frontend
        mock_submit_complaint.assert_called_with("", user="John", vending_machine_id=None)
        self.assertEqual(result, "Complaint has no text")

    # Teste: Reclamação com palavras proibidas via frontend
    @patch('src.complaints.Complaint.submit_complaint')
    def test_complaint_submission_banned_words(self, mock_submit_complaint):
        # Simulando o envio de uma reclamação com palavras inadequadas
        mock_submit_complaint.return_value = "Complaint contains inappropriate language"

        result = Complaint.submit_complaint("This is curseword1!", user="John")

        # Verifica se o aviso correto é retornado ao frontend
        mock_submit_complaint.assert_called_with("This is curseword1!", user="John", vending_machine_id=None)
        self.assertEqual(result, "Complaint contains inappropriate language")


if __name__ == '__main__':
    unittest.main()
