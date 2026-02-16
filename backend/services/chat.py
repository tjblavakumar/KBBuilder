import json
from typing import List, Dict
from services.embeddings import EmbeddingsService
from services.llm_provider import get_llm_provider

class ChatService:
    def __init__(self, kb_id: int, model_id: str, provider: str = 'bedrock', api_key: str = None, profile_name: str = 'default'):
        self.kb_id = kb_id
        self.model_id = model_id
        self.provider = provider
        self.llm_provider = get_llm_provider(provider, model_id, api_key, profile_name)
        self.embeddings_service = EmbeddingsService(kb_id, provider, api_key, profile_name)
    
    def chat(self, user_message: str, n_results: int = 5) -> Dict:
        """Generate RAG-based response"""
        try:
            # Retrieve relevant chunks
            relevant_chunks = self.embeddings_service.query(user_message, n_results)
            
            if not relevant_chunks:
                return {
                    'response': 'I don\'t have enough information to answer that question.',
                    'sources': []
                }
            
            # Build context from chunks
            context = "\n\n".join([
                f"[{chunk['metadata']['filename']}, Page {chunk['metadata']['page_number']}]\n{chunk['text']}"
                for chunk in relevant_chunks
            ])
            
            # Build prompt
            prompt = f"""You are a helpful assistant. Use the following context to answer the user's question. 
            
Context:
{context}

User Question: {user_message}

Provide a clear and concise answer based on the context. If the context doesn't contain relevant information, say so."""
            
            # Call LLM provider
            response = self.llm_provider.generate_chat_response(prompt)
            
            # Extract sources
            sources = []
            seen = set()
            for chunk in relevant_chunks:
                key = (chunk['metadata']['filename'], chunk['metadata']['page_number'])
                if key not in seen:
                    sources.append({
                        'filename': chunk['metadata']['filename'],
                        'page_number': chunk['metadata']['page_number'],
                        'text': chunk['text'][:200] + '...' if len(chunk['text']) > 200 else chunk['text']
                    })
                    seen.add(key)
            
            return {
                'response': response,
                'sources': sources
            }
        
        except Exception as e:
            raise Exception(f"Chat failed: {str(e)}")
