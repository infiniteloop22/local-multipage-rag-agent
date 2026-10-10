import chromadb
import ollama
import numpy as np

class VectorMemoryBank:
    def __init__(self, collection_name="knowledge_base"):
        self.chroma_client = chromadb.PersistentClient(path="src/chroma_db")
        
        self.chroma_client.delete_collection(name=collection_name)
        
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    def store_document_chunks(self, chunks: list[str]):
        for idx, chunk in enumerate(chunks):
            embedding_response = ollama.embeddings(model="llama3.2:1b", prompt=chunk)
            vector = embedding_response["embedding"]
            self.collection.add(
                embeddings=[vector],
                documents=[chunk],
                ids=[f"doc_chunk_{idx}_{np.random.randint(1000,9999)}"]
            )

    def query_knowledge_base(self, user_question: str, top_k: int = 3) -> str:
        query_embedding = ollama.embeddings(model="llama3.2:1b", prompt=user_question)["embedding"]
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        retrieved_docs_nested = results.get("documents", [])
        return "\n---\n".join(retrieved_docs_nested[0])
