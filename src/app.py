from flask import Flask, request, jsonify, render_template, send_file
from profiles.stock_profile import StockProfile
from profiles.vms_profile import VMProfile
from profiles.comment_profile import CommentProfile
from profiles.complaint_profile import Complaint
from profiles.report_profile import VendingMachineReports
from flask_cors import CORS
import io
import csv

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"
}

@app.route('/')
def index():
    """
    Render the home page with buttons to other pages.
    """
    return render_template('index.html')

@app.route('/stock')
def stock():
    """
    Render the stock page.
    """
    return render_template('stock.html')

@app.route('/get_stock_info', methods=['GET'])
def get_stock_info():
    """
    Endpoint for retrieving stock information about products and their associated vending machines.
    """
    stock_profile = StockProfile(**db_config)
    stock_info = stock_profile.get_stock_info()
    stock_profile.close()
    return jsonify(stock_info)

@app.route('/report')
def report():
    """
    Render the vending machines page.
    """
    return render_template('report.html')

@app.route('/get_stock_report', methods=['GET'])
def get_report():
    """
    Endpoint for retrieving a report about sales and ratings.
    """
    stock_report = VendingMachineReports(**db_config)
    report = stock_report.get_stock_report()
    stock_report.close()
    return jsonify(report)

@app.route('/download_stock_report_csv', methods=['GET'])
def download_stock_report_csv():
    """
    Endpoint para download do relatório de estoque em formato CSV.
    """
    stock_report = VendingMachineReports(**db_config)
    csv_file = stock_report.generate_stock_report_csv()
    stock_report.close()

    # Retornar o arquivo CSV
    return send_file(
        io.BytesIO(csv_file.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='stock_report.csv'
    )

@app.route('/download_stock_report_pdf', methods=['GET'])
def download_stock_report_pdf():
    """
    Endpoint para download do relatório de estoque em formato PDF.
    """
    stock_report = VendingMachineReports(**db_config)
    pdf_file = stock_report.generate_stock_report_pdf()
    stock_report.close()

    # Retornar o arquivo PDF
    return send_file(
        io.BytesIO(pdf_file.getvalue()),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='stock_report.pdf'
    )


@app.route('/vms')
def vms():
    """
    Render the vending machines page.
    """
    return render_template('vms.html')

@app.route('/get_vm_info', methods=['GET'])
def get_vm_info():
    """
    Endpoint for retrieving vending machine information.
    """
    vm_profile = VMProfile(**db_config)
    vm_info = vm_profile.get_vm_info()
    vm_profile.close()
    return jsonify(vm_info)

@app.route('/get_vm_products/<int:vm_id>', methods=['GET'])
def get_vm_products(vm_id):
    """
    Endpoint for retrieving vending machine products.
    """
    vm_profile = VMProfile(**db_config)
    vm_products = vm_profile.get_vm_products(vm_id)
    vm_profile.close()
    return jsonify(vm_products)

@app.route('/comment')
def comment():
    """
    Render the comment page.
    """
    return render_template('comment.html')

# Route to add a comment
@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    product_id = data['product_id']
    user_id = data['user_id']
    text = data['text']

    try:
        comment_profile = CommentProfile(**db_config)
        comment_id = comment_profile.create_comment(product_id, user_id, text)
        return jsonify({"success": True, "comment_id": comment_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})
    
# Route to get comments for a product
@app.route('/get_comments/<int:product_id>', methods=['GET'])
def get_comments(product_id):
    comment_profile = CommentProfile(**db_config)
    comments = comment_profile.get_comments_by_product(product_id)
    comment_profile.close()
    return jsonify(comments)

# Route to the complaints page for commun users
@app.route('/complaint')
def complaints():
    return render_template('complaints.html')

# Route to add a complaint
@app.route('/add_complaint', methods=['POST'])
def add_complaint():
    data = request.json
    vending_machine_id = data.get('vending_machine_id')  # Usa get para evitar KeyError
    user_id = data.get('user_id')  # Usa get para evitar KeyError
    text = data.get('text')  # Usa get para evitar KeyError

    try:
        complaint_manager = Complaint(**db_config)
        complaint_id = complaint_manager.create_complaint(user_id, vending_machine_id, text)  # Alterado a ordem dos parâmetros
        return jsonify({"success": True, "complaint_id": complaint_id})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})



# Route to the complaints page for admin users
@app.route('/admin_complaints')
def admin_complaints():
    return render_template('complaints_viewer_manager.html')


# Route to get complaints 
@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    try:
        complaint_manager = Complaint(**db_config)
        complaints = complaint_manager.get_all_complaints()
        return jsonify(complaints)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
