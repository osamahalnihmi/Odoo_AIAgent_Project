import requests
import spacy

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

def get_invoice_by_number(invoice_number):
    url = f"http://127.0.0.1:5000/invoices/by_number/{invoice_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_query(query):
    query_lower = query.lower()  # convert once
    doc = nlp(query_lower)
    invoice_num_str = None
    # Look for a numeric token
    for token in doc:
        if token.like_num:
            invoice_num_str = token.text
            break

    if "list" in query_lower and "invoice" in query_lower:
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
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input(">> ").strip()
        if user_input.lower() == "exit":
            break
        
        # Process the query using NLP
        result = process_query(user_input)
        
        if result["action"] == "list":
            invoices = list_invoices()
            if invoices:
                print("Invoice List:")
                for inv in invoices:
                    print(f"  ID: {inv['id']} - Invoice Number: {inv['invoice_number']} - Client: {inv['client']}")
            else:
                print("No invoices found.")
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
            print("I'm sorry, I didn't understand that command. Try 'list invoices' or 'get invoice <id>'.")
            
if __name__ == "__main__":
    main()

