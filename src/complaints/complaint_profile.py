'''
    This module contains the Complaint class, which is responsible for managing complaints in the database.

    Author: Lavinia Dias

    Requires:
    - mysql.connector

'''
import mysql.connector
import os
import sys
from datetime import datetime
from utils import contains_banned_words
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database_manager import DatabaseManager


class Complaint:
    def __init__(self, host, user, password, database):
        self.__connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.__cursor = self.__connection.cursor()

    def __create_table(self):
        """
        Creates the complaints table in the MySQL database if it does not already exist.
        The table stores complaints with a vending machine ID and the complaint text.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Complaints (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            vending_machine_id INT ,
            user_id CHAR(36),
            text TEXT NOT NULL,
            FOREIGN KEY (vending_machine_id) REFERENCES VendingMachines(id)
        )
        """
        self.create_table(create_table_sql)

    def create_complaint(self,vending_machine_id,user_id, text):
        """
        Creates a new complaint in the database.

        Parameters:
            vending_machine_id (int): The ID of the vending machine the complaint is about.
            text (str): The text of the complaint.

        Returns:
            complaint_id (int): The ID of the newly created complaint.
        """
        # If the complaint is empty, raise an error
        if not text or text.strip() == "":
            raise ValueError("Complaint cannot be empty.")
        # If the complaint contains banned words, raise an error
        if contains_banned_words(text):
            raise ValueError("Complaint contains banned words.")

        query = """
        INSERT INTO Complaints (timestamp, vending_machine_id, text, user_id)
        VALUES (%s, %s, %s, %s)
        """
        self.__cursor.execute(query, (self._get_current_timestamp(), vending_machine_id, text, user_id))
        self.__connection.commit()
        return self.__cursor.lastrowid
    


    def get_complaints_by_vending_machine(self, vending_machine_id):
        """
        Retrieves all complaints associated with a vending machine from the database.

        Parameters:
            vending_machine_id (int): The ID of the vending machine to retrieve complaints for.

        Returns:
            complaints (list): A list of dictionaries containing the details of the complaints.
        """
        query = "SELECT * FROM Complaints WHERE vending_machine_id = %s"
        self.__cursor.execute(query, (vending_machine_id,))
        complaints = self.__cursor.fetchall()
        
        return [
            {
                'complaint_id': complaint[0],
                'vending_machine_id': complaint[2],  
                'user_id': complaint[4],  
                'text': complaint[3],                
                'timestamp': complaint[1].strftime('%Y-%m-%d %H:%M:%S') if isinstance(complaint[1], datetime) else complaint[1]  
            }
            for complaint in complaints
        ]

    def get_complaint(self, complaint_id):
        """
        Retrieves a complaint from the database by its ID.

        Parameters:
            complaint_id (int): The ID of the complaint to retrieve.

        Returns:
            complaint (dict): A dictionary containing the details of the complaint.
        """
        query = "SELECT * FROM Complaints WHERE id = %s"
        self.__cursor.execute(query, (complaint_id,))
        complaint = self.__cursor.fetchone()
        if complaint:
            return {
                'complaint_id': complaint[0],
                'vending_machine_id': complaint[2], 
                'user_id': complaint[4],  
                'text': complaint[3],                
                'timestamp': complaint[1].strftime('%Y-%m-%d %H:%M:%S') if isinstance(complaint[1], datetime) else complaint[1] 
            }
        else:
            return None
        
    def get_all_complaints(self):
        """
        Retrieves all complaints from the database, along with user information.

        Returns:
            complaints (list): A list of dictionaries containing the details of all complaints.
        """
        query = """
        SELECT c.id, c.timestamp, c.vending_machine_id, c.text, u.id AS user_id, u.name AS user_name
        FROM Complaints c
        JOIN Users u ON c.user_id = u.id
        """
        self.__cursor.execute(query)
        complaints = self.__cursor.fetchall()

        return [
            {
                'complaint_id': complaint[0],
                'timestamp': complaint[1].strftime('%Y-%m-%d %H:%M:%S') if isinstance(complaint[1], datetime) else complaint[1],
                'vending_machine_id': complaint[2],
                'user_id': complaint[4],
                'text': complaint[3],
                'user_name': complaint[5]
            }
            for complaint in complaints
        ]

    def delete_complaint(self, complaint_id):
        """
        Deletes a complaint from the database by its ID.

        Parameters:
            complaint_id (int): The ID of the complaint to delete.
        """
        query = "DELETE FROM Complaints WHERE id = %s"
        self.__cursor.execute(query, (complaint_id,))
        self.__connection.commit()

    def _get_current_timestamp(self):
        """
        Gets the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
        
        Returns:
            str: The current timestamp.
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    complaint_manager = Complaint(**db_config)
    print("Complaint class created successfully.")

    # Inserting complaints
    complaint_id = complaint_manager.create_complaint(1, 1, 'Bad product!')

    # Retrieving complaints by vending machine
    complaints = complaint_manager.get_complaints_by_vending_machine(1)
    print("Complaints for vending_machine_id 1:", complaints)