# scripts/extract_ir_batch.py
import os
import pdfplumber
import pandas as pd
from pathlib import Path

INPUT_DIR = Path("data/")
TEXT_OUTPUT_DIR = Path("output/text/")
TABLE_OUTPUT_DIR = Path("output/tables/")

TEXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TABLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_pdf(pdf_path):
    base_name = pdf_path.stem
    print(f"📄 Verarbeite: {base_name}")

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""

        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n--- Seite {i+1} ---\n{text}"

            tables = page.extract_tables()
            for j, table in enumerate(tables):
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df.to_csv(TABLE_OUTPUT_DIR / f"{base_name}_p{i+1}_t{j+1}.csv", index=False)

        if full_text.strip():
            with open(TEXT_OUTPUT_DIR / f"{base_name}_text.txt", "w", encoding="utf-8") as f:
                f.write(full_text)

def run_batch():
    for pdf_file in INPUT_DIR.glob("*.pdf"):
        process_pdf(pdf_file)

if __name__ == "__main__":
    run_batch()
