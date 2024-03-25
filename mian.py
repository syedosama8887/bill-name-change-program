import re
import PyPDF2
import fitz

def extract_data_from_pdf(pdf_path, replacement_name=None):
    extracted_data = {}
    original_name = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Assume that the relevant information is in the first page
        first_page = reader.pages[0]
        text = first_page.extract_text()
        # Convert the extracted text into a list
        lines = text.split('\n')
        # Remove lines containing specific patterns
        # Remove lines containing specific keys
        filtered_lines = [line for line in lines if not re.search(r'Amount:|Date:', line)]
        # Display the keys and values
        i = 0
        for line in filtered_lines:
            # Customize the extraction logic based on your PDF structure
            if i == 0:
                original_name = line.strip()  # Store the original name
                if replacement_name:
                    extracted_data['name'] = replacement_name
                else:
                    extracted_data['name'] = line.strip()
            elif i == 16:
                date_info = filtered_lines[i] + filtered_lines[i+1] + filtered_lines[i+2]
                # Find the second period (".") index
                second_period_index = date_info.find('.', date_info.find('.') + 1)
                extracted_date = date_info[second_period_index + 3:].strip()
                extracted_data['due date'] = extracted_date
            elif i == 23:
                first_space_index = filtered_lines[i].find(' ')
                second_space_index = filtered_lines[i].find(' ', first_space_index + 1)
                extracted_amount = filtered_lines[i][first_space_index:second_space_index].strip()
                extracted_data['bill amount'] = extracted_amount
            i += 1
        
        # Replace the original name in the PDF with the replacement name
        if replacement_name:
            replace_name_in_pdf(pdf_path, original_name, replacement_name)
    
    extracted_data['original name'] = original_name  # Add original name to the extracted data
    return extracted_data

def replace_name_in_pdf(pdf_path, original_name, replacement_name):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    for page in pdf_document:
        # Search for the original name and replace it with the replacement name
        text_instances = page.search_for(original_name)
        for inst in text_instances:
            page.insert_text((inst[0], inst[1]), replacement_name, fontsize=10)

    # Save the modified PDF file
    # pdf_document.save(pdf_path, incremental=True)
    pdf_document.close()

# Example usage
pdf_path = 'pdffiles/0400034237962_712014486568.pdf'
replacement_name = 'SYED OSAMA AHMED'
extracted_data = extract_data_from_pdf(pdf_path, replacement_name=replacement_name)
print("Original Name:", extracted_data['original name'])
print("Replaced Name:", extracted_data['name'])
print("Extracted Data:", extracted_data)
x