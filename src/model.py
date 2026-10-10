import ollama
from pydantic import BaseModel, Field

class DocumentResponse(BaseModel):
    agent_response: str = Field(
        description="A conversational text response answering the user's question using only the verified reference context."
    )
    documents: list[int] = Field(
        description="A list of page or frame integer numbers found in the text that were used to build this output."
    )

class Model:
    def __init__(self):
        pass

    def query_rag_engine(self, user_query, context_blocks):
        with open("src/prompt.txt", 'r') as file:
            content = file.read()

        final_content = content.format(
            context_blocks=context_blocks,
            user_query=user_query
        )

        response = ollama.chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': final_content}],
            format=DocumentResponse.model_json_schema()
        )

        output = response['message']['content']
        with open('src/model_output.txt', 'w') as file:
            file.write(output)
        print("Written to file model_output.txt...\n")

        structured_data = DocumentResponse.model_validate_json(output)
        return structured_data
