# app.py

from flask import  Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_core.prompts import  PromptTemplate
from langchain_community.llms import CTransformers
from langchain_core.output_parsers import StrOutputParser
from src.prompt import *
from dotenv import load_dotenv
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GENAI_API_KEY'))

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

embeddings = download_embeddings()
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mchat"  # change if desired

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.5}
)

prompt = PromptTemplate(template=prompt_template, input_variables=["previous_context","current_context","question"])

# llm = CTransformers(
#     model='model/llama-2-7b-chat.ggmlv3.q4_0.bin',
#     model_type='llama',
#     config={
#         'max_new_tokens' : 512,
#         'temperature':0.5
#     }

# )

# class CustomQAFlow:
#     def __init__(self, retriever, llm, prompt, max_token_length=500):
#         """
#         Custom flow for QA using chunks from document objects.
        
#         Args:
#         - retriever: The retriever to obtain document objects.
#         - llm: The language model for processing each chunk.
#         - prompt: The prompt format for question and context.
#         - max_token_length: Maximum number of tokens per chunk (default is 500).
#         """
#         self.retriever = retriever
#         self.llm = llm
#         self.prompt = prompt
#         self.max_token_length = max_token_length
#         self.parser = StrOutputParser()

#     def split_text(self, text):
#         """Splits the document text into smaller chunks."""
#         words = text.split()
#         chunks = []
#         current_chunk = []

#         for word in words:
#             current_chunk.append(word)
#             if len(" ".join(current_chunk)) >= self.max_token_length:
#                 chunks.append(" ".join(current_chunk))
#                 current_chunk = []

#         if current_chunk:  # Append any remaining chunk
#             chunks.append(" ".join(current_chunk))
        
#         return chunks

#     def invoke(self, question):
#         """
#         Process the question by:
#         1. Retrieving documents (with text in page_content)
#         2. Splitting the content of each document
#         3. Processing each chunk and collecting results
#         4. Combining results across all chunks and documents
#         """
#         # Step 1: Retrieve documents from retriever
#         retrieved_documents = self.retriever.invoke(question)  # Ensure this correctly retrieves documents

#         final_answers = []
        
#         # Step 2: Process each document
#         for document in retrieved_documents:
#             # Extract text from the document's page_content field
#             document_text = document.page_content

#             # Split the document into smaller chunks
#             chunks = self.split_text(document_text)
            
#             # Step 3: Process each chunk and collect the answers
#             document_answers = []
#             previous_context = ""  # Keep track of previous context for continuity

#             for chunk in chunks:
#                 # Prepare the input with previous context and the current chunk of document text
#                 context_input = {
#                     "previous_context": previous_context, 
#                     "current_context": chunk, 
#                     "question": question
#                 }

#                 # Create the prompt with previous and current context
#                 prompt_input = self.prompt.format(
#                     previous_context=context_input["previous_context"], 
#                     current_context=context_input["current_context"], 
#                     question=context_input["question"]
#                 )

#                 # Invoke the language model with this chunk
#                 answer = self.llm.invoke(prompt_input)
                
#                 # Parse the model's response
#                 parsed_answer = self.parser.parse(answer)
                
#                 # Collect the parsed answer and update previous context
#                 document_answers.append(parsed_answer)
#                 previous_context += " " + chunk  # Update previous context with the current chunk

#             # Combine answers for the current document
#             final_answers.append(" ".join(document_answers))
        
#         # Step 4: Return combined results across all documents
#         combined_answer = " ".join(final_answers)  # Optionally summarize this if too long
#         return combined_answer

# # Example usage:
# # Assuming `retriever`, `llm`, and `prompt` are already defined, and `retriever` returns document objects
# custom_qa_flow = CustomQAFlow(retriever, llm, prompt, max_token_length=512)


class CustomQAFlow:
    def __init__(self, retriever, prompt):
        """
        Custom flow for QA using document objects and calling the Gemini API.
        
        Args:
        - retriever: The retriever to obtain document objects.
        - prompt: The prompt format for question and context.
        """
        self.retriever = retriever
        self.prompt = prompt

    def generate_response(self, prompt_input):
        """Call Gemini API to generate the response based on prompt input."""
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt_input)
        return response.text

    def invoke(self, question):
        """
        Process the question by:
        1. Retrieving relevant documents.
        2. Combining the content of all documents.
        3. Passing the combined content and question to the Gemini API for generating an answer.
        """
        # Step 1: Retrieve documents
        retrieved_documents = self.retriever.invoke(question)

        # Step 2: Combine the content of all retrieved documents
        combined_content = " ".join([doc.page_content for doc in retrieved_documents])

        # Prepare the prompt input with the combined content
        prompt_input = self.prompt.format(
            current_context=combined_content,  # Combined document content as context
            question=question
        )

        # Step 3: Call the Gemini API with the combined context
        answer = self.generate_response(prompt_input)

        return answer


# Example usage
custom_qa_flow = CustomQAFlow(retriever, prompt)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg")  # Get user input from the form
    print(f"User input: {msg}")
    if msg:
        result = custom_qa_flow.invoke(msg)  # Call the custom QA flow to get the chatbot response
        print("Response: ", result)
        return jsonify({"response": result})  # Send the response back to frontend as JSON
    return jsonify({"response": "I didn't get that. Can you rephrase your question?"})


if __name__ == '__main__':
    app.run(debug=True)

