# Imports
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from scripts.secret import OPENAI_KEY
from scripts.document_loader import load_document
import streamlit as st
import os
from langchain.vectorstores import Chroma

# Path to the saved FAISS index
INDEX_PATH = "./chroma_index" # "./faiss_index"

# Create a Streamlit app
st.title("Asistente IA Kong Gi Kwan")
#Kong Gi Kwan AI Assistant


# Code to work around document loader from Streamlit and make it readable by langchain
temp_file = "./documents/AcademiaKongGiKwan.pdf"

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
        # st.write("Loading existing index...")
        # Cargar el índice Chroma desde el almacenamiento local
        vector_db = Chroma(persist_directory=INDEX_PATH, embedding_function=embeddings)
    else:

        # Load document and split it into chunks for efficient retrieval.
        chunks = load_document(temp_file)

        # Message user that document is being processed with time emoji
        st.write("Processing document... :watch:")

        # Create vector database containing chunks and embeddings
        vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=INDEX_PATH)
        vector_db.persist()
        st.write("Index created and saved locally.")

    return vector_db

vector_db = load_or_create_vector_db()
# Create a document retriever
retriever = vector_db.as_retriever()
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_KEY)

# Create a system prompt
# It sets the overall context for the model.
# It influences tone, style, and focus before user interaction starts.
# Unlike user inputs, a system prompt is not visible to the end user.

system_prompt = (
    "You are a helpful assistant. Use the given context to answer the question."
    "If you don't know the answer, say you don't know. "
    "{context}"
)

# Create a prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Create a chain
# It creates a StuffDocumentsChain, which takes multiple documents (text data) and "stuffs" them together before passing them to the LLM for processing.

question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Creates the RAG
chain = create_retrieval_chain(retriever, question_answer_chain)

# Streamlit input for question
question = st.text_input("Ask a question about the document:")
if question:
    # Answer
    response = chain.invoke({"input": question})['answer']
    st.write(response)


# Para Subir la app: https://streamlit.io/cloud 