import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import uuid
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain_community.document_loaders import PyPDFLoader
# Initialize ChromaDB client and collection
client = chromadb.Client()
messages_collection = client.create_collection("webdata_collection")

# Initialize the Sentence Transformer model
model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def load_web_data(url):
    try:
        # Create a WebBaseLoader instance with the provided URL
        loader = WebBaseLoader(url)
        
        # Load the web page content
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(data)
        print(f"Loaded {len(document_chunks)} documents from {url}")
        print(document_chunks)
        return document_chunks

    except Exception as e:
        print(f"Error loading web data: {str(e)}")
        return None

def process_web_data(data):
    if data is None:
        print("No data to process.")
        return
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Prepare documents, embeddings, metadatas, and ids
    documents = []
    metadatas = []
    ids = []

    for index, document in enumerate(data):
        # Extract page content from the document
        content = document.page_content

        # Prepare metadata
        metadata = {
            'source_url': document.metadata.get('source_url', 'unknown'),
            'page_number': document.metadata.get('page_number', index + 1),
        }
        metadatas.append(metadata)

        # Collect document content for embedding
        documents.append(content)
        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each document
    print(metadatas)
    print(documents)

    # Embed the documents
    embeddings = model.encode(documents, convert_to_tensor=True)
    

    # Add documents to the ChromaDB collection
    messages_collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),  # Convert embeddings to a list
        metadatas=metadatas,
        ids=ids,
    )

    print(f"Stored {len(documents)} document(s) in ChromaDB.")

def add_web_data(url):
    # Load web data from the given URL
    print(f"Loading data from {url}")
    web_data = load_web_data(url)

    # Process web data and add it to the ChromaDB collection
    process_web_data(web_data)
    print("Web data processing complete.")

# Example usage