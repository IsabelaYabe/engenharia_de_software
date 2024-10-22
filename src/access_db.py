import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="nova_senha"
)

def get_connection():
    return mydb