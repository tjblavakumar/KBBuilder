import os
import requests
import fitz  # PyMuPDF
from typing import List, Dict
from pathlib import Path

class PDFProcessor:
    def __init__(self, kb_id: int, base_path: str = "../data"):
        self.kb_id = kb_id
        self.kb_path = Path(base_path) / f"kb_{kb_id}"
        self.pdf_path = self.kb_path / "pdfs"
        self.pdf_path.mkdir(parents=True, exist_ok=True)
    
    def download_pdf(self, url: str, filename: str) -> str:
        """Download PDF from URL and save to kb folder"""
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            file_path = self.pdf_path / filename
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(file_path)
        except Exception as e:
            raise Exception(f"Failed to download {filename}: {str(e)}")
    
    def extract_text_from_pdf(self, file_path: str) -> List[Dict[str, any]]:
        """Extract text from PDF with page numbers using PyMuPDF"""
        try:
            doc = fitz.open(file_path)
            pages_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                if text.strip():  # Only include pages with text
                    pages_data.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'filename': Path(file_path).name
                    })
            
            doc.close()
            return pages_data
        except Exception as e:
            raise Exception(f"Failed to extract text from {file_path}: {str(e)}")
    
    def get_page_count(self, file_path: str) -> int:
        """Get total page count from PDF"""
        try:
            doc = fitz.open(file_path)
            count = len(doc)
            doc.close()
            return count
        except Exception as e:
            return 0
