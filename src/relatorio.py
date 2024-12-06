import mysql.connector

class VendingMachineReports:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()

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
            vm.Name AS vm_name,
            p.Quantity AS stock_quantity
        FROM
            Products p
        JOIN VMs vm ON p.VMID = vm.VMID
        """
        self.cursor.execute(query)
        stock_data = self.cursor.fetchall()

        return stock_data

    def generate_html_report(self, stock_data):
        """
        Gera o relatório completo em HTML.
        """
        html_content = """
        <html>
        <head><title>Relatório das Vending Machines</title></head>
        <body>
            <h1>Relatório de Vending Machines</h1>

            <h2>Relatório de Estoque</h2>
            <table border="1">
                <tr><th>Produto</th><th>Máquina</th><th>Estoque disponível</th></tr
        """
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
        for row in stock_data:
            html_content += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                </tr>
            """
        html_content += "</table>"

        html_content += "</body></html>"

        # Salvar o relatório em um arquivo HTML
        with open("relatorio_vending_machines.html", "w") as file:
            file.write(html_content)

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.cursor.close()
        self.connection.close()


# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}

# Gerar os relatórios
report = VendingMachineReports(db_config)
#sales_data = report.get_sales_report()
#ratings_data = report.get_ratings_report()
stock_data = report.get_stock_report()

# Gerar e salvar o relatório em HTML
report.generate_html_report(stock_data)

# Fechar a conexão com o banco de dados
report.close()

print("Relatório gerado com sucesso: relatorio_vending_machines.html")
