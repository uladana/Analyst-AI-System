import os
import gradio as gr
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

# Embedding-Model
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
retriever = db.as_retriever()

# Prompt-Template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Beantworte die Frage basierend auf dem folgenden Kontext.
Wenn du die Antwort nicht weißt, gib ehrlich zu, dass du es nicht weißt.

Kontext:
{context}

Frage:
{question}
""".strip()
)

# Hauptmodell (Gemini)
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt": prompt_template})
except ResourceExhausted as e:
    print("⚠️ Gemini-Quota überschritten. Fallback wird vorbereitet...")

# Fallback (z. B. Falcon)
fallback_llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.0
)
fallback_chain = RetrievalQA.from_chain_type(llm=fallback_llm, retriever=retriever, chain_type_kwargs={"prompt": prompt_template})

# Gradio-Logik
def answer_and_validate(user_query):
    try:
        print("🧠 Frage wird mit Gemini verarbeitet...")
        return qa_chain.invoke({"query": user_query})["result"]
    except Exception as e:
        print(f"⚠️ Gemini-Fehler: {e}\n→ Fallback wird verwendet...")
        try:
            return fallback_chain.invoke({"query": user_query})["result"]
        except Exception as fallback_error:
            import traceback
            traceback_str = traceback.format_exc()
            print("❌ Fallback-Fehler:", traceback_str)
            return f"❌ Fallback fehlgeschlagen:\n{fallback_error}"

# Gradio-GUI
with gr.Blocks(title="Analyst-AI-System") as demo:
    gr.Markdown("# 📊 Analyst AI (Gemini + Fallback)")
    with gr.Row():
        input_text = gr.Textbox(label="Frage eingeben", placeholder="z.B. Was steht im Risikobericht?")
    with gr.Row():
        output_text = gr.Textbox(label="Antwort", interactive=False)
    with gr.Row():
        ask_button = gr.Button("Frage stellen")
    ask_button.click(fn=answer_and_validate, inputs=input_text, outputs=output_text)

demo.launch()
