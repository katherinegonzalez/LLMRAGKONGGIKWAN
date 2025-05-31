# Imports
from langchain_openai import OpenAIEmbeddings
from scripts.document_loader import load_document
import os
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma 
from utils.constants import INDEX_PATH, temp_paths
from utils.constants import OPENAI_KEY

# Function to load or create the vector database
def load_or_create_vector_db():

    # Generate embeddings
    # Embeddings are numerical vector representations of data, typically used to capture relationships, similarities,
    # and meanings in a way that machines can understand. They are widely used in Natural Language Processing (NLP),
    # recommender systems, and search engines.
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY,
                                    model="text-embedding-ada-002")
    # Check if the index already exists
    if os.path.exists(INDEX_PATH):
      
        # Load the chroma index from local storage
        vector_db = Chroma(persist_directory=str(INDEX_PATH), embedding_function=embeddings)
    else:
        # Load documents and split it into chunks for efficient retrieval.
        chunks = []
        for temp_file in temp_paths:
            loaded_chunks = load_document(temp_file)
            print(f"{temp_file} -> {len(loaded_chunks)} chunks")
            chunks.extend(loaded_chunks)
        
        # Message that document is being processed
        print("Processing document... :watch:")

        # Create vector database containing chunks and embeddings
        vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=INDEX_PATH)
        vector_db.persist()
        print("Index created and saved locally.")

    return vector_db