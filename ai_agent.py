import requests

def get_invoice(invoice_id):
    """
    Fetches invoice data from the API for a given invoice ID.
    """
    url = f"http://127.0.0.1:5000/invoices/{invoice_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    print("Welcome to the Invoice AI Agent!")
    print("Type commands like 'get invoice 1' or 'exit' to quit.")
    
    while True:
        user_input = input(">> ").strip().lower()
        if user_input == "exit":
            break
        elif user_input.startswith("get invoice"):
            parts = user_input.split()
            if len(parts) >= 3:
                try:
                    invoice_id = int(parts[2])
                    invoice_data = get_invoice(invoice_id)
                    if invoice_data:
                        print("Invoice Data:")
                        for key, value in invoice_data.items():
                            print(f"  {key}: {value}")
                    else:
                        print("Invoice not found!")
                except ValueError:
                    print("Invalid invoice ID. Please enter a number.")
            else:
                print("Usage: get invoice <id>")
        else:
            print("Unknown command. Try 'get invoice 1' or 'exit'.")

if __name__ == "__main__":
    main()
