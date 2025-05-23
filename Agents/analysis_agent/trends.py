# agents/analysis_agent/trends.py

import os
import json
import pandas as pd
import re

def extract_year_from_filename(filename):
    match = re.search(r"(20[1-2][0-9])", filename)
    if match:
        return int(match.group(1))
    return None

def load_json_data(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            year_match = re.search(r"(20[1-2][0-9])", file)
            year = int(year_match.group(1)) if year_match else None

            companies = ["Apple", "Microsoft", "Google", "NVIDIA", "Meta"]
            company = next((c for c in companies if c.lower() in file.lower()), "Unbekannt")

            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                try:
                    entries = json.load(f)
                    for entry in entries:
                        if isinstance(entry, dict):
                            entry["source_file"] = file
                            entry["year"] = year  # clave: columna debe llamarse 'year'
                            entry["company"] = company
                            data.append(entry)
                except Exception as e:
                    print(f" Error en {file}: {e}")
    return pd.json_normalize(data)

def preprocess(df):
    df = df[df["year"].notna()]
    df = df[df["year"].between(2019, 2024)]
    df["date"] = pd.to_datetime(df["year"].astype(int).astype(str) + "-01-01")

    # ➕ Extraer trimestre desde el nombre del archivo
    df["quarter"] = df["source_file"].str.extract(r'(1q|2q|3q|4q)', expand=False)
    df["quarter"] = df["quarter"].str.upper().fillna("Jährlich")  # Si no hay trimestre, se asume "ANUAL"

    df_grouped = df.groupby(["company", "year", "quarter"]).size().reset_index(name="document_count")
    return df_grouped
