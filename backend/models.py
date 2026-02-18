from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional, List
from datetime import datetime

class ScanUrlRequest(BaseModel):
    url: str

class PDFInfo(BaseModel):
    filename: str
    url: str
    size: Optional[str] = None

class ScanUrlResponse(BaseModel):
    pdfs: list[PDFInfo]
    total: int

class BedrockModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    model_id: str
    model_name: str

class BedrockModelsResponse(BaseModel):
    models: list[BedrockModel]
    default_model: str

class OpenAIModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    model_id: str
    model_name: str

class OpenAIModelsResponse(BaseModel):
    models: list[OpenAIModel]
    default_model: str

class PDFDocument(BaseModel):
    filename: str
    url: str

class CreateKBRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    name: str
    model_id: str
    provider: str = 'bedrock'  # 'bedrock' or 'openai'
    api_key: Optional[str] = None  # Required for OpenAI
    documents: List[PDFDocument]

class CreateKBResponse(BaseModel):
    id: int
    name: str
    status: str
    message: str

class ChatRequest(BaseModel):
    message: str
    api_key: Optional[str] = None

class SourceReference(BaseModel):
    filename: str
    page_number: int
    text: str

class ChatResponse(BaseModel):
    response: str
    sources: List[SourceReference]

class ChatHistoryItem(BaseModel):
    id: int
    user_message: str
    bot_response: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    history: List[ChatHistoryItem]

class DocumentInfo(BaseModel):
    id: int
    filename: str
    url: str
    page_count: Optional[int]
    status: str
    added_at: datetime

class KBDetail(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    id: int
    name: str
    model_id: str
    provider: str
    created_at: datetime
    updated_at: datetime
    documents: List[DocumentInfo]
    document_count: int

class KBListItem(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    id: int
    name: str
    model_id: str
    provider: str
    created_at: datetime
    document_count: int

class KBListResponse(BaseModel):
    knowledge_bases: List[KBListItem]
    total: int

class UpdateKBRequest(BaseModel):
    name: str
