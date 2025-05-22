import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from qa_agent import run_qa_check
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI


# === Umgebungsvariablen laden ===
load_dotenv()

# === Google Gemini konfigurieren ===
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# === Primäres LLM (Gemini 1.5 Pro) ===
def get_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-1.5-pro-latest",
        temperature=0.3,
        convert_system_message_to_human=True
    )

# === Fallback LLM (HuggingFace Flan-T5) ===
def get_fallback_llm():
    return HuggingFaceHub(
        repo_id="google/flan-t5-xl",
        model_kwargs={"temperature": 0}
    )

# === Embedding & Chroma ===
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)
retriever = db.as_retriever()

# === QA-Kette initialisieren ===
try:
    llm = get_gemini_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
except Exception as e:
    if "429" in str(e):
        print("⚠️ Gemini-Quota überschritten. Wechsle zu HuggingFace-Modell...")
        llm = get_fallback_llm()
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
    else:
        raise e
