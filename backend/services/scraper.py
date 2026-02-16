import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List
from models import PDFInfo

def format_size(bytes_size: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def get_pdf_size(url: str) -> str:
    """Get PDF file size using HEAD request"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        if 'content-length' in response.headers:
            size_bytes = int(response.headers['content-length'])
            return format_size(size_bytes)
        return "Unknown"
    except Exception as e:
        return "Unknown"

def scan_url_for_pdfs(url: str) -> List[PDFInfo]:
    """Scan a webpage and extract all PDF download links"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_links = []
        seen_urls = set()
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Check if it's a PDF link
            if href.lower().endswith('.pdf'):
                full_url = urljoin(url, href)
                
                # Avoid duplicates
                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)
                
                # Extract filename
                filename = full_url.split('/')[-1]
                
                # Get file size
                size = get_pdf_size(full_url)
                
                pdf_links.append(PDFInfo(
                    filename=filename,
                    url=full_url,
                    size=size
                ))
        
        return pdf_links
    
    except requests.RequestException as e:
        raise Exception(f"Failed to scan URL: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing webpage: {str(e)}")
