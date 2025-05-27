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

#Kong Gi Kwan AI Assistant

# Path to the saved Chroma index
INDEX_PATH = "./chroma_index" # "./faiss_index"

# Create a Streamlit app
st.title("Asistente IA Kong Gi Kwan")

# Code to work around documents loader from Streamlit and make it readable by langchain
temp_paths = ["./documents/AcademiaKongGiKwan.pdf", "./documents/ProgramaAscensoKongGiKwan.pdf"]

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
        vector_db = Chroma(persist_directory=INDEX_PATH, embedding_function=embeddings)
    else:
        # Load documents and split it into chunks for efficient retrieval.
        chunks = []
        for temp_file in temp_paths:
            loaded_chunks = load_document(temp_file)
            print(f"{temp_file} -> {len(loaded_chunks)} chunks")
            chunks.extend(loaded_chunks)
        
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

# load ask and questions history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show history
for speaker, message in st.session_state.chat_history:
    with st.chat_message("user" if speaker == "🧑‍💬" else "assistant"):
        st.markdown(message)

# User input
user_input = st.chat_input("Haz una pregunta")

if user_input:
    # Show user message
    st.session_state.chat_history.append(("🧑‍💬", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # show spinner while it loads
    with st.spinner("Cargando respuesta..."):
        response = chain.invoke({"input": user_input})["answer"]

    # Show chat response
    st.session_state.chat_history.append(("🤖", response))
    with st.chat_message("assistant"):
        st.markdown(response)

# Para Subir la app: https://streamlit.io/cloud 