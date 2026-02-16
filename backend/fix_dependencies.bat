@echo off
echo =========================================
echo Fixing Dependencies
echo =========================================
echo.

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo WARNING: Virtual environment not activated!
    echo Please run: venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo Virtual environment detected: %VIRTUAL_ENV%
echo.

echo Installing/Upgrading packages...
echo.

REM Install langchain packages
pip install --upgrade langchain==0.3.14
pip install --upgrade langchain-text-splitters==0.3.4

REM Install OpenAI
pip install --upgrade openai==1.54.0

REM Install other dependencies
pip install --upgrade tiktoken==0.8.0
pip install --upgrade faiss-cpu==1.9.0.post1

echo.
echo =========================================
echo Verifying installations...
echo =========================================
echo.

python -c "import langchain; print('✓ langchain')" 2>nul || echo ✗ langchain - NOT INSTALLED
python -c "import langchain_text_splitters; print('✓ langchain-text-splitters')" 2>nul || echo ✗ langchain-text-splitters - NOT INSTALLED
python -c "import openai; print('✓ openai')" 2>nul || echo ✗ openai - NOT INSTALLED
python -c "import tiktoken; print('✓ tiktoken')" 2>nul || echo ✗ tiktoken - NOT INSTALLED
python -c "import faiss; print('✓ faiss-cpu')" 2>nul || echo ✗ faiss-cpu - NOT INSTALLED

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo You can now run: python app.py
echo.
pause
