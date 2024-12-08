import mysql.connector
import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class VendingMachineReports:
    def __init__(self, host, user, password, database):
        self.__connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.__cursor = self.__connection.cursor()

    # def get_sales_report(self):
    #     """
    #     Gera o relatório de vendas, incluindo total de vendas e faturamento por produto e por máquina.
    #     """
    #     query = """
    #     SELECT
    #         p.Name AS product_name,
    #         vm.Name AS vm_name,
    #         SUM(v.Quantity) AS total_sales,
    #         SUM(v.Quantity * p.Price) AS total_revenue
    #     FROM
    #         Sales v
    #     JOIN Products p ON v.ProductID = p.ProductID
    #     JOIN VMs vm ON p.VMID = vm.VMID
    #     GROUP BY p.Name, vm.Name
    #     ORDER BY total_sales DESC
    #     """
    #     self.cursor.execute(query)
    #     sales_data = self.cursor.fetchall()

    #     return sales_data

    # def get_ratings_report(self):
    #     """
    #     Gera o relatório de avaliações, incluindo a média de avaliações por produto e o total de avaliações por produto.
    #     """
    #     query = """
    #     SELECT
    #         p.Name AS product_name,
    #         AVG(r.Rating) AS average_rating,
    #         COUNT(r.Rating) AS total_ratings
    #     FROM
    #         Ratings r
    #     JOIN Products p ON r.ProductID = p.ProductID
    #     GROUP BY p.Name
    #     ORDER BY average_rating DESC
    #     """
    #     self.cursor.execute(query)
    #     ratings_data = self.cursor.fetchall()

    #     return ratings_data

    def get_stock_report(self):
        """
        Gera o relatório de estoque, mostrando a quantidade de cada produto disponível nas vending machines.
        """
        query = """
        SELECT 
            p.Name AS product_name, 
            p.Quantity AS product_quantity,
            vm.Name AS vending_machine_name
        FROM 
            Products AS p
        JOIN 
            VMs AS vm ON p.VMID = vm.VMID
        """
        self.__cursor.execute(query)
        stock_data = self.__cursor.fetchall()

        return [
        {
            "product_name": row[0],
            "vending_machine_name": row[2],
            "product_quantity": row[1]
        }
        for row in stock_data
    ]

    def generate_stock_report_csv(self):
        """
        Gera o relatório de estoque em formato CSV.
        """
        query = """
        SELECT 
            p.Name AS product_name, 
            p.Quantity AS product_quantity,
            vm.Name AS vending_machine_name
        FROM 
            Products AS p
        JOIN 
            VMs AS vm ON p.VMID = vm.VMID
        """
        self.__cursor.execute(query)
        stock_data = self.__cursor.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Product Name", "Product Quantity", "Vending Machine Name"]) 
        for row in stock_data:
            writer.writerow(row)
        output.seek(0)  
        return output
    
    def generate_stock_report_pdf(self):
        """
        Gera o relatório de estoque em formato PDF.
        """
        query = """
        SELECT 
            p.Name AS product_name, 
            p.Quantity AS product_quantity,
            vm.Name AS vending_machine_name
        FROM 
            Products AS p
        JOIN 
            VMs AS vm ON p.VMID = vm.VMID
        """
        self.__cursor.execute(query)
        stock_data = self.__cursor.fetchall()
        
        output = io.BytesIO()
        pdf = canvas.Canvas(output, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        pdf.drawString(30, 750, "Stock Report")
        pdf.drawString(30, 735, "-----------------------------------------")

        y_position = 720
        for row in stock_data:
            product_name, product_quantity, vending_machine_name = row
            pdf.drawString(30, y_position, f"Product: {product_name}, Quantity: {product_quantity}, Machine: {vending_machine_name}")
            y_position -= 15
            if y_position < 50: 
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = 750

        pdf.save()
        output.seek(0)
        return output

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.__cursor.close()
        self.__connection.close()


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    stock_report = VendingMachineReports(**db_config)
    stock_data = stock_report.get_stock_report()
    for stock in stock_data:
        print(stock)

    stock_report.close()