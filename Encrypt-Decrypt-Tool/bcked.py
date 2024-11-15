from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from io import BytesIO
import PyPDF2
import re

app = Flask(__name__)
CORS(app)

# Increase the maximum content length to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB



# Caesar Cipher function
def caesar_cipher(text, shift, encrypt=True):
    result = []
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            offset = shift if encrypt else 26 - shift
            result.append(chr((ord(char) - ord(base) + offset) % 26 + ord(base)))
        else:
            result.append(char)  # Non-alphabetic characters are not changed
    return ''.join(result)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    # Use PyPDF2 to extract text from each page
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""  # Extract text from each page
    return text

# Function to create a new PDF with the modified text
def create_pdf_from_text(modified_text):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Break the text into lines to fit within PDF
    lines = modified_text.splitlines()
    for line in lines:
        pdf.write(10, line)
    
    # Create a BytesIO object to save the generated PDF in memory
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)  # Rewind to the beginning of the PDF
    return pdf_output

@app.route('/process', methods=['POST'])
def process_file():
    # Get file and data from frontend
    file = request.files['file']
    key = int(request.form['key'])
    mode = request.form['mode']

    # Ensure the file is a PDF
    if not file.filename.lower().endswith('.pdf'):
        return "Invalid file format. Only PDF files are allowed.", 400

    # Read the PDF file content
    try:
        content = extract_text_from_pdf(file)
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}", 400

    # Process the content (encrypt or decrypt)
    encrypt = mode == 'encrypt'
    processed_content = caesar_cipher(content, key, encrypt)

    # Create a new PDF with the processed content

    try:
        processed_pdf = create_pdf_from_text(processed_content)
    except Exception as e:
        return f"Error creating PDF: {str(e)}", 500

    # Return the processed PDF as a response
    return send_file(processed_pdf, as_attachment=True, download_name="output.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
