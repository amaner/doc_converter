# Document Converter

A simple Python utility that converts PDF and Word documents (doc and docx) to text (.txt) format.

## Features

- Automatically scans a directory named 'documents' for PDF and Word files
- Converts PDF files to text using PyPDF2
- Converts DOCX files to text using python-docx
- Converts DOC files to DOCX and then to text (Mac only, using textutil)
- Logs conversion progress and errors

## Requirements

- Python 3.6 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF and Word documents in a directory named 'documents' in the project folder
2. Run the script:

```bash
python doc_converter.py
```

The script will:
- Create a 'documents' directory if it doesn't exist
- Convert all PDF and Word files in the 'documents' directory to text format
- Save the text files in the same directory with the same filename but with a .txt extension

### Optional Arguments

- `--dir`: Specify a different base directory (the 'documents' folder should be inside this directory)

Example:
```bash
python doc_converter.py --dir /path/to/your/directory
```

## Notes

- For .doc files, conversion is only supported on macOS using the built-in textutil command
- The original files are preserved during conversion
