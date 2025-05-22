from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from pathlib import Path
import json

# === Verzeichnisse ===
JSON_DIR = Path(r"C:\Users\ahmad\Analyst-AI-System\data\Processed\json")
CHROMA_DB_DIR = "chroma_db"

def load_documents():
    docs = []
    for file in JSON_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            text = json_data.get("text", "")
            if text.strip():
                # Text in Chunks aufteilen
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
                chunks = splitter.split_text(text)
                for i, chunk in enumerate(chunks):
                    docs.append(Document(
                        page_content=chunk,
                        metadata={
                            "source": json_data["source_file"],
                            "company": json_data["company"],
                            "chunk_id": i
                        }
                    ))
    return docs

def build_vectorstore():
    documents = load_documents()
    print(f"📄 {len(documents)} Text-Chunks werden eingebettet...")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents,
        embedding=embedding_model,
        persist_directory=CHROMA_DB_DIR
    )
    print("✅ Embedding abgeschlossen & Vektorindex gespeichert.")

if __name__ == "__main__":
    build_vectorstore()
