from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

#  function to extract text from pdf files in a directory
def extract_text_from_pdf(directory):
    loader = DirectoryLoader(directory, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


# function to split the text into chunks
def split_text_into_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=480, chunk_overlap=20)
    chunks = text_splitter.split_documents(documents)
    return chunks

# download embeddings from hugging face
def download_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",model_kwargs={'device': 'cpu'},encode_kwargs={'normalize_embeddings': True})
    return embeddings