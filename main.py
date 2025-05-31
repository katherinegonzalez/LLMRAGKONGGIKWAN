__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Imports
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from utils.constants import OPENAI_KEY
import streamlit as st
from langchain.vectorstores import Chroma
from scripts.vector_db import load_or_create_vector_db

#Kong Gi Kwan AI Assistant

vector_db = load_or_create_vector_db()
# Create a document retriever
retriever = vector_db.as_retriever()
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_KEY)

# Create a Streamlit app
st.title("Asistente IA Kong Gi Kwan")

# Create a system prompt
# It sets the overall context for the model.
# It influences tone, style, and focus before user interaction starts.
# Unlike user inputs, a system prompt is not visible to the end user.

system_prompt = (
    "Eres un asistente experto en Taekwondo, dedicado a enseñar y apoyar a estudiantes de la academia Kong Gi Kwan. "
    "Responde con claridad, respeto y precisión, basándote en el contexto dado." #, si el contexto no tiene la información entonces basate en la historia, la filosofía, la técnica y la estructura del Taekwondo."
    "Si no sabes la respuesta o falta información, reconoce tus límites y di que no cuentas con la información. "
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