from ingestion import IngestionRouter
from ocr import LocalOCRProcessor
from knowledgebase import VectorMemoryBank
from model import Model

def main():
    router = IngestionRouter()
    ocr_engine = LocalOCRProcessor()
    memory_bank = VectorMemoryBank()
    model = Model()

    processing_queue, choice = router.get_ingestion_source()
    
    if choice == "document":
        text_chunks = ocr_engine.extract_and_chunk_multiple(processing_queue)
        memory_bank.store_document_chunks(text_chunks)
        
        user_query = "Summarize the document."
        context_blocks = memory_bank.query_knowledge_base(user_query, top_k=3)
        structured_data = model.query_rag_engine(user_query, context_blocks)
        print(structured_data.agent_response)

        while True:
            user_query = input("\nQuery about document (type 'exit' to quit): ")
            if user_query == 'exit':
                break

            context_blocks = memory_bank.query_knowledge_base(user_query, top_k=3)
            structured_data = model.query_rag_engine(user_query, context_blocks)
            print(structured_data.agent_response)

        return

    elif choice == "direct_chat":
        while True:
            user_query = input("\nQuery the LLM (type 'exit' to quit): ")
            if user_query == 'exit':
                break

            context_blocks = memory_bank.query_knowledge_base(user_query, top_k=3)
            structured_data = model.query_rag_engine(user_query, context_blocks)
            print(structured_data.agent_response)

if __name__ == "__main__":
    main()
