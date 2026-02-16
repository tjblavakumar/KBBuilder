import json
import pickle
from typing import List, Dict
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitters import RecursiveCharacterTextSplitter
import tiktoken
import faiss
import numpy as np
from pathlib import Path
from services.llm_provider import get_llm_provider

class EmbeddingsService:
    def __init__(self, kb_id: int, provider: str = 'bedrock', api_key: str = None, profile_name: str = 'default', base_path: str = "../data"):
        self.kb_id = kb_id
        self.provider = provider
        self.llm_provider = get_llm_provider(provider, None, api_key, profile_name)  # model_id not needed for embeddings
        
        # FAISS setup
        self.vector_path = Path(base_path) / f"kb_{kb_id}" / "vectors"
        self.vector_path.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.vector_path / "faiss.index"
        self.metadata_file = self.vector_path / "metadata.pkl"
        
        # Initialize or load FAISS index
        if self.index_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            with open(self.metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = None
            self.metadata = []
        
        # Text splitter for semantic chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            length_function=self._count_tokens,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken"""
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    
    def chunk_text(self, pages_data: List[Dict]) -> List[Dict]:
        """Chunk text from pages with metadata"""
        chunks = []
        
        for page_data in pages_data:
            text = page_data['text']
            page_num = page_data['page_number']
            filename = page_data['filename']
            
            # Split text into chunks
            text_chunks = self.text_splitter.split_text(text)
            
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    'text': chunk,
                    'metadata': {
                        'filename': filename,
                        'page_number': page_num,
                        'chunk_index': i
                    }
                })
        
        return chunks
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using configured provider"""
        return self.llm_provider.generate_embedding(text)
    
    def store_chunks(self, chunks: List[Dict]) -> int:
        """Store chunks with embeddings in FAISS"""
        try:
            embeddings = []
            total = len(chunks)
            
            print(f"  Generating embeddings: 0/{total}", end='', flush=True)
            
            for i, chunk in enumerate(chunks, 1):
                # Generate embedding
                embedding = self.generate_embedding(chunk['text'])
                embeddings.append(embedding)
                
                # Store metadata
                self.metadata.append({
                    'text': chunk['text'],
                    'metadata': chunk['metadata']
                })
                
                # Progress update every 10 chunks or at the end
                if i % 10 == 0 or i == total:
                    print(f"\r  Generating embeddings: {i}/{total}", end='', flush=True)
            
            print()  # New line after progress
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings).astype('float32')
            
            # Create or add to FAISS index
            if self.index is None:
                dimension = embeddings_array.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
            
            self.index.add(embeddings_array)
            
            # Save index and metadata
            faiss.write_index(self.index, str(self.index_file))
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
            
            return len(chunks)
        except Exception as e:
            raise Exception(f"Failed to store chunks: {str(e)}")
    
    def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Query FAISS for relevant chunks"""
        try:
            if self.index is None or len(self.metadata) == 0:
                return []
            
            query_embedding = self.generate_embedding(query_text)
            query_vector = np.array([query_embedding]).astype('float32')
            
            # Search in FAISS
            distances, indices = self.index.search(query_vector, min(n_results, len(self.metadata)))
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata):
                    results.append({
                        'text': self.metadata[idx]['text'],
                        'metadata': self.metadata[idx]['metadata'],
                        'distance': float(distances[0][i])
                    })
            
            return results
        except Exception as e:
            raise Exception(f"Failed to query: {str(e)}")
