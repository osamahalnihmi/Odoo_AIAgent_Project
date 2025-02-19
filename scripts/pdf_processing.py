import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2.
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    print(f"Warning: No text found on page {page_num}.")
        return text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    # Replace 'sample_invoice.pdf' with the path to your PDF invoice file
    sample_pdf = "sample_invoice.pdf"
    extracted_text = extract_text_from_pdf(sample_pdf)
    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("No text extracted.")
