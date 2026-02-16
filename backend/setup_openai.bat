@echo off
echo ========================================
echo OpenAI Integration Setup
echo ========================================
echo.

echo Installing OpenAI package...
call venv\Scripts\activate.bat
pip install openai==1.54.0

echo.
echo Running database migration...
python migrate_db.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now use OpenAI as an alternative to AWS Bedrock.
echo Get your API key from: https://platform.openai.com/api-keys
echo.
pause
