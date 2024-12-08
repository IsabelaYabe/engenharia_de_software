import mysql.connector
import io
import csv

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

    # def generate_html_report(self, stock_data):
    #     """
    #     Gera o relatório completo em HTML.
    #     """
    #     html_content = """
    #     <html>
    #     <head><title>Relatório das Vending Machines</title></head>
    #     <body>
    #         <h1>Relatório de Vending Machines</h1>

    #         <h2>Relatório de Estoque</h2>
    #         <table border="1">
    #             <tr><th>Produto</th><th>Máquina</th><th>Estoque disponível</th></tr
    #     """
        # for row in sales_data:
        #     html_content += f"""
        #         <tr>
        #             <td>{row[0]}</td>
        #             <td>{row[1]}</td>
        #             <td>{row[2]}</td>
        #             <td>{row[3]}</td>
        #         </tr>
        #     """
        # html_content += "</table>"

        # html_content += """
        #     <h2>Relatório de Avaliações</h2>
        #     <table border="1">
        #         <tr><th>Produto</th><th>Média de Avaliação</th><th>Total de Avaliações</th></tr>
        # """
        # for row in ratings_data:
        #     html_content += f"""
        #         <tr>
        #             <td>{row[0]}</td>
        #             <td>{row[1]}</td>
        #             <td>{row[2]}</td>
        #         </tr>
        #     """
        # html_content += "</table>"

        # html_content += """
        #     <h2>Relatório de Estoque</h2>
        #     <table border="1">
        #         <tr><th>Produto</th><th>Máquina</th><th>Quantidade em Estoque</th></tr>
        # """
        # for row in stock_data:
        #     html_content += f"""
        #         <tr>
        #             <td>{row[0]}</td>
        #             <td>{row[1]}</td>
        #             <td>{row[2]}</td>
        #         </tr>
        #     """
        # html_content += "</table>"

        # html_content += "</body></html>"

        # # Salvar o relatório em um arquivo HTML
        # with open("relatorio_vending_machines.html", "w") as file:
        #     file.write(html_content)
        
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

        # Gerar CSV em memória
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Product Name", "Product Quantity", "Vending Machine Name"])  # Cabeçalhos do CSV
        for row in stock_data:
            writer.writerow(row)
        output.seek(0)  # Voltar ao início do arquivo para leitura
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