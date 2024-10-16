import uuid
import mysql.connector
import os
import sys
from utils import contains_banned_words
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database_manager import DatabaseManager
    

class ComplaintProfile:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def __create_table(self):
        """
        Creates the complaints table in the MySQL database if it does not already exist.
        The table stores complaints along with the vending_machine_id they are associated with.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Complaints (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            vending_machine_id INT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (vending_machine_id) REFERENCES VendingMachines(id)
        )
        """
        self.create_table(create_table_sql)

    def create_complaint(self, vending_machine_id, text):
        """
        Creates a new complaint in the database.

        Parameters:
            vending_machine_id (int): The ID of the vending machine the complaint is associated with.
            text (str): The text of the complaint.

        Returns:
            complaint_id (str): The ID of the newly created complaint.
        """
        # if the complaint is empty, raise an error
        if not text:
            raise ValueError("Complaint cannot be empty.")
        # if the complaint contains banned words, raise an error
        if contains_banned_words(text):
            raise ValueError("Complaint contains banned words.")

        query = "INSERT INTO complaints (vending_machine_id, text, timestamp) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (vending_machine_id, text, self._get_current_timestamp()))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_complaints_by_machine(self, vending_machine_id):
        """
        Retrieves all complaints associated with a vending machine from the database.

        Parameters:
            vending_machine_id (int): The ID of the vending machine to retrieve complaints for.

        Returns:
            complaints (list): A list of dictionaries containing the details of the complaints.
        """
        query = "SELECT * FROM complaints WHERE vending_machine_id = %s"
        self.cursor.execute(query, (vending_machine_id,))
        complaints = self.cursor.fetchall()
        
        return [
            {
                'complaint_id': complaint[0],
                'vending_machine_id': complaint[1],
                'text': complaint[2],
                'timestamp': complaint[3] if isinstance(complaint[3], str) else complaint[3].strftime('%Y-%m-%d %H:%M:%S')
            }
            for complaint in complaints
        ]

    def get_complaint(self, complaint_id):
        """
        Retrieves a complaint from the database by its ID.

        Parameters:
            complaint_id (str): The ID of the complaint to retrieve.

        Returns:
            complaint (dict): A dictionary containing the details of the complaint.
        """
        query = "SELECT * FROM complaints WHERE id = %s"
        self.cursor.execute(query, (complaint_id,))
        complaint = self.cursor.fetchone()
        if complaint:
            return {
                'complaint_id': complaint[0],
                'vending_machine_id': complaint[1],
                'text': complaint[2],
                'timestamp': complaint[3]
            }
        else:
            return None
        
    def delete_complaint(self, complaint_id):
        """
        Deletes a complaint from the database by its ID.

        Parameters:
            complaint_id (str): The ID of the complaint to delete.
        """
        query = "DELETE FROM complaints WHERE id = %s"
        self.cursor.execute(query, (complaint_id,))
        self.connection.commit()

    
    def _get_current_timestamp(self):
        """
        Gets the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
        
        Returns:
            str: The current timestamp.
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    complaint_profile = ComplaintProfile(**db_config)
    print("ComplaintProfile class created successfully.")

    # Inserting a complaint
    vending_machine_id = 1
    text = "TEST COMPLAINT"
    complaint_id = complaint_profile.create_complaint(vending_machine_id, text)
    print(f"Complaint created with ID: {complaint_id}")

    # Retrieving complaints by machine
    complaints = complaint_profile.get_complaints_by_machine(vending_machine_id)
    print("Complaints for vending_machine_id 1:")
