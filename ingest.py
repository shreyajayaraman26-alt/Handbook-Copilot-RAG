from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load the handbook PDF
pdf_path = "data/harvard hb.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("PDF loaded successfully!")
print("Number of pages:", len(documents))

# 2. Split the handbook into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Text split successfully!")
print("Number of chunks:", len(chunks))

# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating embeddings...")

# 4. Store embeddings in ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("Embeddings stored successfully!")
print("ChromaDB created successfully!")

print("\nHANDBOOK RAG DATABASE READY!")