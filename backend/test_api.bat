@echo off
echo Testing KB Builder Phase 3...
echo.

echo Step 1: Scan URL for PDFs
curl -X POST http://localhost:8000/api/scan-url -H "Content-Type: application/json" -d "{\"url\":\"https://ithandbook.ffiec.gov/it-booklets/\"}"

echo.
echo.
echo Step 2: Get Bedrock Models
curl http://localhost:8000/api/bedrock/models

echo.
echo.
echo Step 3: Create Knowledge Base (Example)
echo Note: Replace the documents array with actual PDFs from step 1
echo curl -X POST http://localhost:8000/api/kb -H "Content-Type: application/json" -d "{\"name\":\"FFIEC IT Handbook\",\"model_id\":\"anthropic.claude-3-5-sonnet-20240620-v1:0\",\"documents\":[{\"filename\":\"example.pdf\",\"url\":\"https://example.com/example.pdf\"}]}"

echo.
echo.
echo Step 4: Chat with KB (Example - use KB ID from step 3)
echo curl -X POST http://localhost:8000/api/kb/1/chat -H "Content-Type: application/json" -d "{\"message\":\"What is this document about?\"}"

echo.
echo.
echo Step 5: Get Chat History
echo curl http://localhost:8000/api/kb/1/history

echo.
echo.
echo Step 6: Cleanup Old History
echo curl -X DELETE http://localhost:8000/api/kb/1/history/cleanup
