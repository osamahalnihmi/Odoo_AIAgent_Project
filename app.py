from flask import Flask, jsonify, request
from database_setup import Invoice, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


# Initialize Flask application
app = Flask(__name__)

# Configure the database session (using SQLite from our database_setup.py)
engine = create_engine('sqlite:///invoices.db')
Session = sessionmaker(bind=engine)


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_invoice', methods=['POST'])
def upload_invoice():
    """
    Endpoint to upload a new invoice PDF.
    The file is saved, processed, and the parsed data is stored in the database.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Process the file using your existing invoice processing script
    from scripts.invoice_processing import parse_invoice_data
    from database_setup import Invoice, Session

    data = parse_invoice_data(file_path)
    if not data:
        return jsonify({"error": "Failed to extract invoice data from file"}), 500

    session = Session()
    invoice = Invoice(
        invoice_type = data.get("invoice_type"),
        client = data.get("client"),
        invoice_number = data.get("invoice_number"),
        invoice_date = data.get("invoice_date"),
        due_date = data.get("due_date"),
        total_amount = data.get("total_amount"),
        vat_number = data.get("vat_number"),
        products = str(data.get("products"))
    )
    session.add(invoice)
    session.commit()
    session.close()

    return jsonify({"message": "Invoice uploaded and stored successfully!", "invoice_id": invoice.id}), 201

@app.route('/invoices', methods=['GET'])
def get_invoices():
    """
    Retrieve a list of all stored invoices.
    """
    session = Session()
    invoices = session.query(Invoice).all()
    session.close()
    invoice_list = []
    for inv in invoices:
        invoice_list.append({
            "id": inv.id,
            "invoice_type": inv.invoice_type,
            "client": inv.client,
            "invoice_number": inv.invoice_number,
            "invoice_date": inv.invoice_date,
            "due_date": inv.due_date,
            "total_amount": inv.total_amount,
            "vat_number": inv.vat_number,
            "products": inv.products
        })
    return jsonify(invoice_list)

@app.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """
    Retrieve details of a specific invoice.
    """
    session = Session()
    invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
    session.close()
    if invoice:
        invoice_data = {
            "id": invoice.id,
            "invoice_type": invoice.invoice_type,
            "client": invoice.client,
            "invoice_number": invoice.invoice_number,
            "invoice_date": invoice.invoice_date,
            "due_date": invoice.due_date,
            "total_amount": invoice.total_amount,
            "vat_number": invoice.vat_number,
            "products": invoice.products
        }
        return jsonify(invoice_data)
    else:
        return jsonify({"error": "Invoice not found"}), 404

@app.route('/invoices/by_number/<invoice_number>', methods=['GET'])
def get_invoice_by_number(invoice_number):
    session = Session()
    invoice = session.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()
    session.close()
    if invoice:
        invoice_data = {
            "id": invoice.id,
            "invoice_type": invoice.invoice_type,
            "client": invoice.client,
            "invoice_number": invoice.invoice_number,
            "invoice_date": invoice.invoice_date,
            "due_date": invoice.due_date,
            "total_amount": invoice.total_amount,
            "vat_number": invoice.vat_number,
            "products": invoice.products
        }
        return jsonify(invoice_data)
    else:
        return jsonify({"error": "Invoice not found"}), 404

@app.route('/invoices/due_date/<path:due_date>', methods=['GET'])
def get_invoices_by_due_date(due_date):
    """
    Retrieve all invoices with a specific due date.
    """
    session = Session()
    invoices = session.query(Invoice).filter(Invoice.due_date == due_date).all()
    session.close()
    
    if invoices:
        invoice_list = []
        for inv in invoices:
            invoice_list.append({
                "id": inv.id,
                "invoice_type": inv.invoice_type,
                "client": inv.client,
                "invoice_number": inv.invoice_number,
                "invoice_date": inv.invoice_date,
                "due_date": inv.due_date,
                "total_amount": inv.total_amount,
                "vat_number": inv.vat_number,
                "products": inv.products
            })
        return jsonify(invoice_list)
    else:
        return jsonify({"error": "No invoices found for due date " + due_date}), 404

@app.route('/invoices/client/<client_name>', methods=['GET'])
def get_invoices_by_client(client_name):
    """
    Retrieve all invoices for a given client (case-insensitive search).
    """
    session = Session()
    invoices = session.query(Invoice).filter(Invoice.client.ilike(f"%{client_name}%")).all()
    session.close()
    
    if invoices:
        invoice_list = []
        for inv in invoices:
            invoice_list.append({
                "id": inv.id,
                "invoice_type": inv.invoice_type,
                "client": inv.client,
                "invoice_number": inv.invoice_number,
                "invoice_date": inv.invoice_date,
                "due_date": inv.due_date,
                "total_amount": inv.total_amount,
                "vat_number": inv.vat_number,
                "products": inv.products
            })
        return jsonify(invoice_list)
    else:
        return jsonify({"error": "No invoices found for client " + client_name}), 404



# Optionally, you can add a POST endpoint to upload and store a new invoice.
# For now, we'll keep it simple.

if __name__ == "__main__":
    app.run(debug=True)
