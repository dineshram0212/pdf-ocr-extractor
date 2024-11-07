import re
import sys
from PIL import Image
from pdf2image import convert_from_path
import pyocr
import pyocr.builders
import cv2

# Initialize OCR Tool
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
langs = tool.get_available_languages()
lang = langs[0]  # Selecting the first available language

# Function to convert PDF to images and save them
def pdf_to_images(pdf_path):
    """Converts PDF pages to images and returns a list of image filenames."""
    pages = convert_from_path(pdf_path)
    img_files = []
    for i, page in enumerate(pages):
        img_name = f"page_{i}.png"
        page.save(img_name, 'PNG')
        img_files.append(img_name)
    return img_files

# Function to perform OCR on an image and return extracted text
def extract_text_from_image(image_path):
    """Extracts text from an image using OCR."""
    image = Image.open(image_path)
    text = tool.image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    return text.strip().replace("|", "")

# Function to clean and extract specific data from text using regex
def extract_data_from_text(text, patterns):
    """Extracts data from text using specified regex patterns."""
    values = {}
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            values.update(match.groupdict())
    return values

# Main pipeline function to process PDF, extract text, and find specific data
def process_pdf(pdf_path, patterns):
    """Processes a PDF to extract and clean data based on regex patterns."""
    images = pdf_to_images(pdf_path)  # Step 1: Convert PDF to images
    extracted_data = []

    for img in images:
        text = extract_text_from_image(img)  # Step 2: Extract text from image
        data = extract_data_from_text(text, patterns)  # Step 3: Extract data using regex
        extracted_data.append(data)

    return extracted_data

# Define regex patterns for specific fields to extract
patterns = [
    r'(?P<cert_no>TC No :\s+(\w+))',
    r'(?P<Heat_no>Heat No:\s+(\w+))',
    r'(?P<Material_spec>Grade :\s+\w+\s+\w+\s+\w+\s+\w+-\w+\s+&\s+(\w+-\w+-\w+\s+\w+\s+\w+))',
    r'(?P<heat_treatment>HEAT TREATMENT:\s+(\w+\s-\s\w+\s\w+\s\w+\s\w+\s\w+\(\w+\s\w+\s\w\)\s\w+\s\w+\s\w+.\w+\s\w+\s\w+\s\w+\s\w+\s\w+.))'
]

# Example usage
if __name__ == '__main__':
    pdf_path = 'Sanmar.pdf'  # Path to the PDF file
    extracted_info = process_pdf(pdf_path, patterns)
    
    for i, data in enumerate(extracted_info):
        print(f"Data from page {i+1}:")
        print(data)
