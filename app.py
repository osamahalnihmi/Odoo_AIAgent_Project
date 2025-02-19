from flask import Flask, jsonify, request
from database_setup import Invoice, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Initialize Flask application
app = Flask(__name__)

# Configure the database session (using SQLite from our database_setup.py)
engine = create_engine('sqlite:///invoices.db')
Session = sessionmaker(bind=engine)

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

@app.route('/invoices/due_date/<due_date>', methods=['GET'])
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


# Optionally, you can add a POST endpoint to upload and store a new invoice.
# For now, we'll keep it simple.

if __name__ == "__main__":
    app.run(debug=True)
