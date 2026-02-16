from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import init_db, get_db, KnowledgeBase, Document, ChatHistory
from models import (
    ScanUrlRequest, ScanUrlResponse, BedrockModelsResponse, OpenAIModelsResponse,
    CreateKBRequest, CreateKBResponse, ChatRequest, ChatResponse, 
    ChatHistoryResponse, ChatHistoryItem, KBListResponse, KBListItem,
    KBDetail, DocumentInfo, UpdateKBRequest
)
from services.scraper import scan_url_for_pdfs
from services.bedrock_client import BedrockClient
from services.openai_client import OpenAIClient
from services.pdf_processor import PDFProcessor
from services.embeddings import EmbeddingsService
from services.chat import ChatService
from datetime import datetime, timedelta, timezone
import shutil
from pathlib import Path
from config import get_config
import requests

app = FastAPI(title="KB Builder API", version="1.0.0")

# CORS middleware for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "KB Builder API", "status": "running"}

@app.post("/api/scan-url", response_model=ScanUrlResponse)
async def scan_url(request: ScanUrlRequest):
    """Scan a URL and discover all PDF files"""
    try:
        pdfs = scan_url_for_pdfs(request.url)
        return ScanUrlResponse(pdfs=pdfs, total=len(pdfs))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/validate-pdfs")
async def validate_pdfs(request: dict):
    """Validate PDF URLs to check if they're accessible"""
    try:
        urls = request.get('urls', [])
        results = []
        
        for url_info in urls:
            url = url_info.get('url')
            filename = url_info.get('filename')
            
            try:
                # HEAD request to check if URL is accessible
                response = requests.head(url, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    status = 'available'
                    reason = 'OK'
                elif response.status_code == 404:
                    status = 'unavailable'
                    reason = '404 Not Found'
                elif response.status_code == 403:
                    status = 'unavailable'
                    reason = '403 Forbidden'
                else:
                    status = 'unavailable'
                    reason = f'HTTP {response.status_code}'
                    
            except requests.exceptions.Timeout:
                status = 'unavailable'
                reason = 'Timeout'
            except requests.exceptions.ConnectionError:
                status = 'unavailable'
                reason = 'Connection Error'
            except Exception as e:
                status = 'unavailable'
                reason = str(e)[:50]
            
            results.append({
                'url': url,
                'filename': filename,
                'status': status,
                'reason': reason
            })
        
        return {'results': results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bedrock/models", response_model=BedrockModelsResponse)
async def get_bedrock_models():
    """Get list of available AWS Bedrock models"""
    try:
        bedrock = BedrockClient()
        models = bedrock.list_available_models()
        default_model = bedrock.get_default_model()
        return BedrockModelsResponse(models=models, default_model=default_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/openai/models", response_model=OpenAIModelsResponse)
async def get_openai_models():
    """Get list of available OpenAI models"""
    try:
        openai_client = OpenAIClient()
        models = openai_client.list_available_models()
        default_model = openai_client.get_default_model()
        return OpenAIModelsResponse(models=models, default_model=default_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kb", response_model=KBListResponse)
async def list_knowledge_bases(db: Session = Depends(get_db)):
    """List all knowledge bases"""
    try:
        kbs = db.query(KnowledgeBase).all()
        kb_list = []
        
        for kb in kbs:
            doc_count = db.query(func.count(Document.id)).filter(Document.kb_id == kb.id).scalar()
            kb_list.append(KBListItem(
                id=kb.id,
                name=kb.name,
                model_id=kb.model_id,
                provider=kb.provider,
                created_at=kb.created_at,
                document_count=doc_count
            ))
        
        return KBListResponse(knowledge_bases=kb_list, total=len(kb_list))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kb/{kb_id}", response_model=KBDetail)
async def get_knowledge_base(kb_id: int, db: Session = Depends(get_db)):
    """Get knowledge base details"""
    try:
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        
        documents = db.query(Document).filter(Document.kb_id == kb_id).all()
        doc_list = [
            DocumentInfo(
                id=doc.id,
                filename=doc.filename,
                url=doc.url,
                page_count=doc.page_count,
                status=doc.status,
                added_at=doc.added_at
            )
            for doc in documents
        ]
        
        return KBDetail(
            id=kb.id,
            name=kb.name,
            model_id=kb.model_id,
            provider=kb.provider,
            created_at=kb.created_at,
            updated_at=kb.updated_at,
            documents=doc_list,
            document_count=len(doc_list)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/kb/{kb_id}")
async def update_knowledge_base(kb_id: int, request: UpdateKBRequest, db: Session = Depends(get_db)):
    """Update knowledge base name"""
    try:
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        
        kb.name = request.name
        kb.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        return {"message": "Knowledge base updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/kb/{kb_id}")
async def delete_knowledge_base(kb_id: int, db: Session = Depends(get_db)):
    """Delete knowledge base and all associated data"""
    try:
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        
        # Delete files
        kb_path = Path(f"../data/kb_{kb_id}")
        if kb_path.exists():
            shutil.rmtree(kb_path)
        
        # Delete from database (cascade will handle documents and history)
        db.delete(kb)
        db.commit()
        
        return {"message": "Knowledge base deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/kb", response_model=CreateKBResponse)
async def create_knowledge_base(request: CreateKBRequest, db: Session = Depends(get_db)):
    """Create a new knowledge base with PDF processing and embeddings"""
    import traceback
    try:
        config = get_config()
        
        print(f"\n{'='*60}")
        print(f"Creating Knowledge Base: {request.name}")
        print(f"Provider: {request.provider}")
        print(f"Model: {request.model_id}")
        print(f"Documents: {len(request.documents)}")
        print(f"{'='*60}\n")
        
        # Use API key from request, or fall back to config
        api_key = request.api_key
        if request.provider == 'openai' and not api_key:
            print("Using API key from config.yml")
            api_key = config.get_openai_api_key()
            if not api_key:
                raise HTTPException(
                    status_code=400, 
                    detail="OpenAI API key not found. Please add it to backend/config.yml. See backend/config.example.yml for reference."
                )
        else:
            print("Using API key from request")
        
        # Create KB record
        print("Step 1: Creating KB record in database...")
        kb = KnowledgeBase(
            name=request.name,
            model_id=request.model_id,
            provider=request.provider,
            api_key=api_key,  # Store the API key (from request or config)
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(kb)
        db.commit()
        db.refresh(kb)
        print(f"✓ KB created with ID: {kb.id}\n")
        
        # Initialize services
        print("Step 2: Initializing services...")
        pdf_processor = PDFProcessor(kb.id)
        embeddings_service = EmbeddingsService(kb.id, request.provider, api_key)
        print("✓ Services initialized\n")
        
        all_chunks = []
        
        print(f"Step 3: Processing {len(request.documents)} document(s)...")
        # Process each PDF
        for idx, doc in enumerate(request.documents, 1):
            try:
                print(f"\n  Document {idx}/{len(request.documents)}: {doc.filename}")
                
                # Download PDF
                print(f"    - Downloading from {doc.url[:50]}...")
                file_path = pdf_processor.download_pdf(doc.url, doc.filename)
                print(f"    ✓ Downloaded to {file_path}")
                
                # Get page count
                page_count = pdf_processor.get_page_count(file_path)
                print(f"    ✓ PDF has {page_count} pages")
                
                # Create document record
                document = Document(
                    kb_id=kb.id,
                    filename=doc.filename,
                    url=doc.url,
                    file_path=file_path,
                    page_count=page_count,
                    status='processing',
                    added_at=datetime.now(timezone.utc)
                )
                db.add(document)
                db.commit()
                
                # Extract text
                print(f"    - Extracting text from {page_count} pages...")
                pages_data = pdf_processor.extract_text_from_pdf(file_path)
                print(f"    ✓ Text extracted")
                
                # Chunk text
                print(f"    - Chunking text...")
                chunks = embeddings_service.chunk_text(pages_data)
                all_chunks.extend(chunks)
                print(f"    ✓ Created {len(chunks)} chunks (total: {len(all_chunks)})")
                
                # Update document status
                document.status = 'completed'
                db.commit()
                print(f"    ✓ Document processed successfully\n")
                
            except Exception as e:
                print(f"    ✗ Error processing document: {str(e)}\n")
                # Mark document as failed
                if 'document' in locals():
                    document.status = 'failed'
                    db.commit()
                raise Exception(f"Failed to process {doc.filename}: {str(e)}")
        
        # Store all chunks with embeddings
        print(f"\nStep 4: Generating embeddings for {len(all_chunks)} chunks...")
        print(f"  This may take a while...")
        total_chunks = embeddings_service.store_chunks(all_chunks)
        print(f"✓ All embeddings generated and stored\n")
        
        print(f"{'='*60}")
        print(f"✓ Knowledge Base Created Successfully!")
        print(f"  ID: {kb.id}")
        print(f"  Name: {kb.name}")
        print(f"  Documents: {len(request.documents)}")
        print(f"  Chunks: {total_chunks}")
        print(f"{'='*60}\n")
        
        return CreateKBResponse(
            id=kb.id,
            name=kb.name,
            status="success",
            message=f"Knowledge base created with {len(request.documents)} documents and {total_chunks} chunks"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"ERROR creating KB: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/kb/{kb_id}/chat", response_model=ChatResponse)
async def chat_with_kb(kb_id: int, request: ChatRequest, db: Session = Depends(get_db)):
    """Chat with a knowledge base using RAG"""
    try:
        # Get KB
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        
        # Initialize chat service with provider info
        chat_service = ChatService(kb_id, kb.model_id, kb.provider, kb.api_key)
        
        # Get response
        result = chat_service.chat(request.message)
        
        # Save to history
        history = ChatHistory(
            kb_id=kb_id,
            user_message=request.message,
            bot_response=result['response'],
            timestamp=datetime.now(timezone.utc)
        )
        db.add(history)
        db.commit()
        
        return ChatResponse(
            response=result['response'],
            sources=result['sources']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kb/{kb_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(kb_id: int, db: Session = Depends(get_db)):
    """Get chat history for a knowledge base (last 7 days)"""
    try:
        # Get KB
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        
        # Get history from last 7 days
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        history = db.query(ChatHistory).filter(
            ChatHistory.kb_id == kb_id,
            ChatHistory.timestamp >= seven_days_ago
        ).order_by(ChatHistory.timestamp.desc()).all()
        
        return ChatHistoryResponse(
            history=[
                ChatHistoryItem(
                    id=h.id,
                    user_message=h.user_message,
                    bot_response=h.bot_response,
                    timestamp=h.timestamp
                )
                for h in history
            ]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/kb/{kb_id}/history/cleanup")
async def cleanup_old_history(db: Session = Depends(get_db)):
    """Delete chat history older than 7 days"""
    try:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        deleted = db.query(ChatHistory).filter(
            ChatHistory.timestamp < seven_days_ago
        ).delete()
        db.commit()
        
        return {"message": f"Deleted {deleted} old chat history records"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
