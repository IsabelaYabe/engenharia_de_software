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
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import contains_banned_words
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
        CREATE TABLE IF NOT EXISTS Complaints
            (
            ComplaintID INT AUTO_INCREMENT,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            VMID INT,
            UserID INT,
            Text VARCHAR(250) NOT NULL,
            PRIMARY KEY (ComplaintID),
            FOREIGN KEY (VMID) REFERENCES VMs(VMID),
            FOREIGN KEY (UserID) REFERENCES User(UserID)
            );
        """
        self.create_table(create_table_sql)

    def create_complaint(self, user_id, vending_machine_id, text):
        """
        Creates a new complaint in the database.

        Parameters:
            user_id (int): The ID of the user creating the complaint.
            vending_machine_id (int or None): The ID of the vending machine the complaint is about, or None if not applicable.
            text (str): The text of the complaint.

        Returns:
            complaint_id (int): The ID of the newly created complaint.
        """
        # Validate input text
        if not text or text.strip() == "":
            raise ValueError("Complaint cannot be empty.")
        if contains_banned_words(text):
            raise ValueError("Complaint contains banned words.")
        
        # SQL query to insert a complaint
        query = """
        INSERT INTO Complaints (Timestamp, VMID, UserID, Text)
        VALUES (CURRENT_TIMESTAMP, %s, %s, %s)
        """
        
        # Execute the insertion, using `None` if `vending_machine_id` is not provided
        self.__cursor.execute(query, (vending_machine_id, user_id, text))
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
        query = "SELECT * FROM Complaints WHERE VMID = %s"
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
        query = "SELECT * FROM Complaints WHERE ComplaintID = %s"
        self.__cursor.execute(query, (complaint_id,))
        complaint = self.__cursor.fetchone()
        if complaint:
            return {
                'complaint_id': complaint[0],
                'vending_machine_id': complaint[2], 
                'user_id': complaint[3],  # Atualizado para usar a coluna UserID
                'text': complaint[4],                
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
        SELECT c.ComplaintID, c.Timestamp, c.VMID, vm.Name, c.Text, c.UserID
        FROM Complaints c
        LEFT JOIN VMs vm ON c.VMID = vm.VMID;
        """
        self.__cursor.execute(query)
        complaints = self.__cursor.fetchall()

        return [
            {
                'complaint_id': complaint[0],
                'timestamp': complaint[1].strftime('%Y-%m-%d %H:%M:%S') if isinstance(complaint[1], datetime) else complaint[1],
                'vending_machine_id': complaint[2],
                'vm_name': complaint[3],
                'text': complaint[4],
                'user_id': complaint[5]  # Incluindo UserID na saída
            }
            for complaint in complaints
        ]

    def delete_complaint(self, complaint_id):
        """
        Deletes a complaint from the database by its ID.

        Parameters:
            complaint_id (int): The ID of the complaint to delete.
        """
        query = "DELETE FROM Complaints WHERE ComplaintID = %s"
        self.__cursor.execute(query, (complaint_id))
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
    print("Inserting complaints...")
    complaint_manager.create_complaint(1, 1, "The vending machine is not working.")
    complaint_manager.create_complaint(2, 2, "The vending machine is out of stock.")
    complaint_manager.create_complaint(3, 3, "The vending machine is too loud.")
    print(complaint_manager.get_all_complaints())
    print("Complaints inserted successfully.")
    
