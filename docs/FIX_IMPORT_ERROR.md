# Fix: ModuleNotFoundError: No module named 'langchain.text_splitters'

## Quick Fix

Run these commands in your activated virtual environment:

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate.bat  # Windows

# Install the missing package
pip install langchain-text-splitters==0.3.4

# Verify it worked
python check_imports.py
```

## What Happened?

The `langchain-text-splitters` package is a separate package from `langchain` (as of langchain v0.1+). It needs to be installed separately.

## Solution 1: Install Missing Package (Recommended)

```bash
pip install langchain-text-splitters==0.3.4
```

## Solution 2: Reinstall All Dependencies

```bash
pip install -r requirements.txt
```

## Solution 3: Use Fix Script

### Linux/Mac:
```bash
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

### Windows:
```bash
fix_dependencies.bat
```

## Verify Installation

Run the check script:

```bash
python check_imports.py
```

You should see:
```
✓ langchain
✓ langchain-text-splitters
✓ All packages are installed correctly!
```

## If Still Not Working

### Option 1: Check pip version
```bash
pip --version
# Should be pip 20.0 or higher
pip install --upgrade pip
```

### Option 2: Clear pip cache
```bash
pip cache purge
pip install --no-cache-dir langchain-text-splitters==0.3.4
```

### Option 3: Reinstall langchain ecosystem
```bash
pip uninstall langchain langchain-text-splitters -y
pip install langchain==0.3.14
pip install langchain-text-splitters==0.3.4
```

### Option 4: Check Python version
```bash
python --version
# Should be Python 3.8 or higher
```

## Code Fix Applied

I've also updated `backend/services/embeddings.py` to handle both import styles:

```python
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitters import RecursiveCharacterTextSplitter
```

This makes it compatible with different langchain versions.

## After Fixing

Once the package is installed, start your app:

```bash
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Still Having Issues?

1. Make sure virtual environment is activated
2. Check you're in the correct directory
3. Verify requirements.txt has the package listed
4. Try creating a fresh virtual environment:

```bash
# Deactivate current venv
deactivate

# Remove old venv
rm -rf venv

# Create new venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

## Prevention

To avoid this in the future, always run:

```bash
pip install -r requirements.txt
```

after pulling new code or when setting up the project.
