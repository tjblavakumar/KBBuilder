#!/bin/bash

echo "========================================="
echo "Fixing Dependencies"
echo "========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

echo "✓ Virtual environment detected: $VIRTUAL_ENV"
echo ""

echo "Installing/Upgrading packages..."
echo ""

# Install langchain packages
pip install --upgrade langchain==0.3.14
pip install --upgrade langchain-text-splitters==0.3.4

# Install OpenAI
pip install --upgrade openai==1.54.0

# Install other dependencies
pip install --upgrade tiktoken==0.8.0
pip install --upgrade faiss-cpu==1.9.0.post1

echo ""
echo "========================================="
echo "Verifying installations..."
echo "========================================="
echo ""

python3 << 'EOF'
import sys

packages = [
    ('langchain', 'langchain'),
    ('langchain_text_splitters', 'langchain-text-splitters'),
    ('openai', 'openai'),
    ('tiktoken', 'tiktoken'),
    ('faiss', 'faiss-cpu'),
]

all_ok = True
for module, package in packages:
    try:
        __import__(module)
        print(f"✓ {package}")
    except ImportError:
        print(f"✗ {package} - NOT INSTALLED")
        all_ok = False

if all_ok:
    print("\n✓ All packages installed successfully!")
    sys.exit(0)
else:
    print("\n✗ Some packages failed to install")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✓ Setup Complete!"
    echo "========================================="
    echo ""
    echo "You can now run: python app.py"
else
    echo ""
    echo "========================================="
    echo "✗ Setup Failed"
    echo "========================================="
    echo ""
    echo "Try running: pip install -r requirements.txt"
fi
