import pdfplumber
import pandas as pd
import json
from pathlib import Path

# === Verzeichnisse ===
INPUT_DIR = Path(r"C:\Users\ahmad\Analyst-AI-System\data\Raw")
JSON_OUTPUT_DIR = Path(r"C:\Users\ahmad\Analyst-AI-System\data\Processed\json")
CSV_OUTPUT_DIR = Path(r"C:\Users\ahmad\Analyst-AI-System\data\Processed\tables")

# Ordner anlegen
JSON_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_pdf(pdf_path):
    base_name = pdf_path.stem
    company = pdf_path.parent.name
    print(f"📄 Verarbeite: {company}/{base_name}")

    json_data = {
        "company": company,
        "source_file": pdf_path.name,
        "text": "",
        "tables": []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    json_data["text"] += f"\n--- Seite {i+1} ---\n{text}"

                tables = page.extract_tables()
                for j, table in enumerate(tables):
                    if table:
                        table_dict = {
                            "page": i + 1,
                            "table_index": j + 1,
                            "data": table
                        }
                        json_data["tables"].append(table_dict)

                        # Tabelle separat als CSV speichern
                        df = pd.DataFrame(table[1:], columns=table[0])
                        csv_filename = f"{company}_{base_name}_p{i+1}_t{j+1}.csv"
                        df.to_csv(CSV_OUTPUT_DIR / csv_filename, index=False)

        # JSON-Datei speichern
        json_filename = f"{company}_{base_name}.json"
        with open(JSON_OUTPUT_DIR / json_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON & Tabellen gespeichert für: {base_name}")
    
    except Exception as e:
        print(f"❌ Fehler bei {base_name}: {e}")

def run_batch():
    pdf_files = list(INPUT_DIR.rglob("*.pdf"))
    print(f"📚 Gefundene PDFs: {len(pdf_files)}")

    for pdf in pdf_files:
        process_pdf(pdf)

if __name__ == "__main__":
    run_batch()
