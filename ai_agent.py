import requests
import spacy
import re

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def get_invoice(invoice_id):
    url = f"http://127.0.0.1:5000/invoices/{invoice_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def list_invoices():
    url = "http://127.0.0.1:5000/invoices"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
def list_invoices_by_client(client_name):
    url = f"http://127.0.0.1:5000/invoices/client/{client_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def list_invoices_by_due_date(due_date):
    url = f"http://127.0.0.1:5000/invoices/due_date/{due_date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_invoice_by_number(invoice_number):
    url = f"http://127.0.0.1:5000/invoices/by_number/{invoice_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_query(query):
    query_lower = query.lower()
    doc = nlp(query_lower)
    invoice_num_str = None
    client_name = None

    # Look for a numeric token for invoice id/number
    for token in doc:
        if token.like_num:
            invoice_num_str = token.text
            break

    # Check if the query contains "for <client>" using regex
    client_match = re.search(r'for ([\w\s]+)', query_lower)
    if client_match:
        client_name = client_match.group(1).strip()

    # Check if the query contains a date in MM/DD/YYYY format
    date_matches = re.findall(r'\d{2}/\d{2}/\d{4}', query_lower)
    
    if "list" in query_lower and "invoice" in query_lower:
        # If a client name is specified, filter by client
        if client_name:
            return {"action": "list_by_client", "client_name": client_name}
        # If the query mentions "due" and we have a date, use that endpoint
        elif "due" in query_lower and date_matches:
            return {"action": "list_by_due_date", "due_date": date_matches[0]}
        else:
            return {"action": "list"}
    elif ("get" in query_lower or "show" in query_lower) and "invoice" in query_lower and invoice_num_str:
        # If the number has more than 3 digits, assume it's the invoice_number
        if len(invoice_num_str) > 3:
            return {"action": "get_by_number", "invoice_number": invoice_num_str}
        else:
            return {"action": "get", "invoice_id": int(invoice_num_str)}
    else:
        return {"action": "unknown"}

def main():
    print("Welcome to the Invoice AI Agent!")
    print("You can ask things like:")
    print("  - 'List invoices'")
    print("  - 'Get invoice 1'")
    print("  - 'Show me invoice 7003012'")
    print("  - 'List invoices for Meesan Clinic'")
    print("  - 'List invoices due on 02/19/2025'")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input(">> ").strip()
        if user_input.lower() == "exit":
            break
        
        result = process_query(user_input)
        
        if result["action"] == "list":
            invoices = list_invoices()
            if invoices:
                print("Invoice List:")
                for inv in invoices:
                    print(f"  ID: {inv['id']} - Invoice Number: {inv['invoice_number']} - Client: {inv['client']}")
            else:
                print("No invoices found.")
        elif result["action"] == "list_by_due_date":
            invoices = list_invoices_by_due_date(result["due_date"])
            if invoices:
                print(f"Invoices due on {result['due_date']}:")
                for inv in invoices:
                    print(f"  ID: {inv['id']} - Invoice Number: {inv['invoice_number']} - Client: {inv['client']}")
            else:
                print(f"No invoices found with due date {result['due_date']}.")
        elif result["action"] == "list_by_client":
            invoices = list_invoices_by_client(result["client_name"])
            if invoices:
                print(f"Invoices for {result['client_name']}:")
                for inv in invoices:
                    print(f"  ID: {inv['id']} - Invoice Number: {inv['invoice_number']} - Client: {inv['client']}")
            else:
                print(f"No invoices found for client {result['client_name']}.")
        elif result["action"] == "get":
            invoice_data = get_invoice(result["invoice_id"])
            if invoice_data:
                print("Invoice Data:")
                for key, value in invoice_data.items():
                    print(f"  {key}: {value}")
            else:
                print("Invoice not found!")
        elif result["action"] == "get_by_number":
            invoice_data = get_invoice_by_number(result["invoice_number"])
            if invoice_data:
                print("Invoice Data:")
                for key, value in invoice_data.items():
                    print(f"  {key}: {value}")
            else:
                print("Invoice not found!")
        else:
            print("I'm sorry, I didn't understand that command. Try a command like 'list invoices', 'get invoice <id>', 'list invoices for <client>', or 'list invoices due on <MM/DD/YYYY>'.")
            
if __name__ == "__main__":
    main()

