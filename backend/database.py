from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class KnowledgeBase(Base):
    __tablename__ = 'knowledgebases'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    model_id = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False, default='bedrock')  # 'bedrock' or 'openai'
    api_key = Column(String(500), nullable=True)  # For OpenAI API key (encrypted in production)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    documents = relationship("Document", back_populates="knowledge_base", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="knowledge_base", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    kb_id = Column(Integer, ForeignKey('knowledgebases.id'), nullable=False)
    filename = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)
    file_path = Column(String(1000))
    page_count = Column(Integer)
    status = Column(String(50), default='pending')
    added_at = Column(DateTime, default=datetime.utcnow)
    
    knowledge_base = relationship("KnowledgeBase", back_populates="documents")

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True)
    kb_id = Column(Integer, ForeignKey('knowledgebases.id'), nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    knowledge_base = relationship("KnowledgeBase", back_populates="chat_history")

# Database setup
DATABASE_URL = "sqlite:///./kb_builder.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
