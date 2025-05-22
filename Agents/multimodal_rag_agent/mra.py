import os
import json
import re
from dotenv import load_dotenv
from pathlib import Path
import shutil

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

PROCESSED_DIR = Path(os.getenv("PROCESSED_DIR", r"C:\Users\hshakademie7\Desktop\Analyst-AI-System\data\processed"))
PERSIST_DIR = Path(os.getenv("PERSIST_DIR", r"C:\Users\hshakademie7\Desktop\Analyst-AI-System\data\embeddings"))

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# ➕ Helpers to detect company and year from filenames
def detect_company_from_filename(filename):
    return filename.split("_")[0].capitalize()  # e.g. "apple_2023.json" → Apple

def detect_year_from_filename(filename):
    match = re.search(r'\d{4}', filename)
    return match.group(0) if match else "unknown"

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def load_all_json_files(processed_dir: Path):
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

    files = list(processed_dir.glob("*.json"))
    if not files:
        print("❌ Keine JSON-Dateien gefunden.")
        return []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"⚠️ Fehler beim Laden der Datei {file.name}: {e}")
                continue

        company = detect_company_from_filename(file.name)
        year = detect_year_from_filename(file.name)

        chunks = []
        for entry in data:
            entry_text = ""
            if 'text' in entry and entry['text']:
                entry_text += entry['text'].strip() + "\n"
            if 'table' in entry and entry['table']:
                table = entry['table']
                if isinstance(table, list):
                    for row in table:
                        if isinstance(row, dict):
                            row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
                        else:
                            row_str = ", ".join(str(cell) for cell in row)
                        entry_text += row_str + "\n"
            if entry_text.strip():
                chunks.append(entry_text.strip())

        if chunks:
            split_chunks = text_splitter.split_text("\n\n".join(chunks))
            for chunk in split_chunks:
                if chunk.strip():
                    documents.append(Document(
                        page_content=chunk,
                        metadata={
                            "source": str(file),
                            "company": company,
                            "year": year
                        }
                    ))

    print(f"✅ Insgesamt {len(documents)} Dokumente aus {len(files)} Dateien geladen.")
    for i, doc in enumerate(documents[:3]):
        print(f"\n📄 Dokument {i+1} (Ausschnitt):\n{doc.page_content[:300]}")

    return documents

def create_or_load_vectorstore(documents):
    vectorstore = Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embedding_model,
        collection_name="investor_reports"
    )

    count_before = vectorstore._collection.count()
    print(f"🧠 Vectorstore currently has {count_before} vectors.")

    if count_before == 0:
        print("⚙️ Erstelle neue Vektoren...")

        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        print(f"🔍 Testing embedding generation...")
        try:
            test_embedding = embedding_model.embed_documents([texts[0]])
            print(f"✅ Embedding generated, vector length: {len(test_embedding[0])}")
        except Exception as e:
            print(f"⚠️ Fehler beim Generieren des Test-Embeddings: {e}")
            return vectorstore

        print(f"🔢 Erzeuge Embeddings für {len(texts)} Dokumente...")
        embeddings = embedding_model.embed_documents(texts)

        batch_size = 5000
        total_added = 0
        for text_chunk, meta_chunk, embed_chunk in zip(
            chunk_list(texts, batch_size),
            chunk_list(metadatas, batch_size),
            chunk_list(embeddings, batch_size),
        ):
            vectorstore.add_texts(texts=text_chunk, metadatas=meta_chunk, embeddings=embed_chunk)
            total_added += len(text_chunk)
            print(f"💾 Added {total_added} vectors so far...")

        count_after = vectorstore._collection.count()
        print(f"💾 Vektoren gespeichert (automatisch). Aktuelle Anzahl: {count_after}")

        if count_after == 0:
            print("⚠️ Warnung: Keine Vektoren wurden hinzugefügt! Bitte prüfe Dokumente und Embeddings.")
    else:
        print("✅ Vectorstore geladen.")
        print("🧠 Anzahl gespeicherter Vektoren:", count_before)

    return vectorstore

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a precise and factual assistant for investor report analysis.

🧠 Context:
{context}

❓ Question:
{question}

📈 Answer:
"""
)

def setup_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 90})
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1,
        ),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )
    return qa_chain

def run_agent():
    print("📂 Lade und verarbeite JSON-Daten...")
    documents = load_all_json_files(PROCESSED_DIR)
    if not documents:
        print("❌ Keine Dokumente zum Einbetten gefunden. Beende das Programm.")
        return

    vectorstore = create_or_load_vectorstore(documents)
    qa_chain = setup_qa_chain(vectorstore)
    print("\n🧠 Analyst Agent ist bereit! Tippe eine Frage oder 'exit' zum Beenden.")

    while True:
        question = input("\n❓ Deine Frage: ").strip()
        if not question:
            print("Bitte gib eine gültige Frage ein.")
            continue
        if question.lower() in ["exit", "quit"]:
            print("👋 Tschüss!")
            break

        try:
            result = qa_chain.invoke(question)
            print("\n🤖 Antwort:")
            print(result["result"])
        except Exception as e:
            print(f"⚠️ Fehler: {e}")

if __name__ == "__main__":
    run_agent()
