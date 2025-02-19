from scripts.invoice_processing import parse_invoice_data
from database_setup import Invoice, Session

def store_invoice_data(pdf_path):
    # Parse the invoice data from the PDF
    data = parse_invoice_data(pdf_path)
    if data:
        session = Session()
        # Create a new Invoice record. For 'products', we store the list as a string.
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
        print("Invoice stored successfully!")
    else:
        print("No data extracted from the invoice.")

if __name__ == "__main__":
    pdf_path = "sample_invoice.pdf"  # Ensure this file is in your project folder.
    store_invoice_data(pdf_path)
