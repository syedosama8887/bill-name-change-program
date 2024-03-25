import re
import PyPDF2

class PDFManipulator:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_data(self):
        extracted_data = {}
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            first_page_text = reader.pages[0].extract_text()
        
        lines = first_page_text.split('\n')
        filtered_lines = [line for line in lines if not re.search(r'Amount:|Date:', line)]

        for i, line in enumerate(filtered_lines):
            if i == 0:
                extracted_data['original name'] = line.strip()
            elif i == 16:
                date_info = filtered_lines[i] + filtered_lines[i+1] + filtered_lines[i+2]
                second_period_index = date_info.find('.', date_info.find('.') + 1)
                extracted_date = date_info[second_period_index + 3:].strip()
                extracted_data['due date'] = extracted_date
            elif i == 23:
                first_space_index = filtered_lines[i].find(' ')
                second_space_index = filtered_lines[i].find(' ', first_space_index + 1)
                extracted_amount = filtered_lines[i][first_space_index:second_space_index].strip()
                extracted_data['bill amount'] = extracted_amount

        return extracted_data

    def replace_name(self, replacement_name):
        original_name = self.extract_data()['original name']
        new_pdf_path = self.pdf_path.replace('.pdf', '_modified.pdf')
        
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                text = page.extract_text()
                text = text.replace(original_name, replacement_name)
                writer.add_page(page)

            with open(new_pdf_path, 'wb') as output_file:
                writer.write(output_file)

        return new_pdf_path

def generate_pdf_from_template(template_path, data, output_path):
    # Code for generating PDF from template goes here
    pass  # Placeholder for actual implementation

# Example usage
pdf_path = 'pdffiles/0400034237962_712014486568.pdf'
replacement_name = 'SYED OSAMA AHMED'

pdf_manipulator = PDFManipulator(pdf_path)
modified_pdf_path = pdf_manipulator.replace_name(replacement_name)

# Generate new PDF from template
template_path = 'template.pdf'  # Replace with the path to your template PDF file
data = pdf_manipulator.extract_data()
generate_pdf_from_template(template_path, data, 'output.pdf')
