from src.helper import download_embeddings, split_text_into_chunks, extract_text_from_pdf
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import getpass
import os
import time

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')


data = extract_text_from_pdf("data/")
print("data loaded")
chunks = split_text_into_chunks(data)
print("chuncks created")
embeddings = download_embeddings()
print("embedding model downloaded")

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
print("vector store initialized")


from uuid import uuid4

uuids =[str(uuid4()) for _ in range(len(chunks))]

vector_store.add_documents(documents=chunks, ids=uuids)

