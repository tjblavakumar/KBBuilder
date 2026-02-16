#!/usr/bin/env python3
"""
Check if all required imports are available
"""
import sys

def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name} - NOT INSTALLED")
        print(f"  Error: {e}")
        return False

def main():
    print("=" * 50)
    print("Checking Required Packages")
    print("=" * 50)
    print()
    
    checks = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('sqlalchemy', 'sqlalchemy'),
        ('bs4', 'beautifulsoup4'),
        ('requests', 'requests'),
        ('boto3', 'boto3'),
        ('pydantic', 'pydantic'),
        ('pymupdf', 'pymupdf'),
        ('faiss', 'faiss-cpu'),
        ('langchain', 'langchain'),
        ('tiktoken', 'tiktoken'),
        ('schedule', 'schedule'),
        ('openai', 'openai'),
    ]
    
    results = []
    for module, package in checks:
        results.append(check_import(module, package))
    
    print()
    print("=" * 50)
    print("Checking langchain-text-splitters specifically")
    print("=" * 50)
    print()
    
    # Try both import methods
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        print("✓ langchain_text_splitters (new style import)")
        langchain_ok = True
    except ImportError:
        print("✗ langchain_text_splitters (new style import) - FAILED")
        try:
            from langchain.text_splitters import RecursiveCharacterTextSplitter
            print("✓ langchain.text_splitters (old style import)")
            langchain_ok = True
        except ImportError as e:
            print("✗ langchain.text_splitters (old style import) - FAILED")
            print(f"  Error: {e}")
            langchain_ok = False
    
    results.append(langchain_ok)
    
    print()
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    
    if all(results):
        print("✓ All packages are installed correctly!")
        print()
        print("You can now run: python app.py")
        return 0
    else:
        print("✗ Some packages are missing")
        print()
        print("To fix, run:")
        print("  pip install -r requirements.txt")
        print()
        print("Or specifically for langchain-text-splitters:")
        print("  pip install langchain-text-splitters==0.3.4")
        return 1

if __name__ == "__main__":
    sys.exit(main())
