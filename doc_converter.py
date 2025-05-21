#!/usr/bin/env python3
"""
Document Converter
-----------------
A simple utility to convert PDF and Word documents to text format.
"""

import os
import sys
import argparse
from pathlib import Path
import PyPDF2
from docx import Document
import subprocess
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_pdf_to_text(pdf_path, output_path):
    """Convert a PDF file to text format."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text)
            
            logger.info(f"Successfully converted {pdf_path} to {output_path}")
            return True
    except Exception as e:
        logger.error(f"Error converting PDF {pdf_path}: {str(e)}")
        return False

def convert_docx_to_text(docx_path, output_path):
    """Convert a DOCX file to text format."""
    try:
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)
        
        logger.info(f"Successfully converted {docx_path} to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error converting DOCX {docx_path}: {str(e)}")
        return False

def convert_doc_to_text(doc_path, output_path):
    """Convert a DOC file to text format using textutil (Mac) or alternative methods."""
    try:
        # Check if we're on macOS and can use textutil
        if sys.platform == 'darwin':
            temp_docx = f"{doc_path}.docx"
            subprocess.run(['textutil', '-convert', 'docx', '-output', temp_docx, doc_path], check=True)
            success = convert_docx_to_text(temp_docx, output_path)
            os.remove(temp_docx)  # Clean up temporary file
            return success
        else:
            logger.error("DOC conversion not implemented for this platform")
            return False
    except Exception as e:
        logger.error(f"Error converting DOC {doc_path}: {str(e)}")
        return False

def process_directory(directory_path):
    """Process all PDF and Word documents in the given directory."""
    directory = Path(directory_path)
    
    if not directory.exists():
        logger.error(f"Directory {directory_path} does not exist")
        return False
    
    # Create documents directory if it doesn't exist
    documents_dir = directory / 'documents'
    if not documents_dir.exists():
        logger.info(f"Creating documents directory at {documents_dir}")
        documents_dir.mkdir()
    
    # Count of processed files
    processed_count = 0
    
    # Process all files in the documents directory
    for file_path in documents_dir.glob('*'):
        if not file_path.is_file():
            continue
            
        output_path = file_path.with_suffix('.txt')
        
        # Skip if the file is already a text file
        if file_path.suffix.lower() == '.txt':
            continue
            
        # Process based on file extension
        if file_path.suffix.lower() == '.pdf':
            if convert_pdf_to_text(file_path, output_path):
                processed_count += 1
        elif file_path.suffix.lower() == '.docx':
            if convert_docx_to_text(file_path, output_path):
                processed_count += 1
        elif file_path.suffix.lower() == '.doc':
            if convert_doc_to_text(file_path, output_path):
                processed_count += 1
    
    logger.info(f"Processed {processed_count} documents")
    return True

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Convert PDF and Word documents to text format.')
    parser.add_argument('--dir', type=str, default=os.getcwd(),
                        help='Directory containing the documents folder (default: current directory)')
    
    args = parser.parse_args()
    process_directory(args.dir)

if __name__ == '__main__':
    main()
