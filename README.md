# PDF Data Extraction Pipeline

This project is a Python pipeline for extracting specific structured data from PDF documents. The code converts PDF pages into images, performs OCR (Optical Character Recognition) on each image, and applies regex patterns to extract targeted information. This is particularly useful for extracting technical or structured data from scanned documents or PDF reports.

## Features

- Converts PDF pages into individual images.
- Uses OCR to extract text from images.
- Cleans and parses the text to extract specific fields using regular expressions.
- Returns structured data for each page, making it easy to use in downstream applications.

## Requirements

- Python 3.7+
- `opencv-python`
- `pdf2image`
- `pillow`
- `pyocr`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dineshram0212/pdf-ocr-extractor
   cd pdf-ocr-extractor
   ```
